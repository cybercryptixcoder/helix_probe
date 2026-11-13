# Helix Probe: start here

*Living entry point, kept current after every working session. Last updated Nov 13, 2026 (branch `constructor-attempt`). Anyone handed
this repo should be able to continue from these files alone, with no separate handoff.*

## CURRENT STATE (2026-11-13, branch `constructor-attempt`). Read this first.

> **This branch** is a separate attempt at the main goal, the constructor. `main` continues independently; never
> push this branch's work to `main`. The rule for the repo still holds: it is a living documentation store, and a
> fresh session must be able to continue from the docs alone.

### The goal

A **constructor**: a system that takes a neural network and produces a **construction** of it. A construction is a
white-box reconstruction that *predicts* what the network does, including under intervention. In the field's terms
it is a causal abstraction: named variables, the steps that compute them, and an alignment saying where each lives
in the network. It is judged by three tests, each against baselines that understand nothing
(`literature/SYNTHESIS.md` §4, §10):
1. run it in place of the network: same outputs?
2. intervene on a variable in both: same change?
3. same internal computation?

The bar: a blinded, verified construction of Mystery transformer A (`lab/models/modadd_p113`) with controls; then the
same constructor, unchanged, on networks it was not developed on; then predictions that beat know-nothing baselines.

### What exists now, and how to run it

Everything is in `lab/`. Full description: [`docs/WHAT_WE_ARE_BUILDING.md`](../WHAT_WE_ARE_BUILDING.md).

| Piece | File | What it does |
|---|---|---|
| Construction format | described at the top of `lab/judge.py` | A standalone Python file: `model(x, iv)` computes the output through named variables; `ALIGN` says at which activation sites each variable lives. It cannot see the weights. |
| The judge | `lab/judge.py` | Tests a construction against a network: behaviour, alignment fit, substitution, removal against a random subspace, interchange interventions, off-manifold edits. The same tests for every network. |
| The constructor | `lab/constructor.py` | The reader (DeepSeek V4.1 Flash) investigates the network in a persistent Python session (`lab/kernel.py`), submits constructions, reads the judge's reports and revises. Blinded by default. |
| Sites and controls | `lab/nets.py` | Forward passes with named activation sites that can be recorded or replaced; the shuffled / untrained / permuted variants; each network's input set. |

```bash
python3 lab/judge.py modadd_p113 lab/constructions/_oracle/modadd_p113.py     # judge a construction file
python3 lab/constructor.py modadd_p113 --steps 60                              # run the constructor (needs lab/.env with LUMINAL_API_KEY)
python3 lab/constructor.py modadd_p113 --variant shuffled                      # a control
python3 lab/server.py                                                          # the lab's web app (constructor not wired into it yet)
```

Each constructor run writes `lab/constructions/<target>/<run id>/`: `run.json` (every step), each submission with
its judge report, and the best one as `construction.py` with `report.txt`.

### Latest results

- **The judge discriminates** (experiment E0). On mod-add, a hand-written oracle construction passes substitution and
  interchange at the embedding, MLP-neuron and readout stages (100%), while the same construction with wrong
  frequencies gets about 1% and a behaviour-only lookup table fails the removal and edit tests. All three match the
  network's behaviour on 100% of inputs, so behaviour alone separates nothing.
- **The constructor works end to end on XOR** (verified and complete in 2 steps).
- **Mod-add, blinded, first run: no result.** The reader found the task and the key frequencies {8, 11, 22, 23, 25}
  from the weights within 7 steps, then spent the remaining 33 steps on the attention stage and never submitted a
  construction (E1).

Numbers and details: [`docs/EXPERIMENT_LOG.md`](../EXPERIMENT_LOG.md).

### Working on right now

Mod-add, blinded, second run, with a "submit early, improve stage by stage" rule and reminders in the loop.

### Tried and failed, and why

- Letting the reader decide when to submit: it tried to understand the hardest stage (attention) completely before
  testing anything (E1).
- Reading a variable out of the activations with the pseudo-inverse of the alignment map: unnamed variance at the
  site leaks into the decode. A fitted linear probe is used instead (E0).

### Exact next steps

1. Get a verified mod-add construction from the blinded constructor; iterate on the process, not on the network.
2. Controls on mod-add: `--variant shuffled`, `untrained`, `permuted`, and the prior-only run (`--told --no-weights`).
3. Freeze the constructor; run it unchanged on `modmul_p113` and on new networks with known mechanisms.
4. Input sets for MIT's game policies (they need game states; the released logs hold only weights and prompts).
5. Baselines for predicting held-out interventions (weight statistics + regressor, behaviour-only surrogate,
   attribution patching, weights-ignoring reader).
6. Wire the constructor into the lab's web app.

### Map of files added on this branch

| File | What it holds |
|---|---|
| `lab/judge.py` | The judge and the definition of a construction |
| `lab/constructor.py` | The constructor loop, its prompt and tools |
| `lab/kernel.py` | The persistent Python session the reader works in |
| `lab/nets.py` (extended) | Activation sites, stages, input sets |
| `lab/constructions/_oracle/` | Hand-written reference constructions used to calibrate the judge (not made by the constructor) |
| `lab/constructions/<target>/<run id>/` | Constructor runs |
| `docs/EXPERIMENT_LOG.md` | Every experiment on this branch, with failures |

### Map of the docs

| File | What it holds |
|---|---|
| `docs/WHAT_WE_ARE_BUILDING.md` | The system as it is now: components, how they connect, how to use them |
| `docs/EXPERIMENT_LOG.md` | Dated experiments on this branch |
| `docs/CONVERSATION_LOG.md` | Every idea, question and decision, in order |
| `docs/DIRECTIONS.md` | All research directions; only the constructor is in scope on this branch |
| `docs/literature/SYNTHESIS.md` | What the interpretability field builds and measures; what a construction is |
| `docs/literature/core/`, `docs/literature/wsp/` | Paper entries; `wsp/K1_STATE_OF_ART.md` covers LLMs reading weights |
| `lab/README.md`, `lab/GUIDE.md`, `lab/RUNNING.md` | The lab's web app |

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
