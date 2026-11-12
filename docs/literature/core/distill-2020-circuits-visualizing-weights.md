# Visualizing Weights

- **Key:** distill-2020-circuits-visualizing-weights
- **Authors / organisation:** Chelsea Voss, Nick Cammarata, Gabriel Goh, Michael Petrov, Ludwig Schubert, Ben Egan, Swee Kiat Lim, Chris Olah; OpenAI with Mount Royal University and Stanford (Distill Circuits thread)
- **Date:** 2021-02-04
- **Link:** https://distill.pub/2020/circuits/visualizing-weights/
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Interpretability work mostly studies activations (what a network sees), while weights, which say how each layer is computed from the previous one, are rarely examined directly. The authors collect practical techniques for making weights readable, framing weights as the compiled instructions of the network. They name three obstacles: hidden-layer weights lack context, important interactions skip layers, and weight tensors are huge. The goal is a toolkit for the circuits programme of reading algorithms out of parameters.

## What they studied
InceptionV1 (ImageNet), examples from conv2d2, mixed3a, mixed3b, mixed4d_5x5, mixed5b_5x5; general remarks on residual and bottleneck architectures. Unit: weights between neurons, between layers, and factors of weights.

## How they did it
They present a set of techniques, each illustrated on examples. Contextualise weights by labelling each input and output neuron with its feature visualisation, and fix an output neuron to show its highest-magnitude input weights as spatial heatmaps. Use small multiples to show weights between two whole neuron families. Feature-visualise the input vector at each spatial position to see what each position of a kernel looks for. Reduce input channels with one-sided NMF to three factors shown as RGB for quick whole-layer views (revealing weight banding), and decompose an output neuron's weights into NMF factors that map back to input neurons (e.g. high-low frequency detectors largely explained by two factors). Compute "expanded weights" between non-adjacent layers by multiplying through intermediate layers, in practice by taking gradients through a linearised model, which also lets them jump over low-channel bottleneck layers that are often polysemantic.

## What counts as an explanation here
Visual, human-read depictions of weight structure annotated with feature labels: which inputs excite or inhibit a unit at which spatial positions, possibly summarised by a few factors. These support circuit descriptions; they do not predict behaviour on their own.

## How they judged success
No formal evaluation or benchmark; success is that known circuits become legible. The only numbers are illustrative factor coefficients.

## What they found
The methods make several known circuits readable (e.g. high-low frequency detectors, curve circuits). Expanded weights equal the true linear map when the path is linear, and for nonlinear paths approximate the expected gradient up to a constant under the assumption that intermediate neurons fire independently with equal probability. Weights, activations and attributions are complementary: what, how, and why a unit fired.

## Limits and open problems they name
Expanded weights can cancel to near zero when a unit uses both signs of an interaction nonlinearly (boundary detectors). Factors are not aligned with neurons or nonlinearities and can be polysemantic, making whole-model reasoning harder. Focusing on large weights ignores a long tail whose importance is unknown. Sparsity might help but is unproven. Multi-layer nonlinear interactions, per-example gradients, choosing which neurons to study, and interpreting smooth "orbital" patterns in expanded weights remain open.

## What we take from it
Directly reusable tools for reading weights: expanded (virtual) weights via gradients of a linearised model, NMF of weight tensors, and labelling weight endpoints with feature identities. Key caveat for a predictive model: linear expanded weights miss sign-dependent nonlinear interactions, so a weight-read model needs per-path or input-conditioned corrections. The weights/activations/attributions split is a useful framing for what our model must contain.

## Tags
unit: weights | neuron | layer
form: description
method: weight-analysis | decomposition
eval: human-rating
goal: understanding
