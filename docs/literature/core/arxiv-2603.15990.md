# W2T: LoRA Weights Already Know What They Can Do

- **Key:** arxiv-2603.15990
- **Authors / organisation:** Xiaolong Han, Ferrante Neri, Zijian Jiang, Fang Wu, Yanfang Ye, Lu Yin, Zehong Wang; University of Surrey, Stanford University, University of Notre Dame
- **Date:** 2026-03
- **Link:** https://arxiv.org/abs/2603.15990
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Can you tell what a LoRA adapter does (what data it was trained on, how well it performs, which task it is for)
just from its weights, without running the base model or seeing training data? The obstacle is that a LoRA
update BA can be factored in infinitely many ways (any invertible r x r matrix can be inserted), so an encoder
trained on raw factors may learn the arbitrary factorisation instead of the update. They want a symmetry-free
representation and an encoder on top of it, as a step toward searching and auditing large adapter libraries.

## What they studied
LoRA adapters (rank 8) on Stable Diffusion v1.4 (CelebA-LoRA, 10,177 adapters, one per identity; CUB-LoRA, 11,788,
one per image) and Llama-3.2-3B (GoEmotions-LoRA, 20,000, one per sample; ARC-Easy-LoRA, 10,000 randomised
full-data runs; a retrieval set of 1,296 adapters over ARC-C, BoolQ, GSM8K, MBPP plus 600 few-shot queries). Unit:
per-module LoRA update, pooled into a whole-adapter embedding.

## How they did it
Canonicalisation: thin QR of B and A-transpose, form a small r x r core from the two R factors, take its SVD and
lift the singular vectors back; this gives the exact SVD of the update without forming it, and the singular
values and subspaces are provably invariant to the reparameterisation. Encoder: each rank component becomes a
token from its left/right singular vectors, modulated by its singular value (FiLM on log(1+sigma)); a rank-level
transformer mixes the r tokens per matrix, sigma-weighted pooling gives one token per position, a position-level
transformer with layer and module-type embeddings mixes positions, and attention pooling gives the adapter
embedding (about 17.75M parameters). Tasks: predict training-data attributes with a linear head, regress ARC-Easy
accuracy, retrieve adapters by task with an encoder trained on ARC-Easy only, and transfer from SD1.4 to SD1.5
adapters zero-shot. Splits 8:1:1, five runs.

## What counts as an explanation here
A learned embedding that predicts coarse properties of the adapter (attributes, accuracy, task identity). No
mechanism; the "reading" is a trained predictor.

## How they judged success
Macro-F1, Micro-F1, AUROC for attributes; MAE, RMSE, Pearson, Spearman for accuracy; NDCG@10 (and Hit@1) for
retrieval. Baselines: GLNet (equivariant), MLP, CNN, ViT on raw factors, and training-free raw-weight cosine for
retrieval. Ablations remove canonicalisation and each transformer level; an invariance test applies random
reparameterisations and measures embedding drift.

## What they found
Accuracy regression on ARC-LoRA: Pearson 98.98 and MAE 0.32 vs GLNet 92.78 and 0.43. Attributes: CUB Macro-F1
18.34 vs 10.73 (GLNet); CelebA roughly tied (50.38 vs 48.61); GoEmotions low in absolute terms (Macro-F1 5.67).
Retrieval NDCG@10 average 65.71 vs 43.97 (GLNet) and 35.73 (raw cosine), though raw cosine wins on GSM8K. SD1.4 to
SD1.5 transfer reaches 48.06 vs an in-domain 50.24. Canonical SVD takes about 0.78 ms vs 73.17 ms for direct SVD.
Removing canonicalisation is the biggest loss, dropping performance close to raw-factor baselines; without it,
embeddings drift sharply under reparameterisation.

## Limits and open problems they name
Only single LoRAs on a fixed backbone and layout; no merged or multi-adapter cases; only discriminative tasks;
retrieval is a proxy with no retrieval-specific training; possible misuse for profiling third-party adapters.

## What we take from it
Canonicalise before you read: removing a known weight symmetry was the single largest gain, which is a cheap
design rule for any weight reader we build (permutation for MLP neurons/heads, GL(r) for low-rank factors). The
SVD view (singular values plus subspaces per module) is a natural unit for reading. The invariance test (apply a
random symmetry transform, measure output change) is a check our white-box model should pass too. Caveat:
predicting accuracy from weights is far coarser than predicting per-input behaviour.

## Tags
unit: weights
form: probe | other
method: weight-analysis | decomposition | other
eval: prediction/simulation | benchmark | ablation
goal: understanding | evaluation-of-methods
