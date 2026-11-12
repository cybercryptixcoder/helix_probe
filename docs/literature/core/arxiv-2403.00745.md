# AtP*: An Efficient and Scalable Method for Localizing LLM Behaviour to Components

- **Key:** arxiv-2403.00745
- **Authors / organisation:** János Kramár, Tom Lieberum, Rohin Shah, Neel Nanda; Google DeepMind
- **Date:** 2024-03
- **Link:** https://arxiv.org/abs/2403.00745
- **Kind:** paper
- **Read from:** full text (HTML, main text and early appendices; text after Appendix B.3 not read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Activation patching gives trustworthy causal effects per component but costs a forward pass per node, which is
impossible at the scale of modern LLMs (they note ~2.7 billion neuron nodes for Chinchilla 70B at context 1024).
Attribution patching (AtP), a first-order gradient approximation, gets estimates for all nodes from two forward
passes and one backward pass. The authors want to know how often AtP misses important nodes, fix those failures,
and give a cheap way to bound what was missed, so localisation can scale.

## What they studied
Pythia models from 410M to 12B parameters (main plots on Pythia-12B). Nodes: individual MLP neurons
(post-activation) and per-head attention query, key, value and output at each token position. Settings: single
prompt pairs (CITY-PP factual recall, IOI-PP, RAND-PP random Pile text) and distributions (reduced IOI with 120
pairs; A-AN indefinite-article prediction with 100 pairs).

## How they did it
Ground truth is the per-node activation-patching effect on loss (negative log-prob of the clean target). They
identify two failure modes of AtP that cause false negatives: attention saturation (the softmax is saturated on
one prompt, so the local gradient badly underestimates the effect of a query/key change) and cancellation
(direct and indirect effects nearly cancel, so small approximation errors swamp the estimate). Fixes: a QK fix
that recomputes the attention softmax exactly for query/key changes, and GradDrop, which zeroes the gradient
through each layer's residual contribution in turn and averages absolute estimates. They compare AtP and AtP*
against brute-force patching, iterative, subsampling, block and hierarchical search, using a pipeline of cheap
ranking followed by real patching of the top nodes. They also build a statistical diagnostic: subsampling
estimates plus a one-sided Welch t-test give an upper confidence bound on the largest effect among nodes AtP*
ranked low.

## What counts as an explanation here
A ranked list of components with estimated causal effects on a behaviour: localisation, the first step toward a
circuit, not a mechanism.

## How they judged success
Cost of verified recall: forward passes needed (estimation plus verification) to recover the true top-K nodes,
plotted against K at 100% or 90% recall; IRWRGM relative cost, a single scalar relative to an oracle that verifies
nodes in true order. False-negative analysis by node type. Confidence bounds on missed effects at 90/99/99.9%.

## What they found
AtP clearly beats the other cheap methods, and AtP* improves further. The QK fix removes many attention-node
false negatives; GradDrop mainly fixes large neuron false negatives caused by cancellation. Performance holds on
random prompt pairs, so it does not depend on a crisp circuit. On distributions, subsampling becomes
relatively cheaper and GradDrop matters less. Recommendations: AtP* for single pairs, AtP+QK fix for attention on
distributions, plain AtP for neurons on distributions, subsampling for many pairs. They note SAE features would
cut node counts by roughly 20–50x.

## Limits and open problems they name
Few prompt distributions tested, often one pair; neurons may not be meaningful units; coarse nodes (whole layers)
untested and possibly worse; the ground-truth metric is total effect and can miss instrumentally important nodes;
distribution averages can hide prompt-specific nodes; ranking rather than effect size is evaluated and false
positives are not assessed; only Pythia.

## What we take from it
A scalable estimator and an evaluation design. If our white-box model must predict the effect of ablating or
patching every component, AtP* is a cheap baseline to compare against, and its known failure points (saturated
softmax, cancelling paths) are exactly where a linearised or weight-derived model will also err. The "cost of
verified recall" framing and the false-negative confidence bound are reusable ways to report how much of the true
causal picture a cheap method recovers.

## Tags
unit: neuron | head
form: graph
method: attribution | patching
eval: patching | benchmark
goal: evaluation-of-methods | understanding
