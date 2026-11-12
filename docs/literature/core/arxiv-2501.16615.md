# Sparse Autoencoders Trained on the Same Data Learn Different Features

- **Key:** arxiv-2501.16615
- **Authors / organisation:** Gonçalo Paulo, Nora Belrose; EleutherAI
- **Date:** 2025-01
- **Link:** https://arxiv.org/abs/2501.16615
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Many hope SAEs can list all the features a model uses, which would help safety audits. That hope assumes there is one objective feature decomposition. The authors test this by training SAEs that differ only in random initialisation seed and measuring how many features they share.

## What they studied
Main: Pythia 160M, SAEs on the sixth MLP layer, 2^15 latents, first 8B Pile tokens, same data order across seeds. Also Llama 3 8B (FFN SAE, 131K latents), SmolLM and GPT-2 (residual and MLP). Architectures: ReLU+L1, Gated, TopK. Unit: SAE latents.

## How they did it
Latents of two SAEs are paired one-to-one by the Hungarian algorithm maximising cosine similarity, done separately for encoder and decoder vectors. A latent is "shared" if both matchings give the same partner with cosine ≥ 0.7; otherwise it is an "orphan". Max-cosine matching is used as a check. They vary architecture, width, k, training length, model size and layer, train up to nine seeds to see how the orphan fraction scales, and score latents with automated detection-based interpretability.

## What counts as an explanation here
Not an explanation method itself; it audits whether an SAE dictionary is a stable, unique description of the model.

## How they judged success
Fraction of shared latents across seeds; similarity distributions; trend of orphan fraction with number of seeds (power-law fit with offset); detection scores of shared vs orphan latents; firing frequency vs sharing.

## What they found
Only 42% of latents are shared between two Pythia-160M seeds, and about 30% for Llama 3 8B. With nine seeds, ~35% of latents still appear in only one SAE, and the decline is slow. Frequently firing latents tend to be shared. Orphans are often interpretable too (average detection score 0.72 overall), so one run misses interpretable features. TopK SAEs are more seed-dependent than ReLU/Gated even at matched sparsity; more latents and larger k reduce overlap, longer training increases it; overlap is lower in early and final layers. Absorption is not the main cause. They attribute this to the non-convex SAE loss with many local optima.

## Limits and open problems they name
Detailed analysis mostly on one model and one dataset; the 0.7 threshold is a choice; interpretability relies on an LLM scorer; only nine SAEs for the asymptotic trend.

## What we take from it
Warning for any white-box model built on a single SAE dictionary: the dictionary is one of many valid decompositions, not the model's "true" features. Claims should be robust across seeds; report cross-seed overlap (Hungarian matching on encoder and decoder, cosine ≥ 0.7) as a stability control. This favours defining our explanation by what it predicts (behaviour under intervention) rather than by matching a canonical feature list.

## Tags
unit: feature
form: dictionary
method: SAE
eval: benchmark
goal: evaluation-of-methods, science
