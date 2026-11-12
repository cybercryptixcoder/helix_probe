# Can SAEs Capture Neural Geometry? (paper: Do Sparse Autoencoders Capture Concept Manifolds?)

- **Key:** arxiv-2604.28119
- **Authors / organisation:** Usha Bhalla, Thomas Fel (co-first), Can Rager, Sheridan Feucht, Tal Haklay, Daniel Wurgaft, Siddarth Boppana, Matthew Kowal, Vasudev Shyam, Owen Lewis, Thomas McGrath, Jack Merullo, Atticus Geiger, Ekdeep Singh Lubana; Goodfire with Harvard, Northeastern, Technion, Stanford
- **Date:** 2026-04 (arXiv); Goodfire post 2026-05-21
- **Link:** https://arxiv.org/abs/2604.28119 (post: https://www.goodfire.com/research/can-saes-capture-neural-geometry)
- **Kind:** paper
- **Read from:** full text (post plus arXiv HTML main body; appendix text partly cut off)
- **Relevance to us:** 3 (central)

## What they wanted, and why
SAEs rest on the linear representation hypothesis: each concept is one direction. But many concepts in LLMs (days, years, colours, temperature) sit on curved, low-dimensional manifolds. The authors ask whether SAEs capture such manifolds, and if so in what form, since the answer decides whether the field's main decomposition tool is a sound basis for understanding and steering. Their post's metaphor is the blind men and the elephant: each SAE direction gives a locally correct but partial view.

## What they studied
Synthetic: 48 manifold instances of eight types (circle, sphere, torus, Möbius strip, Swiss roll, helix, flat disk, segment) embedded in R^128, with TopK SAEs of width 512. Real: Llama-3.1-8B, layer-19 residual stream (d = 4096), SAEs trained on 500M Pile tokens in five architectures (standard L1, JumpReLU, TopK, BatchTopK, Matryoshka) at x8 and x16 width (32,768 / 65,536 atoms), k in {64, 128, 256}; only SAEs above 0.85 variance explained kept. Concepts: colours, temperature, age, geography, days, years, formality, sentence length, political bias. Unit: SAE atoms and groups of atoms.

## How they did it
They model activations as an additive mixture of manifolds (a direction is a 1-D ray special case) and define how a dictionary can relate to a manifold: compact subspace capture (a fixed small set of atoms spans the manifold and is used for all its points; a theorem gives sufficient conditions via sparse-recovery results), or tiling, where atoms act as local detectors with receptive fields, either nearly disjoint (shattering) or heavily overlapping (dilution). They also argue convex-hull style point-based SAEs cannot factor superposed manifolds. On synthetic data they sweep sparsity to see which regime appears. On Llama they first show manifold structure by PCA and by centroid-interpolation steering, then measure restricted R² (how well a manifold's activations are reconstructed using only its top features) as the support size grows, plot piecewise-linear reconstructions, tuning curves and receptive fields. To regroup atoms they compare five affinity measures (decoder cosine, conditional co-activation, Pearson correlation of magnitudes, pointwise mutual information, pairwise Ising couplings fit to binarised codes), and decode each group by projecting onto its decoder subspace. Finally they run the Ising grouping unsupervised on a BatchTopK SAE (x8, k = 64).

## What counts as an explanation here
A geometric object rather than a list of directions: a group of SAE atoms whose span and co-activation pattern reconstructs a continuous concept manifold with its own coordinates. Partial and descriptive; prediction is limited to steering by interpolating along the manifold.

## How they judged success
Synthetic: recovery of the ground-truth manifold partition and the regime as a function of k. Real: restricted R² versus support size relative to the manifold's ambient dimension; qualitative tuning curves and receptive fields; block-diagonal structure of each affinity matrix for supervised concepts; reconstruction of continuous geometry from group decoding versus raw activations; optimal-transport alignment across SAE runs (in an appendix); unsupervised recovery of known manifolds. Few numeric scores are given for grouping; most comparisons are figures.

## What they found
- Synthetic: three regimes as k grows: shattering at low k, compact capture near k = 4, dilution at high k. Even without compact capture, Ising couplings recover blocks matching the true manifolds, and decoding via the recovered groups reconstructs each manifold.
- Real SAEs are in the dilution regime: restricted R² keeps rising well past each manifold's ambient dimension; each feature covers a local patch; tuning curves look like population codes (for years, many features track the ones digit with period 10, others the decade); the tiling geometry depends on architecture (TopK splits space angularly, L1 linearly).
- Ising couplings and conditional co-activation give clean blocks; decoder cosine and Pearson correlation fail.
- Unsupervised Ising grouping recovered temperature, colour and political-bias manifolds and surfaced a new candidate manifold for epistemic uncertainty in scientific text.
- Individual features do not align across SAE runs, but codes restricted to one manifold do, suggesting the coordinate system is stable even when atoms are not.
- They argue run-to-run instability, brittle single-feature steering and weak autointerp are consistent with manifolds being tiled.

## Limits and open problems they name
Post-hoc grouping is a workaround; featurizers still emit 1-D atoms. Mixed selectivity hurts recovery, and Ising captures only pairwise dependence. One model, one layer for real data. They do not verify a strict differential-geometric manifold definition. Point-based SAEs that factor superposed manifolds remain open. Next steps named: featurizers targeting manifolds directly, and studying the operations over these geometries.

## What we take from it
Central for choosing our unit of analysis. If a white-box model inherits SAE atoms as its variables, curved concepts will appear as many partial, locally valid features with no clean coordinate; it should instead expose continuous manifold-valued variables. Reusable method: binarise feature codes, fit pairwise Ising couplings (or conditional co-activation), and cluster to find feature groups; then use restricted R² versus support size to tell compact capture from tiling. Warning: decoder cosine similarity (a weight-only signal) failed to group features here, so weight-geometry alone may not recover manifold structure without activation statistics.

## Tags
unit: feature, direction
form: dictionary, other (manifold / feature group)
method: SAE, decomposition, steering
eval: other (restricted R², regime recovery on synthetic ground truth, cross-run alignment)
goal: evaluation-of-methods, understanding
