# Bilinear MLPs Enable Weight-based Mechanistic Interpretability

- **Key:** arxiv-2410.08417
- **Authors / organisation:** Michael T. Pearce, Thomas Dooms, Alice Rigg, Jose Oramas, Lee Sharkey; independent, University of Antwerp, Apollo Research
- **Date:** 2024-10
- **Link:** https://arxiv.org/abs/2410.08417
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Element-wise nonlinearities stop you from reading what an MLP computes off its weights, so interpretability falls back
on activations over a dataset. The authors show that if the MLP is a bilinear layer (a GLU with no nonlinearity,
(Wx) * (Vx)), each output is an exact quadratic form of the input, so the layer's computation can be analysed with linear
algebra on the weights alone. The larger goal is weight-based interpretability that does not depend on data, and
possibly formal guarantees.

## What they studied
Shallow image classifiers (embedding, one bilinear layer of 512 units, head) on MNIST and Fashion-MNIST; a 6-layer
bilinear transformer (~30M parameters, d 512) on a cleaned TinyStories; bilinear GPT-2-style models (162M and 335M) on
FineWeb for low-rank experiments; TopK SAEs (4x, k=30) on MLP inputs and outputs; TinyLlama-1.1B fine-tuned from
SwiGLU into bilinear. Unit: weights (the third-order bilinear tensor and its eigenvectors).

## How they did it
Stack the layer's interaction matrices into a third-order tensor and symmetrise. Main method: pick an output direction
(a class logit via the unembedding, or an SAE output feature), contract the tensor with it to get one symmetric
interaction matrix, and eigendecompose; the output along that direction is a sum of eigenvalue-weighted squared
projections onto eigenvectors, and truncation gives the best low-rank approximation. Alternatives: express the tensor in
an SAE input/output basis to read direct feature-to-feature interactions, or use a higher-order SVD when no features are
known. They test regularisers (input noise, weight decay, dropout) for interpretable eigenvectors, recover a planted
labelling function (Casper MI challenge), build adversarial masks purely from weights (pseudoinverse of top
eigenvectors, no forward passes), dissect a sentiment-negation circuit in layer 4 of the TinyStories model, and measure
how well 1 or 2 eigenvectors approximate SAE output features.

## What counts as an explanation here
For each output direction, a short list of input directions (eigenvectors) with signed weights saying which input
patterns push it up or down quadratically. It is exact for the layer (not an approximation) and, truncated, a
predictive low-rank surrogate. Predictions can be checked by constructing inputs from weights alone.

## How they judged success
Accuracy after eigenvector truncation; cross-run cosine similarity of top eigenvectors; recovery of a known ground-
truth function; accuracy drop and target steering from weight-derived adversarial masks versus random-permutation
masks; eigenvalues versus a random-matrix baseline; correlation between low-rank approximations and actual SAE feature
activations (on active inputs); loss versus SwiGLU/ReGLU at fixed epochs and fixed compute.

## What they found
MNIST eigenvectors look like class prototypes or stroke detectors; Fashion-MNIST gives edge detectors; dense Gaussian
input noise gives the cleanest features. Top eigenvectors are consistent across runs (cosine about 0.8 to 0.9) and
truncation to a few costs about 0.01% accuracy. The planted labelling function was recovered from weights. Weight-only
adversarial masks beat random baselines. In the negation circuit, top eigenvalues 0.62 and -0.66 far exceed random; a
two-eigenvector approximation correlates 0.66 with the feature (0.76 at high activation). Across features, single-
eigenvector approximations average about 0.65 correlation and most exceed 0.75 with two; longer SAE training raised
mean correlation from 0.17 to 0.59. Bilinear layers need about 6% more data than SwiGLU at fixed epochs, roughly equal
at fixed compute; TinyLlama conversion cost about 0.05 loss.

## Limitations and open problems they name
Needs meaningful output directions; deep models depend on data-derived SAE features. Eigenvectors are not guaranteed
monosemantic, and high-rank spectra are harder. Evidence is from small models and one cherry-picked circuit. Biases
interact awkwardly with the quadratic form. Slight performance cost. Future: sparse dictionary learning on the tensor,
weight-based safety bounds, larger models.

## What we take from it
A clear example of an architecture where "read the weights, get a predictive model" is literally true for one layer:
the decomposition is exact and its truncations are measurable surrogates. Two reusable ideas: generate test inputs from
weights alone (adversarial masks) as a check that a weight-read explanation predicts behaviour; and score low-rank
weight explanations by correlation with real activations. Warning: still needs a feature basis for intermediate
directions, which reintroduces data dependence.

## Tags
unit: weights | layer
form: direction | replacement-model
method: weight-analysis | decomposition | training-interpretable | SAE
eval: prediction/simulation | ablation | benchmark | downstream-task
goal: understanding | science
