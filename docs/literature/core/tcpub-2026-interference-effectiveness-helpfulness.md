# Characterizing interference weights in a tiny language model

- **Key:** tcpub-2026-interference-effectiveness-helpfulness
- **Authors / organisation:** Nicholas L. Turner, Jeffrey Wu, Joshua Batson; Anthropic
- **Date:** 2026-08-21
- **Link:** https://transformer-circuits.pub/2026/interference_effectiveness_helpfulness/index.html
- **Kind:** blog/research post
- **Read from:** full text (via a page-summarising fetch; plots not inspected directly)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The hope is to read a network's global weights like a program. Even in a good feature basis, the virtual weights
between features contain interference weights: connections forced by superposition that are irrelevant or harmful.
If these could be removed, what remains might be a sparse, readable model. Earlier work showed interference in toy
models and suspected it in Claude 3.5 Haiku; this study measures it in an actual trained transformer, with its
effect on outputs and loss, to see whether pruning interference reveals a sparse circuit.

## What they studied
A one-layer decoder-only transformer: residual width 256, 4 heads of dimension 64, a 1024-wide ReLU MLP, 4,096-token
vocabulary, 1,024-token context, about 2.9M parameters (about 0.79M excluding embeddings), no normalisation or
biases; trained for one pass on about 9.8 x 10^7 tokens of English and code from Common Corpus (test loss 3.38). The
MLP is replaced by a 4,096-feature JumpReLU transcoder. The model is expanded into a "virtual weight model" of six
weight families (Tokens to Logits, Features to Logits, Tokens via OV to Logits, Tokens to Features, Tokens via OV to
Features, and QK), about 331M weights, roughly 100x the original parameters. Unit: individual virtual weights.

## How they did it
They defined two per-weight scores. Effectiveness: how much a weight changes the output distribution, estimated as
a second-order (Fisher) approximation to KL divergence, computed over about 537M tokens. Helpfulness: the mean change
in loss when the weight is ablated (positive = helps), estimated on a random sample of 7,765 weights with 1B-token
estimates and confidence intervals. They pruned weights by effectiveness versus raw magnitude at many densities and
measured loss increase; plotted helpfulness against effectiveness per family; computed how much density is needed to
retain a given share of positive helpfulness; ran case studies (a Chinese-text feature, a word-ending feature, a code
newline feature); and used a region-of-practical-equivalence analysis against per-family loss budgets.

## What counts as an explanation here
A sparse set of virtual weights in a feature basis that is enough to reproduce the model's behaviour, i.e. a
weight-level program. The paper tests whether such a sparse readable set exists; it concludes not yet in this basis.

## How they judged success
Loss increase (nats) under pruning at each density; Fisher-KL effectiveness; ablation helpfulness with confidence
intervals; share of helpfulness mass retained versus density; comparison against raw-magnitude pruning as baseline;
qualitative plausibility of top weights (e.g. sensible token continuations); effect-size analysis.

## What they found
Raw magnitude misleads: the largest Tokens-to-Logits weight from one token points to a continuation that never
occurs in training, is harmful, and is about three orders of magnitude less effective than top weights. Pruning the
least effective 70% of weights costs about 0.01 nats; 85% costs about 0.07 to 0.1; Fisher pruning beats magnitude
pruning at almost every density; at 1% density performance degrades a lot. The most effective weights are mostly
helpful, but helpful and harmful weights overlap in the middle. About 47.6% of sampled weights help and 12.7% are
dead. Keeping 90% of helpfulness needs about 2.43% density and 99% needs about 13.6%, which would still be roughly
double the original parameter count. In the newline case, two position paths nearly cancel (slope -0.993, r^2 0.912).

## Limits and open problems they name
Tiny model; effectiveness and helpfulness are expensive and need scalable proxies (they name ERA and TWERA).
Transcoder and heads are likely polysemantic, so the basis is imperfect. Joint removals are nonlinear and missed by
single-weight scores. Helpfulness is noisy and there is no clean split in effectiveness. Pruning by effectiveness does
not yield a sparse interpretable model; the authors suspect the basis, not the metric, is at fault.

## What we take from it
Most directly relevant entry for reading weights. Reusable: the virtual-weight-model expansion, Fisher-KL
effectiveness and ablation helpfulness as per-weight scores, loss-versus-density pruning curves with magnitude as
baseline, and helpfulness-mass-versus-density as a sparsity measure. Key warning: even in a 1-layer model the
"readable" weight set is not small in a transcoder basis, so a predictive white-box model from weights probably
needs a better basis (e.g. transforms, see tcpub-2025-bulk-update-molt) and must handle cancelling paths.

## Tags
unit: weights
form: graph
method: weight-analysis
eval: ablation
goal: understanding
