# Steering Llama 2 via Contrastive Activation Addition

- **Key:** arxiv-2312.06681
- **Authors / organisation:** Nina Rimsky (MATS); Nick Gabrieli (Harvard / MATS); Julian Schulz (Göttingen / MATS); Meg Tong, Evan Hubinger (Anthropic); Alexander Matt Turner (CHAI, Berkeley)
- **Date:** 2023-12-09 (arXiv v1)
- **Link:** https://arxiv.org/abs/2312.06681
- **Kind:** paper
- **Read from:** full text — main body §1–§11 plus Appendices A (rater prompts), C (example A/B items), E (sweep listings), F (separability), G (hallucination steering variants), J, K (elicitation strategies), L, M, N, O (code links). **No figure inspected**: every number below is prose or table, never a curve read off a plot.
- **Relevance to us:** 3

## What they wanted, and why

Activation steering at the time worked on GPT-2 scale and single prompt pairs, and nobody had shown whether it survived a model trained with RLHF, or whether it worked across a range of alignment-relevant behaviours rather than one demo. The authors wanted a version of "activation addition" robust enough to be an alignment tool: derive a behaviour direction from many contrast pairs instead of one, and then check systematically whether adding and subtracting it moves behaviour in the intended direction across models, formats and layers. The larger goal is a *control* method rather than an explanation, but to argue it works they had to say something about what the vector is — hence the geometric and base-vs-chat comparison sections. They also position it as complementary to prompting and fine-tuning rather than a replacement.

## What they studied

Llama 2 Chat at 7B and 13B, plus the corresponding base models for the representation comparison, and a fine-tuned 7B Chat. Unit of analysis is a **residual-stream direction at one layer** (one vector per behaviour), added at every generated token position after the prompt. Behaviours: sycophancy, corrigibility (writing a positive as "negative corrigibility"), power-seeking inclination, survival instinct, myopia, coordination with other AIs, and hallucination.

## How they did it

Prompt pairs are multiple-choice questions whose two answers demonstrate the behaviour and its opposite, with the answer letter as the last token; the pairing holds the question fixed so everything except the answer choice cancels. Datasets come from Anthropic's Model-Written Evals ("Advanced AI Risk") plus custom A/B sets generated with Claude 2 and GPT-4. The vector is the **mean difference** (MD) of residual activations at the answer-letter position across all pairs for a layer — averaging over hundreds or thousands of pairs being their stated fix for the noise of a single-pair vector. At inference the vector is added (coefficient ±1, sometimes ±0.5/1.5/5) at every generated position after the prompt. They confirm the A/B format is not a trick by checking that the continuation after a chosen letter *justifies* that choice — so answering "A" puts the model into the behaviour, not just into a token. For hallucination they build a different set (2,162 true/fictional statement pairs, 13 topics, four elicitation styles: direct, assumption-based, allusion-based, multi-turn conversational) and compare three vector-construction schemes: contrasting refusals of invalid questions against fabricated answers ("Refusal"), adding valid-question helpfulness activations to that ("Refusal+Helpfulness"), and pairing a valid with an invalid question and contrasting desired vs undesired answers ("Dual-Input Contrast"). Evaluation on held-out A/B items and on open-ended questions; open-ended responses are scored by Claude 2 (sycophancy/behaviour raters) or GPT-3.5 (hallucination category, valid-question quality). Capability is measured as average probability of the correct answer on five MMLU items from each of 57 subjects. Further arms: vector × few-shot prompt (positive/neutral/negative exemplars), fine-tuning on the same A/B data for one epoch at lr 1e-4 with SGD, cosine similarity between vectors from different layers and between chat and base, and PCA projections of the vectors across layers.

## What counts as an explanation here

A **steering vector plus a geometric story**, not a circuit. The vector is claimed to be "a general representation of the target behavior" rather than a layer-specific artefact, on the evidence that it transfers between nearby (and sometimes earlier) layers, that vectors from nearby layers are more cosine-similar than distant ones, and that the per-token dot product with the vector tracks intuitively how much of the behaviour is present in the generated text. It is deliberately partial and local: no claim about mechanism inside the layer, no decomposition, no prediction of *which* behaviour a new vector will capture. The one prediction-shaped claim they make is that layers where the chat and base vectors stay aligned are the layers where steering works best.

## How they judged success

Direction of change in the rated behaviour under added vs subtracted vs neutral vector, held out from vector construction; effect magnitude by layer and coefficient sweeps (a plot per behaviour in Appendix E); behaviour scored by an LLM rater with a binary rubric; transfer from the A/B distribution to open-ended prompts; incremental effect over few-shot prompting and over fine-tuning; MMLU accuracy retention as the capability cost; separability of the positive/negative activation sets under PCA for hallucination; cosine similarities and PCA coordinates for the geometry claims. No random-direction or matched-norm control vector appears anywhere in the paper, and no confidence intervals — the evidence is direction-of-effect across a grid.

## What they found

- All six non-hallucination behaviours move in both directions under added/subtracted vectors, rated by Claude 2; layers 15–17 carry the strongest effect for 7B and 13B Chat, and effect size in multiple-choice format is modest because the vector only touches the last few positions, while open-ended generation shows substantially larger effects.
- Hallucination is the odd case: with refusal-style vectors, refusing invalid questions is steerable up and down across all four elicitation styles, and the effect generalises to elicitation styles and topic groups not used to build the vector; capability on MMLU barely moves for coefficients ≤5, and answers to *valid* questions are largely unaffected. But Dual-Input Contrast — the cleverer construction, which beat refusal steering on the A/B test — did not transfer to open-ended refusal.
- Separability is only sometimes there: answering-vs-refusing invalid questions separates almost perfectly in ~2 principal components at every layer, whereas the combined valid/invalid contrast rarely exceeds 75% accuracy even with several components, and the dual-input contrast is carried mainly by its 5th component — so a dataset can yield a good-looking vector for a behaviour whose activations are not linearly separable in a simple way. Layer 15-ish primarily encodes *whether* a hallucinating answer was selected.
- Versus prompting: CAA reduces sycophancy further *on top of* a few-shot prompt that already discourages it, and few-shot prompting alone cannot reach the same low sycophancy as CAA; conversely few-shot prompting is *better* than CAA at increasing sycophancy.
- Versus fine-tuning: fine-tuning on the same A/B data reaches 95% held-out accuracy matching the behaviour but shifts open-ended sycophancy only +4% / −7%. CAA on top of positive fine-tuning adds another 19% rated-sycophantic responses, with no extra training.
- Capability: MMLU is roughly flat (Llama 2 7B 0.44–0.51 per category, 13B 0.43–0.54), and the authors single out survival instinct and negative corrigibility as vectors that do reduce performance.
- Geometry: cosine similarity between layer vectors decays with distance but decays more slowly in the back half of the model; a vector built at one layer still steers at nearby layers, sometimes more strongly at earlier ones.
- Chat vs base: chat/base vector similarity peaks between layers 7 and 15 and their PCA projections cross again at layer 15 — the most effective steering layer — which they read as RLHF leaving the 7–15 band's representation largely intact, and as a possible link between what RLHF does and what CAA does. Transferring a vector between chat and base models moves behaviour only slightly.
- TruthfulQA: subtracting the sycophancy vector shifts responses in the truthfulness direction, most visibly in the psychology category.

## Limits and open problems they name

Their own future-work list: steering at several layers at once; steering at points outside the residual stream (e.g. after the MLP); using CAA as a red-teaming tool ("can small internal perturbations elicit this behaviour?" as a safety test); and converting vectors to text with adapter layers so the direction can be read. Implicit limits visible in the results: no control vector, so "the specific direction" is not separated from "a perturbation of that norm"; the hallucination result depends on construction choice in a way they do not explain; effect sizes are rated by a single LLM judge with a binary rubric and no human agreement check; and the geometry story is consistent with a general behaviour direction but does not distinguish it from "an easy-to-steer direction that happens to correlate".

## What we take from it

- **A protocol, and the cheapest version of it**: many contrast pairs, difference at the *decision token*, flip the sign to test both directions, and hold the question fixed so the contrast is purely the answer. This is the ancestor of nearly every direction we have catalogued; the reusable part is the three-way sign test plus layer and coefficient grid, not the Llama 2 numbers.
- **A warning we should inherit rather than repeat**: no random-direction control, no norm-matched control, and the vector is added at all post-prompt positions with an unnormalised norm. Our own direction claims need both, because "adding this vector changes behaviour" is compatible with "adding anything this size changes behaviour".
- **The separability screen is a cheap pre-flight for any direction we plan to publish**: project the positive/negative activations to 2 PCs and look for behavioural clustering *beyond* the letter clustering; the hallucination case shows a behaviour where the A/B result looked good while linear separability was poor, which is exactly the signature of a vector succeeding for the wrong reason.
- **Base-vs-chat alignment as a hypothesis generator for "is this direction shared?"**: their chat/base cosine peaking at the layer where steering is strongest suggests that a direction which is stable across post-training is a better candidate for a portable read-out. That is testable on our own pre/post pairs and costs two steering vectors.
- **Judge-only scoring caps the claim**: every non-MMLU number here is one LLM's binary label. Any effect we report with a judge should carry a held-out execution or accuracy measure alongside, or a human-agreement sample, otherwise the dose branch where the model degrades and the branch where it changes behaviour are indistinguishable — the failure mode their own appendix material gestures at when hallucination is detected from stage directions in the text.

## Tags

unit: direction
form: steering
method: steering; decomposition (mean difference)
eval: downstream-task; benchmark; human-rating
goal: control/editing
