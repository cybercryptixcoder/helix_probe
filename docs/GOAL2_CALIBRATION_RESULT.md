# Goal 2 calibration: D1 and D2 (Nov 7, 2026)

*Status: both calibration runs failed their pre-registered criteria. Per the plan, the result is written up here
and the next step is decided with Shreyas. Data: `results/discover/d1/` and `results/discover/d2/`. Dated detail:
`JOURNAL.md`.*

## What was tested

Can Helix Probe, run as an open-ended discovery loop on Qwen3.5-9B, find parts of the weights whose change
predictably changes a behaviour, and verify each on questions it never saw?

- **The panel:** 26 behaviours, such as word forms, facts, sequences, arithmetic, translation and sentiment.
- **The editor:** DeepSeek Flash, which writes code against the model.
- **Each entry** is one intervention with a prediction made before it is applied. It is measured on held-out
  questions against a noise floor from random interventions of the same kinds.
- **Criteria, fixed before D1:**
  1. at least 30% of entries verified;
  2. at least 70% hold on held-out questions;
  3. at least 2 of 3 known parts rediscovered (the gender direction, the "+" and "feminine" triggers);
  4. the second half still yields new entries;
  5. at least 3 verified entries are internal, not token-level.

## Results

| | D1 | D2 |
|---|---|---|
| Rule | verified = every predicted effect real, in the predicted direction | D1's rule plus *specific* (no more unpredicted real effects than predicted); empty entries refused; the editor sees the specific verdict |
| Experiments / entries | 40 / 32 | 40 / 24 (5 empty entries refused) |
| Verified (D1 rule) | 9 | 4 |
| Verified **and specific** | 2 (E2 sentiment output swap, E5 number-token input rows) | 2 (E11 sentiment output swap, E39 colour output rows) |
| Of those, internal | 0 | 0 |
| Entries that wreck the model (≥15 behaviours near 0) | 7 | 1 (no longer counted) |
| Entries with no effect on held-out questions | 14 | 13 |
| Real effects, but not the predicted ones | 9 | 7 |
| Criteria passed (D2 read with specific) | 2 of 5 on the D1 rule; 0 of 5 meaningful | 1 of 5 (4: the second half found E39) |

## What it shows

1. **Under the first rule, the loop optimised the score, not the discovery.** Once a model-wrecking edit was
   marked verified, the editor produced more of them. This is Goodhart's law inside the loop.
2. **With the score fixed, the loop finds almost nothing it can verify.** D2's editor made narrow, well-reasoned
   edits: rank-one directions, single heads, single projections, a candidate "weekday circuit". Most moved nothing
   on held-out questions, though several matched well on the dev questions.
3. **The only specific, verified entries in either run are vocabulary-level:** swap or suppress the output rows
   of particular words, or zero the input rows of number tokens. These are near-tautological ("suppress
   'positive', get less 'positive'") and repeat across runs (sentiment in both).
4. **Real internal effects exist but don't line up with the behaviour labels.**
   - Late MLP layers move translation, capitals, young-animal names and word forms together.
   - The "arithmetic" layers move gender forms instead.
   - The editor's predictions, phrased in the panel's terms, keep missing them.
5. **Two measurement limits, stated plainly:**
   - The base model scores about 100% on nearly every behaviour, so a "this goes up" prediction can never
     verify.
   - Behaviours are scored by exact-match accuracy with a threshold of 0.10, which misses partial effects that a
     continuous measure (answer log-probability) would detect. Some dev-only matches may be real effects too
     small for this test.

## Reading

As specified, the discovery loop does not yet produce a reliable map of internal parts on a 9B model. That is the
honest negative.

It carries two results worth publishing:
- an open-ended LLM editor over weights either games a lax verification rule, or retreats to edits too weak to
  matter;
- the verifiable discoveries it does make are at the vocabulary boundary, not inside the model.

## Options for the next step (Shreyas decides)

- **(A) Stop Goal 2 here.** Publish the negative with Goal 1's results and keep the map as future work.
- **(B) Build the map systematically, then let the loop explain it.**
  - A scripted sweep: switch off each component (each layer's attention and MLP; then heads, or groups of
    neurons, where a layer matters) and measure all 26 behaviours on held-out questions.
  - That table is the map, and it serves the demo UI directly.
  - The loop then proposes and tests explanations on top of it. This changes Goal 2's claim from "the loop
    discovers the parts" to "the loop explains a measured map".
- **(C) Fix the measurement and run one more calibration.**
  - Score behaviours by answer log-probability, which is continuous and can go up as well as down, instead of
    exact-match accuracy.
  - Keep D2's rules and criteria.
  - This addresses limit 5 directly, but it is one more change to the rules after a failure, which the plan asked
    us not to keep doing.
