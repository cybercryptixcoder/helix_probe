# Helix Probe

**Point it at a black box. It runs one small experiment at a time and builds a model of how the box works: a model
it can run, that has to predict each experiment before seeing it.**

Helix Probe is a loop for learning how a system works by trial and error, and then using what it learned. It doesn't
search for the best answer, and it has no evolutionary or optimizer layer. Three narrow roles take turns, one call at
a time:
- an experimenter chooses one experiment;
- an updater revises the model when the box surprises it;
- a theorist writes a model from scratch from the evidence alone.

The box itself is the judge. Whatever is being studied plugs in through one adapter file. Nothing in the core knows
what the box is: a function, a toy, or a video game.

Status (November 2026): **v3**. v1 and v2 are frozen in `versions/` for comparison.
- The walkthrough: `docs/helix_probe_explainer_v3.html` (earlier versions: `docs/helix_probe_explainer_v2.html`, `_v1.html`).
- Publishable results so far, with their configurations: `docs/RESULTS_LOG.md`.

## The loop (one whiteboard)

```
each step:
  1 ACT      the box has a goal and the model can plan a way there?  ──yes──► run the first piece of that plan
             otherwise the EXPERIMENTER picks one experiment (every 2nd one is a random ordinary probe)
  2 RUN      the model predicts the result BEFORE the box answers; code compares the two (0..1)
  3 REPAIR   wrong?  the UPDATER revises the model         ── kept only if it explains the PAST better
  4 RETHINK  every 6 experiments, or when repairs stall,
             the THEORIST writes a model from scratch      ── kept only if it predicts the FUTURE better:
                                                              on trial for the next 3 experiments against the current model
```

Two rules decide everything, both computed by code:
- **Fixes must explain the past.** An updater's fix replaces the model only if it fits the notebook better. On a tie,
  the shorter model wins.
- **New theories must predict the future.** A theorist's model goes on trial and takes over only if it predicts the
  next experiments at least as well as the current model. On a tie, fit decides, then size.

**Hidden state.** Some boxes remember: a lock that counts presses, a game whose screen doesn't show everything.
- For these, every probe carries its history since the last reset.
- The model can then keep that memory explicitly, by replaying the history inside `predict()`.
- The prompts ask for exactly that when a box is stateful.

## What is kept, and where to look when something is off

| File (per run) | What | If this looks wrong... |
|---|---|---|
| `notebook.jsonl` | every experiment: why, the probe, what the model predicted, what came back, the match, the cost | the box or the experimenter |
| `calls.jsonl` | every model call: role, system prompt, prompt, reply, reasoning, tokens, seconds | a role's prompt or reply |
| `offers.jsonl` | every candidate model, its scores, kept or not and why | the judging rule |
| `trials.jsonl`, `trial.json` | every theory trial, experiment by experiment; the one in progress | the trial |
| `model/v###.py` | every model that was ever current, with its scores (`.json`) | the updater or theorist |
| `curve.csv` | one row per step: experiments, cost, model version, fit, size, on-arrival hits, held-out | progress |
| `summary.json` | the end state, with the box's own official score if it has one | |

## Running it

```bash
cp .env.example .env                       # an OpenAI-style endpoint; Luminal's DeepSeek V4.1 Flash by default
python -m probe.run envs/hidden_lock.py --steps 20
python -m probe.run envs/find_strings.py --env-arg fid=f00019 --steps 25
python -m probe.run envs/arc_agi3.py --env-arg game=ls20-9607627b --steps 60 --budget 300
python tests/test_v3.py                    # offline checks: hidden state, trials, planner, budget, resume
```

- Python 3.10+, standard library only. The FIND boxes need numpy and scipy; ARC-AGI-3 needs Python 3.12+ and `pip install arc-agi`.
- `--steps` is the total number of experiments. Rerun with the same `--out` and a bigger `--steps` to continue.
- A stopped or killed run resumes from its files. Stateful boxes are restored by replaying their actions.
- `bench/restore.py` rebuilds run folders from what was pushed to `results/`, so a job can continue from GitHub alone.

## Plugging in a box: one file

```python
from probe.env import Environment

class MyBox(Environment):
    name = "my_box"
    brief = "What the experimenter is told: what it can do, what comes back. Nothing about the insides."
    probe_format = 'probe: {...}   observation: {...}'
    def probe(self, p):          return {...}       # run one experiment for real (required)
    def random_probe(self, rng): return {...}       # an ordinary probe: the random experiments (recommended)
    def compare(self, pred, obs): ...               # 0..1; a recursive default is provided
    # optional: validate, cost (budget units), stateful + full_probe/restore/view_state (boxes that remember),
    # goal/done (boxes with goals), plan_actions/advance/state_key/max_probe (planning through the model),
    # make_tasks (goals for stateless boxes), view_probe/view_obs (compact views for the prompts)
```

In `envs/`:
- toys: `scrambled_grid.py`, `knob_box.py`, `hidden_lock.py` (hidden state);
- FIND: `find_numeric.py`, `find_strings.py`;
- ARC-AGI-3: `arc_agi3.py`, any of the 25 public games.

## Benchmarks

- **FIND** (Schwettmann, Rott Shaham et al., NeurIPS 2023): probe a black-box function, then write code that
  reproduces it. `bench/find/` holds:
  - an 80-function sample and FIND's official scorers;
  - FIND's published agents (GPT-4, GPT-3.5, Llama-2), scored the same way;
  - `aia.py`, FIND's own agent protocol replicated, to run any model the way FIND ran GPT-4 (the same-model control).
- **ARC-AGI-3** (ARC Prize, 2026): 25 public games with no instructions. `bench/arc/run.py` plays them in the
  official toolkit's local mode and scores them with its official calculator against human action counts.

The VM jobs:
- `scripts/run_find.sh` (v2, `docs/V2_JOB.md`);
- `scripts/run_v3.sh` (v3: the AIA control, FIND, ARC; `docs/V3_JOB.md`).

Results are in `results/`.
