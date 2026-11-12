# Circuit Tracing: Revealing Computational Graphs in Language Models

- **Key:** tcpub-2025-attribution-graphs-methods
- **Authors / organisation:** Emmanuel Ameisen, Jack Lindsey, Adam Pearce, Wes Gurnee, Nicholas L. Turner, Brian Chen, Craig Citro (core) and others; Joshua Batson (correspondence); Anthropic
- **Date:** 2025-03-27
- **Link:** https://transformer-circuits.pub/2025/attribution-graphs/methods.html
- **Kind:** paper (Transformer Circuits Thread)
- **Read from:** full text (main body and limitations; appendices only partly)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Neurons are polysemantic and whole MLP blocks or heads are too coarse, so neither is a good unit for explaining a
specific output. The authors want a general, largely automatic way to trace, for one prompt, the step-by-step
computation from input tokens through interpretable intermediate features to the output logit. The larger goal is
a "microscope" for model internals that supports mechanistic claims, checked by interventions, about real
production models; the companion biology paper is the first large application.

## What they studied
An 18-layer Anthropic model ("18L") and Claude 3.5 Haiku. Unit: cross-layer transcoder (CLT) features (300K-10M
for 18L, 300K-30M for Haiku), assembled into per-prompt attribution graphs; also prompt-independent "global" virtual
weights between features. Case prompts: an acronym ("National Digital Analytics Group" -> DAG), factual recall
(Michael Jordan -> basketball), two-digit addition.

## How they did it
1. Train a CLT: each feature reads the residual stream at one layer (JumpReLU encoder) and writes to the MLP outputs
of that layer and all later ones; loss is summed MSE over layers plus a tanh sparsity penalty. 2. Swap CLT outputs
for MLP outputs to get a replacement model. 3. For a given prompt, build a local replacement model: freeze the
original attention patterns and normalisation denominators, and add an error node at every (position, layer) equal
to the residual between true MLP output and CLT output, so the local model reproduces the original's activations
and logits exactly. 4. Because this local model is linear in feature activations, compute direct edges between
nodes (embeddings, features, errors, top logits covering 95% of probability) as activation times a Jacobian-derived
virtual weight with stop-gradients. 5. Prune to nodes/edges with highest influence on the logits (about 10x fewer
nodes, about 500x fewer edges). 6. Label features by hand from top activations and logit effects; group related ones
into supernodes in an interactive UI. 7. Validate by intervening in the original model: negative steering (scale by
-1) or constrained patching of supernodes over a layer range, checking downstream feature changes and output
changes (e.g., suppressing a "_6" feature turns 36+59=95 into 98). They also derive global weights between features
and filter interference using coactivation statistics (target-weighted expected residual attribution, TWERA),
applied to 10,000 addition prompts.

## What counts as an explanation here
An attribution graph: a pruned, labelled DAG of features with linear edge weights, for one prompt, under frozen
attention, with error nodes marking what is unexplained. Explicitly partial (OV-only, ignores why attention attends
where it does). It is predictive in a limited sense: the graph predicts which interventions should change which
downstream features and outputs.

## How they judged success
Normalized reconstruction MSE and L0 of the CLT; fraction of prompts where the replacement model's top token matches
the original; replacement score (share of end-to-end graph paths that pass through features rather than error
nodes); completeness score (logit-influence-weighted share of input edges coming from features or embeddings);
average path length; automated feature interpretability (Sort Eval, Contrastive Eval); Spearman correlation between
graph-predicted influence and actual ablation effect; perturbation faithfulness (cosine similarity and normalized MSE
of downstream activations between replacement and real model after an intervention). Baselines: per-layer
transcoders (PLTs) and thresholded neurons.

## What they found
Largest 18L CLT (10M features, mean L0 88): about 11.5% normalized reconstruction error; Haiku CLT (30M, L0 235):
about 21.7%. The 18L replacement model matches the original's next token on about half of tested prompts. At 10M
features on 18L: CLT completeness 0.80 / replacement 0.61 vs PLT 0.78 / 0.37; average path length 2.3 vs 3.7 on a
capital-analogy prompt. A 1M CLT beats 10M PLTs on MSE and KL with 5-10x less compute. CLTs beat PLTs, which beat
thresholded neurons, on automated interpretability. Graph influence vs ablation effect: Spearman 0.72 (20 prompts).
After a perturbation, replacement-model activations agree with the real model at roughly 0.6-0.8 cosine one layer
later, degrading over more layers. Pruning at the default threshold cut the acronym graph from 236 to 55 nodes while
completeness fell from 0.87 to 0.70. Global analysis of addition revealed operand, lookup-table, sum and magnitude
features.

## Limits and open problems they name
Attention/QK circuits missing (e.g., cannot say why the model attends to the right name in induction); large
reconstruction error ("dark matter"), sometimes nearly all nodes are errors on obfuscated prompts; only active
features shown, so inhibition is hard to see; graphs remain large (hundreds of features, thousands of edges);
feature splitting and absorption put features at the wrong abstraction, requiring manual supernodes; global weights
suffer interference; mechanistic unfaithfulness: the CLT can match activations with a different mechanism, and
prediction degrades many layers downstream. Labelling from dataset examples alone caused errors.

## What we take from it
This is the closest existing thing to the object we want, and its scorecard is the one to beat. Reuse: (1) the local
replacement model with explicit error nodes as an honest accounting of what is unexplained; (2) replacement and
completeness scores and graph-influence vs ablation-effect correlation as measures; (3) perturbation faithfulness
measured layer by layer, which is exactly "prediction under intervention"; (4) global virtual weights plus
interference filtering (TWERA) as a weight-reading step that is prompt-independent. Warning: their predictive power
decays with depth, attention is frozen rather than explained, and only about half of next-token predictions survive
full replacement; a weight-derived model should report the same metrics and specifically attack these gaps.

## Tags
unit: feature, circuit
form: graph, replacement-model, dictionary
method: transcoder, attribution, steering, ablation, weight-analysis
eval: faithfulness, completeness, ablation, prediction/simulation, human-rating
goal: understanding, science
