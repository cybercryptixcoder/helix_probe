# Helix Probe: start here

*Living entry point, kept current after every working session. Last updated Nov 13, 2026. Anyone handed
this repo should be able to continue from these files alone, with no separate handoff.*

## CURRENT STATE (2026-11-13). Read this first.

> **The rule for this repo:** it is a living documentation store. After every exchange, record every idea, question, decision, finding, hypothesis and build request (`docs/CONVERSATION_LOG.md`). A fresh session must be able to continue from the docs alone.

### The goal

Make a neural network interpretable by building a **white-box reconstruction** of it: a model that *predicts* the network's behaviour, including under interventions. A correlation table does not count. In the field's terms this is a **causal abstraction**. It has:
- named variables;
- the steps that compute them;
- an alignment saying where each variable lives in the network (which neurons, heads, subspaces or weights).

It is judged by three questions, in increasing strictness (`literature/SYNTHESIS.md` §4, §10):
1. Does it produce the same outputs when run in place of the network?
2. Does it respond the same way to interventions (IIA, ablation prediction)?
3. Does it compute the same way inside (Jacobian / internal-state agreement)?

Each is measured against baselines that understand nothing.

### What we are building toward

A **constructor**: a method in which an LLM reads a network's weights (and may write code to probe them) and produces such a construction. The construction is runnable Python plus an alignment table. The first paper needs **one solid construction made by the constructor** on a small network. A general constructor comes later.

Order of work:
- **K0, replicate first.** Rediscover a published construction (Nanda's modular addition) without the reader seeing the answer, with blinding, variants and controls.
- **K1, the reader interface.** What we hand the LLM, what we ask it, and what answer we want, measured rather than guessed.
- **K2:** fine-tune a reader to read better (method open).
- **K3:** the loop (only a sketch).

All are in `DIRECTIONS.md` §2f.

### Building now

The **Weight Reading Lab** (`lab/`): a local web app for doing K1 by hand. It is live-tested. Spec and status: [`docs/WHAT_WE_ARE_BUILDING.md`](../WHAT_WE_ARE_BUILDING.md). Use: `lab/GUIDE.md`. Run: `lab/RUNNING.md`.

### Results so far (K1, DeepSeek V4.1 Flash)

| Test | Result |
|---|---|
| XOR / parity, tiny nets | Read correctly (text and python modes) |
| MIT Breakout policy, MIT's prompt (channel names given) | **Breakout, 97%: correct** |
| Same, **blinded** (no context, neutral question) | **Wrong:** "MNIST-style digit classifier". It saw real spatial structure but miscounted the inputs (485 instead of 500) and filled the gap with a dataset prior. |
| Same, shuffled control, blinded | Correctly declined to name a task (also miscounted: 498) |
| First blinded attempt at 32k output | Ran out of budget, no answer |

Reading so far: in text mode, MIT's success depends mostly on the context text. That matches the literature (`literature/wsp/K1_STATE_OF_ART.md`).

### Next steps

1. **Blinded python-mode run** on the same game policy: can it measure the 10×10×5 input layout with code?
2. Context-off runs on the other 3 games and on the permuted variant.
3. Mod-add transformer (**Mystery transformer A**), python mode, blinded: does it find the Fourier frequencies {8, 23, 25, 11, 22}? (Mod-mul is also available, as **Mystery transformer C**.)
4. Then design K1 properly as an experiment: prompts × formats × access × controls.

### Not decided (do not treat as settled)

- The loop, its roles and agents (K3 is a sketch; do not build it first).
- The form of the construction (Python plus alignment is a candidate).
- K2's fine-tuning method.
- Slicing vs letting the reader query the weight store.
- `ideas/SCIFI_AGENTIC_INTERPRETER.md` is explicitly **not** the plan.

### Map of the docs

| File | What it holds |
|---|---|
| `docs/WHAT_WE_ARE_BUILDING.md` | The current build, what is decided and what is open |
| `docs/CONVERSATION_LOG.md` | Every idea, question and decision, in order |
| `docs/DIRECTIONS.md` | All research directions; §2f = constructor, K0–K3 |
| `docs/literature/SYNTHESIS.md` | What the interpretability field builds and measures; what a construction is |
| `docs/literature/core/` | 193 paper entries plus an index |
| `docs/literature/wsp/` | Weight-space programming follow-ups (Nov 2026), plus `K1_STATE_OF_ART.md` |
| `docs/JOURNAL.md` | Dated log of events |
| `lab/` | The Weight Reading Lab (code, specimens, guide) |

Proposals, pitches and personal plans are deliberately kept **out of this public repo**.

> **SUPERSEDED.** Everything below this line is the earlier state (Nov 8–11), kept for history.

---

## The two goals (from `docs/NORTH_STAR.md`)

1. **Goal 1, capability removal:** show that Helix Probe lets a cheap model switch off one specific ability inside
   a real language model by editing its weights directly, while the rest keeps working, and that the loop, not
   luck, is what makes it work.
2. **Goal 2, the map:** the same loop, pointed at discovery instead of search, builds a verified map of which parts
   of the model do what. It leads to a demo where you change a part and watch behaviour change.

## Where things stand (Nov 8, 2026, 02:30 ET). Read this first.

**Nothing is running.** No Colab runtimes exist; `wsp` was reclaimed and `wsp2` was stopped at Shreyas's request.
The ≤9-minute check-ins were stopped by Shreyas. Every result is on GitHub, apart from the raw files of six 9B r0
runs, which were lost (their results are recorded in JOURNAL). The plain-language summary of everything found is
**`docs/FINDINGS.md`**.

### Goal 1: remove one ability by direct weight edits, and show the loop is why

- **Steps 0–3 done; 2b and 2c done** (the extra helix2 runs and the 0.8B axis).
- **Result:**
  - real removals (verdict v2: gone in every wording, precise, durable): helix2 2/12, MIT 0/9, Helix 0/9;
  - both successes are two-digit addition: the 9B readout edit (helix2 r5) and the 0.8B internal edit
    (helix2 r1);
  - every other pass was a trigger-token swap.
  - Full table: JOURNAL, Nov 7, 20:30.
- **Next: Step 4, the write-up.** No GPU is needed.
  - Contents: results table, how each edit works, honest negatives, how to re-run.
  - Sources: FINDINGS.md, the JOURNAL table, `results/edit*/`.
  - Open question for Shreyas: write now, or first add about 6 more helix2 addition runs (9B and 0.8B, about
    6–8 GPU hours) to firm up 2/12?

### Goal 2: a verified map of which parts do what, then a UI

- **D0 done. D1 and D2 both failed** their 5 pre-registered criteria (`GOAL2_CALIBRATION_RESULT.md`).
- **Shreyas has not yet chosen the next step:**
  - (A) stop, and publish the negative with Goal 1;
  - (B) recommended: a scripted ablation sweep over components × 26 behaviours on held-out questions is the map,
    the loop then explains it, and that drives the D4 UI. About 8–10 h, 3–4 of them on GPU;
  - (C) score behaviours by answer log-probability and run one more calibration. About 4 h, plus D3/D4 if it
    passes.

### Vision (`NORTH_STAR.md`)

- Goal 1: type a behaviour change in words, get updated weights back.
- Goal 2: a UI over the measured map.

### Decisions waiting for Shreyas

1. Goal 2: A, B or C.
2. Goal 1: write up now, or more helix2 runs first.

3. Direction (added Nov 11): `docs/DIRECTIONS.md` lists every candidate direction and proposes a lead one (a
   measured map, then testing whether an AI reader can predict it). Does it replace or join the two goals?

Do not start GPU work without his answer.

### To restart GPU work (Colab)

1. Redo the Colab sign-in (`06_OPERATIONS.md`, "Colab headless"): `google-colab-cli` 0.7.5 with
   `OAUTHLIB_RELAX_TOKEN_SCOPE=1`. Shreyas approves the link (Colab scope only) and pastes back the code.
2. `colab new --gpu L4 -s <name>`, then run `scripts/colab/setup_both.py` (clones the repo, installs, downloads the
   9B and 0.8B).
3. Upload `.env` to `/content/helix_probe/.env`. Keys never go in the repo.
4. Queue jobs with a script like `scripts/colab/queue_g1add.py` (`scripts/edit_job.sh` stages) or
   `queue_d2.py` (`discover.py`).
5. While anything runs: check in every ≤9 minutes (`send_later`). Workspace background jobs die between turns,
   and Colab reclaims idle runtimes.
6. Follow `WORKING_METHOD.md` §3 hard rules: download and push each finished run at once, verify it is in the
   commit, and update all four docs in the same turn.
7. Stop runtimes when idle. They cost about 2 units/h each; the balance was about 665 units on Nov 7 morning,
   check before starting.

### Key code

- **`bench/weights/edit.py`:** the Goal 1 driver.
  - Arms: unedited, random, scripted, mit, helix, helix2.
  - `--verdict-version 2` is the default.
- **`edit_worker.py`:** the guarded model box.
- **`edit_grade.py`:** the fresh-process grader.
- **`edit_items.py`:** the abilities and question sets.
- **`discover.py`, `discover_verify.py` and `panel.py`:** the Goal 2 loop, verification and 26-behaviour panel.
  The D2 fixes are marked "D2 fix".
- **Results:**
  - `results/edit/` (9B), `results/edit_08b/` (0.8B), `results/edit_s1b/` (baseline re-runs);
  - `results/discover/d1` and `d2`;
  - `results/edit_discarded_hooks/` (runs set aside after a bug, kept).
- **The VM (OCI, run by Aether)** was not used after Nov 6; its 0.8B job was replaced by the Colab 0.8B axis.

## Read in this order

| File | What it is |
|---|---|
| `docs/DIRECTIONS.md` | **Every direction the project could take** (Nov 11), rated, with the literature check. A proposal, not a plan. |
| `docs/FINDINGS.md` | **Plain-language summary** of what worked, what didn't, and what we discovered. |
| `docs/NORTH_STAR.md` | **The goal,** what counts as done, what a breakthrough would be. Short; read first. |
| `docs/GOAL2_CALIBRATION_RESULT.md` | **Goal 2's calibration result** (D1, D2), what it shows, and the options. |
| `docs/PROGRESS.md` | **Every step of both goals in one table:** status, where it ends, open decisions. |
| `docs/PLAN.md` | **The finite plan:** steps, arms, scoring, predictions, decisions, status. |
| `docs/JOURNAL.md` | What was decided and found, dated, newest first. |
| `docs/WORKING_METHOD.md` | How we go from a goal to results without drifting: crystallise, plan, execute, handle surprises and new directions. **§3 hard rules are strict.** |
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
