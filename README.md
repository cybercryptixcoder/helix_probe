# Helix Probe

**Point it at a black box. It runs one small experiment at a time, and each result sharpens a model of how the box works.**

Helix Probe doesn't search for the best answer. It is a loop that makes an LLM learn how a system works by trial and
error: it asks one question at a time, never asks the same question twice, and turns what it learns into a model it
can check. The thing being studied plugs in through one adapter file; nothing in the core knows what it is.

## The loop

```
          ┌──────────────────────────── context: library + model + notebook (wrong ones in full) ─┐
          ▼                                                                                        │
  PROPOSE one experiment ──► run it on the box ──► model predicted it? ── yes ──► next step ───────┤
                                                        │ no                                        │
                                                        ▼                                           │
                                              REVISE the model ──► replay every experiment (code) ──┘
                                                                   keep it only if it fits at least as well
```

Each LLM call does one small job: choose one experiment, or update the model after a surprise. No conversation
carries over between calls. Only the three memories do.

## The three memories

| | What it holds | Who writes it | How it's used |
|---|---|---|---|
| **Notebook** | Every experiment: the question, the probe, what came back, what the model predicted, how well it matched | Code, append-only | "What was tried". Stops repeats; it's the evidence every model is checked against |
| **Model** | **Beliefs** (short claims citing their experiments: "B moves right 2 [E3, E9]") **+ `predict(probe)`**, Python that simulates the box | The LLM, after a surprise | The internal model of the box. Because it is code, it can be *tested* and *used* |
| **Library** | Knowledge handed in from outside: rules, domain facts, tricks | You (adapter's `knowledge`, or `--knowledge file.md`) | Read-only head start |

These are the choices that keep it simple:

- **The model is executable.** Beliefs in words can't be checked. `predict()` can: it is replayed on every
  experiment in the notebook, and code, not the LLM, says how good it is. A new version replaces the old one only if
  its average match over the whole notebook is at least as good (the one idea kept from Helix Evolve: the judge is code).
- **Surprise drives everything.** If the model predicted an experiment correctly, nothing is rewritten. Revisions
  happen only when the box disagrees with the model.
- **The model compresses the notebook.** The experimenter sees in full only the experiments its model still gets
  wrong, plus the latest few; everything else is one index line marked `[ok]`. What is understood doesn't need to be
  re-read, so the context stays small after a thousand experiments.
- **Knowing it and using it are the same model.** In solve mode the experimenter proposes candidate probes for a
  goal, `predict()` simulates them for free, and only the most promising one is run for real. A model that really
  learned the box gets a character from any A to any B; a lookup table doesn't.

## How you know it works

Three numbers, all computed by code:

| Number | What it measures | Where |
|---|---|---|
| **fit** | Share of the notebook the current model predicts exactly | `curve.csv`, every step |
| **held-out** | Share of a fixed set of random probes, **never shown to the experimenter**, that it predicts exactly. This is the real learning curve: memorising the notebook doesn't raise it | `curve.csv`, each new model version |
| **goals** | Goals reached, and real tries used, after learning | `summary.json` |

Ablations that come for free: run with and without the library (`--no-env-knowledge`), with different step budgets,
or (a small change) with the model hidden from PROPOSE, to see what each memory contributes.

## Running it

```bash
cp .env.example .env            # fill in an OpenAI-style endpoint: Luminal, OpenAI, OpenRouter, Ollama...
python -m probe.run envs/scrambled_grid.py --steps 40 --tasks 5
python -m probe.run envs/knob_box.py --steps 30 --tasks 5 --no-env-knowledge
python -m probe.run envs/knob_box.py --offline --steps 5      # no model: checks the plumbing only
python -m tests.test_offline                                  # offline checks of the mechanism
```

No dependencies beyond Python 3.10+. Rerun the same command with the same `--out` to continue a run.

Each run folder holds `notebook.jsonl` (every experiment), `model/v###.py` + `.json` (every model version with its
beliefs, fit and held-out score), `curve.csv`, `calls.jsonl` (every prompt and reply), `heldout.json` and
`summary.json`.

## Plugging in a new box: one file

```python
from probe.env import Environment, Task

class MyBox(Environment):
    name = "my_box"
    brief = "What the experimenter is told: what it can do, what comes back. Say nothing about the insides."
    probe_format = 'probe: {"...": ...}   observation: {"...": ...}'
    knowledge = ""                                   # optional library text

    def probe(self, p):          return {...}        # run one experiment for real (required)
    def validate(self, p):       return None         # or an error string (optional)
    def random_probe(self, rng): return {...}        # for the held-out set (optional, strongly recommended)
    def make_tasks(self, rng, n): return [Task("goal text", lambda obs: ...)]   # for solve mode (optional)
    # compare(pred, obs) -> 0..1 defaults to a recursive match over dicts/lists/numbers; set `tolerance`, or override
```

The two in `envs/`:
- `scrambled_grid.py`: a game with five unlabeled buttons, walls, and one button that behaves differently in the
  upper half of the board. Goals: get from A to B in 8 presses.
- `knob_box.py`: three dials and a switch moving a dot, with an interaction (a dial past 7 shifts y). Goals: put
  the dot at a point.

Other boxes the same mechanism fits, each one adapter file:
- **A small transformer's internals:** probe = (prompt, which heads or neurons to ablate or patch); observation =
  top tokens and a few logit differences. `predict()` becomes a circuit hypothesis that can be executed.
- **A model's behaviour:** probe = a prompt built from controlled features; observation = labelled features of the
  reply. The model is a rule for when the behaviour changes.
- **A hidden cellular automaton:** probe = a starting grid; observation = the grid after k steps. The model is the
  rule.
- **A physics toy with unknown constants:** probe = initial conditions; observation = the trajectory. The model is
  the equations.
- **An undocumented program or API:** a CLI tool, a file format, a pricing endpoint. Probe = inputs; observation =
  output fields.

## Deliberately left out

One experimenter, one experiment at a time: no parallel streams, no mutator, no separate researcher and coder roles,
no populations. If something is added later, it should be because a run's traces show it's missing, and the
ablations above should be able to measure whether it helped.

## Known limits and open questions

- **Noisy boxes.** Everything assumes the box is deterministic. A noisy box needs repeated probes and a `compare`
  that scores against a distribution.
- **Some models are hard to write as code.** For interpretability, `predict()` may only manage part of the
  observation; `compare` gives partial credit, and the beliefs carry what the code can't.
- **The model can over-fit the notebook.** The prompt forbids lookup tables and the held-out score exposes them, but
  nothing blocks them yet.
- **Beliefs aren't checked one by one.** Only the code is. Scoring each belief from the experiments it cites
  (as the Atlas did) is a possible next layer.
- **Choosing experiments is left to the LLM.** A next step is to measure how much better its choices are than random
  probes at the same budget: that comparison is the clearest test of whether directed reasoning beats plain sampling.
