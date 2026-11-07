# Helix Probe: start here

*Living entry point, kept current after every working session. Last updated Nov 7, 2026, 12:15 ET. Anyone handed
this repo should be able to continue from these files alone, with no separate handoff.*

## The two goals (from `docs/NORTH_STAR.md`)

1. **Goal 1, capability removal:** show that Helix Probe lets a cheap model switch off one specific ability inside
   a real language model by editing its weights directly, while the rest keeps working, and that the loop, not
   luck, is what makes it work.
2. **Goal 2, the map:** the same loop, pointed at discovery instead of search, builds a verified map of which parts
   of the model do what. It leads to a demo where you change a part and watch behaviour change.

## Where things stand (Nov 7, 12:15 ET)

- **Goal 1** (plan steps 0–4, `PLAN.md`):
  - Steps 0 and 1 are done.
  - Step 2 (MIT-style one conversation vs Helix vs helix2, 3 runs each, gender and addition on the 9B) is on its
    last run, then a regrade.
  - Step 3 (the comeback test) is measured inside every grade already.
  - Step 4 (write-up) is next.
  - The 0.8B scale axis on the VM has not produced results in the repo.
- **What Goal 1 shows so far:**
  - The pre-registered verdict can be passed by swapping a trigger word ("+", "feminine"). The post-hoc reworded
    measure catches that every time.
  - The only LLM edits that survive rewording came from the loop arms: helix gender r2 and helix2 addition r0.
  - The scripted (non-LLM) method is still the best on gender.
- **Goal 2** (D0–D4):
  - D0 (build) is done.
  - D1 (calibration) is done and **failed** its pre-registered criteria: the verification rule rewarded edits
    that wreck the model, and the editor learned to produce them.
  - Fixes for D2 are proposed and wait for Shreyas. D3 (long run) and D4 (demo) have not started.
- **Runtimes:** `wsp` (Colab L4) is running the Goal 1 queue. `wsp2` is idle. Both are kept alive by check-ins
  every ≤9 minutes from the workspace that holds the Colab sign-in.
- **Older results:**
  - FIND: Helix Probe beats the same model without the loop by a wide margin.
  - ARC-AGI-3 pilot: 0 levels.
  - Exp 1 (weight reading): the loop adds nothing.
  - Details: `03_ANALYSIS.md` and `10_INTERPRETABILITY_TRACK.md`.

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
