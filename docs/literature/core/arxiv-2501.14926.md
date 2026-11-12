# Interpretability in Parameter Space: Minimizing Mechanistic Description Length with Attribution-based Parameter Decomposition (APD)

- **Key:** arxiv-2501.14926
- **Authors / organisation:** Dan Braun, Lucius Bushnaq, Stefan Heimersheim, Jake Mendel, Lee Sharkey; Apollo Research
- **Date:** 2025-01
- **Link:** https://arxiv.org/abs/2501.14926
- **Kind:** paper
- **Read from:** full text of main body (appendices partly)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Most mechanistic interpretability is "activations first": learn sparse dictionaries of activation directions, then try
to connect them into circuits. The authors list its problems (reconstruction error, feature splitting, dense latent
connections, unexplained feature geometry) and propose a "parameters first" route: decompose the weights themselves
into mechanisms. The guiding principle is minimum description length: the best explanation uses as few, as simple,
mechanisms per input as possible while still adding up to the real network. APD is the first method in this line and
the root of SPD (arxiv-2506.20790) and VPD (goodfire-research-interpreting-lm-parameters).

## What they studied
Only toy models with known ground truth: Toy Model of Superposition (ReLU(W^T W x + b)) as TMS_5-2 and TMS_40-10; a toy
compressed-computation model (one residual MLP with d_resid 1000, 50 neurons, 100 features, target y = x + ReLU(x)); and
a cross-layer distributed version (two MLPs of 25 neurons). Unit: weights (parameter components spanning layers).

## How they did it
The network's parameter vector is approximated by a sum of C parameter components. Three losses: faithfulness (MSE
between the sum and the true parameters); minimality (for each input, compute gradient attributions of the output to
each component, keep only the top-k most attributed, run a forward pass with only those, and match the target output,
using batch top-k); and simplicity (a Schatten-p quasi-norm on singular values of each active component's matrices, so
components prefer low rank and few layers). Biases form one always-on component. They over-provision components
(130 for 100 features, 200 for the 2-layer model) because some die. For compressed computation they run a causal-
scrubbing-style test: randomly ablate half the components but keep the one for the active feature, versus ablating that
one.

## What counts as an explanation here
A set of parameter-space vectors ("mechanisms") that sum to the network's weights, of which only a few are needed on any
input, each as simple as possible. Meant to be a complete and minimal description; predicts which mechanisms can be
removed on a given input without changing output.

## How they judged success
Mean Max Cosine Similarity (MMCS) and Mean L2 Ratio (ML2R) against ground-truth rank-one mechanisms in TMS; comparison
of component neuron-contribution patterns with the target model; MSE histograms under "scrubbed" vs "anti-scrubbed"
ablations, with a monosemantic-neuron reference line. SVD and NMF are dismissed on theoretical grounds (they cannot
produce more components than the matrix rank); no empirical comparison with SAEs or transcoders.

## What they found
TMS: MMCS 0.998 (5-2) and 0.996 (40-10), with ML2R 0.893 and 0.935 showing some shrinkage. Compressed computation: one
component per feature computation, matching the target's neuron contributions; scrubbed ablations barely change MSE,
anti-scrubbed ones raise it a lot. Cross-layer: components per feature that span both layers, but messier, with more
components covering two features. The 2-D TMS case was brittle.

## Limitations and open problems they name
Memory cost similar to many copies of the model; heavy hyperparameter tuning, especially top-k; gradient attributions
are first-order and fail when gradients are small; rank-based simplicity privileges within-layer mechanisms; shrinkage;
toy models only. Open directions include multidimensional features, decomposition-friendly architectures, and uses in
anomaly detection, editing and memorisation studies.

## What we take from it
The conceptual foundation for reading mechanisms directly from weights, with MDL as an explicit objective
(faithful + minimal + simple) that can score competing white-box explanations. The planted-toy-model protocol and
scrubbed/anti-scrubbed ablation are cheap tests we can reuse. Its failures (top-k sensitivity, attribution unreliability,
cost) are exactly what SPD and VPD fix, so for implementation start from those.

## Tags
unit: weights
form: replacement-model | causal-abstraction
method: decomposition | weight-analysis | attribution
eval: ablation | faithfulness | benchmark
goal: understanding | science
