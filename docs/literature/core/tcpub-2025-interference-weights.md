# A Toy Model of Interference Weights

- **Key:** tcpub-2025-interference-weights
- **Authors / organisation:** Chris Olah, Nicholas L. Turner, Tom Conerly; Anthropic
- **Date:** 2025-07-29
- **Link:** https://transformer-circuits.pub/2025/interference-weights/index.html
- **Kind:** blog/research post
- **Read from:** full text (via a page-summarising fetch; plots not inspected directly)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Attribution graphs explain one prompt at a time; the larger goal is global circuit analysis, reading the weights
themselves. The obstacle is weight superposition: if two layers store features in superposition, the effective
("virtual") weights between features are forced to contain many spurious connections, interference weights, that do
not serve the training objective. The authors want precise definitions and a toy setting where real and
interference weights can be separated, so that cheap heuristics for filtering them can be validated. Whether
interference weights can be ignored may decide whether global mechanistic analysis is feasible. Described as an
informal, low-confidence note.

## What they studied
Two toy models. (1) A Toy-Models-of-Superposition autoencoder (h = Wx, output ReLU(W^T h + b)), 100 features in 20
dimensions, feature density 0.02, deliberately undertrained; virtual weights U = W^T W. (2) A more realistic model
y = ReLU(Ax + v) with untied projections, where the true feature map A is block-diagonal and sparse: 128 features in
16 dimensions, 8 blocks, within-block density 0.1, input density 0.3, constant bias -0.1, two seeds. Unit: virtual
feature-to-feature weights.

## How they did it
They gave two definitions. Definition 1: interference = actual virtual weights minus "ideal" weights obtained by
fine-tuning the feature-to-feature matrix in the lifted (feature) space with a small regulariser. Definition 2:
interference = weights whose individual ablation changes loss by less than a small threshold. They coloured virtual
weights by their ablation loss effect and compared across seeds. Using "real" = ablation loss increase above 0.0001
as ground truth, they compared four cheap heuristics (weight magnitude, expected attribution, target-weighted
attribution, activation frequency) against an ideal ranking using precision-recall curves and a "loss gain versus
precision" curve (summed loss effect captured). Appendices examine nonlinear parameter sharing, converged isotropic
geometry, correlated features, and how the definitions conflict.

## What counts as an explanation here
A circuit read directly from weights, after removing interference: the "real" virtual weights are the explanation.
This entry is about how to define and identify that subset, not about a finished explanation.

## How they judged success
Agreement with the ablation-based ground truth: precision-recall and loss-gain-versus-precision curves for each
heuristic; consistency of real weights across seeds; resemblance to patterns seen in real models (logit-weight
histograms and seed scatter plots from Towards Monosemanticity). No headline numbers per heuristic are given.

## What they found
Toy models reproduce the interference signatures seen in real models: interference weights vary independently
across seeds while real weights are consistent. Real and interference weights overlap in magnitude, so magnitude
thresholds fail. Judged by loss captured rather than recall, heuristics look much more promising. With correlated
features, a low-rank structure appears whose ablation hurts loss only because it cancels other interference, so loss
effects are non-additive and the two definitions can disagree.

## Limits and open problems they name
Toy models only; low confidence. Ideal weights are hard to define outside toys (fine-tuning can create new
superposition or learn new weights). The definitions are not equivalent and others are plausible. Real features are
not perfectly monosemantic. Principled definitions do not scale to millions of features. Whether interference can
be ignored for alignment purposes needs scrutiny.

## What we take from it
Directly relevant to reading weights: raw virtual weights are not circuits, and any weight-reading pipeline needs an
interference filter. The ablation-loss definition gives a ground truth we can compute on small models; the
loss-captured-versus-precision curve is the right metric for judging cheap filters; cross-seed consistency is a
cheap, label-free signal of real weights. Also a warning that weight effects are non-additive, so per-weight scores
will not compose into a predictive model without checking joint ablations.

## Tags
unit: weights
form: graph
method: weight-analysis
eval: ablation
goal: understanding
