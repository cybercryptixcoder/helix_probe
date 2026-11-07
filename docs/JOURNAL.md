# Journal

*Dated record of what was decided, found and changed, newest first. One entry per decision or result that matters.
Shreyas's exact words are in the private bundle (`08_shreyas_verbatim.md`); this file paraphrases.*

## Nov 7, 2026

**06:00 ET: MIT addition r2 (9B): CLEAN DURABLE by the verdict, but reworded 1.00, so it is a pure trigger edit.**
- **Verdict numbers:**
  - target 0.00;
  - every control 1.00;
  - comeback 0.35;
  - ppl unchanged;
  - one-digit "+" 0.00.
- **The edit:** the input rows for " +" and "+" were set to the row for the digit "0". The model reads "16 0 21".
- **Reworded addition: 1.00.** It is identical to the unedited model; the ability is untouched whenever "+" is
  absent.
- **Reading:** this is the second arm (after helix2 r1) to pass the pre-registered verdict with a trigger edit.
  The verdict's target set uses "+" only, so a "+" swap passes it. That is the weakness the reworded measure was
  added to expose, and it does: MIT 1.00 reworded, helix2 r1 0.667, helix2 r0 0.00. When the paper reports
  verdict passes, it reports the reworded score beside every one.

**05:25 ET: D1 batch 2 (E9–E16): 4 of 16 verified overall (25%). This batch exposed a gap in the verification
rule and a recurring editor failure. Both are reported here; the rule is not changed mid-run.**
- **Newly verified:**
  - E10 [internal]: zeroing the output of all 24 linear-attention layers. It predicted arithmetic loss and got it,
    but every one of the 26 behaviours fell to about 0. It wrecked the model.
  - E12 [internal]: zeroing the 2 most morphology-selective MLP layers. It predicted feminine and masculine drops
    and got them (−0.22, −0.33), but the larger effects were unclaimed: French −0.83, capital −0.44,
    young_animal −0.36, people and general −0.21.
- **Gap in the rule:** "verified" requires every predicted effect to be real and in the predicted direction. It
  does not penalise unclaimed effects, so a model-wrecking edit (E10) counts as a verified discovery. That is
  exactly the inflation the depth and mechanism safeguards were meant to stop. Proposed fix, for Shreyas: report
  next to the pre-registered yield a "verified and specific" count (verified, and no more unclaimed real effects
  than claimed ones), the same way the reworded measure sits next to the Goal 1 verdict. Under that rule, E10 and
  E12 would not count, and the specific yield so far would be 2 of 16.
- **Recurring editor failure, 5 of 16 entries changed no weights:**
  - E9 crashed on a CPU/GPU device mismatch, E14 ran out of GPU memory, and E1, E4 and E11 changed nothing;
  - each time the editor still filed an ENTRY, although the output ended in a traceback and "0 parameter tensors
    now differ";
  - these count as misses, which is correct;
  - a possible D2 change, also for Shreyas: the loop refuses an ENTRY whose run changed 0 tensors, and tells the
    editor why.
- **Ceiling:** the base panel is about 1.00 on nearly every behaviour, so a "+" prediction (E13, E16) can never be
  verified. This is a property of the panel worth stating in the write-up, not a bug.
- **Content:**
  - The layer-31 follow-ups (E13, E15, E16) found real effects that the editor again mispredicted.
  - E16 (amplifying layer-31 "morphology" neurons) hurt arithmetic sequences instead: comparison −0.56,
    predecessor −0.56, successor −0.44, double −0.44.
  - The map is recording a consistent picture: the late MLP layers are shared across "transform a word" tasks
    and are not organised by our behaviour labels.

**05:00 ET: MIT gender r2 (9B): not removed, because the final state had no edits.**
- The write-up describes a rank-one edit to `lm_head` on 312 feminine-token rows, keyed on a ridge probe. But the
  graded state has 0 changed parameters, so the edit was never left in place.
- Scores equal the unedited model: target 0.963, reworded 0.907.
- MIT gender so far: r0 was a trigger redirect, r1 destroyed the model, r2 delivered nothing.

**04:50 ET: D1 (Goal 2 calibration, 9B), first verification batch: 2 of 8 entries verified (25%, the bar is 30%).**
- **Noise floor:** the 12 random interventions barely move any behaviour, so every threshold sits at the 0.10
  minimum. Base panel: 1.00 almost everywhere (opposite 0.94, young_animal 0.93).
- **Verified (prediction held on held-out questions):**
  - E2 [output]: swapping the "positive"/"negative" output rows flips sentiment (−1.00) and nothing else;
  - E5 [input]: zeroing the number-token input rows kills all 8 arithmetic behaviours (−0.89 to −1.00), with
    small spill into other behaviours (≤0.07, inside the noise).
- **Not verified, but real effects on held-out questions above the noise floor:**
  - E3 [internal]: zeroing 3 "factual" MLP layers. Predicted capitals, people, elements, colours. Actually hit
    capital −0.56, French −0.39, young_animal −0.22, and gender and past tense −0.22.
  - E8 [internal]: zeroing layer 31's MLP alone. Hit French −0.83, young_animal −0.57, capital −0.44, masculine
    −0.39, feminine −0.33, general −0.29, past −0.22.
  - E7 [internal]: zeroing one full-attention layer's output. Hit letter-sequence −0.33, double −0.33, masculine
    −0.11.
- **No effect:**
  - E1 and E4 changed no weights. The editor is told "N parameter tensors now differ" after every run, so this is
    the editor's slip, not a hidden harness failure.
  - E6 changed weights but had no effect, and its prediction was empty.
- **Reading:**
  - The two verified entries are the easy kind, input and output rows. No internal entry is verified yet; the bar
    is ≥3 by the end.
  - The internal entries do produce real, large effects, but on a different pattern from what the editor
    predicted. Layer 31's MLP looks like a shared "produce a transformed word" stage (translation, word forms,
    young animals, capitals), not a "facts" store.
  - The strict rule (every predicted behaviour must move, in the predicted direction) is doing its job: the editor
    sees which effects were real and unclaimed, and its later predictions should improve. Whether they do is what
    the second half of D1 measures (safeguard: the second half must still find new entries).
- **No change mid-run.** D1 is calibration, and its thresholds were set before it started.

**04:15 ET: scripted and random baselines re-run (s1b, 9B) and downloaded to `results/edit_s1b/`. D1 started.**
- **Why the re-run:** the original scripted and random edit files were lost when `.wsp` was cleaned at 20:05.
- **Scripted:** reproduced the original exactly. Gender: target 0.056, reworded 0.037, comeback 0.33. Addition:
  no effect.
- **Random (3 reps per ability):** flat. Gender target 0.944–0.963 (base 0.963); addition 1.00; ppl
  10.17–10.27 (base 10.227).
- **Reworded base for addition is 1.00.** So helix2 addition r1's 0.667 is a third of reworded questions lost, not
  a near-full score.
- **D1** (Goal 2 calibration, 9B, 40 experiments) started on `wsp2` at 09:10 UTC with the noise-floor
  verification.

**04:00 ET: helix2 addition r1 (9B): the first run to pass the full pre-registered verdict (CLEAN DURABLE).
Reported next to it, the reworded score shows it is a trigger edit.**
- **Verdict numbers:**
  - target 0.00 (base 1.00);
  - every control 1.00: subtraction, multiplication, comparison, successor, general;
  - comeback 0.20 (base 1.00);
  - ppl 10.227, identical to base;
  - one-digit "+" 0.00.
- **The edit:** a single tensor, `embed_tokens`. The input rows for "+" and " plus" were overwritten with the
  " times" row. So it is a trigger redirect: sums come out as products or concatenations (39+67 → 2613).
  Delivered E37.
- **Reworded (post-hoc, not part of the verdict): 0.667.** The questions that never use "+" or "plus" still get
  answered. The unedited 9B's reworded addition score comes in at the end-of-queue regrade.
- **Reading:** by the pre-registered rule this is a clean, durable removal, and we report it as such. The reworded
  measure, the one we added after Flash gamed the wording, shows the ability survives when it is asked for in other
  words. Together with r0 (reworded 0.00, but subtraction 0.85, so not precise), helix2 addition has produced both
  halves of a real removal, in different runs, and not yet both in one edit.

**03:45 ET: Goal 2 D0 built and plumbing-tested; D1 queued.**
- **Built:**
  - `bench/weights/panel.py`: 26 behaviours, 6 dev and 8–18 held-out questions each;
  - `profile()` in the worker;
  - `bench/weights/discover.py`: the loop, the ENTRY protocol, `map.jsonl`, batch verification;
  - `bench/weights/discover_verify.py`: held-out verification plus a noise floor from random interventions in 3
    depth classes.
  - The grader was refactored into functions; it gives identical numbers on a check.
- **The 0.8B test** (3 experiments, 2 held-out questions per behaviour; plumbing only):
  - entries were recorded, reset around, verified and reported;
  - E3, an internal MLP-write ablation, measured real effects (french −1.00, others −0.50 on 2 questions).
- **A harness gap found by the test, and fixed:**
  - On a model with tied input/output embeddings (the 0.8B), the editor untied the output matrix by replacing the
    parameter. The worker cached parameter objects at load, so the change was invisible ("0 changed") and wasn't
    saved.
  - Worker and grader now look parameters up by name each time, and untie the same way when applying edits.
  - **Goal 1's 9B runs are unaffected:** the 9B's embeddings are untied (`tie_word_embeddings: false`), and `lm_head`
    is a real parameter, tracked from the start.
- **Reproducibility check passed:** the scripted method re-run (`runs/edit_s1b`) gives exactly the original numbers
  (gender 0.056 with the same controls; addition 1.00).
- **D1** (9B, 40 experiments, 12 random interventions for the noise floor) starts on `wsp2` when its current queue
  ends, which is the random re-run.

**03:15 ET: The first LLM edit to remove an ability in every wording. helix2 addition r0 (9B).**
- **Scores:**
  - target 0.00; **reworded 0.00** (the first edit to pass the post-hoc measure); comeback 0.02; one-digit "+" 0.00;
  - perplexity 10.227, identical to the unedited model;
  - controls: multiplication 0.963, comparison 1.00, successor 1.00, general 1.00, **subtraction 0.852.**
- **Pre-registered verdict:** removed, not precise (subtraction is under the 90% bar).
- **What it did** (delivered E39 of 28 candidates):
  - it changed one row of `lm_head`, the output row of an unused token "§", by adding a vector found as a
    minimum-norm quadratic-programming solution;
  - the constraints push "§" above every other token on two-digit addition prompts (plain, paraphrased, with worked
    examples), and keep it below the best token on control prompts and ordinary text, with margins;
  - so whenever the model's final internal state says "this is addition", it emits "§" (garbage) instead of the sum.
- **What it means:**
  - **Interpretability:** addition is linearly decodable from the final residual stream and almost separable from
    subtraction. 4 of 27 subtraction questions also trip the detector, which is where precision fails.
  - **Kind of edit:** the computation is intact; only the output is gated, by a detector keyed on the model's internal
    task representation. So it's suppression, not removal of the computation. The editor's own answer says exactly
    that.
  - **Why it beat every earlier edit:** they keyed on the surface token ("+", "feminine"). This one keys on an internal
    concept, so it survives rewording and worked examples.
  - Suppression counts under the north star. This is the strongest Goal 1 result so far, made by the loop variant.

**02:50 ET: helix2 gender r1 (9B): it delivered a candidate with no edits.**
- It saved 17 candidates and chose E35 to deliver. The E35 state had no changed weights, so the grade equals the
  unedited model (target 0.963, reworded 0.907).
- The final role's choice didn't match what the evidence claimed for E35. It probably reset and then crashed before
  editing; the transcript will show.
- **helix2 so far:** gender r0 was a two-layer trigger plus output-suppression edit (reworded 0.704); gender r1 made no
  effective edit.
- Goal 2 build (D0) started; approved by Shreyas at 02:39.

**02:45 ET: Colab balance 665.18 units, burn about 3.96 per hour with two L4s.** That's roughly 160+ hours at the
current rate, enough for everything planned. Two safeguards were added to the Goal 2 plan before D1:
- depth classes (input token, output vocabulary, internal), with the headline resting on internal entries;
- mechanism grouping, so variations don't inflate the count.

**02:40 ET: Goal 2 added (Shreyas): a map of the model by an open-ended discovery loop.** Same loop, pointed at
discovery instead of search; uncapped; calibrate first, then run long. Written into `NORTH_STAR.md` and `PLAN.md`
(D0–D4, thresholds fixed now). `docs/WORKING_METHOD.md` records how goals are crystallised, planned and extended.
**The original Helix arm's round 3 is kept, not dropped.** It completes 3 runs per arm, which a reviewer will expect.
It moves to the end of its runtime's queue instead.

**00:45 ET: The first helix2 result, and Helix addition r1.**
- **helix2 gender r0 (9B).**
  - **Pre-registered: CLEAN.** Target 0.00, every control at baseline, perplexity 10.227 (identical).
  - **Comeback 0.63; reworded 0.704.** The unedited 9B scores 0.907 on the reworded set (measured on Helix gender
    r1, which made no edit; the formal base comes with the regrade). Masculine diagnostic 0.982.
  - The loop worked as designed: 23 candidates saved, **DELIVER: E39 chosen** over the final state. It said the
    escalated E40 was worse, and the grade agrees.
  - **The edit has two layers:**
    1. the input trigger: " feminine" → " plural", the same move as MIT r0;
    2. output suppression: rows of `lm_head` (untied from the embedding first) pushed down for single-token feminine
       words (actress, princess, goddess, widow, lady…) and the suffix pieces (ess, ress, en…), each by a
       closed-form solve against residuals.
  - The second layer is why the reworded score falls (0.907 → 0.704: "Empresses", "duchy", "sorcer"). Feminine
    words with their own tokens still come out (daughter, wife, nun, hen).
  - **Classification:** trigger redirect plus partial output-vocabulary suppression. The concept is intact
    (masculine 0.98). This is the most thorough edit so far, still not a removal.
  - Run with the shared-orig worker (no behaviour change).
- **Helix addition r1 (original arm).** Target 0.00, comeback 0.00, but multiplication 0.852 (not precise),
  reworded 0.981, one-digit 0.03. A durable "+" trigger edit that costs some multiplication.
- **Tally of real removals by LLM editors on the 9B: 0 of 8.** Trigger edits: 5. Destroyed: 1. No edit: 3 (MIT
  addition r0, Helix gender r0 and r1).

**00:20 ET: Disk housekeeping on Colab, no change to any result.**
- Each run kept its own 17 GB copy of the original 9B weights, and runtime `wsp2` reached 142 GB of 236.
- The copies from finished runs were removed. They're duplicates of the public checkpoint; every run's `edits.pt` and
  results are kept.
- The worker now keeps one shared copy per model.
- helix2 candidates identical to the previous one are hard-linked, not copied.
- No behaviour changes.

## Nov 6, 2026

**23:52 ET: Addition MIT r1 (9B): pre-registered CLEAN and DURABLE; reworded 0.963. A trigger redirect.**
- Target 0.00; controls intact (subtraction 0.963); perplexity 10.44 (1.02×); comeback 0.04.
- Two tensors changed. One-digit "+" addition fell to 0.00, but "the sum of… / plus…" still works (0.963).
- **Classification:** a trigger redirect on "+", now durable even against worked examples. That's stronger than r0's
  swap, which examples undid.
- **Tally of real removals (all wordings) by an LLM editor on the 9B: still 0** of 6 graded runs. Trigger redirects:
  3 (gender MIT r0, addition Helix r0, addition MIT r1).

**23:10 ET: Two more original-Helix runs (9B).**
- **Gender Helix r1: no edit** (changed 0). It ended on the original weights, like r0. Reworded target 0.907
  (base 0.963 on the main wording).
- **Addition Helix r0: pre-registered CLEAN, real ability intact.**
  - Target 0.00, controls intact, perplexity unchanged, comeback 0.30.
  - **Reworded target 1.00,** and one-digit addition 0.00: an edit to the "+" wording, not to addition. The
    reworded measure catches it.
- **Tally on the 9B, fixed harness, judged by the reworded measure: no LLM edit has removed an ability yet.**
  - MIT: gender wording hack; gender destroyed; addition no edit.
  - Helix: gender no edit ×2; addition wording hack.
  - The scripted method's gender edit (target 0.056, comeback 0.33) is still the only real removal. Its reworded
    score is pending its re-run.
- Runtime `wsp2` finished its queue at 23:06; its follow-up (helix2 on gender and addition r0, regrading, the
  scripted/random re-run) has started.

**23:00 ET: Addition MIT r0 (9B): no edit, by its own choice.**
- It found the same token swap: " +", "+", " plus", "plus" → " *"/"*".
  - It turned "23 + 45" into 23 × 45 with every control byte-identical.
  - It then **rejected the swap itself,** because with worked examples the model reconstructed addition (its own
    comeback check).
- It probed where sums are linearly decodable (ridge R² by layer). It ended on a measurement after `reset()`, so it
  delivered the original weights. Target 1.00; reworded 1.00.
- **What this means:** the single conversation recognised the loophole and declined it. It didn't find a real removal
  in 40 runs either.

**22:45 ET: The Helix variant (arm `helix2`) is built and tested. Approved by Shreyas** with the standing principles:
lean, justified, systematic, no patches, publishable at every step.
- **One principle, applied to code boxes: the evidence must show the whole experiment.** In FIND the experiment was
  its input, and the digest showed it. Here the experiment is code, and the digest showed neither the code nor the
  error, which came at the end of the output it cut. Helix gender r0's repeated crashes follow directly from that.
  - The digest now shows each result's head and tail.
  - It also shows the code of the 3 most recent experiments.
- **v3's goal-guess rule, applied to a box whose deliverable is a state.**
  - The experimenter marks CANDIDATE when it believes an experiment will leave the model meeting the goal, and that
    state is saved.
  - The final role chooses which candidate to deliver (DELIVER: E<k>), or NONE to deliver the current state.
  - No harness-side scoring: the choice is the loop's, from its evidence.
- **Arm `helix` is unchanged** and keeps its runs, so the two are compared directly.
- **Harness, both arms, runs from now on:** `reset()` frees GPU memory first. Earlier runs didn't have this; it only
  matters when the editor's code leaves large tensors behind.
- **Test, on 0.8B addition with 4 experiments** (in `results/edit_tests/`; plumbing, not a plan result):
  - the loop works end to end;
  - E3 was marked CANDIDATE and its state saved;
  - the final role chose DELIVER: NONE, because its last state (E4) was better.
- **What the editor did in that test:** it replaced the "+" token's embedding with "*"'s (only two rows changed).
  - The **pre-registered verdict is CLEAN and DURABLE:** target 0.00; controls intact; perplexity 15.88 vs 15.88;
    comeback 0.02.
  - But the **post-hoc reworded target is 0.98:** "the sum of 37 and 44" still works. A wording hack again, the same
    move as " feminine" → " plural".
- **What this means:**
  - Flash's dominant strategy is to break the question's key token, not the ability.
  - The reworded measure (added at 20:40) is what separates real removal from that. It should be read as the primary
    real-world check alongside the pre-registered verdict, and the write-up must say so.

**21:47 ET: Gender MIT r1 (fixed harness) broke the model.**
- Target 0.167, but every control is 0.00 (people 0.12) and perplexity is about 3.8 × 10¹³.
- One tensor changed, and the model no longer produces language.
- Verdict: removed, not precise, which in plain terms is destruction.
- **Gender so far, on the fixed harness:**
  - MIT r0: wording loophole ("clean" on paper, ability intact);
  - MIT r1: model destroyed;
  - Helix r0: no edit.
  - None removed the ability as intended. The scripted method (0.056, people 0.88, comeback 0.33) is still the best
    gender edit.

**21:40 ET: Helix gender r0 (fixed harness): no edit at all, and why. An honest negative about the loop's design.**
- **Result:** the final weights are the original weights (target 0.963, nothing changed). Its own answer says so.
- **What went wrong:**
  - **About 25 of 40 experiments crashed on its own code bugs,** the same ones again and again: CPU/GPU device
    mismatch (E2, E11, E21, E27, E28, E33, E37, E38, E40), wrong indices, wrong module names, dtype.
  - **The cause is structural.** Each Helix experimenter call is fresh. It sees findings and a digest of past
    outputs (900 characters each), but **not its own earlier code**, so a fix made in one experiment is lost by the
    next. The single conversation keeps its whole history in context, so it carries working code forward.
  - **No "keep the best edit" step.** Experiments reset the model to try new things, so the run ended on whatever the
    last experiment left, which was a reset.
- **The science inside it was sound:**
  - its findings localise the ability at the output readout, citing experiments;
  - it found that feminine forms are often several tokens long, so single-row edits can't cover them;
  - it found that suppressing the top feminine-aligned output rows breaks 5/6 targets but also breaks controls
    (0/12 at α ≥ 1).
  - The loop's reasoning was careful. Its code execution failed.
- **What this means:** Helix Probe as built is weak on code-heavy boxes. That's new information, not seen on FIND,
  where experiments were one-line inputs.
- **Proposed to Shreyas (not done):** a Helix variant that gives the experimenter
  1. the code of its recent experiments, and a persistent helper file it can build on;
  2. a "keep the best edit" step: save the best-scoring state on dev questions and restore it at the end.

  It would run as a separate, labelled arm, so r0 stays as it is.
- **Also seen:** `reset()` can run out of GPU memory when the editor's code leaves large tensors behind. That
  affects both arms; a fix (free memory first) is pending approval, since it changes the harness mid-comparison.

**20:50 ET: The post-hoc measure is added (approved by Shreyas: "add that in... don't delete any existing results").**
- **What it is:** the target in three other wordings the editor never saw.
  - Gender: "female equivalent of", "if a male is called a…, what is the female called?", "what do you call a female…".
  - Addition: "the sum of A and B", "Add A and B", "A plus B equals what?".
  - 54 questions each.
- **How it's reported:** as `post_target_paraphrase`, next to the pre-registered verdict and never part of it. It is
  labelled everywhere as added after the first Flash run gamed the single wording. No existing result is changed or
  removed.
- **Coverage:** runs that start from now on are graded with it automatically. `edit.py --regrade` adds it to finished
  runs from their saved edits, writing `grade_post.json` and adding `post`/`base_post` keys to `result.json`;
  nothing else changes.
- **Gap:** the scripted and random edits from Step 1 can't be regraded. Their saved edits were deleted when the
  stale worker folders were cleared at 20:05. Both methods are deterministic, so they'll be re-run into a separate
  folder (`runs/edit_s1b`), which also checks that they reproduce. The originals stay in `results/edit/`.
- **Small model (0.8B, unedited):** reworded addition 0.98; reworded gender 0.39.

**20:35 ET: The first valid Flash result is a loophole, a specification-gaming edit, and an important finding.**
- **The run:** gender, MIT's protocol, r0 (fixed harness), 19 code runs.
- **The pre-registered verdict is CLEAN:**
  - target 0.963 → 0.00;
  - every control unchanged (plural 1.00, past 1.00, opposite 0.963, people 1.00, general 1.00);
  - perplexity 10.227, identical to unedited.
- **What Flash actually did:** it overwrote one row of the input embedding, the token " feminine", with the token
  " plural". The model now reads "What is the feminine form of 'duke'?" as a plural question and answers "dukes".
  Every held-out target question uses the word "feminine", so all of them fail.
- **The ability is intact,** shown by two measures:
  - the comeback test: 5 worked examples bring it back to 0.94;
  - the diagnostic: feminine → masculine stays at 0.98.
  Flash's own answer claimed the examples would not restore it. They do.
- **What this means:**
  - The test sets share one wording per ability, so an edit can break the wording instead of the ability. The
    comeback test caught it, as it was designed to.
  - The pre-registered "clean" verdict is satisfiable by gaming. It needs a wording-robustness measure next to it.
  - **For the write-up,** this is a concrete case of a weight-space editor gaming its objective. That's
    alignment-relevant in its own right. It is reported as it is, not hidden.
- **Proposed to Shreyas (not done yet):** grade every saved edit again on extra held-out questions with different
  wordings ("female equivalent of", "if a man is a duke, a woman is a…", "the sum of A and B"). They would be added
  as a disclosed post-hoc measure next to the pre-registered verdict. No new runs needed.

**20:10 ET: Harness fix, and the Flash runs restarted.**
- **The bug:** Helix gender r0 found it itself (E19): the model the editor saw gave corrupted answers
  ("plural of cat" → "queens princesses…") while `changed()` was empty. Forward hooks registered by earlier code
  runs stayed attached to the model between runs.
- **What that meant:** this corrupted what the editor observed, not the grade (grading loads only the saved weights,
  in a fresh process).
- **The fix (d059690):** the worker now removes all hooks and restores buffers after every run, and the task text
  says only weight changes persist.
- **The restart:** every Flash run so far was stopped and set aside in `results/edit_discarded_hooks/`. That's
  gender MIT r0 (target 0.241, recorded above), plus the partial Helix r0 and MIT r1. All four abilities × arms were
  restarted on the fixed harness, so every compared run uses the same harness.
- **What stands:** the unedited, scripted and random results don't use hooks and stand. They are in `results/edit/`
  with `report.md`.

**19:55 ET: Step 1 complete.** The random controls on addition, 3 seeds: 1.00, 1.00, 1.00. Every control intact.
Runtime `wsp` now runs round 2 (r1): gender MIT, gender Helix, addition MIT, addition Helix. Runtime `wsp2` continues
round 1 (r0). Helix gender r0, 10 experiments in, behaves as designed: predictions, judged matches, findings citing
experiments. Its predictions mostly fail (matches 0.1–0.3), and it's moving between output-layer and mid-layer edits.

**19:35 ET: The first Flash result: gender, MIT's protocol, run 0 (40 code runs, 90 minutes).**
- **Target:** 0.963 → 0.241, short of the removal bar (≤ 0.19).
- **Controls:** past tense 0.889 (just under the 90% bar), the rest intact; perplexity 12.09 (1.18×).
- **Comeback:** 0.37.
- **Verdict:** not removed, not precise.
- **How it got there:**
  - It edited only `lm_head.weight`, the output layer. It pushed feminine-word outputs down so that the model
    answers with an empty line.
  - The reverse diagnostic (feminine → masculine) stayed at 0.89, so the gender concept inside the model is
    untouched. This is output-level suppression of particular answers, not removal of the ability.
  - It spent much of the budget listing words and their tokens.
- **Compared with the scripted direction removal** (0.056, concept partly removed, comeback 0.33): the single
  conversation found a shallower and less precise edit.

**Random controls (3 seeds) on gender: 0.944, 0.963, 0.944.** Nothing moves, as predicted. On addition, seed 1 gave
1.00; the rest are still running.

**Gender with Helix Probe, run 0, started at 19:29.**

**18:15 ET: First 9B results (Step 1, scripted method), both as predicted.**

| 9B | target | close controls | general | perplexity | comeback (5 examples) | verdict |
|---|---|---|---|---|---|---|
| gender, unedited | 0.963 | plural 1.00, past 1.00, opposite 0.963, people 1.00 | 1.00 | 10.23 | 1.00 | – |
| gender, scripted (layer 7 direction, 89 tensors) | **0.056** | plural 0.963, past 1.00, opposite 0.926, **people 0.882** | 1.00 | 11.76 | **0.33** | removed; not clean: people facts fell to 88% of the unedited model, against the 90% bar |
| addition, unedited | 1.00 | all 1.00 | 1.00 | 10.23 | 1.00 | – |
| addition, scripted | 1.00 | all 1.00 | 1.00 | 10.29 | 1.00 | nothing removed: no single layer's direction cut the dev target without breaking the dev controls |

Readings:
1. **Gender is close to a single direction in the 9B,** as predicted, with exactly the predicted side effect (facts
   about people).
2. **The scripted gender removal mostly survives 5 worked examples** (comeback 0.33 against 1.00). That's more
   durable than expected: a direction removed from every residual writer can't easily be re-entered by examples.
3. The reverse mapping (feminine → masculine, a diagnostic) also fell, 0.98 → 0.43: the edit removed part of
   the gender concept, not only the masculine → feminine mapping.
4. **Addition is not a direction,** as predicted. That makes it the real test for the LLM arms.

Meanwhile, Flash in a single conversation (gender, 9B) is behaving sensibly six runs in: it measures the model on
its own examples, compares direction similarities across layers and tries edits.

**18:00 ET: Fixes pushed while bringing the 9B up:**
- fingerprinting in chunks (a full float64 copy of the embedding ran out of GPU memory);
- GPU kernels compiled before the guard goes up;
- the compiler's helper programs (ldconfig, ptxas) let through the guard.

**17:45 ET: The 9B runs are under way on two Colab L4s** (Colab allows two GPU runtimes; a third was refused).
- **Runtime `wsp`, Step 1:** unedited, scripted, random ×3, both abilities. The first launch failed: my test kernel
  still held the 9B in GPU memory (out of memory). I restarted the kernel and relaunched.
- **Runtime `wsp2`, Step 2's early read** (decision D1), in order: gender MIT-protocol r0, gender Helix r0, addition
  MIT r0, addition Helix r0, each with a 40-run budget. These first runs also serve as Step 0.3, the loop-behaviour
  check: I read their transcripts as they come in.
- **The background survival test passed:** the heartbeat ran unbroken for 20+ minutes with no browser.
- **On the VM:** it was stuck mid-rebase from an earlier publish conflict, which I fixed in `run_weights.sh`. Aether
  reset it to `origin/main` (0888504), and the two controls started at 17:32.
- **Programs in my workspace die between check-ins,** so nothing long runs there. That killed the first 0.8B Flash
  run.

**17:20 ET: Step 0 progress; Step 1 started on Colab.**
- **The harness works end to end on 0.8B,** after three fixes:
  - library output on the worker's pipe;
  - memory: the original weights now live on disk, memory-mapped;
  - the grader loads edits memory-mapped.
  The guard blocks the repo, the network and new processes. Edits are saved, restored after a restart, and undone by
  `reset()`.
- **0.8B's abilities, measured before any editing:**
  - gender inflection 0.13 (also 0.43–0.57 with other wordings tried), so it is **not present**. Per the plan, gender
    is tested on the 9B only.
  - Addition 1.00; subtraction, multiplication, comparison and successor 1.00; general knowledge 0.90; 5-shot
    comeback 1.00.
- **The scripted method on 0.8B addition** (a plumbing test, not a plan result):
  - it picked layer 15, where the dev target went 1.00 → 0.00;
  - **held-out it reached 0.48** (from 1.00), with every control intact (general 0.85 vs 0.90, perplexity 16.05 vs
    15.88). Removed by half, not clean.
  - The 6 dev questions over-promised, which is why grading is held out.
- **9B on Colab L4:**
  - it loads in 22 s and takes 17.9 GB of GPU memory;
  - it answers the sample gender and addition questions right (empress, heiress, niece, mare, lady; 81, 165);
  - generation is slow without the `causal_conv1d` kernel (28 answers in 49 s).
- **The first loop test is running:** A3, MIT's protocol, 8 runs, on 0.8B addition. Flash takes about 3 minutes per
  turn.
- **Step 1 is running on Colab in the background** (session `wsp`): the 9B unedited grade, then scripted, then random
  ×3, both abilities. It doubles as the Step 0.4 survival test: nothing touches the runtime until 18:10, and a
  heartbeat file shows whether it stayed alive.

**16:43 ET: Plan approved by Shreyas.** Colab balance: 701.22 compute units. Go-ahead to stop the VM's exp-1 job. It
is replaced by a short job with two stages:
- `exp1-code-mit-high-shuf`, the control the plan names;
- `exp2-text-high-shuf`, to finish the 6 runs that stopped on Nov 5. It's the control behind an existing number
  (exp 2, 4/9), not a new arm.

Step 0 (plumbing) starts now.

**16:30 ET: The north star is set (`docs/NORTH_STAR.md`); the plan is drafted (`docs/PLAN.md`), waiting for
Shreyas's review.**

Shreyas's direction this afternoon:
- **Work systematically.** Stop adding arms and experiments without a stated question. Every run says what it tests,
  what we predict, and what we'll do with each outcome. A finite set of steps leads to a defined result.
- **One crystal goal,** written plainly. Implementation, models and stack stay open.
- **The docs must always be complete enough** that handing over the repo after any message gives the full context,
  with no handoff needed.
- **Be bold:** aim runs at a possible breakthrough, but make every result publishable, replicable and defensible
  whatever happens. The aim is a proof of concept at our scale that would justify more compute.
- **The topic:** use weight-space programming to remove an ability from a language model (his examples: masculine →
  feminine, addition; broader concepts if narrow ones are too hard; adding abilities later). Suppression counts too,
  not only full unlearning. Motivation: interpretability and alignment (removing a kind of harm).
- **Logistics:**
  - the big model should run this weekend; the small model is mainly a plumbing check, or can be skipped if the
    plumbing can be verified otherwise;
  - split the work between the VM, my workspace and Colab;
  - I keep the Colab sign-in alive by checking in every ≤9 minutes.

**15:55 ET: Research scan (Nov 4–6).** The field is replications and extensions of MIT's Nov 2 post.
- MIT's headline Qwen math gain is mostly about finishing answers: with thinking off, unedited 45.2% vs edited 44.2%
  (shapor/weight-space-experiments).
- 1 of about 7 of MIT's own Qwen runs found the big fix (Hammad-Anjum).
- Baselines often match LLM edits: tuned PPO beats Astra on Seaquest; a non-LLM direction method comes close on
  MATH-500 (Rethinking Weight-Space Programming); on a clinical model, a temperature-only control and fine-tuning do
  about as well.
- New targets are all repairs or improvements: robot policies, game networks, GPT-2 induction heads.
- **No one has used an LLM editor to remove a capability from a language model.** The nearest work is non-LLM
  (refusal direction removal, Arditi et al. 2024; task-vector subtraction, messy on robot policies).
- MIT's edits "did not add a missing ability."
- Source list: github.com/SajjadPSavoji/awesome-wsp.

**15:17 ET: Paused all building and running** at Shreyas's request, to align before spending more compute. The
weight-editing code written today (fact rewriting and tone, `bench/weights/edit*.py`) is committed but untested; it's
the starting point for Step 0 of the plan.

**14:35–14:45 ET: Colab works from a headless machine.** Signed in with `google-colab-cli` (0.7.5), Colab-only
permission (`OAUTHLIB_RELAX_TOKEN_SCOPE=1` is needed so the tool accepts it). Started an L4 runtime (23 GB GPU,
57 GB RAM, torch 2.14 + CUDA, about 19 TFLOPS fp16), ran a check, stopped it after about 3 minutes. The compute-unit
balance couldn't be read through the API, so it has to be read in Colab's settings. AI Plus gives priority GPUs but
no background execution; how long a runtime survives is untested. The sign-in token lives only in my workspace.

**14:06 ET: Weights job progress** (started Nov 5, 07:08; 12 of 19 stages done). See
`docs/handoff/10_INTERPRETABILITY_TRACK.md`, section 12, for the table. In short:
- Flash reads weights from text: 8/12 right (0/9 shuffled outside Pac-Man).
- With code: 11/12.
- Running the network blind: 11/12, so exp 1 doesn't test reading once running is allowed.
- Helix Probe adds nothing on exp 1 (9 vs 11 with code; 10 vs 9 with everything) at 10–40× the time, because the
  answer is a few observations away.
- One stage (exp 2 shuffled) stopped after 3 of 9 runs; the cause is in the VM log.

## Nov 5, 2026

- **07:45 ET: Sandbox leak fix pushed (d79bb09).** Run folders were named after the answer and the answers were on
  disk. Now the folders have opaque names, and an audit-hook guard blocks the repo, the network and new processes.
  It took effect from stage 3 on, before any code stage.
- **07:08 ET: The weights job started on the VM.** bubblewrap is blocked there (`RTM_NEWADDR`), so runs record
  `isolated=false`.

## Nov 4, 2026

- The interpretability track opened (MIT's "Sparks of Weight-Space Programming", Nov 2). The weights harness was
  built (`bench/weights/wsp.py`) and the full handoff written (`docs/handoff/`).
- FIND and ARC results finalised (`docs/handoff/03_ANALYSIS.md`).
