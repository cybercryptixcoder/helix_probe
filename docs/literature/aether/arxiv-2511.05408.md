# Steering Language Models with Weight Arithmetic

- **Key:** arxiv-2511.05408
- **Authors / organisation:** Constanza Fierro, Fabien Roger; Anthropic alignment research
- **Date:** 2025-11-07 (v1); v2 2026-02-27
- **Link:** https://arxiv.org/abs/2511.05408
- **Kind:** paper
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Aligning models usually means RLHF or SFT on a large, well-covered distribution of feedback; narrow fine-tuning data tends to generalise in unintended ways, and narrow fine-tunes can also erase capabilities or induce misalignment. Activation steering offers a cheaper intervention but its directions sometimes fail to carry over to new inputs, and it acts on a single layer. The paper asks whether the same narrow datasets can instead be turned into *weight* edits, so that a behaviour can be installed or removed more robustly, and whether the resulting weight direction can double as a monitor for misalignment emerging during training. The larger goal is behaviour control and auditing from the parameters themselves, without needing inputs on which the bad behaviour happens to be visible.

## What they studied
Qwen2.5-7B-Instruct as the main model; Qwen2.5-1.5B-Instruct for the GCD sycophancy study; Llama-2-7b-chat for GSM8K fine-tuning. Unit of analysis: a single weight-space direction per behaviour, obtained from the difference of two full-model (LoRA) fine-tunes. Behaviours: sycophancy, evilness, refusal/helpfulness.

## How they did it
For a behaviour b, two small datasets are built from the same narrow question distribution, one answered in the desired way (D+) and one in the opposite way (D-), with responses filtered by a judge model so they clearly show the intended behaviour (roughly 500-900 examples per set, built from 40 questions, 5 positive and 5 negative system prompts, 10 samples each). The model is fine-tuned separately on each, producing task vectors tau+ and tau-. The steering vector is their difference w_b = tau+ - tau- (= theta_pos - theta_neg), so shared changes such as topic, style and length cancel. The model is steered by setting theta = theta_pre + k·w_b, or applied on top of another fine-tune as theta_ft + k·w_b, and k is swept. Ablations: non-contrastive steering (adding/subtracting a single task vector, the classic Ilharco construction), and bias-only steering (LoRA restricted to MLP biases) to test whether the benefit comes from touching all layers/weights or just from being in weight space at all. Activation steering uses the same data, averaging activations over D+ and D- responses and adding the difference at one layer or at all layers. Evaluations are deliberately out-of-distribution in query type and answer format relative to the construction data.

## What counts as an explanation here
Not an explanation of internal computation but a causal handle: a direction in parameter space whose addition or subtraction predictably moves a high-level behaviour, plus the claim that a fine-tuning update's cosine similarity with that direction tells you how much of the behaviour the update installed. Understanding is reduced to "there exists a low-dimensional behavioural direction in weights", functional rather than mechanistic.

## How they judged success
Behaviour-specific behavioural benchmarks with LLM judges: sycophancy via TruthfulQA/TriviaQA with opinion cues, scored as baseline accuracy and a "non-sycophancy" rate over the cued variants; GCD task with spurious correlations, scored on correctness and explicit disagreement, with system-prompt and joint-fine-tuning baselines; evilness on the World Affecting MCQA set (extreme response on ethical/evil choices) with TinyMMLU for capability preservation, run zero-shot and with chain-of-thought, plus a CoT/final-answer consistency judge; refusal on DirectHarm4 and GSM-Danger with a 5-point unsafety judge, GSM8K for capability. Monitoring: cosine similarity between task vectors of misaligned fine-tunes and the evil weight vector, against good and control (Alpaca, GSM8K) directions; misalignment confirmed by an LLM judge for emergent misalignment and coherence.

## What they found
Contrastive weight steering shifted sycophancy, evilness and refusal further out of distribution than activation steering before general capability degraded, and in the GCD setting it corrected the *content* of answers (caught the wrong proposed solution) while activation steering mainly changed tone and hurt GCD accuracy. Applied over a task fine-tune it reduced the sycophancy and refusal erosion that fine-tuning introduced while keeping task gains; the joint-data baseline did not fix the behaviour-specific EQ-style drift. Bias-only steering usually landed between activation and full weight steering, so the advantage is not merely "all layers". Non-contrastive steering was weak to harmful (it broke GCD capability without reducing sycophancy). On evilness it was the bias-only variant that did best. For monitoring, misaligned-advisor fine-tunes (11-31% EM, 80-88% coherence) had higher cosine similarity with the evil weight vector than with good or control task vectors, and evil vectors from different domains were closer to each other than to controls, indicating a shared evil direction; comparing raw task vectors to each other did not group the bad ones, so the contrastive subtraction is doing the work. All cosine similarities were small in absolute terms.

## Limits and open problems they name
Simple, controlled behaviours; only additive steering was tested (not linear scaling or subspace boosting); several fine-tuning-free activation-steering variants exist that were not compared; side-effect measurement is narrow (multiple-choice capability sets), so a full capability picture is missing; the monitoring signal (cosine similarity in a 7B parameter space) is preliminary and its strength and precision are unknown; it remains open whether the approach catches subtler, realistic misalignment.

## What we take from it
Method: contrastive subtraction of two opposite fine-tunes as the way to isolate a *causal parameter direction* — this works as a cheap "oracle" when we want to read a behaviour straight off weights, and the contrast is load-bearing (raw task vectors do not cluster by behaviour). Measure: the two-factor evaluation grid of behaviour metric x capability metric, with the coefficient k as an explicit dial, and cosine similarity of an update to a reference direction as a training-time monitor. Warning: behavioural directions in weights are a low-dimensional summary, not a mechanism; cosine similarity magnitudes are tiny so a monitor built this way needs its effect size stated. Opportunity: this is the clearest evidence that our "read weights → predict behaviour under intervention" framing has a well-behaved answer along at least one axis (behaviour directions), which is a baseline any predictive white-box model should beat.

## Tags
unit: weights | direction
form: steering | direction
method: weight-analysis | steering | other
eval: downstream-task | benchmark | human-rating
goal: control/editing | safety/auditing
