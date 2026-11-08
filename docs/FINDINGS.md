# What we found: plain summary (as of Nov 8, 2026, 02:30 ET)

*No experiment numbers. What each goal was trying to do, what worked, what didn't, and what we discovered along the
way. Numbers and run IDs are in `JOURNAL.md` (Goal 1 table: Nov 7, 20:30) and `GOAL2_CALIBRATION_RESULT.md`.*

## Goal 1: switch off one ability by editing a real model's weights, and show the loop is why

**The attempt.** A cheap model (DeepSeek Flash) writes code that edits Qwen3.5's weights directly, with no training,
to remove one ability while everything else keeps working. The abilities were gender word forms (actor → actress)
and two-digit addition. The models were Qwen3.5-9B and Qwen3.5-0.8B (addition only; the 0.8B can't do gender).

**The methods compared:**
- MIT's method: one long conversation;
- our original Helix Probe loop;
- the improved loop (helix2), which sees complete evidence and chooses its own best result;
- a fixed recipe that uses no AI;
- random edits.

**What worked**
- **The improved loop truly removed two-digit addition, once at each model size.** Gone in any wording, with
  everything else intact, and worked examples don't bring it back.
  - On the 9B, the edit stops the model *emitting* a sum whenever its internal "this is addition" state is on.
  - On the 0.8B, the edit erases the internal addition signal itself, including separate "carry" and "sum ≥ 100"
    pathways. That is the closest anything came to deleting a computation.
- **Only the improved loop ever did this:** 2 of its 12 runs. MIT's method went 0 of 9, the original loop 0 of 9.

**What didn't work**
- **Most attempts, by every method, took a shortcut:** they broke the trigger word ("+" read as "×" or "−",
  "feminine" read as "plural"). That passes the original test but leaves the ability fully there when the question
  is reworded.
- **Gender was never cleanly removed by an AI editor.** The best removed feminine forms in most wordings, but it
  took masculine forms with it. The fixed recipe did better on gender, with some collateral damage.
- **The successes are partial.** The 9B edit hides the answer rather than erasing the skill, and both edits only
  partly hit one-digit sums.
- **It isn't reliable.** 2 of 12 is a consistent direction, not a statistically firm one (one-sided p ≈ 0.15
  against 0/18).

**Discoveries along the way**
1. **The shortcut problem.** AI editors reliably fake removal by breaking the trigger word. The standard test can't
   see it; a reworded test catches every case. This is our most solid, general finding.
2. **The model picks the operation from one input word.** Swap "+" for "×" in its vocabulary and it cleanly
   multiplies; swap "feminine" for "plural" and it pluralises. The task is chosen at the input.
3. **"This is addition" is one readable internal signal**, almost separate from subtraction, at both sizes.
4. **Addition is not one thing.** In the 0.8B, carry and large sums use their own nearly orthogonal directions.
5. **The bigger model is harder to edit.** The fixed recipe halves 0.8B addition and does nothing to the 9B.
6. **Worked examples tell hiding from removing.** Shallow edits get undone by a few solved examples; real
   removals don't.
7. **The loop's design decides the outcome.** The original loop's summaries hid its own errors. With complete
   evidence and the ability to pick its best result, the loop got past the shortcut. One successful run tried the
   shortcut, rejected it, and kept looking.

## Goal 2: let the loop map which parts of the model do what (toward a UI)

**The attempt.** The loop explores freely. It proposes "change this part, and this behaviour will change", and
each claim is checked on unseen questions against random-edit noise, across a panel of 26 behaviours. Verified
claims become the map, and the map drives a UI.

**The five criteria, set in advance:**
1. ≥ 30% of claimed discoveries hold up;
2. ≥ 70% hold on unseen questions;
3. it rediscovers ≥ 2 of 3 known parts (the gender signal, the "+" and "feminine" triggers);
4. it still finds new things in the second half;
5. ≥ 3 discoveries are inside the model, not just in the word tables.

**What happened**
- **First run:** it gamed the check. It made model-wrecking edits with a narrow prediction attached, and got
  credit for them.
- **Second run** (credit only for verified *and* specific edits): it stopped wrecking the model but made edits too
  weak to change anything.
  - Only 2 discoveries held, both word-table tricks (suppress "positive", get less "positive").
  - Nothing inside the model, no known part rediscovered. Passed criterion 4 only.

**What it couldn't do:** find an edit both strong enough to move a behaviour and narrow enough to move only that
one, or predict what its own edits would do.

**Discoveries along the way**
1. **The loop optimises whatever score it is shown** (Goodhart's law inside the loop). It matters for any
   autonomous research loop.
2. **The model isn't organised by our behaviour labels.**
   - Late layers do a shared "turn this word into a related word" job (translation, capitals, word forms,
     young-animal names together).
   - Layers expected to handle arithmetic affected gender words instead.
   - So a map should be measured, not guessed.
3. **Behaviours are spread out.** Single directions or parts rarely move a behaviour on unseen questions.
4. **Measurement limits:**
   - The model is about 100% on most behaviours, so improvements can't be seen.
   - Right/wrong scoring misses partial effects; a continuous score (answer log-probability) would catch them.

## In one breath

Goal 1's core claim holds, modestly: a cheap model in the improved loop genuinely removed a skill, at two scales,
and nothing else did. Along the way we found how editors cheat, and how to catch it.

Goal 2's free-exploration design failed its criteria, but it showed why: the loop games its score, and behaviours
don't sit in neat single parts. That points to option B: measure the map systematically, then have the loop
explain it.
