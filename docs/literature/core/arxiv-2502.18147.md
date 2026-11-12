# Jacobian Sparse Autoencoders: Sparsify Computations, Not Just Activations

- **Key:** arxiv-2502.18147
- **Authors / organisation:** Lucy Farnik, Tim Lawson, Conor Houghton, Laurence Aitchison; University of Bristol
- **Date:** 2025-02 (v2 2025-06)
- **Link:** https://arxiv.org/abs/2502.18147
- **Kind:** paper
- **Read from:** full text (HTML; main text and appendices summarised)
- **Relevance to us:** 3 (central)

## What they wanted, and why
SAEs make activations sparse but leave the computation between layers dense, so one still cannot read off how input features produce output features. The authors want the mapping across an MLP to itself be sparse: each output feature computed from only a few input features. This is a step from describing representations toward describing computation, i.e. small readable circuits.

## What they studied
Pythia-410m (main, layer 15), plus Pythia-70m and Pythia-160m. Unit: the function from input-SAE latents to output-SAE latents across one MLP (feature-to-feature edges).

## How they did it
They train two TopK SAEs together, one on the MLP input and one on its output. The composite function f_s (TopK → input decoder → MLP → output encoder) maps input latents to output latents. The loss is both SAEs' reconstruction MSE plus an L1 penalty on the Jacobian of f_s scaled by λ/k²; λ = 0 gives ordinary separately trained SAEs. To make this tractable they only consider the k×k block for active latents and derive a closed form for GPT-2-style MLPs needing three matrix multiplies (a GLU version is derived but not tested). Training costs about 2x a single SAE (72 vs 33 minutes on Pythia-70m, 100M tokens). They sweep λ, compare with standard SAEs and with randomly re-initialised transformers, and test whether each scalar input→output latent function is linear.

## What counts as an explanation here
A sparse bipartite graph of feature-to-feature dependencies across one MLP, with (mostly) linear edge weights given by the Jacobian, plus feature descriptions. Partial (one layer) but locally predictive: the Jacobian entry predicts how an output latent changes when an input latent is nudged.

## How they judged success
Jacobian sparsity (share of entries above thresholds such as 0.01, out of k² = 1024, over ~10M tokens); variance explained of both SAEs; CE loss increase when reconstructions are spliced in; automated fuzzing interpretability scores; linearity classification of sampled scalar functions; control comparison with random-init models.

## What they found
JSAEs strongly cut the number of large Jacobian entries versus standard SAEs, with little cost at moderate λ (sweet spot λ ≈ 0.5 for Pythia-410m, ≈ 1 for Pythia-70m); larger λ mainly hurts the output SAE. Latent interpretability matches standard SAEs. Of 10,000 sampled scalar functions, 88% are linear, 10% JumpReLU-like, ~2% other; for 97.7% of sampled pairs the Jacobian closely predicts the effect of shifting an input latent by 1. Trained models have much sparser Jacobians than random ones, and JSAEs help more on trained models, suggesting real sparse computational structure. Example: a "text is German" output latent built from German-token, place-name and related input latents.

## Limits and open problems they name
Single MLP layer only; GPT-2-style MLP only (GLU untested); relies on TopK; the Jacobian is local and only a proxy for computational sparsity; linearity is not verified by fitting a linear model; no quantitative comparison with transcoders.

## What we take from it
A direct template for a predictive white-box layer model: sparse, mostly linear feature-to-feature maps whose edges can be checked by intervention (Jacobian vs actual effect of a +1 shift is a ready-made prediction test). The random-init control is a cheap, valuable baseline for any claim of "structure". The closed-form Jacobian through the MLP weights is close to reading computation from weights. Open gap: chaining such layers into a whole-model replacement.

## Tags
unit: feature, weights
form: graph, dictionary, replacement-model
method: SAE, decomposition, weight-analysis
eval: prediction/simulation, faithfulness
goal: understanding, science
