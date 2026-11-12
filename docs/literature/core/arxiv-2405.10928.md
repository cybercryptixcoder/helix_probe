# The Local Interaction Basis: Identifying Computationally-Relevant and Sparsely Interacting Features in Neural Networks

- **Key:** arxiv-2405.10928
- **Authors / organisation:** Lucius Bushnaq, Stefan Heimersheim, Nicholas Goldowsky-Dill, Dan Braun, Jake Mendel, Kaarel Hänni, Avery Griffin, Jörn Stöhler, Magdalena Wache, Marius Hobbhahn; Apollo Research (plus Cadenza Labs and independents)
- **Date:** 2024-05
- **Link:** https://arxiv.org/abs/2405.10928
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Neurons are polysemantic, so they are bad units of explanation. The authors look for a change of basis for each layer's
activations, derived from the network's own Jacobians (i.e. how the weights propagate change), that drops directions
irrelevant to later computation and makes interactions between adjacent layers sparse. It builds on their
parameterisation-invariance framework and is an early weight/gradient-informed alternative to SAEs, assuming features
are not in superposition.

## What they studied
A 1-layer modular-addition transformer (mod 113, 5 seeds); a CIFAR-10 MLP (two hidden layers of 60 ReLUs, about 47-48%
test accuracy); GPT-2-small (85M); TinyStories-1M. Unit: directions (basis vectors per layer) and edges between them.

## How they did it
Per layer: centre activations, rotate to principal components, drop near-zero-variance directions, whiten. Then, going
backwards from the output, compute Jacobians of next-layer features with respect to current-layer features over the
dataset, take the SVD, rotate into the right singular vectors, drop directions with zero singular value (no downstream
effect), and scale by singular values so features are weighted by downstream importance. Edges are integrated-gradients
attributions, RMS-averaged over data (and tokens). Sparsity is tested by bisection search for the fewest edges that keep
performance; modules by Leiden clustering. Transformers need restructuring (LayerNorm variance as a separate feature,
biases folded, stochastic Jacobian estimates). The baseline is the same pipeline in a plain PCA basis.

## What counts as an explanation here
A per-layer basis of features plus a sparse, possibly modular interaction graph between layers. Partial and
descriptive; it does not aim to be a predictive surrogate, though features can be probed and intervened on.

## How they judged success
Hand counts of computationally irrelevant features; monosemanticity as variance explained by one Fourier term (modular
addition); number of ablatable edges at a performance threshold (99.9% accuracy; within 0.1 points for CIFAR; loss
increase under 0.1 for GPT-2); Leiden modularity; probe AUROC and an intervention test on CIFAR. Baseline: PCA.

## What they found
Toys: LIB removes irrelevant features (e.g. about 3 vs 14 in a modular-addition middle layer), is sparser than PCA in
attention and in 3 of 5 seeds for the MLP, and in every CIFAR layer and seed; no consistent monosemanticity gain;
modularity works only for a cherry-picked seed. On CIFAR it isolates an animal-vs-vehicle direction (probe AUROC 0.932
vs model 0.946); setting it to the true label lifts accuracy from 47.6% to 54.6%. GPT-2: positional features are clean
(about 97% of variance in four directions) but most other directions are uninterpretable, the graph is dense, and about
80-95% of edges are ablatable in both bases with LIB only slightly better. TinyStories-1M: LIB consistently sparser. The
authors conclude LIB gives no substantial gain on language models.

## Limitations and open problems they name
The non-overcomplete assumption likely fails in LMs (superposition). Interpretability judgments are subjective, and SAE
features looked more interpretable; PCA (not SAEs) was the baseline. Leiden modularity is unreliable. Edge ablation can
go off-distribution. Jacobians are expensive for transformers. No proof that the SVD basis is sparsest. Future: an
overcomplete, sparse-coding version (which became the parameter-decomposition line).

## What we take from it
A documented negative result: a complete-basis, gradient-derived rotation cannot capture LM features because of
superposition, which is why the same group moved to overcomplete parameter decompositions (APD, SPD, VPD). Reusable
pieces: "drop directions with no downstream effect" as a relevance filter, PCA as a baseline, and edge-ablation
bisection as a sparsity measure. Warning against assuming a non-overcomplete feature basis in our own white-box model.

## Tags
unit: direction | layer
form: dictionary | graph
method: weight-analysis | attribution | decomposition | ablation | probing
eval: ablation | human-rating
goal: understanding | science
