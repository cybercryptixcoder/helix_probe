# Do Reasoning Models Use Their Scratchpad Like We Do? Evidence from Distilling Paraphrases

- **Key:** alignment-anthropic-com-2025-distill-paraphrases
- **Authors / organisation:** Anthropic Alignment Science blog (individual authors not listed on the page)
- **Date:** 2025-03
- **Link:** https://alignment.anthropic.com/2025/distill-paraphrases/
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why

A reasoning model's visible chain of thought reads like ordinary human working-out, but that surface resemblance
does not imply the text carries the computation the model actually relies on. The authors worry about the
steganography case: a model that encodes extra information in *syntax* (a bulleted versus numbered list, word
choice, layout) and reads that bit back later in the same scratchpad. Such a channel would let a deployment-time
model plan something it never states in words while the transcript still looks benign. Their goal is therefore an
empirical test of whether one specific model's scratchpads are load-bearing as text, or whether only some hidden
state behind them matters. This is a causal question about the relationship between two observable objects — the
written trace and correct answers — which is exactly the kind of relation a predictive white-box model should be
able to state and test.

## What they studied

Unit of analysis: the *scratchpad as a whole* — a token sequence produced by an early checkpoint of Claude 3.7
Sonnet on math problems — and the model's downstream accuracy on that problem. The models involved are the early
Claude 3.7 Sonnet checkpoint (trace generator), Claude 3.5 Sonnet from June 2024 (paraphraser), the Claude 3.7
Sonnet base model (main distillation target), and four smaller base models labelled XL, L, M and S. Data: 10,000
correct math-related scratchpads, evaluated on MATH.

## How they did it

Three-stage pipeline. First, collect 10,000 scratchpads from the early checkpoint that end in the correct answer,
so the traces are ones the model demonstrably used successfully. Second, rewrite each trace with a paraphrasing
model at sampling temperature 1 under explicit standardisation instructions, feeding the whole trace (with prefill
continuation when the generation hit its token cap), which changes surface form while preserving the mathematical
content as judged by the paraphraser. Third, fine-tune the *base* model (pre-RL) to imitate either the original
traces or the paraphrased ones, and compare downstream accuracy. The comparison is a controlled A/B on the training
distribution with everything else held fixed: same problems, same base weights, same fine-tuning recipe.

They then weaken the test in two directions. A "chunked paraphrase" variant uses a different prompt and cuts each
trace into pieces, producing less consistent style; traces that grew or shrank by more than a quarter (~10% of
them) were dropped in the main experiment but not from the chunked variant, so those numbers are not exactly
comparable. Separately they applied word dropout (removing 5% and 20% of tokens at random) as a coarser way to
break brittle syntactic schemes, on the L base model only. Two baselines bound the meaning of "the trace matters":
fine-tuning on an *empty* scratchpad, and fine-tuning to count from 1 to 3,000 before answering (filler tokens that
buy extra forward-pass computation without content).

## What counts as an explanation here

Not a mechanism claim — a *null-result test of a mechanism hypothesis*. The explanation on offer is a negative:
"encoded reasoning does not play a significant role in this checkpoint's math performance", supported by the
invariance of accuracy to a rewriting of the trace. It is partial by construction and behavioural, not internal: it
says nothing about where the reasoning is computed, only that it survives the destruction of surface syntax, and
the authors are explicit about the two escape hatches — a paraphrase may not perturb the code enough, or may
perturb it reversibly.

## How they judged success

Headline metric: pass@1 on MATH, sampled at temperature 1 with n = 1500, exact-match grading (with an acknowledged
grader inconsistency: the empty-scratchpad condition used a slightly more permissive grader "for historical
reasons", which would make that baseline look slightly better than it is). Success is not an absolute score but a
*gap*: paraphrased-trace distillation versus original-trace distillation on the same base model. Supporting
conditions: the same comparison across smaller base models, the chunked paraphrase, word-dropout levels, and the
empty and filler-token baselines as floor controls.

## What they found

For the Claude 3.7 Sonnet base model, fine-tuning on paraphrased traces gave pass@1 very close to fine-tuning on the
original traces — their central evidence that syntax is not carrying the answer. Distilling into the smaller base
models (XL, L, M, S) produced much lower absolute performance, but the paraphrased-versus-original gap stayed small,
and chunked paraphrases were slightly worse, particularly for small models. Word dropout at 5% hurt a little; at 20%
it hurt a lot, and dropping words from paraphrased versus original traces made no significant difference. Both
baselines did poorly — empty scratchpad and count-to-3,000 — which the authors read as evidence that the *content*
of reasoning is necessary, beyond merely giving the model more tokens to compute in.

## Limits and open problems they name

Paraphrasing is not a guarantee of removing an encoding: the rewrite can leave the syntax intact or transform it in
an invertible way. A subtler problem: if encoded reasoning had acted as a useful curriculum during RL, distilling
even a perfect paraphrase could beat a model that never had it, so a *high* score would have been uninformative in
one direction while a *low* score remains the informative one. Word dropout's mixed signal is called out as
ambiguous, partly because base models struggle to imitate heavily degraded traces at all, which confounds "the trace
was damaged" with "the student could not copy it". This is a single model family, a single benchmark (MATH), and one
behavioural readout; nothing here probes internals.

## What we take from it

- **Method (reusable null):** "distil a transformed trace, keep accuracy" is a cheap, self-contained test that a
  surface feature of a trajectory is not the variable the model uses. It is the trace-level analogue of the
  frozen-reader control: intervene on the form, require the function to survive.
- **Measure:** report the *gap between conditions on the same base model*, never an absolute pass rate — the small
  models here score far lower overall while showing the same invariance, and an absolute number would have obscured
  that.
- **Warning (the asymmetry):** an invariance result (no degradation) licenses "not dependent on this feature"; a
  degradation result licenses almost nothing, because the intervention may simply have made the data harder to
  imitate. Any "we ablated the channel and performance fell, therefore it was used" claim needs a damage-matched
  control — here, the word-dropout arm is exactly the cautionary case.
- **Warning (curriculum confound):** a model trained *through* a representation can keep its benefit after the
  representation is removed, so distillation-style tests cannot fully rule out a channel that mattered during
  learning. Same shape as the "model organism built by re-encoding existing outputs" confound — the intervention
  has to be applied before, not after, the capability is formed for a clean answer.
- **Positive anchor for intervention work:** the empty and filler-token baselines are the right floor for any claim
  that a sequence's *content* (rather than its length) does work — a cheap control we should reuse whenever we
  compare a model's behaviour with and without some scaffold.
- **Framing:** encoded reasoning is a coordination problem between two readouts — what the model writes and what it
  computes — and the field's test is behavioural invariance rather than a probe. A white-box model would want to
  predict the invariance, not merely measure it.

## Tags

unit: whole-model
form: description
method: training-interpretable
eval: downstream-task
goal: safety/auditing
