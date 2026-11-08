# Helix Probe: start here

*Living entry point, kept current after every working session. Last updated Nov 7, 2026, 20:50 ET. Anyone handed
this repo should be able to continue from these files alone, with no separate handoff.*

## The two goals (from `docs/NORTH_STAR.md`)

1. **Goal 1, capability removal:** show that Helix Probe lets a cheap model switch off one specific ability inside
   a real language model by editing its weights directly, while the rest keeps working, and that the loop, not
   luck, is what makes it work.
2. **Goal 2, the map:** the same loop, pointed at discovery instead of search, builds a verified map of which parts
   of the model do what. It leads to a demo where you change a part and watch behaviour change.

## Where things stand (Nov 7, 20:30 ET; step-by-step table in `docs/PROGRESS.md`)

- **Goal 1** (plan steps 0–4, `PLAN.md`):
  - Steps 0–3 are done. Step 2's table is in JOURNAL (Nov 7, 12:20). The six r0 runs' raw files were lost with the
    old runtime `wsp2`; their results are kept in JOURNAL.
  - Running on the new `wsp2`, approved by Shreyas at 12:59 ET:
    - three more helix2 addition runs on the 9B (done: r3 and r4 were "+" swaps, r5 passed v2);
    - then the 0.8B addition axis (every arm). Done. MIT and Helix are 0/6, all "+" swaps. helix2 r0 and r2 were
      "+" swaps; **helix2 r1 passed v2** by removing internal "addition", "carry" and
      "≥100" directions from every residual writer, which acts on the computation, not the output.
    - Both are scored with verdict v2, where "removed" must also hold in other wordings.
  - **Totals across both sizes, real removals under v2:** helix2 2/12, MIT 0/9, Helix 0/9. Table in JOURNAL
    (Nov 7, 20:30).
  - Step 4 (write-up) is next.
- **What Goal 1 shows so far:**
  - The pre-registered verdict (v1) can be passed by breaking a trigger word ("+", "feminine"). The reworded
    measure catches it.
  - The only LLM edits that survive rewording came from the loop arms: Helix gender r2, helix2 addition r0, and
    the two that pass the strict verdict v2 (two-digit addition removed in every wording, precisely and durably):
    - 9B helix2 r5 suppresses number outputs whenever the final state reads "addition";
    - 0.8B helix2 r1 removes the addition directions inside the model.
  - MIT and the original Helix never get past the "+" shortcut at either size under v2.
  - The scripted method is still the best on gender.
- **Goal 2** (D0–D4):
  - D0 is done.
  - D1 is done and failed: its rule rewarded edits that wreck the model, and the editor learned to produce them.
  - D2 (D1 with three fixes: verified *and* specific, no empty entries, the editor sees the strict verdict) is
    done and also failed: 2 of 24 entries are specific, both output-level, and no internal part was found.
  - The write-up is `docs/GOAL2_CALIBRATION_RESULT.md`. The next step waits for Shreyas (options A–C).
- **Vision** (`NORTH_STAR.md`):
  - Goal 1: type a behaviour change in words and get updated weights back.
  - Goal 2: a UI over the verified map of the weights.
- **Hard rules** (`WORKING_METHOD.md` §3): every finished run goes to GitHub at the next check-in; docs are updated
  in the same turn as the event.
- **Runtimes:** `wsp` was reclaimed by Colab while idle (nothing lost; every result was already on GitHub).
  `wsp2` was stopped at Shreyas's request (Nov 7, 20:50 ET). No Colab runtimes are running, and the ≤9-minute check-ins were stopped
  by Shreyas, so the Colab sign-in will need his re-approval (`06_OPERATIONS.md`). Restarting needs
  `colab new --gpu L4 -s NAME` plus `setup_both.py` and a `.env` upload (`scripts/colab/README.md`). Check-ins every ≤9 minutes from the workspace
  that holds the Colab sign-in keep both alive.
- **Older results:**
  - FIND: Helix Probe beats the same model without the loop by a wide margin.
  - ARC-AGI-3 pilot: 0 levels.
  - Exp 1 (weight reading): the loop adds nothing.
  - Details: `03_ANALYSIS.md` and `10_INTERPRETABILITY_TRACK.md`.

## Read in this order

| File | What it is |
|---|---|
| `docs/NORTH_STAR.md` | **The goal,** what counts as done, what a breakthrough would be. Short; read first. |
| `docs/GOAL2_CALIBRATION_RESULT.md` | **Goal 2's calibration result** (D1, D2), what it shows, and the options. |
| `docs/PROGRESS.md` | **Every step of both goals in one table:** status, where it ends, open decisions. |
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
