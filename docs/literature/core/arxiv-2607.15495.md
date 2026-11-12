# Verbalizable Representations Form a Global Workspace in Language Models

- **Key:** arxiv-2607.15495
- **Authors / organisation:** Wes Gurnee, Nicholas Sofroniew (core), Adam Pearce, Mateusz Piotrowski, Isaac Kauvar, Runjin Chen, Anna Soligo, Paul Bogdan, Euan Ong, Rowan Wang, T. Ben Thompson, David Abrahams, Subhash Kantamneni, Emmanuel Ameisen, Joshua Batson, Jack Lindsey (correspondence); Anthropic
- **Date:** 2026-07-06
- **Link:** https://transformer-circuits.pub/2026/workspace/index.html (also arXiv 2607.15495)
- **Kind:** paper
- **Read from:** abstract and sections (first ~60% of the web version: methods, main experiments, controls, reflection-training application, discussion; later appendices not read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Cognitive science distinguishes the small part of processing that is available for report and deliberate use
("access consciousness", global workspace theory) from automatic processing. The authors ask whether LLMs have an
analogous privileged subset of representations that can be reported, deliberately modulated, used in internal
reasoning, flexibly reused, and are selective to tasks that need them. Finding such a subset would link
interpretability to introspection and self-report, and give a compact space to monitor. They take no position on
phenomenal consciousness.

## What they studied
Claude Sonnet 4.5 (default), corroborated on Haiku 4.5 and Opus 4.5, some analyses on Opus 4.6. Layers rescaled to
0-100. Unit: directions in the residual stream tied to vocabulary tokens (J-lens vectors) and their sparse
nonnegative span (J-space); also attention heads that broadcast this content.

## How they did it
The Jacobian lens: for each layer, average the Jacobian from that layer's residual stream to the final layer over
positions of 1,000 pretraining-like prompts; read an activation by applying this mean Jacobian then the unembedding
(the logit lens is the special case of an identity Jacobian). Each token gets a J-lens vector; activations are
decomposed into sparse nonnegative combinations (gradient pursuit, k up to ~25). Tests per workspace property:
swapping J-lens coordinates for one concept with another and checking whether the verbal report changes (14
categories); concept injection and "think about / ignore X" instructions; swapping intermediate concepts in 50 two-hop
prompts; swaps on function templates (16 templates, 192 trials); selectivity tasks (language ID, line counting) where
some readouts should change and others should not; ablating top J-lens directions across a band of layers and
measuring benchmark damage (MMLU, SQuAD, sentiment, multi-hop, Caesar cipher, translation, TriviaQA, GSM8K). Controls:
random directions, a randomly rotated J-lens set, isotropic-gain baselines, SAE features stratified by J-lens
kurtosis, layer-matched random head sets, logit lens. Application: counterfactual reflection training on Haiku 4.5,
with honesty benchmarks and lens ablations.

## What counts as an explanation here
A readout of which token-nameable concepts are "in the workspace" at a layer and position, plus causal evidence that
those coordinates drive report and reasoning. A bag of concepts, not a circuit; partial; predictive in that swapping
coordinates predicts changes in report and reasoning outputs.

## How they judged success
Swap success rates (target reaches top-1 or top-5); variance share of the J-space component; occupancy versus
random-direction controls; benchmark accuracy drops under ablation vs random-head and random-direction controls; CKA
layer structure; honesty benchmark scores (fabrication, deception) before and after training and under ablation.

## What they found
Pure J-lens swaps hit top-5 in 88% of trials. The J-space part of a concept vector holds only a median 6-7% of its
variance, yet swapping it succeeds 59% of the time vs 5% for the remainder. Two-hop intermediate swaps succeed in 54%
(Haiku 4.5), 70% (Sonnet 4.5) and 70% (Opus 4.5) of trials. Function-template swaps reach top-1 in 76/192 trials (101
at doubled strength). Ablating the top-10 J-lens directions spares shallow tasks but substantially hurts multi-hop
reasoning, cipher decoding, translation and TriviaQA. A workspace-like band runs from roughly layer 38 to 92 of 100;
J-space explains at most about 10% of activation variance and has about 25 occupied slots. Reflection training cut
fabrication from 0.25 to 0.07 and deception from 0.38 to 0.05; ablating ethics/reflection lens vectors largely undid
the fabrication gain (0.07 to 0.22).

## Limits and open problems they name
Lens covers only single-token concepts; shows presence but not binding or roles; some readouts uninterpretable;
workspace boundaries set post hoc; early-layer absence may be a lens artefact; selectivity criterion not shown to
generalise; emergence during training unknown; J-space monitoring not claimed sufficient; consciousness analogies
are suggestive only.

## What we take from it
(1) The mean-Jacobian lens is a cheap, largely weight-and-gradient-derived map from internal states to vocabulary
that beats the logit lens; it is a candidate component for reading what a mid-layer state "means" in a white-box
model. (2) A useful structural prior: a small, capacity-limited subspace (~10% of variance) carries most of the
reportable, flexibly reused content, so a predictive model might prioritise it. (3) Strong control design (rotated
basis, random directions, layer-matched random heads) worth copying. (4) Swap success rate is a clean
prediction-under-intervention metric.

## Tags
unit: direction, head, layer
form: direction, probe
method: other (Jacobian lens), steering, ablation
eval: prediction/simulation, ablation, downstream-task
goal: science, safety/auditing, understanding
