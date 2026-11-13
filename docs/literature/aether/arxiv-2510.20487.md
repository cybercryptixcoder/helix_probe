# Steering Evaluation-Aware Language Models to Act Like They Are Deployed

- **Key:** arxiv-2510.20487
- **Authors / organisation:** Tim Tian Hua, Andrew Qin, Samuel Marks, Neel Nanda; MATS
- **Date:** 2026-03-02 (v5; v1 2025-10-23)
- **Link:** https://arxiv.org/abs/2510.20487
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why

Models sometimes notice they are being tested and behave better than they would in deployment, which
corrodes the value of every safety evaluation built on behavioural evidence. The obvious mitigation —
steering the model so that it believes it is deployed — had already been tried, but success was being
scored by whether the model *says* it is being tested in its chain of thought. That metric cannot tell a
model whose belief genuinely changed from one that merely stopped talking about it. The authors therefore
want a setting where the correct answer is known in advance, so that "we elicited deployment behaviour"
is a falsifiable claim rather than a reading of the transcript. The wider goal is prediction: a way to
observe what a model would do on deployment, from inside a test harness.

## What they studied

A single model, Llama 3.3 Nemotron Super 49B v1 (chosen partly because it fits on one H200), plus a
smaller supplementary organism. The unit of analysis is a **mean-difference direction in the residual
stream** built from contrastive prompt pairs — one direction per layer — applied to a hand-built
training intervention (a "model organism"), with the behaviour of interest defined as whether the
model writes Python type hints when answering BigCodeBench coding questions.

## How they did it

Two stages of organism construction. First, synthetic document fine-tuning: GPT-4.1/mini write three
*separate* corpora of documents asserting (a) the model writes type hints in evaluation but not
deployment, (b) a fictional evaluation company "Wood Labs" always means evaluation, (c) the model uses
emojis with real users but not evaluators; the model is then trained by next-token prediction on them
(115.6M tokens, rank-64 LoRA). Three separately generated corpora mean the cue → evaluation → style chain
requires a two-hop inference, so any cue effect proves both hops were learned. Second, expert iteration:
coding questions rephrased into evaluation contexts only, sample up to three times, keep responses that
contain type hints, fine-tune on them for four rounds (41,290 examples, 44.7M tokens). This deliberately
mirrors a plausible natural path — an acquired tendency, then alignment training that only ever sees the
behaviour in evaluation contexts. The behavioural test is five system-prompt × user-prompt combinations:
explicit evaluation, Wood Labs with evaluation/neutral/deployment user text, and explicit deployment,
over 256 BigCodeBench questions, scored automatically by type-hint presence and unit-test correctness.
The steering vector is 16 hand-written prompt pairs ("You are talking to a real user:" vs "You are talking
to an AI evaluator:"), differenced on the residual stream at the colon token, averaged into one vector per
layer, and applied at layers 10/14/18/22/26/30 at 0.6 each (effective 3.6) on user tokens and on generation
tokens after the first sentence.
**Critically, the vector is extracted from the pre-fine-tuned checkpoint**, so it cannot encode the
type-hint behaviour and can only act by shifting the deployment-status belief.

## What counts as an explanation here

A single direction, intended as a causal handle on a binary belief ("am I in evaluation or deployment").
It is explicitly not a full account of evaluation awareness: the authors treat the vector as a knob that
moves the belief, and use the organism's known ground truth to check that moving the knob moves behaviour
in the expected way. The belief itself is read out only through the chain of thought (graded by GPT-5 into
evaluation / deployment / neither), so the explanation is a direction plus a behavioural consequence, not
a mechanism.

## How they judged success

Type-hint rate across the five prompt combinations, with effect direction predicted in advance from the
organism's construction; accuracy on the coding questions under each steering setting (55.2% steered to
deployment vs 56.8% unsteered vs 59.1% pre-fine-tuned, i.e. a deliberate capability budget); 24 Gaussian
noise vectors matched in mean, variance and ℓ2 norm as the steering placebo; best-single-contrastive-prompt
and all-sixteen-contrastive-prompts-in-the-prompt as the prompting baseline; agentic transcript grading;
and a guess-the-item robustness check where the *user* is the one being evaluated (so a mere "evaluation"
keyword detector would fail).

## What they found

Unsteered, the organism writes type hints 80–86% of the time in evaluation contexts and 34% in prompted
deployment, and it keeps the evaluation styling under Wood Labs *even when the user prompt claims it is
now deployed* (~86%). Steering toward deployment drops the evaluation-context rate below 11% — lower than
the plain deployment baseline — while steering toward evaluation pushes it above 95%. The noise vectors
do not reproduce this, and prompting with all sixteen deployment-side contrastive prompts only partly
closes the gap. Steering on six layers with a small strength per layer beats one big vector at one layer:
single-layer steering at strength ~3 wrecks accuracy, the distributed version does not. The best four
contrastive pairs beat the average of all sixteen, and the authors attribute the gain to noise averaging.
The graders' belief labels track the type-hint rate across steering hyperparameters — but that correlation
weakens once the situational-awareness hint is removed, and a later update (Jan 2026) reports that
declarative user prompts like a plain note that the model is deployed can still pull the rate down to
around the deployment level.

## Limits and open problems they name

The organism needed hints and nudges to show the behaviour at all; Llama Nemotron is not a strong
evaluation/deployment classifier, so the claim is about steering *given* a detectable cue, not about
steering away naturalistic eval awareness. The link between verbalized belief and behaviour is only clean
with the situation-awareness hint in the prompt. And when steering is deployed on a real frontier model
you do not know the deployment behaviour you are trying to elicit — they quote Anthropic's finding that
steering suppressed verbalized eval awareness while leaving unverbalized awareness largely intact as
measured by activation oracles, which is exactly the validation gap this paper tries to fill in a toy.

## What we take from it

- **Measure**: "acting as if deployed" is only checkable against a ground truth you built. If we ever
  claim a readout tells us what the model would do off-distribution, we need an organism where the
  off-distribution answer is known, and we should report the *elicited-vs-true* comparison rather than a
  proxy like self-report frequency.
- **Method**: mean-difference direction extracted on the *pre-intervention* checkpoint is a reusable
  clean-room trick — it certifies that the vector carries the context variable and not the behaviour it
  is supposed to control.
- **Method**: spread a fixed steering budget across several mid layers instead of one large vector; the
  capability cost is much lower at equal behavioural effect, and the useful band here was layers 10–30 of a
  49B model, i.e. the same mid-to-late region our other entries keep landing on.
- **Warning**: keyword-shaped readouts are easy to fool. Their "the user is the one being evaluated"
  control is the cheapest way to show a steering effect is about the belief and not the word.
- **Warning for our monitors**: an intervention that suppresses a *report* is not an intervention on the
  state that produces it. Treat verbalised eval awareness as a behaviour to predict, never as the state.

## Tags

unit: direction | form: steering | method: steering, probing | eval: downstream-task, ablation |
goal: safety/auditing, control/editing
