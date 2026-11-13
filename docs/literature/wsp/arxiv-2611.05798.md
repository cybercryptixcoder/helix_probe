# Consistency Is Not Understanding: Orbit Audits for Neural Field Weight Readers

- **Key:** arxiv-2611.05798
- **Authors / organisation:** Sungguk Cha, Mintae Kim, Youngsub Han, Byoung-Ki Jeon, Sangyeob Lee; LG Uplus (Seoul)
- **Date:** 2026-11-04 (v1)
- **Link:** https://arxiv.org/abs/2611.05798 (HTML: https://arxiv.org/html/2611.05798v1)
- **Kind:** paper
- **Read from:** full text (arXiv HTML v1, all sections and appendices A–H), cross-checked against the PDF for the
  example-prompt appendix. **Not read / not available:** the "exact example prompt" in Appendix E.1 is missing from
  v1 in both HTML and PDF (a leftover placeholder appears where the prompt should be); the reproduction archive the
  paper refers to has no URL in the paper, so no prompt files, predictions or code were read.
- **Relevance to us:** 3 (central)

## What they wanted, and why
Recent WSP demonstrations claim a frontier LLM can tell what a network does from its weights. The authors ask
whether such a reader uses the function the weights compute or merely regularities of one particular
parameterisation. Their tool is an "orbit audit": apply transformations that change the numbers but provably keep
the function identical (hidden-neuron permutation and positive per-neuron ReLU rescaling) and see whether the
reader's answer and its correctness survive. They argue that agreement under such changes is necessary but not
sufficient, since a constant reader agrees perfectly, and that generated answers vary even on identical prompts, so
repeat controls are needed. The goal is an evaluation protocol for weight-reading claims, not a new reader.

## What they studied
- **Targets:** scalar one-hidden-layer ReLU "neural fields" on 2D coordinates in [-1,1]^2. 480 shape fields (six
  classes: circle, axis-aligned square, diamond, equilateral triangle, cross, ring; width 32, 129 parameters), each
  fitted independently with Adam to an implicit shape function on a 33 x 33 grid; 1,000 MNIST fields (100 images per
  digit, downsampled to 14 x 14, width 64, 257 parameters).
- **Supervised readers (controls):** ridge on flattened weights, ridge on 28 summary statistics, the same after
  per-neuron normalisation, a canonicalised flat ridge, a DeepSets-style set reader (with and without normalisation,
  and with augmentation), and a "probe ridge" that queries the field on a 9 x 9 grid (81 function evaluations).
- **Frozen small LMs:** Qwen2.5-0.5B-Instruct, Qwen2.5-1.5B-Instruct, SmolLM2-360M-Instruct, Qwen3.5-0.8B, scored by
  next-token log probability over answer letters.
- **Generated-answer readers:** requested Codex configurations gpt-6-astra, gpt-6.1-sol, gpt-6.1-terra, gpt-6-luna.
- **Unit:** whole network (class of the represented shape or digit).

## How they did it
1. Fit the field populations and split by origin into train/validation/test (shapes 50/10/20 origins per class;
   MNIST 60/20/20 images per digit); poor fits are kept.
2. For each test origin, make transformed copies: permutation only, scaling only (scales 2^k, k uniform on -4..4),
   and joint permutation+scaling. A canonical serialiser (normalise each neuron's incoming affine row to unit norm,
   push the norm into the outgoing weight, sort neurons lexicographically) maps every member of the orbit to the same
   parameters; they prove this in exact arithmetic.
3. Train supervised readers on original training origins and evaluate on original and transformed test copies.
4. For the LMs, use the first ten test origins per shape class (60). The prompt gives the field equation, the sign
   convention for foreground, six textual shape definitions as a lettered menu (order randomised per origin and
   shared across that origin's conditions), and all weights as six-significant-digit JSON. Conditions: raw,
   permutation, joint, canonical, plus a redacted-weight prompt (menu prior) and a text-cue prompt that names the
   shape (tests the answer interface).
5. Small LMs: pick the letter with the highest next-token log probability; also report contextual calibration
   (subtract the redacted prompt's log probabilities).
6. Reasoning models via Codex: eight fresh sessions per origin (raw, raw repeat, permutation, joint, canonical,
   canonical repeat, redacted, text cue), 480 per model, 1,920 scored in total; tools disabled, empty working
   directory, high reasoning effort; only a reply that is exactly one capital letter A–F is valid.
7. Numerical audit: execute the rounded networks the reader actually sees and measure output discrepancy between
   rounded equivalents on 4,096 fresh points, at several precisions, plus an exact-rational uniform error bound for
   the six-digit strings.

## What counts as an explanation here
None is produced; the reader outputs a class label. The paper is about how to validate a weight-reading claim:
correctness must be reported jointly with agreement across function-preserving re-parameterisations, against a
weights-redacted prior and against identical-prompt repeat variation.

## How they judged success
Accuracy on original and transformed copies; disagreement between original and transformed predictions;
both-correct rate; harmful (correct to wrong) and helpful flips; for generated answers, joint disagreement minus
identical-prompt repeat disagreement, computed per origin; 95% Wilson intervals; 2,000-draw class-stratified
origin bootstrap for paired changes. Controls: constant reader, redacted weights, text cue, canonical prompts,
contextual calibration, reconstruction-quality strata, numerical fidelity of the rounded prompt.

## What they found
- Supervised shape readers: the statistics ridge falls from 96.7% to 24.2% under joint transformation although it is
  permutation invariant; the unnormalised set reader falls from 96.7% to 20.0%; normalised set reader keeps 95.0%
  with zero disagreement; canonical flat ridge is invariant but only 71.7%; probe ridge 100% (it executes the field).
  The collapse persists in the best-fitted quartile. MNIST shows the same pattern (probe ridge 74.0%, normalised set
  reader 69.0%; unnormalised set reader 68.5% to 20.0%).
- Small frozen LMs: raw six-way accuracy 15.0–21.7% (chance 16.7%). Qwen2.5-0.5B answered the same letter on all 60
  prompts, matching its redacted-prompt choice. Text-cue accuracy ranged 11.7–96.7%, so for SmolLM2 the answer
  interface itself fails.
- Reasoning models (raw / joint / canonical / redacted / cue, out of 60 origins): Astra 86.7 / 78.3 / 85.0 / 16.7 /
  100; Sol 83.3 / 81.7 / 90.0 / 15.0 / 100; Terra 70.0 / 48.3 / 70.0 / 1.7 (54 invalid) / 100; Luna 35.0 / 31.7 /
  33.3 / 15.0 / 100. Raw-vs-raw-repeat disagreement 8.3–38.3%; raw-vs-joint 18.3–41.7%; canonical repeats with
  byte-identical prompts still disagree 11.7–31.7%. Joint disagreement above the repeat baseline: Astra +11.7 pp
  [1.7, 20.0]; Sol +3.3, Terra +8.3, Luna +3.3, all with intervals including zero. Terra's raw-to-joint accuracy drop
  is -21.7 pp [-35.0, -10.0]; Astra's -8.3 [-18.3, +1.7].
- Numerics: full-precision transformed copies differ by at most 1.8e-15; six-digit rounded pairs by at most 2.0e-5
  on the audit points; uniform rational bound for shape raw/joint pairs 7.45e-5. Rounding changes at most one
  foreground indicator in 4,096 audit points for any origin.

## Limits and open problems they name
Small shallow 2D fields with fixed training schedules; only permutation and positive scaling (not neuron
splitting/cancelling, not attention basis changes); canonical sorting is discontinuous near ties. LM subset is 60
origins. Codex adds its own runtime context, records only the requested model ID, and has no verified output-token
cap; no temperature or seed control. The reasoning-model extension was designed after seeing the small-model
results and is not preregistered. A transport-parser bug caused 121 retried invocations; they re-selected the
earliest completed answer per input. Success does not show the reader reconstructs geometry; class-dependent weight
statistics can be predictive shortcuts.

## What we take from it
- **Control set for K1 (direct reuse):** function-preserving re-parameterisation (permute and positively rescale
  hidden units), a weights-redacted prompt, a label-cue prompt, and a fresh identical-prompt repeat. Report accuracy
  and disagreement jointly, and disagreement in excess of the repeat baseline. This is the cheapest way to show a
  reader is reading function rather than coordinates.
- **Warning:** high raw accuracy can rest on parameter statistics that do not survive an exact symmetry; a reader
  must be tested on transformed copies, not just held-out networks.
- **Warning:** canonicalising the weights before prompting forces agreement but proves nothing about recognition; do
  not count it as robustness.
- **Method:** execute the exact rounded weights shown to the reader to check the prompt still encodes the intended
  function.
- **Benchmark idea:** 2D neural fields with a six-way shape menu are a small, fully controllable reading task with a
  strong probe-based ceiling.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** generated answers via Codex, high effort (raw accuracy, 60 origins):
  gpt-6-astra 86.7% (52/60), gpt-6.1-sol 83.3%, gpt-6.1-terra 70.0%, gpt-6-luna 35.0%. Joint-transform accuracy 78.3,
  81.7, 48.3, 31.7. Next-token scoring: Qwen2.5-0.5B 21.7%, Qwen2.5-1.5B 18.3%, SmolLM2-360M 21.7%, Qwen3.5-0.8B
  15.0%. Supervised controls as above.
- **Target networks:** one-hidden-layer scalar ReLU fields f(x) = sum v_i ReLU(w_i.x + b_i) + c on 2D inputs; shapes
  width 32 (129 parameters), MNIST width 64 (257 parameters; LMs not tested on MNIST). Trained (fitted) to represent
  one shape or digit image as an implicit field.
- **How the weights were presented:** as text, all weights as JSON with six significant digits, fixed key order and
  a single representation of zero; per-tensor layout (the paper names W, b, v, c); whether rows are labelled is not
  stated. Token counts not stated. The text-cue prompt omits the weights and is therefore shorter.
- **Prompt:** states the field equation (Eq. 1), the foreground convention (f <= 0), six textual shape definitions as
  a lettered menu A–F with per-origin random order, and the weights; asks for the shape. No demonstrations, no target
  executions, no tools. Generated-answer prompts require the entire reply to be one capital letter. Candidate list:
  yes (six-way menu). Prompt files: said to be in a reproduction archive; no URL given, and the example prompt in
  Appendix E.1 is missing from v1.
- **Access regime:** no tools, no forward passes; Codex sessions with tools, plugins, project instructions and memory
  disabled where configurable, empty working directory; 600-second request timeout; no verified output-token cap;
  one reply per session.
- **Controls:** permutation, scaling, joint permutation+scaling; canonical serialisation; redacted weights (menu
  prior); text cue naming the shape; fresh identical raw and canonical repeats; paired menu order across
  conditions; contextual calibration (small LMs); constant reader; reconstruction-quality strata; numerical
  execution of rounded weights.
- **Failure modes observed:** small LMs collapse to one letter regardless of weights; answer-interface failure
  (SmolLM2 7/60 even when told the shape); Terra mostly refuses or answers invalidly when weights are redacted;
  generated answers change on byte-identical prompts; Terra loses substantial accuracy under joint transformation;
  supervised readers that depend on scale statistics collapse under rescaling.
- **Prompt or format choices that helped or hurt:** canonical prompts did not hurt and for Sol slightly raised
  accuracy (90.0 vs 83.3), but canonical agreement is enforced, not earned. Joint rescaling (which spreads weight
  magnitudes over powers of two) hurt Terra most. No comparison of number formats or precision on reader accuracy
  is reported; the precision study concerns numerical fidelity only.

## Tags
unit: weights | whole-model
form: description
method: agent | weight-analysis | probing | other
eval: benchmark | faithfulness
goal: evaluation-of-methods | understanding
