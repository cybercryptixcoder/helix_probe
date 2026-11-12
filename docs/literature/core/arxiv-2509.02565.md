# Understanding Sparse Autoencoder Scaling in the Presence of Feature Manifolds

- **Key:** arxiv-2509.02565
- **Authors / organisation:** Eric J. Michaud, Liv Gorton, Tom McGrath; Goodfire (Michaud also MIT)
- **Date:** 2025-09
- **Link:** https://arxiv.org/abs/2509.02565 (Goodfire page https://www.goodfire.com/research/sae-scaling-with-feature-manifolds redirects here)
- **Kind:** paper
- **Read from:** full text (main body and most appendices; the fetched HTML was cut off partway through the appendices)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
SAE reconstruction loss falls as a power law in the number of latents, and the field partly reads this as "bigger dictionaries find more features". The authors ask whether multi-dimensional features (feature manifolds, e.g. a circle for days of the week) could break that reading: an SAE might keep spending new latents to tile a few common manifolds more finely instead of discovering new, rarer features. If so, scaling SAEs would leave much of the model's content undiscovered ("dark matter") even while loss keeps going down. The work is a step toward knowing whether SAE dictionaries can converge on a complete feature inventory at all.

## What they studied
Mostly a theoretical model, checked with toy SAEs on synthetic manifolds (circles, hyperspheres, manifolds with radial variation) and a numerical allocation simulation. For real-model context they look at latent-frequency statistics of Gemma Scope SAEs (JumpReLU, 16k and 32k latents) and decoder-direction geometry of ReLU/L1 SAEs on Inception-v1. Unit: SAE latents versus underlying features (discrete or manifold-shaped).

## How they did it
They adapt Brill's (2024) capacity-allocation model of neural scaling. Activations are assumed to be sums of sparse features, each living in its own subspace with a firing frequency p_i and dimension d_i. The SAE is idealised: each latent belongs to exactly one feature, its decoder lies in that feature's subspace, and feature subspaces are orthogonal. Total loss then becomes a weighted sum of per-feature losses, sum_i p_i L_i(n_i), where n_i latents are assigned to feature i under a budget of N, and the question becomes the optimal allocation. With only discrete features whose frequencies follow a power law with exponent 1+alpha, the optimum gives one latent per feature, loss scales as N^-alpha and the number of discovered features D(N) grows linearly. Adding manifold features whose own loss falls as n^-beta when given n latents yields two regimes depending on whether alpha or beta is larger. They then train toy ReLU SAEs (L1 coefficient 0.1) on manifold data to measure beta empirically, run a numerical allocation with one manifold and many discrete features, and inspect Gemma Scope latent-frequency slopes to guess plausible alpha.

## What counts as an explanation here
A scaling theory: a closed-form account of how an SAE's latent budget gets divided between features, which predicts loss-vs-N exponents and how many distinct features a dictionary of a given size will discover. It is explicitly a framing, not a decomposition of any specific model.

## How they judged success
Agreement between predicted and simulated scaling exponents; measured beta (loss-vs-latents slope on a manifold) for toy SAEs; D(N)/N (fraction of latents that correspond to distinct features); latent frequency-rank slopes in Gemma Scope; nearest-neighbour cosine similarity among decoder directions in LLM and vision SAEs. No downstream task benchmarks.

## What they found
- Benign regime (alpha < beta): loss scales as N^-alpha and D(N)/N tends to a constant. Pathological regime (beta < alpha): loss scales as N^-beta, D(N) grows only as N^((1+beta)/(1+alpha)), and the fraction of latents that are new features goes to zero.
- In a simulation with beta much smaller than alpha, a 100-million-latent SAE discovered only about 3 million features.
- Toy SAEs on hyperspheres of dimension 6-8 showed beta of roughly 0.05 between 10^2 and 10^4 latents, with some manifolds absorbing at least 10^4 latents without the loss plateauing.
- With radial variation, manifolds saturated quickly (around 2 latents per dimension), suggesting the SAE learns a basis rather than tiling.
- Gemma Scope latent frequency slopes were about -0.57 (32k) and -0.74 (16k), implying alpha around 0.5-0.7 if latents matched features one-to-one.

## Limits and open problems they name
They cannot tell whether real SAEs are in the pathological regime, because real alpha and beta are unknown. The idealising assumptions (latents dedicated to one feature, orthogonal subspaces) are known to be violated by absorption and non-orthogonality. Toy radial-variation results may not transfer. Open: measuring alpha and beta in real models, the effect of "ripples" (small variation in many extra dimensions), and whether absorption/composition distort latent frequencies as a proxy for feature frequencies.

## What we take from it
A warning and a measure. Warning: falling SAE reconstruction loss is not evidence that a dictionary is converging on a complete, predictive inventory of the network's variables; capacity can be soaked up by finely tiling a few manifolds. Measure: tracking D(N)/N (distinct features per latent) and per-concept loss-vs-latents slopes is a cheap check on whether a decomposition is still finding new content. For a weights-based white-box model, it argues for representing known manifold variables directly (as continuous coordinates) rather than as many discrete latents.

## Tags
unit: feature
form: other (scaling theory)
method: SAE, other (theoretical model, toy simulation)
eval: other (scaling exponents, simulation agreement)
goal: evaluation-of-methods, science
