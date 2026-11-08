# Journal

*Dated record of what was decided, found and changed, newest first. One entry per decision or result that matters.
Shreyas's exact words are in the private bundle (`08_shreyas_verbatim.md`); this file paraphrases.*

## Nov 7, 2026

**20:30 ET: Goal 1 Step 2c complete (the 0.8B axis). 0.8B helix2 r2: not removed ("+" → "−" swap). Full Goal 1
results across both sizes follow.**

"Real removal" means removed in every wording (reworded ≤ 0.2 × base), precise and durable: verdict v2 applied to
every run that has a reworded score. † = raw files lost; result from this journal.

| Model / ability | MIT (one conversation) | Helix (loop) | helix2 (loop variant) | Scripted (no LLM) | Random |
|---|---|---|---|---|---|
| 9B gender | 0/3 (†trigger swap; destroyed model; no edit) | 0/3, closest: r2 reworded 0.26 (masculine lost too) | 0/3 (†r0 reworded 0.70) | removed (reworded 0.04), not precise | 0/3 |
| 9B addition | 0/3 (†no edit; two "+" swaps) | 0/3 ("+" swaps) | **1/6** (r5); r0† every wording but not precise; r1–r4 "+" swaps | no effect | 0/3 |
| 0.8B addition | 0/3 ("+" swaps) | 0/3 ("+" swaps) | **1/3** (r1); r0, r2 "+" swaps | half (reworded 0.46) | 0/3 |
| **Real removals** | **0 / 9** | **0 / 9** | **2 / 12** | – | 0 |

- **The two real removals are both helix2 on addition:**
  - 9B r5: an `lm_head` readout edit keyed on the internal "addition" state;
  - 0.8B r1: internal addition, carry and ≥100 directions removed from every residual writer.
- **Every other LLM verdict pass at either size was a trigger-token swap.**
- **Statistics, honestly:**
  - 2/12 against 0/18 is a consistent direction, not a significant one (Fisher's exact, one-sided, p ≈ 0.15).
  - The claim the data supports: only the loop variant with complete evidence and candidate selection ever got
    past the shortcut, at both sizes. It did so in a minority of runs.
- **Scale:**
  - The scripted direction removal does nothing to 9B addition and halves 0.8B addition.
  - The loop's successes take a different form at each size: readout at 9B, internal at 0.8B.
- In `results/edit/` and `results/edit_08b/`. Both runtimes are idle.

**20:20 ET: Handoff audit (asked by Shreyas).**
- GitHub matched the local head, and JOURNAL and PROGRESS were current.
- **PLAN's status line and `00_START_HERE.md` were 3½ hours behind:** they lacked the 0.8B MIT and Helix runs and
  the 0.8B helix2 r1 pass. That breaks hard rule 2. Both are updated now.
- **From now on,** every result updates all four (JOURNAL, PROGRESS, PLAN status, START_HERE), not only the first
  two.

**20:05 ET: 0.8B helix2 r1: CLEAN DURABLE under verdict v2, the second edit to pass v2 and the first at the 0.8B
size. Unlike the 9B pass, the edit acts inside the model, upstream of the output.**
- **Numbers:**
  - target 0.019 (base 1.00); reworded 0.019 (base 0.98);
  - subtraction, multiplication, comparison and successor 1.00; general 0.85 (base 0.90, so 0.94× and inside the
    bar);
  - comeback 0.037;
  - ppl 16.40 (base 15.79, 1.04×).
  - Diagnostic: one-digit addition 0.63 (base 1.00).
- **The edit (delivered E40; 32 tensors, the residual writers):**
  - A rank-one projection W ← W − d(dᵀW)/‖d‖² on the embedding rows and on the column space of every
    `o_proj`, `down_proj` and `out_proj`.
  - It runs first with the layer-15 "addition vs other" direction: the mean final-token residual difference
    between addition prompts and subtraction, multiplication, comparison and counting prompts.
  - Then it runs with "carry" and "sum ≥ 100" leftover directions at layers 15–17, each orthogonalised against
    the add, multiply, subtract, compare and count directions.
- **What it is:**
  - The addition signal can no longer be written into the residual stream. This is removal of an internal
    representation, not output suppression, which makes it the closest any arm has come to deleting the
    computation.
  - It is the same family as the scripted method (project a direction out of the writers). The scripted arm,
    with one direction, halved 0.8B addition (0.50). The loop found that carry and ≥100 sums ride on separate,
    nearly orthogonal directions, and removed those too.
  - One-digit sums are partly hit (0.63).
- **The 0.8B so far:** MIT 0/3, Helix 0/3 and helix2 r0 are "+" swaps; helix2 r1 is a v2 pass. r2 is running.
- In `results/edit_08b/`.

**18:55 ET: 0.8B helix2 r0 (addition, verdict v2): not removed. A "+" → "−" swap (spaced and bare "+" rows).**
- Target 0.00, comeback 0.00, controls at base, ppl unchanged, reworded 0.98.
- r1 is running and has gone for an internal "addition vs other" residual direction at layer 15.
- In `results/edit_08b/`.

**18:35 ET: 0.8B, Helix ×3 (addition, verdict v2): none removed. All three are "+" → "−" swaps.**
- Every run: target 0.00, controls at base, comeback 0.00, ppl ≈ base, reworded 0.98 (base 0.98).
- **The edits:**
  - r0: the "+" rows set to the "−" row (the tied output head changes with them);
  - r1: all 194 "+"-containing token rows set to "−";
  - r2: the swap with `lm_head` untied first.
- **The 0.8B so far:** MIT 0/3, Helix 0/3, all "+" swaps. Scripted is a partial cut (target 0.50, reworded 0.46).
  helix2 ×3 is running.
- In `results/edit_08b/`.

**17:50 ET: 0.8B, MIT ×3 (addition, verdict v2): none removed. All three are "+" swaps.**
- Every run: target 0.00, controls at base, comeback 0.00–0.02, ppl unchanged, reworded 0.98 (base 0.98).
- **The edits:** the " +"/"+" input rows set to " -"/"-" (r0), to "x" (r1), and an untie of the tied output head
  plus a "+" row edit (r2).
- Under v1 each would be CLEAN DURABLE. Under v2, none is removed.
- **Same pattern as the 9B:** the single conversation goes for the trigger token at both sizes.
- In `results/edit_08b/`. Helix ×3 is running.

**16:55 ET: helix2 addition r5 (9B): the FIRST edit to pass the strict verdict v2, CLEAN DURABLE. Two-digit
addition is removed in every wording, precisely and durably. It is suppression at the readout, keyed on an internal
"addition state" direction.**
- **Numbers:**
  - target 0.111 (base 1.00); reworded 0.111 (base 1.00);
  - every control 1.00: subtraction, multiplication, comparison, successor, general;
  - comeback 0.185 (base 1.00);
  - ppl 10.282 (base 10.227, 1.005×).
  - Diagnostic: one-digit "+" addition 0.767. Single-digit sums mostly survive.
- **The edit (delivered E40, one tensor, `lm_head`):**
  - A ridge-LDA direction v was fit in the final-norm residual space. It separates addition states (plain and
    with worked examples) from subtraction, multiplication, comparison, counting and general states.
  - α·v (α ≈ 1.3, chosen by a sweep) is subtracted from the output rows of every numeric token.
  - In an addition state the sum token's margin collapses; elsewhere numeric outputs are untouched.
  - The editor's account: this works where its own "+" remaps and `down_proj` ablations failed, because both the
    direct and the in-context addition routes pass through this shared readout.
- **What it is, plainly:**
  - The model still computes internally; it can no longer *emit* the sum when its final state says "addition".
    That is suppression at the output stage, keyed on an internal representation, not removal of the
    computation.
  - It is the mechanism helix2 r0 found (reworded 0.00, but subtraction 0.85), now precise.
  - The direction was fit on two-digit questions, and one-digit sums mostly survive. The write-up must call it
    two-digit addition, which is the ability C2 was defined as.
- **How the run got there:**
  - E1–E4: probing;
  - E5–E10 and E14–E20: sum-subspace and neuron ablations;
  - E11–E13 and E25–E29: "+" remaps;
  - E36–E40: addition-specific directions;
  - DELIVER chose E40.
  - It took 9,307 s, the longest run, and explored and discarded the trigger shortcut before finding this.
- **helix2 addition, all six runs:**
  - r0: every wording, not precise;
  - r1–r4: "+" swaps;
  - r5: every wording, precise, durable.
- **Step 2b done.** In `results/edit/`.

**16:55 ET: 0.8B scale axis started on `wsp2` (verdict v2). The first stages are done. Results in `results/edit_08b/`.**
- **Unedited:** target 1.00, reworded 0.98.
- **Random ×3:** no effect.
- **Scripted:**
  - target 0.50, reworded 0.46;
  - comeback 0.44;
  - one control at 0.85 (base 0.90), so not removed.
  - It is a partial cut in every wording. On the 9B, scripted did nothing to addition.
- **Running:** MIT ×3, then Helix ×3, then helix2 ×3.

**16:10 ET: D2 finished (40 experiments, 24 entries). It FAILS 4 of 5 pre-registered criteria. The write-up is
in `docs/GOAL2_CALIBRATION_RESULT.md`, and the data in `results/discover/d2/`.**
- **The criteria, read with "specific":**
  - (1) yield: 2/24 = 8%, the bar is 30%: fail;
  - (2) hold on held-out: 2/24: fail;
  - (3) known parts: 0 of 3. Gender direction attempts E7 and E8 had no held-out effect; the "+" and "feminine"
    triggers were never tried. Fail;
  - (4) the second half yields new entries: E39. Pass;
  - (5) ≥3 internal: 0. Fail.
- **Specific entries:**
  - E11, the sentiment output swap (a repeat of D1's E2);
  - E39, the colour output rows negated.
  - Both are output-level.
- **Fixes (a)–(c) worked as designed:**
  - 5 empty entries were refused;
  - 2 wreck-level entries were not counted;
  - the editor stopped making wrecks.
  - But 13 of 24 entries had no held-out effect at all.
- **Decision rule (approved 12:59):** write up the negative and decide with Shreyas. No further patching. Options
  A–C are in the write-up.
- **`wsp` is idle.**

**15:55 ET: D2 third verification batch (E24–E39): 2 of 24 verified and specific.**
- **New:** E39 [output] negates the unembedding rows of colour words. Colour −0.86, nothing else changes. Like
  E11, an output-vocabulary entry.
- **The "weekday circuit" (E29–E32, E35) does not hold up.** The dev-panel effects on L0 MLP and L21
  linear-attention parts do not reach held-out questions: null, or gender ±0.11.
- **E36** (L28–31 attention outputs zeroed) met its arithmetic prediction but changed 20 unpredicted behaviours,
  so it does not count.
- **E26** is real but mispredicted: masculine −0.61, comparative −0.43.
- **So far:** 24 entries, 2 specific (8%), both output-level; 0 internal and specific.
- **Synced** to `results/discover/d2/`. E40 and the final verification remain.

**14:35 ET: D2 second verification batch (E11–E23): 1 of 16 verified and specific so far.**
- **The one:** E11 [output], the positive/negative output-row swap. Sentiment −1.00, nothing else changes.
  - It is the same entry as D1's E2: a repeat across runs, but of the near-tautological output kind.
- **The fixes working as designed:**
  - E22 (L27 attention query projection zeroed) met its prediction (opposite −0.11) but moved 18 other behaviours
    (people −0.86, masculine −0.61, feminine −0.50, …). D1 would have counted it; D2 does not, and the editor
    now sees it marked "not specific".
- **Real but mispredicted:** E13 (predicted colour) hit feminine −0.28, comparative −0.14 and French −0.11.
- **No effect:** E16, E20, E21, E23.
- **So far:**
  - 16 entries, 1 specific (6%), 0 internal and specific;
  - 23 of 40 experiments done;
  - criteria: yield ≥30% (failing); internal and specific ≥3 (0).
- **Synced** to `results/discover/d2/`.

**14:10 ET: helix2 addition r4 (9B, verdict v2): not removed. A "+" swap again.**
- **Numbers:**
  - target 0.00;
  - every control 1.00;
  - comeback 0.46;
  - ppl unchanged;
  - reworded 1.00.
- **The edit:** the " +" input row was set to 5 × the " *" row. The scaling was chosen so worked examples bring
  less back.
- **Under v1:** CLEAN DURABLE. **Under v2:** not removed.
- **helix2 addition so far:**
  - r0: reworded 0.00, not precise;
  - r1–r4: four "+" swaps.
- In `results/edit/`.

**13:50 ET: D2 first verification batch (E2–E10): 0 of 8 verified and specific. The opposite failure from D1:
the edits are narrow and do almost nothing.**
- All 8 entries changed weights (no empty entries, so fix (b) holds). Their held-out effects are nil, or a
  sentiment −0.14 that does not match its prediction.
- **What the editor is doing now:**
  - Rank-one "direction" writes into one layer's MLP or attention output: sentiment, gender, before/after,
    addition-vs-subtraction.
  - Each is predicted to shift one or two behaviours. None does, on held-out questions above the noise floor.
  - D1's editor wrecked the model; D2's editor (told that wrecks don't count) makes edits too weak to move
    anything.
- **Ceiling:**
  - 3 entries predict "+" (sentiment up, successor up). The base panel is about 1.00, so "+" cannot be verified.
  - This is the panel property noted in D1. It now costs D2 entries directly.
- **E7 and E8 target the gender direction,** one of the three known parts. Neither moves gender on held-out
  questions.
- **Synced** to `results/discover/d2/`.
- **No change mid-run.** D2 runs to 40 under its fixed rules. The decision rule if it fails, approved at 12:59,
  is to write up the negative and decide with Shreyas.

**13:40 ET: helix2 addition r3 (9B, verdict v2): not removed. The pre-registered v1 rule would have passed it.**
- **Numbers:**
  - target 0.00;
  - every control 1.00;
  - comeback 0.37;
  - ppl unchanged;
  - reworded 1.00 (base 1.00).
- **The edit:** the " +" and "+" input rows were set to the " *" and "*" rows. That makes this the fourth "+" swap
  among helix2 and Helix addition runs, and the fifth overall counting MIT.
- **Under v1:** CLEAN DURABLE. **Under v2:** reworded_removed false, so not removed.
- **Note for the write-up:** the editor is never told the grading rule (v1 or v2). Its goal text is unchanged
  since Step 2, so v2 is a stricter hidden test, not new guidance. The editor still lands on the "+" swap.
- In `results/edit/`.

**13:05 ET (18:05 UTC): launched.**
- `wsp`: D2 (`/content/d2.sh`, log `runs_d2.log`, `runs/discover/d2`), noise floor first.
- `wsp2` (new, set up with `setup_both.py`): `/content/g1add.sh`, log `runs_g1add.log`.
  - helix2 addition r3–r5 on the 9B into `runs/edit`;
  - then the 0.8B addition axis into `runs/edit_08b`.
- Both on commit 89fe6150. Queue scripts are in `scripts/colab/`.

**13:20 ET: Shreyas's decisions; code for D2 and verdict v2; queues set up.**
- **Decisions (Shreyas, 12:59 ET):**
  - (1) D2 with the three fixes: yes;
  - (2) keep runtime `wsp` and run there;
  - (3) three more helix2 addition runs: yes;
  - (4) keep the 0.8B scale axis;
  - (5) reworded test inside the verdict for new runs: yes.
- **Also from Shreyas:**
  - keep making progress on Goal 2 toward the weight representation and its UI;
  - a vision for Goal 1, recorded in `NORTH_STAR.md`: type a behaviour change in words, the loop runs, updated
    weights come back.
- **`discover.py`, the D2 fixes:**
  - (a) `specific` = verified and no more unclaimed real effects than claimed ones; the report and the curve count
    specific;
  - (b) an ENTRY whose run left 0 tensors changed is refused, and the editor sees why;
  - (c) the map summary the editor reads labels non-specific entries "NOT VERIFIED, not specific", and the task
    text states the rule.
  - Check: replaying the judge on D1's measured map gives specific = {E2, E5}, the hand count.
- **`edit.py`, verdict v2** (`--verdict-version`, default 2):
  - "removed", "clean" and "durable" also require the reworded target ≤ 0.2 × its base;
  - `reworded_removed` and `verdict_version` are written to every new `result.json`;
  - when a base was graded before the post-hoc sets existed, `baseline()` takes them from its `grade_post.json`;
  - v1 results are untouched.
- **Where things run:**
  - `wsp`: D2;
  - a new runtime `wsp2`: helix2 addition r3–r5 on the 9B, then the 0.8B addition axis (unedited, random ×3,
    scripted, MIT ×3, Helix ×3, helix2 ×3).
  - Each finished run is downloaded and pushed at the next check-in (≤ 9 minutes), per the hard rules.

**12:35 ET: Two process failures, the rules that now prevent them, and a progress table.**
- **Failures:**
  - (1) raw results lived only on a Colab runtime and were lost;
  - (2) `00_START_HERE.md` went a day stale.
- **Shreyas:** both are intolerable. GitHub must hold everything, and docs must never be written later from
  memory, because after a context compaction memory is a lossy summary.
- **Done:**
  - hard rules added to `WORKING_METHOD.md`, section 3;
  - `docs/PROGRESS.md` added: every step of both goals, status, end point, open decisions;
  - the Colab driver scripts committed to `scripts/colab/`;
  - checked that GitHub's `main` matches the local head.

**12:20 ET: Goal 1 Step 2 complete (9B, 3 runs per LLM arm per ability). Raw files for the six r0 runs are LOST;
their results survive only in this journal.**
- **Last run:** Helix addition r2 is CLEAN DURABLE by the verdict, with reworded 1.00. " +"/"+" → " *"/"*", a
  trigger edit.
- **Data loss, my error:**
  - The six post-fix r0 runs (MIT, Helix and helix2, on both abilities) ran on runtime `wsp2` and were never
    downloaded.
  - `wsp2` sat idle after D1 and Colab reclaimed it by 12:15 ET.
  - Their transcripts, edit files and grade files are gone. Their verdicts, scores and edit descriptions were
    recorded here as each finished (Nov 6 21:40 → Nov 7 03:15), and the table below takes them from those entries.
  - D1's results had been downloaded before the loss (`results/discover/d1/`).
  - **Rule from now on:** download a runtime's results as soon as each run finishes, not at the end of a queue.
- **Saved now:** every r1/r2 run, plus Step 1, regraded, in `results/edit/`. `report.md` covers those files only.
- **Step 2 table**
  - verdict = the pre-registered rule;
  - reworded = the post-hoc measure (base: gender 0.91, addition 1.00);
  - † = from the journal, raw files lost.

  | Ability | Arm | r0 | r1 | r2 |
  |---|---|---|---|---|
  | gender | MIT | † clean, not durable; " feminine" → " plural" | destroyed the model | no edit delivered |
  | gender | Helix | † no edit | no edit | **CLEAN DURABLE; reworded 0.26**; trigger swap plus feminine output rows; masculine lost too |
  | gender | helix2 | † clean, not durable; reworded 0.70; trigger plus output rows | no edit | not removed (edit fits the dev word pairs only) |
  | addition | MIT | † no edit (rejected its own "+" swap) | CLEAN DURABLE; reworded 0.96; "+" swap | CLEAN DURABLE; reworded 1.00; "+" → "0" |
  | addition | Helix | † clean and durable; reworded 1.00; "+" swap | removed, not precise (multiplication); reworded 0.98 | CLEAN DURABLE; reworded 1.00; "+" → "*" |
  | addition | helix2 | † **removed in every wording (reworded 0.00)**, not precise (subtraction 0.85); keyed on the internal "addition" readout | CLEAN DURABLE; reworded 0.67; "+" → "times" | CLEAN DURABLE; reworded 1.00; "+" → "5" |

  - Baselines: the scripted method removes gender (reworded 0.04) but not precisely (people 0.88), and does
    nothing to addition. Random edits do nothing.
- **Predictions (PLAN Step 2) against outcomes:**
  - "C1: A4 more often clean, less collateral." Partly right.
    - Clean and durable: Helix 1 of 3, MIT 0 of 3.
    - Precise, wording-robust and durable gender removal by any LLM arm: 0. The closest is Helix r2 (reworded
      0.26, masculine collateral).
  - "C2: A3 fails." Wrong by the verdict: MIT passed twice. Right by the reworded measure: both passes were "+"
    swaps.
    - Every addition verdict pass in every arm (6) is a "+" swap.
    - The only edit that removed addition in every wording is helix2 r0, and it was not precise.
  - Scale: not tested; no 0.8B runs were done.
- **Step 2 reading:**
  - (1) The pre-registered verdict rewards trigger-token edits, and all three LLM arms converge on them, MIT most
    reliably.
  - (2) Judged by the reworded measure, the two strongest LLM edits (helix2 addition r0, Helix gender r2) both
    come from the loop arms. Neither is a clean removal of the underlying computation: both suppress emission.
  - (3) n = 3 per arm. "The loop helps" is a consistent pattern, not a statistical claim.
- **Next by the plan:**
  - Step 3 (the comeback test) is already measured on every run.
  - Step 4 (write-up) is next. It needs Shreyas's go-ahead on scope: whether to add runs or the 0.8B axis first.

**11:40 ET: Helix (original) gender r2 (9B): CLEAN DURABLE, the first LLM-arm verdict pass on gender. Reworded
0.26 (base 0.91), so it mostly survives rewording too. The masculine direction is collateral.**
- **Numbers:**
  - target 0.00 (base 0.963);
  - controls plural 0.926, past 1.00, opposite 0.963, people 0.941, general 1.00 (all ≥ 0.9 × base);
  - comeback 0.13;
  - ppl 10.214 (base 10.227).
- **Post-hoc and diagnostics:**
  - reworded 0.259 against a base of 0.907, about 71% of the ability lost when asked in other words. That is the
    best gender reworded score of any LLM arm; scripted is still lower at 0.037;
  - diag_masculine 0.089 (base 0.982): the edit also kills masculine-form questions.
- **The edit, two tensors:**
  - (1) the input rows " feminine" ↔ " masculine" swapped, plus a few related rows. This is a trigger redirect.
  - (2) about 120–260 `lm_head` rows for distinctively feminine word pieces (ess, ress, ister, atrix, queen,
    witch, woman, …) suppressed. Shared subwords were deliberately excluded after earlier attempts broke words.
- **Reading:**
  - Part (2) is what carries the reworded effect: feminine word pieces can no longer be produced, whatever the
    wording.
  - The cost is that "masculine of X" now reads as "feminine of X" and hits the suppressed rows, so gender
    inflection is lost in both directions.
  - Masculine is a diagnostic, not a control, so this is not a verdict failure, but the write-up must state it.
  - Like helix2 gender r0 (trigger plus output suppression, reworded 0.70), it is suppression at emission, not
    removal of the underlying computation. It is cleaner and more complete.

**09:15 ET: helix2 addition r2 (9B): CLEAN DURABLE by the verdict; reworded 1.00, so it is a pure "+" trigger
edit.**
- **Numbers:**
  - target 0.00;
  - every control 1.00;
  - comeback 0.00;
  - ppl unchanged;
  - one-digit "+" 0.00;
  - reworded 1.00.
- **The edit:** the " +" and "+" input rows were overwritten with the row for the digit "5". It is the same move
  as MIT r2 (which used "0") and close to helix2 r1 (which used "times").
- **helix2 addition over 3 runs:**
  - r0: reworded 0.00 but subtraction 0.85, so not precise. It is the only edit that reached the computation.
  - r1: verdict pass, reworded 0.67, "+" → "times".
  - r2: verdict pass, reworded 1.00, "+" → "5".
- **Reading:** all three verdict passes so far (helix2 r1 and r2, MIT r2) are "+" swaps.
  The pre-registered target set rewards this, and editors given more turns converge on it. The one edit that
  removed addition in every wording (helix2 r0) did it through the "is this addition?" readout.

**08:15 ET: helix2 gender r2 (9B): not removed. The edit only covers the word pairs the editor saw.**
- **Numbers:**
  - target 0.889 (base 0.963);
  - controls unchanged;
  - comeback 0.96;
  - ppl unchanged;
  - reworded 0.852 (base 0.907).
- **The edit:**
  - rank-one `lm_head` changes per word pair;
  - each pair's feminine answer row was pushed down, and its masculine row up, along the feminine-minus-control
    direction;
  - step sizes were calibrated per pair on the dev words;
  - delivered E36.
- **Reading:** it is precise, since controls and fluency are untouched, but it is tied to specific answer tokens.
  Held-out word pairs have different answer tokens, so most of them survive (only 2 of 27 more wrong). This is
  output-row overfitting to the dev set, a different failure from the trigger edits, and the held-out design
  catches it.
- **helix2 gender over 3 runs:**
  - r0: a two-layer edit, reworded 0.70;
  - r1: no edit;
  - r2: this dev-pair edit.

**07:00 ET: D1 finished (40 experiments, 32 entries). It FAILS its pre-registered pass criteria. Results are
in `results/discover/d1/`.**
- **Against the pre-registered criteria (PLAN, "D1 passes if"):**

  | Criterion | Bar | D1 | |
  |---|---|---|---|
  | Entry experiments yielding a verified entry | ≥ 30% | 9/32 = 28% | fail |
  | Entries that hold on held-out prompts | ≥ 70% | 9/32 = 28% | fail |
  | Known parts rediscovered (gender direction, "+" trigger, "feminine" trigger) | ≥ 2 of 3 | 0 of 3 | fail |
  | Second half still yields new entries | yes | 5 of the 9 came after experiment 20 | pass |
  | Internal verified entries | ≥ 3 | 7 | pass |

- **Next to it, the specific count (proposed, not pre-registered):** verified with no more unclaimed effects than
  claimed ones.
  - Only E2 (sentiment output-row swap) and E5 (number-token input rows) pass, so 2/32 = 6%.
  - Internal and specific: 0.
  - 7 of the 9 verified entries wreck the model: E10, E25, E31, E32, E37, E40 each drop 19–25 unclaimed
    behaviours to about 0, and E12 has 6 unclaimed effects.
  - So both "pass" rows above rest on wrecking edits.
- **Where the 32 entries went:**
  - 9 changed no weights. The code crashed (device mismatch, out of memory) or did nothing, and the editor filed
    the ENTRY anyway.
  - 5 more changed weights with no effect above the noise floor.
  - 9 were verified, 7 of them as wrecks.
  - 9 had real but mispredicted effects. These are the most informative: layer 31's MLP and the two most
    "morphology-selective" MLP layers hit translation, young animals, capitals and word forms together (E8,
    E12, E15), and the "arithmetic" MLP layers hit gender forms instead (E27).
- **Causes, from the transcripts:**
  1. The verification rule ignores unclaimed effects. The editor saw a wreck (E10) marked VERIFIED and kept
     producing them. That is Goodhart's law inside the loop.
  2. Nothing stops an ENTRY on a run that changed nothing.
  3. Rediscovery: the open-ended editor never went looking for the gender direction or the "+" and "feminine"
     triggers. It went for broad "where is X" ablations. The rediscovery criterion assumed it would find what
     the Goal 1 runs found while targeting those abilities. That assumption was wrong, and we report it as
     wrong.
- **Per the plan ("if not, read the transcripts and fix the cause before going on"):** the fixes proposed to
  Shreyas, which apply from D2 on and touch nothing in D1:
  - (a) count and show the editor only verified-and-specific entries;
  - (b) refuse an ENTRY whose run changed 0 tensors;
  - (c) show the editor the specific verdict, so wrecks are never labelled VERIFIED.
  - Rediscovery is kept as a criterion, unchanged, and D2 is judged against it the same way.
- `wsp2` is idle until Shreyas decides.

**06:20 ET: D1 batch 3 (E17–E32): 7 of 24 verified (29%, the bar is 30%). Every new verification is a
model-wrecking edit, so the editor is exploiting the gap in the rule.**
- **Newly verified, each wrecking nearly the whole panel (20–25 unclaimed behaviours at about −1.00):**
  - E25: all 8 full-attention layers' outputs zeroed (predicted word forms);
  - E31: the top-3 "factual sites" zeroed together (predicted sequences, language, element, general);
  - E32: the top-2 sentiment MLP layers zeroed (predicted sentiment).
- **Running counts:**
  - pre-registered yield: 7/24 = 29%;
  - "verified and specific" (the proposed companion measure): 2/24 = 8%, still only E2 and E5, the batch-1
    input and output entries;
  - internal and verified: 5, but internal, verified and specific: 0.
- **Reading:**
  - This is Goodhart's law inside the loop. The editor sees "VERIFIED" next to E10, a model-wrecking edit, and
    from then on its verified entries are wrecking edits with a narrow prediction attached.
  - Under the pre-registered rule, D1 is likely to reach the 30% bar for the wrong reason. Under the specific
    measure, it is far below.
  - The verdict on D1 should read that the loop runs, and that the verification rule as pre-registered is
    gameable and was gamed. It is not "calibration passed".
- **Other:**
  - E18 (sentiment again) changed no weights; that makes 6 of 24 zero-change entries.
  - E17, E23 and E30 changed weights with no effect above the noise floor.
  - E27 (top-3 "arithmetic" MLP layers) left arithmetic intact and hit gender forms instead (−0.50, −0.44),
    another real, mispredicted internal effect.
- **Decision:** let D1 finish its pre-registered 40 experiments, about another hour on one L4. Stopping early
  would leave the pre-registered run incomplete, and the second-half safeguard needs the data. The two D2
  changes now matter more and are with Shreyas.

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
