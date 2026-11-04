# Helix Probe

**Point it at a black box. It runs one small experiment at a time and builds a model of how the box works: a model
it can run, that is judged on evidence it has never seen.**

Helix Probe is a loop for learning how a system works by trial and error. It doesn't search for the best answer.
Three narrow roles take turns, one call at a time: an experimenter chooses one experiment, an updater revises the
model when the box surprises it, and a theorist writes a model from scratch from the evidence alone. The box itself is
the judge. Whatever is being studied plugs in through one adapter file; nothing in the core knows what it is.

Status (November 2026): **v2**. v1 is frozen in `versions/v1/` for comparison. The walkthroughs:
`docs/helix_probe_explainer_v2.html` (this version: the design, every change from v1, the results) and
`docs/helix_probe_explainer_v1.html`.

## The loop

```
start:  draw a few random probes from the box, run them, SEAL the results (the exam: no LLM ever sees them)

each step:
  EXPERIMENTER  chooses one probe ──► the box answers ──► the current model predicted it beforehand: right?
                                                              │ no
                                                              ▼
                                       UPDATER revises the model (sees the model, the evidence, the surprise)
  every few steps, or when the updater fails twice running:
                                       THEORIST writes a model from scratch (sees the evidence, NOT the model)

  every candidate model is scored by code, and replaces the current one only if it is better on:
      1. the exam (evidence it was never fitted to)   2. the notebook   3. size (shorter wins a tie)
```

## What persists

| | What | Written by |
|---|---|---|
| **Notebook** | every experiment: question, probe, observation, what the model of the time predicted, the match | code, append-only |
| **Exam** | a few random probes and their results, sealed | code, once |
| **Model** | `predict(probe)` in Python, with the beliefs as comments inside it; every accepted version kept | the updater or theorist, kept by code |
| **Library** | knowledge handed in from outside | you |

## How it knows it's learning (all computed by code)

| Signal | What it measures | Seen by the roles? |
|---|---|---|
| **exam** | average match on the sealed probes: can't be raised by memorising | yes: their sense of progress |
| **on arrival** | share of experiments predicted correctly before their result was seen | yes |
| **fit** | average match on the notebook | yes |
| **size** | characters of model code, comments not counted | yes |
| **held-out** | a separate set of random probes, for measurement only | **never** |

## Running it

```bash
cp .env.example .env                       # an OpenAI-style endpoint; Luminal's DeepSeek V4.1 Flash by default
python -m probe.run envs/scrambled_grid.py --steps 30 --tasks 5
python -m probe.run envs/find_strings.py --env-arg fid=f00019 --steps 25
python -m tests.test_offline               # offline checks of every piece
```

Python 3.10+, standard library only (the FIND boxes need numpy and scipy). `--steps` is the total; rerun with the
same `--out` and a bigger `--steps` to continue.

## Plugging in a box: one file

```python
from probe.env import Environment, Task

class MyBox(Environment):
    name = "my_box"
    brief = "What the experimenter is told: what it can do, what comes back. Nothing about the insides."
    probe_format = 'probe: {...}   observation: {...}'
    def probe(self, p):          return {...}       # run one experiment for real (required)
    def random_probe(self, rng): return {...}       # powers the exam and the held-out set (strongly recommended)
    def validate(self, p):       return None        # or an error string
    def compare(self, pred, obs): ...               # 0..1; a recursive default is provided
    def make_tasks(self, rng, n): return [Task("goal", lambda obs: ...)]   # optional goals
```

In `envs/`: `scrambled_grid.py` and `knob_box.py` (toys), and `find_numeric.py` / `find_strings.py` (FIND).

## Benchmark: FIND

FIND (Schwettmann, Rott Shaham et al., NeurIPS 2023) asks an agent to probe a black-box function and write code that
reproduces it. `bench/find/` has an 80-function sample (40 numeric, 40 strings), FIND's official scorers, the
published answers of FIND's own agents (GPT-4, GPT-3.5, Llama-2) scored the same way, a runner for comparing arms
(v2, v2 with random experiments, v2 without the theorist, v1), and the report. The VM job: `scripts/run_find.sh`;
its doc and the results: `docs/V2_JOB.md`, `results/find/`.
