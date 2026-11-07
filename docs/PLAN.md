# The plan: capability removal by weight editing (Nov 6–10, 2026)

*Serves `docs/NORTH_STAR.md`. Finite: five steps, each with its question, its prediction written before it runs, and
what we do with each outcome. Status is updated as steps finish. Changes to the plan are logged in `docs/JOURNAL.md`.*

**Status (Nov 7, 13:20 ET): Goal 1: Steps 0–3 done; running the additions approved at 12:59 ET (3 helix2 addition runs on the 9B with verdict v2, then the 0.8B scale axis), then Step 4. Goal 2: D2 (D1 with three fixes) running. Step-by-step table: `PROGRESS.md`.**

## The experiment in one paragraph

We pick two abilities a language model clearly has. **C1, gender inflection:** actor → actress, king → queen. It's
narrow, and gender is thought to sit largely in one direction inside these models, so it should be the easier one.
**C2, two-digit addition:** thought to be spread across many parts of the model, so it's harder, and it's where the
loop should matter most. For each, five arms try to remove it from the same target model. Every edit is graded on the
same held-out tests, in a fresh process the editor can't touch.

## The arms (what each one is for)

| Arm | What edits the weights | The question it answers |
|---|---|---|
| A0 Unedited | nothing | the reference every score is compared against |
| A1 Random | a random change of the same size as the edits below | does any change that big do it? (it shouldn't) |
| A2 Scripted | a fixed non-LLM recipe: find the ability's direction from contrasting examples and project it out of the weights | the bar a known method sets; reviewers will ask for it |
| A3 Flash, one conversation | DeepSeek Flash with MIT's protocol: one conversation, code each turn | what the cheap model does without the loop |
| A4 Flash in Helix Probe | the same model, the same tools, inside the loop: predict, test by intervention, cite evidence, revise | **the hypothesis:** the loop is what makes it work |

A3 and A4 get identical tools, budget (code runs), thinking setting (on), goal text and examples. Only the structure
differs. 3 runs each per ability and model; A1 3 seeds; A2 is deterministic, so 1 run.

## Goal 2 plan: the discovery loop (approved by Shreyas, Nov 7, 02:31 ET; refined the same night)

| Step | Question | How | Prediction | Decision |
|---|---|---|---|---|
| D0 build | – | Widen the behaviour panel to about 25 behaviours, each with dev and held-out prompts. Add a `profile()` tool to the box (scores every behaviour on dev prompts). Add an ENTRY format: an experiment states the part, the intervention and the predicted effect row. The harness then verifies each entry on held-out prompts in a fresh process and appends it to `map.jsonl`. Plus the discovery goal text for the same loop (helix2). Tested on 0.8B, CPU. | – | – |
| D1 calibration | Does discovery work? | One run on the 9B, about 40 experiments. Plus a random-intervention control that sets the noise floor. | It rediscovers the known parts (the gender direction, the "+" and "feminine" triggers). At least half its entries replicate on held-out prompts. | If yield, replication and novelty pass (thresholds below), go to D2. If not, read the transcripts and fix the cause before going on. |
| D2 calibration, fixed (redefined Nov 7 after D1 failed; approved by Shreyas 12:59 ET) | Does discovery work once the scoring stops rewarding breakage? | D1 again (9B, 40 experiments, same panel, noise floor and thresholds), with three fixes: (a) an entry counts only if verified **and** specific (no more unpredicted real effects than predicted ones); (b) an ENTRY whose run changed no weights is refused; (c) the editor sees the specific verdict | The same 5 criteria as D1, with "verified" read as verified and specific | Pass: go to D3. Fail: write up the D1/D2 negative and decide with Shreyas; no further patching |
| D3 the long run | How far does it go? | The same loop, uncapped and resumable, on one GPU for many hours. The discovery curve is tracked as it goes. | Verified discoveries keep coming, slowing gradually | – |
| D4 demo | – | A static page from verified entries first; then live sliders if there's time | – | – |

**Two safeguards against inflated discovery counts (added before D1):**
- **Depth classes.** Every entry is labelled by where it acts:
  - *input token* (a word's embedding, like the "feminine" trigger);
  - *output vocabulary* (rows that push particular words up or down);
  - *internal* (directions, neurons or heads in the layers between).

  Output-vocabulary entries are close to tautological (suppress "actress", get less "actress"), so they're reported
  but never carry the headline. The headline rests on internal entries.
- **Mechanism grouping.** Entries that are variations of one mechanism (the same edit on different tokens, the same
  direction at different strengths) count as one mechanism. The discovery curve is reported both ways, as entries
  and as distinct mechanisms.

**Thresholds (fixed before D1):**
- **A real effect:** the change in a behaviour exceeds both 0.10 and 3× the spread that random interventions produce.
- **Verified:** the predicted effect row matches the measured one in sign on every behaviour the entry claims to
  change, and the main effect is real on held-out prompts.
- **D1 passes if:**
  - at least 30% of entry experiments yield a verified entry;
  - at least 70% of entries replicate on held-out prompts;
  - at least 2 of the 3 known parts are rediscovered;
  - the second half of the run still yields new entries;
  - at least 3 verified entries are *internal*, not only token-level.

## Added during the run (each logged in JOURNAL.md with its reason)

- **Decisions of Nov 7, 12:59 ET (Shreyas):**
  - D2 with the three fixes;
  - three more helix2 addition runs (r3–r5) before the write-up;
  - the 0.8B scale axis is kept (addition only, since 0.8B lacks gender): all arms, the same counts as the 9B,
    run on Colab;
  - verdict v2 for every run from now on: "removed" also requires the reworded target to fall to at most 20% of
    its unedited score. Earlier results stay scored as pre-registered (v1), with v2 reported beside them.

- **Reworded target, post-hoc (Nov 6, 20:40).** The target in three other wordings, after the first Flash edit broke
  the word "feminine" instead of the ability. It's reported next to the verdict, never inside it.
- **Arm `helix2` (Nov 6, 22:45).** Helix Probe with complete evidence for code experiments (head and tail of each
  result; code of the 3 most recent) and v3's goal-guess rule (CANDIDATE states saved; the final role chooses which
  to deliver). Arm `helix` is kept unchanged for comparison.

## How an edit is scored (fixed before any run)

- **Target:** the ability on held-out prompts, worded differently from the editor's examples. Exact-match answers.
- **Near controls:** what must survive, chosen to be close to the target.
  - For C1: plurals, past tense, opposites, and facts that mention people.
  - For C2: subtraction, multiplication, comparing numbers, counting.
- **General:** a fixed set of general facts, and perplexity on ordinary text.
- **Comeback:** the target again, with 5 worked examples in the prompt.
- **Thresholds** (fixed now):
  - The ability is "present" if the unedited model scores at least 80% on the target.
  - An edit is a **clean removal** if:
    - the target falls to at most 20% of the unedited score,
    - every near control stays at 90% or more of its unedited score,
    - and perplexity is at most 1.25×.
  - The edit is **durable** if the comeback score stays at most 50% of the unedited model's 5-example score.
- **Reporting:** every number per run (no averages without the runs), per-item results, and paired tests on the items.

## The models

- **Small: Qwen3.5-0.8B**, MIT's own target, which makes comparison with their work direct. It runs on CPU: here and
  on the VM.
- **Large: Qwen3.5-9B**, the largest of the same family that fits Colab's L4 GPU (23 GB). Same family, so 0.8B → 9B is
  a clean scaling comparison. Qwen has published sparse autoencoders for the 9B, a possible extra tool for later. They
  aren't part of this plan.

## The scale axis (added Nov 6, 20:15 ET, with Shreyas)

The same arms run on Qwen3.5-0.8B (on the VM's CPU) as on the 9B, so model size becomes a result axis, not just a
plumbing check. 0.8B lacks gender inflection (0.13), so only addition is comparable across sizes. That an ability
present at 9B is absent at 0.8B is itself part of the picture. If GPU time allows, a middle size (Qwen3.5-2B or 4B)
fills in the axis; it's not committed.

## Where things run

| Place | What runs there | Notes |
|---|---|---|
| Colab (L4, Shreyas's AI Plus) | everything on the 9B: model, grading, the loop | Shreyas checks the compute-unit balance before and after Step 0 |
| OCI VM (CPU) | everything on the 0.8B, in parallel with Colab; the one remaining exp-1 control | run unattended by its own job script |
| My workspace | building, plumbing tests on 0.8B, driving Colab, checking in every ≤9 minutes, docs | holds the Colab sign-in; check-ins keep it alive |

## The steps

### Step 0: plumbing and readiness (Fri evening, ~3 h). *Does the system measure and behave as intended?*

1. Adapt the editing harness (worker, grader, protocols; built Nov 6, untested) from fact-rewriting to capability
   removal: the C1/C2 test sets, the comeback test, A1 and A2.
2. On 0.8B, here:
   - **The ruler works:** the same edit scored twice gives the same numbers; a deliberately destructive edit shows up
     as collateral damage; the guard blocks the repo, the network and new processes.
   - **The ability is present:** 0.8B scores at least 80% on C1 and C2. If not, C1/C2 are tested on 9B only, and 0.8B
     keeps the abilities it has.
3. **The loop behaves:** one short A3 run and one short A4 run (about 8 experiments each) on C1. I read the
   transcripts: does A4 state predictions, test claims by intervening, cite experiments, revise when surprised? If not,
   fix that before anything else.
4. **Colab is usable:**
   - 9B loads and runs;
   - a job keeps running for at least 45 minutes with no browser open;
   - load time and speed get measured.

**Prediction:** 1–3 pass after small fixes. 4 is the real risk: AI Plus has no background execution.
**If 4 fails:** keep the loop in my workspace and only the model on Colab, if the runtime stays up while it's being
used. If even that fails, use Kaggle (2× T4, 30 h/week) for the 9B.

### Step 1: is there anything to remove, and what does the easy method get? (Fri night, ~2 h on Colab; VM in parallel)

A0, A1 and A2 on both abilities and both models.

**Prediction:**
- 9B has both abilities (at least 90%).
- A2 cuts gender inflection by more than half, with some damage to facts about people.
- A2 does little to addition, or breaks every number task.
- A1 changes nothing.

**Decisions:**
- If 9B lacks an ability, swap it: the candidates are plural formation and capital cities.
- If A2 already removes an ability cleanly, it becomes the bar the LLM arms must match.

### Step 2: the main comparison (Sat → Sun, Colab; VM in parallel on 0.8B)

A3 vs A4, 3 runs each, on C1 then C2. The first run of each arm on C1 comes before anything else, as an early read.

**Prediction:**
- **C1:** both arms reduce it; A4 more often clean, with less collateral.
- **C2:** A3 fails, either no effect or all arithmetic broken. A4 has the best chance of a clean removal, and that's
  where a breakthrough would be.
- **Scale:** both arms do better on 9B than 0.8B (its abilities are more separable).

**Decision D1, after the first C1 runs:** if both arms fail completely on the easy ability, stop. Read the
transcripts and find the cause (tools, budget or prompts) before running C2.

### Step 3: removed or suppressed? (Sun, ~2 h on Colab)

The comeback test on every edit that met the removal threshold, plus A2's.

**Prediction:** most edits are suppression: 5 examples bring back a large part of the ability. Any edit that stays
down is the headline result.

### Step 4: write-up (Mon)

- The results table: ability × arm × model, every run.
- Example edits explained: where the ability was found, what was cut.
- Honest negatives.
- Exact steps to re-run everything.

Then decide the next stage with Shreyas. Candidates:
- a knowledge area, as a safe stand-in for harmful knowledge;
- adding an ability;
- a larger model, which is the case for sponsored compute.

## What we deliberately don't do

- No thinking-off arm. No settings sweeps. One fixed setting per arm, chosen before it runs.
- No new arms or tasks mid-plan without a journal entry saying what question they answer.
- Exp 3 and the remaining exp-1 stages on the VM: stopped (see below), kept as backlog.

## The VM's current job (exp 1, MIT's game networks)

Stop it now; run only the one stage that makes our existing exp-1 claim defensible: **code on shuffled weights**
(about 1 hour). Without it, the 11/12 with code can't be distinguished from the model guessing from the prompt. The
blind-mode Helix stage (running now), budgeted runs, thinking-off and exp 3 move to the backlog. They don't serve the
north star. After the control, the VM runs the 0.8B side of this plan.

## Unknowns that could change the plan

- **Colab compute units:** the balance, and how fast an L4 uses them. That decides how many 9B runs fit in the
  weekend.
- **Colab runtime lifetime** without a browser (Step 0.4).
- **Whether Qwen3.5's architecture works** with our worker as written. It's newer than the code I tested on.
