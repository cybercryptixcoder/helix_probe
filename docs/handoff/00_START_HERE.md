# Helix Probe: start here

*Living entry point, kept current after every working session. Last updated Nov 6, 2026, 16:30 ET. Anyone handed
this repo should be able to continue from these files alone, with no separate handoff.*

## The goal right now (from `docs/NORTH_STAR.md`)

**Show that Helix Probe lets a cheap model switch off one specific ability inside a real language model by editing
its weights directly, while the rest of the model keeps working, and that the loop, not luck, is what makes it work.**

## Where things stand (Nov 6, 16:30 ET)

- **The plan** for Nov 6–10 is drafted in `docs/PLAN.md` and **waiting for Shreyas's review**. Nothing in it has run.
  It removes two abilities (gender inflection, two-digit addition) from Qwen3.5-0.8B and Qwen3.5-9B, in five arms
  (unedited, random, scripted, Flash in one conversation, Flash in Helix Probe), with held-out grading and a comeback
  test.
- **The editing harness** (`bench/weights/edit*.py`) is written but untested. Step 0 of the plan adapts and tests it.
- **The VM** is still running the exp-1 weights job (stage 13 of 19). The plan stops it and runs only the
  shuffled-code control, then uses the VM for the 0.8B side of the plan.
- **Colab GPUs work** through Shreyas's AI Plus plan (an L4, verified Nov 6). The sign-in lives in the workspace of
  the session that made it, kept alive by check-ins every ≤9 minutes.
- **Results so far:**
  - FIND: Helix Probe 0.85–0.97 against 0.38–0.46 for the same model without the loop.
  - ARC-AGI-3 pilot: 0 of 35 levels.
  - Weight reading (exp 1): Flash 8/12 from text, 11/12 with code; the loop adds nothing there.
  - Details: `03_ANALYSIS.md` and `10_INTERPRETABILITY_TRACK.md`, section 12.

## Read in this order

| File | What it is |
|---|---|
| `docs/NORTH_STAR.md` | **The goal,** what counts as done, what a breakthrough would be. Short; read first. |
| `docs/PLAN.md` | **The finite plan:** steps, arms, scoring, predictions, decisions, status. |
| `docs/JOURNAL.md` | What was decided and found, dated, newest first. |
| `docs/WORKING_METHOD.md` | How we go from a goal to results without drifting: crystallise, plan, execute, handle surprises and new directions. |
| `01_CONCEPT.md` | What Helix Probe is, why, and the vision. Self-contained. |
| `10_INTERPRETABILITY_TRACK.md` | The weight-space track: MIT's work, our harness, results so far (section 12). |
| `02_STATE_AND_RUNS.md` | What's built and everything that ran before Nov 5. |
| `03_ANALYSIS.md` | What the FIND and ARC runs showed. |
| `04_PUBLISHING.md` | Candidate publishable results and references. |
| `05_NEXT_STEPS.md` | The older backlog (FIND, ARC). Superseded by `PLAN.md` while the north star is the focus. |
| `06_OPERATIONS.md` | How to run anything: the VM, Aether prompts, job scripts, Colab from a headless machine. |

**Private, kept out of this public repo,** in a bundle Shreyas holds (`helix_probe_private.zip`):
- `07_PRINCIPLES_AND_RULES.md` (his standing rules);
- `08_shreyas_verbatim.md` (his messages);
- `09_full_transcript_redacted.md`;
- `.env` (keys).

Ask him for it before changing anything. Its messages run to Nov 4; later direction is paraphrased in `JOURNAL.md`.

## The standing rules, briefly

- Lean but uncompromising; whiteboard-explainable; traceable; general.
- Evidence over exceptions.
- Every run has a stated question and a written prediction, and attempts a publishable result fairly.
- No experiments without a place in the plan.
- Keys only in the gitignored `.env`; the repo is public.
- Aether (the VM agent) never sets up cron jobs or timers, never kills or restarts processes unless told to, and
  never edits code.
- Update Shreyas every 10–15 minutes during long work.
- Don't rely on memory or other conversations; these files are the context.

## How to resume

1. Read `NORTH_STAR.md`, `PLAN.md` and the top of `JOURNAL.md`.
2. Check the plan's status line: the next step is whatever it says is waiting.
3. If the work needs Colab, the sign-in from `06_OPERATIONS.md` must be redone in your workspace (Shreyas approves a
   link and pastes back a code).
