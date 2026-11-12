# Toy Models of Superposition

- **Key:** tcpub-2022-toy-model
- **Authors / organisation:** Nelson Elhage, Tristan Hume, Catherine Olsson, et al.; Anthropic (with Harvard collaborators)
- **Date:** 2022-09
- **Link:** https://transformer-circuits.pub/2022/toy_model/index.html
- **Kind:** paper
- **Read from:** full text (via page fetch in two parts)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors ask why some neurons are cleanly interpretable and others respond to unrelated things. They hypothesise
superposition: a network representing more features than it has dimensions by storing them as non-orthogonal
directions. They want to demonstrate it unambiguously in a minimal setting, map when it happens, show computation
can happen in superposition, and lay out how interpretability could get around it, since enumerating all features
would be needed for strong safety claims.

## What they studied
Tiny ReLU networks trained on synthetic sparse inputs: n features compressed into m < n hidden dimensions
(e.g. n=20, m=5 with importance 0.7^i; n=80, m=20 with 0.9^i; 2 features in 1 dimension), plus variants with a
ReLU hidden layer (privileged basis) and a model computing absolute value (100 features, 40 neurons). Units:
features, their weight columns W_i, neurons.

## How they did it
Each input feature is zero with probability S (sparsity) and otherwise uniform; each has an importance weight. The
model maps x to h = Wx and reconstructs either linearly (W^T W x + b) or with a ReLU (ReLU(W^T W x + b)), trained on
importance-weighted MSE. They vary sparsity and importance, train many seeds and keep the lowest-loss solution,
then read the learned W directly. Measurements: ||W_i|| (is the feature represented), interference with other
features, per-feature dimensionality D_i, and dimensions per feature D* = m / ||W||_F^2. They draw phase diagrams
over sparsity and relative importance, graphs of feature geometry, training dynamics, and test adversarial
vulnerability of the learned maps. They also compare with compressed-sensing bounds.

## What counts as an explanation here
The explanation is the weight matrix itself read as a geometric arrangement of feature directions, plus a theory
(phase diagram) predicting which arrangement a model will adopt given feature sparsity and importance. It is
complete for the toy model and predictive of its behaviour; the authors are unsure what transfers to real models.

## How they judged success
Ground truth is known (the synthetic features), so success is whether learned weights match predicted regimes:
loss, ||W_i||, interference, D_i and D*, analytic solutions for the smallest cases (first-order phase transitions
confirmed by discontinuous loss derivatives), and adversarial-attack sensitivity versus superposition level.

## What they found
Linear models never superpose; ReLU models superpose once features are sparse, starting with antipodal pairs.
Phase changes separate three outcomes per feature: not learned, superposed, or dedicated dimension. Dimensionality
clusters at discrete values tied to polytopes (3/4 tetrahedron, 2/3 triangle, 1/2 antipodal pair, 2/5 pentagon,
3/8 square antiprism) and D* sticks at 1 and 1/2. Correlated features tend to sit orthogonal; anticorrelated ones
interfere negatively. Training shows step-like jumps. A ReLU hidden layer creates a privileged basis where neurons
shift from monosemantic (dense) to polysemantic (sparse). Absolute value can be computed in superposition. Adversarial
vulnerability rose over 3x as superposition formed. Compressed-sensing bounds imply feature capacity linear in m
scaled by a sparsity factor.

## Limitations and open problems they name
Very small models whose geometry may be idiosyncratic; hard optimisation; adversarial link only suggestive;
incomplete theory for non-uniform cases; the ReLU-hidden-layer model can be bypassed via bias. Open: statistical
tests for superposition, closed-form solutions, whether it fades with scale, capacity, and how computation works in
superposition. Three proposed strategies: train superposition-free models (e.g. L1, mixture-of-experts), find an
overcomplete basis afterwards (dictionary learning), or hybrids.

## What we take from it
The core reason a white-box model cannot just read neurons or weight rows: features are packed non-orthogonally,
so any weight-reading method needs a decomposition step. The toy setup is an ideal testbed with known ground truth
for validating a weight-reading method before touching real models (we can check that our method recovers the
planted features and predicts behaviour). Measures to reuse: D_i, D*, interference. The phase diagram is a model of
what kind of prediction we want: from data statistics to learned weights.

## Tags
unit: feature, neuron, weights
form: direction, causal-abstraction, other
method: weight-analysis, training-interpretable, other
eval: prediction/simulation
goal: science, understanding
