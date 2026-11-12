# Identifying Functionally Important Features with End-to-End Sparse Dictionary Learning

- **Key:** arxiv-2405.12241
- **Authors / organisation:** Dan Braun, Jordan Taylor, Nicholas Goldowsky-Dill, Lee Sharkey; Apollo Research (Taylor: MATS / University of Queensland)
- **Date:** 2024-05
- **Link:** https://arxiv.org/abs/2405.12241
- **Kind:** paper
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Standard SAEs minimise reconstruction error of activations, but small reconstruction error need not mean the features matter to what the network computes; an SAE can spend capacity on dataset structure the network ignores. The authors want features that are "functionally important", i.e. needed to explain the network's behaviour on its training distribution. The step toward the larger goal: a dictionary that is a faithful, minimal description of the computation, not just of the activation distribution.

## What they studied
GPT-2 small residual stream (main focus layer 6, with layers 2 and 10), plus TinyStories-1M for supplementary runs. Unit: dictionary features (SAE latents).

## How they did it
1. Baseline SAE_local: reconstruct one layer's activations, MSE plus L1 sparsity.
2. SAE_e2e: splice the SAE output into the frozen model in place of the layer's activations and train the SAE to minimise KL divergence between the spliced model's output distribution and the original's, plus L1. Reconstruction of the activation itself is not directly trained.
3. SAE_e2e+ds: additionally penalise differences between spliced and original activations at all downstream layers, so the computation follows the original pathway.
4. Compare at matched L0 and at matched CE-loss increase: CE loss increase, L0, alive dictionary size, downstream-layer reconstruction MSE.
5. Analyse geometry (nearest-neighbour cosine similarities within an SAE, across SAE types and across seeds), run automated interpretability (Bills et al. style) on about 200 features per SAE, and inspect qualitative differences.

## What counts as an explanation here
A sparse feature dictionary at one layer, where "faithful" is redefined as preserving the network's output distribution when spliced in (behavioural faithfulness), rather than reproducing the activation vector. Partial (one layer at a time), and the dictionary is judged by how much of the model's performance it explains per active feature.

## How they judged success
Pareto curves of CE loss increase vs L0; number of alive features; downstream reconstruction MSE (does the spliced model stay on the original computational path?); robustness of features across seeds (cosine similarity); automated interpretability score; qualitative feature inspection.

## What they found
- Pareto improvement: at the same L0, both e2e variants had a CE loss increase under 45% of SAE_local's (L0 range 50-300).
- At layer 6 with similar CE loss increase: local L0 69.4 with 26k alive features (CE increase 0.145); e2e L0 27.5 with 22k (0.144); e2e+ds L0 36.8 with 15k (0.125). So fewer features per input and fewer features overall explain the same amount of behaviour.
- SAE_e2e reconstructs later layers badly (it takes a different route through the network) and its features are not stable across seeds; e2e+ds matches local downstream and is seed-robust.
- Local SAE features are more clustered, read as more feature splitting; e2e+ds partly align with local features.
- Interpretability: no significant autointerp difference at matched L0; at matched CE loss e2e+ds scored higher at layers 2 and 6, not at 10.
- E2e+ds ignores some functionally unimportant directions (e.g. one PCA direction at layer 10), which may explain its cleaner dictionary.

## Limits and open problems they name
Mainly one model and layer; e2e training costs about 2-3.5x more; e2e+ds loss weights barely tuned; pure e2e can find features that reach the right output by an unfaithful internal path; autointerp is an imperfect metric on a small sample; training instability at higher learning rates.

## What we take from it
- **Framing (central):** define faithfulness behaviourally (output KL when spliced in) rather than by reconstruction; this is the right criterion for a predictive white-box model.
- **Warning:** optimising only for output match can yield a surrogate that is right for the wrong internal reasons; adding downstream-activation matching (e2e+ds) keeps the reconstruction on the real computational path. A predictive model built from weights should be checked both ways.
- **Measure:** CE/KL increase when the surrogate is spliced in, downstream-layer MSE, and seed stability are directly reusable.
- **Method:** "how few components explain how much behaviour" (L0 at fixed CE increase) is a useful description-length-like score.

## Tags
unit: feature | layer
form: dictionary | replacement-model
method: SAE
eval: faithfulness | ablation | human-rating
goal: understanding | evaluation-of-methods
