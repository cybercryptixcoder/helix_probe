# Latent Planning Emerges with Scale

- **Key:** arxiv-2604.12493
- **Authors / organisation:** Michael Hanna (ILLC, University of Amsterdam; work done in Anthropic Fellows Program), Emmanuel Ameisen (Anthropic)
- **Date:** 2026-04-14
- **Link:** https://arxiv.org/abs/2604.12493
- **Kind:** paper
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Models write stories and code that look planned without verbalising a plan; earlier interpretability work inferred "latent planning" from the fact that future outputs could be probed from internal states. The authors argue that is insufficient — decodability is not use, and a model with a trivial next-token rule would also look predictive. They propose a causal definition of planning and test, with transcoder feature circuits, how much of it models actually do and how it changes with scale. The aim is a framework that turns "it looks planned" into mechanistic claims that can be verified by intervention.

## What they studied
Qwen-3 0.6B, 1.7B, 4B, 8B, 14B (32B for behaviour only), with transcoders on each MLP. Tasks: article choice (a/an before a planned noun), number agreement (is/are before a planned numeral), Spanish el/la, Chinese measure words, and rhyming couplets. Unit of analysis: transcoder features and the feature circuit (directed graph of feature-to-feature and feature-to-logit direct effects) for one input.

## How they did it
Latent planning is defined by two conditions: (1) forward planning — a representation of a token t causes the model to output t at position n+k, k>1; (2) backward planning — that representation causes the model to produce a preceding context that licenses t. For each example they build a transcoder feature circuit, manually group and label features, and then *programmatically* select "planning features": active at the final input position, and either upweighting the planned word or containing it in five of ten top-activating texts. Causal tests: (a) compute the share of total input-to-logit flow mediated by planning features on correct versus incorrect examples; (b) ablate planning features on successful examples and multiply them by 5 on failing examples, versus random-feature controls; (c) "direct-effect interventions" that upweight the planning features while freezing other features, to rule out plain cosine similarity between the planner direction and the output unembedding. For couplets, rhyme features are found by a heuristic over top-activating subword tokens, then downweighted in the original line and replaced with another couplet's rhyme features; backward planning is tested by re-feeding the steered and original contexts with the final word removed.

## What counts as an explanation here
A feature circuit: named nodes (features, grouped into semantically labelled sets) connected by weighted direct-effect edges, explaining one prediction. Planning is claimed only when an identified feature both drives a distant token and drives the licence for it, so the explanation is expected to be predictively and causally checkable, not merely descriptive.

## How they judged success
Per-class recall (a vs an, minority class emphasised); proportion of total flow through planning nodes; probability of the correct article under ablation/boosting versus random-feature baselines; whether steering planning features changes the planned word (forward planning) and whether the steered context better licenses the steered word (backward planning, tested with the last word removed); rhyme accuracy via CMUDict vowel/final-consonant matching; a three-way manual/AI-graded adaptation metric on TinyStories steerings (contains X; coherent per Claude Sonnet 4 grading plus manual check; context adapted to license X).

## What they found
Small models (0.6-1.7B) always predict the majority article; recall of "an" rises smoothly and exceeds 0.8 by 14B. Notably, <14B models can compute the number in is/are tasks yet still output the wrong verb ("there are 1 dog"), so the failure is planning, not arithmetic. Even poor models contain planning features, but flow through them only exceeds the alternative when the model is right on minority-class items; ablating them hurts and boosting them helps only on those items, and the effect is nearly zero on the majority class. Boosting works on 4B and 8B, showing the mechanism exists before it is reliable. Direct-effect-only interventions are much weaker (zero ablation less harmful, multiplying sometimes hurts), so planning features work largely through activating downstream "say a/an" features rather than by direct similarity to the article's unembedding. On couplets, larger models rhyme at modest rates (14B ≈0.6 exact, ≈0.8 assonant), and their circuits show end-of-line features pulling rhyme features from the first line into the second — forward planning verified by steering (≈40% adoption of a swapped rhyme). Backward planning is largely absent: the steered context does not license the new rhyme better than the original, and re-feeding a steered context without steering reverts to the original rhyme (≈60% versus ≈100% for the original context, an inflated figure since only successful rhymes were kept). A few circuits show local "say X" planning features that produce coherent phrases adapted to a steered word (in the night), increasing with scale.

## Limits and open problems they name
Only simple tasks, because Qwen-3 ≤14B fails at complex planning; one model family, since transcoders for comparable models are missing; the rhyme-feature heuristic has moderate recall; the adaptation metric for local planning is sensitive to steering strength and rests on a small minority of couplets; the paper notes open questions about attributing from high-level actions (refusals) rather than single answer tokens, and that planning is piecemeal rather than one unified circuit.

## What we take from it
Measure — the definition is the main contribution for us: a claimed internal state only counts as "planning" if it causes a distant output *and* the licence for that output; it gives a ready-made two-condition test for any future-directed prediction our white-box model makes. Method: ablation-versus-boost asymmetry plus random-feature controls is a clean way to show a feature matters where the model fights its prior; the direct-effect-only intervention is the right control for "is this just an unembedding similarity artefact" and should be standard. Framing: planning appears as a *piecemeal* capability keyed to task frequency and loss importance — so a predictive model should condition on which task regime it is in, not assume uniform planning. Warning: the couplet result is a concrete negative — internal rhyme features exist and cause the rhyme, yet context adaptation does not follow; having the representation is not enough.

## Tags
unit: feature | circuit | layer
form: graph | description
method: transcoder | attribution | ablation | steering
eval: ablation | patching | downstream-task | prediction/simulation
goal: understanding | evaluation-of-methods | debugging
