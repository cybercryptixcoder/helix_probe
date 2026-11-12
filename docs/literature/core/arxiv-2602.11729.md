# Cross-Architecture Model Diffing with Crosscoders: Unsupervised Discovery of Differences Between LLMs

- **Key:** arxiv-2602.11729
- **Authors / organisation:** Thomas Jiralerspong (Mila / Anthropic Fellows Program), Trenton Bricken (Anthropic)
- **Date:** 2026-02-12 (arXiv); Anthropic blog post "A 'diff' tool for AI models" 2026-03-13
- **Link:** https://arxiv.org/abs/2602.11729 (blog: https://www.anthropic.com/research/diff-tool)
- **Kind:** paper
- **Read from:** full text (first ~40% of arXiv HTML: method, toy validation, main results, limitations) plus blog post
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Standard safety evaluations only catch risks someone thought to test for. Model diffing instead surfaces what differs between two models without a hypothesis. Crosscoder diffing had only been used for a base model versus its fine-tune; the authors want it to work across different architectures and training lineages, so that, e.g., a new model can be screened for unexpected behaviours relative to a known one. They argue standard crosscoders hide model-unique features by forcing them into shared ones, and propose an architecture to fix this.

## What they studied
Pairs of open-weight models: Llama-3.1-8B-Instruct vs. Qwen3-8B, and GPT-OSS-20B vs. DeepSeek-R1-0528-Qwen3-8B, using middle-layer residual activations (e.g. layer 12 of GPT-OSS, 16 of DeepSeek). Data: 100M token-aligned activation pairs from a 50/50 mix of FineWeb and LMSYS-Chat-1M. Unit: crosscoder features (shared vs. model-exclusive). Also a synthetic toy with known concepts.

## How they did it
They introduce the Dedicated Feature Crosscoder (DFC): the dictionary (131,072 features) is partitioned into model-A-only (5%), model-B-only (5%) and shared (90%) blocks; each model is reconstructed only from its own block plus the shared one, so exclusive features structurally cannot write to the other model. Training uses BatchTopK (k = 200, annealed from 1000), Adam, 100k steps. Different tokenizers are aligned by a greedy window-expansion on decoded text (~99% of sequences aligned). Baselines: a standard BatchTopK crosscoder (exclusivity judged post hoc by relative decoder norm) and the designated-shared-feature crosscoder. In a toy with 2,048 concepts in 256 dimensions (2.5% exclusive per model; model B an affine transform of A), they measure recovery of planted concepts. On real models, features are auto-explained and flagged by Claude 4.1 Opus, filtered by detection score ≥ 0.8, and candidates are validated by steering (adding the decoder vector scaled to the feature's max activation) and LLM-judge ratings over 30 prompts. An "exclusivity score" uses model stitching (an affine map between models) to steer the stitched feature in the other model and has a judge rate similarity.

## What counts as an explanation here
A list of model-exclusive features with natural-language labels, each validated as causally controlling a behaviour via steering. It is a screening tool for differences, not a mechanism.

## How they judged success
Toy: concept recovery rate (cosine > 0.8 to a planted concept), averaged over 5 seeds. Real: dead-feature fraction, detection score, fraction of variance explained (parity check against the standard crosscoder); exclusivity score 1–5 from stitching plus LLM judge; steering effect rated 1–5 by an LLM judge; reproducibility across seeds and partition sizes. Also transfer of persona steering vectors through the shared space as a sanity check.

## What they found
In the toy, DFC recalls exclusive concepts better than both baselines (especially when the dictionary is undercomplete) at the cost of more false positives; exclusive concepts are learned later than shared ones, and DFC shortens that delay. On real models DFC matches the standard crosscoder on quality (FVE 0.817 both; detection 87.78% vs 87.77%; dead 5.0% vs 5.6%), while its exclusive features score high on exclusivity where many standard-crosscoder "exclusive" features score 1. Found features: a Chinese-Communist-Party-alignment feature in Qwen3-8B and DeepSeek (suppressing it let Qwen discuss Tiananmen; amplifying produced pro-government statements), an American-exceptionalism feature in Llama, and ChatGPT-identity and copyright-refusal features in GPT-OSS-20B (amplifying caused over-refusal of a sandwich recipe). The CCP feature recurred in 5/5 runs; American exceptionalism in 4/5 (the paper is internally inconsistent on these counts).

## Limits and open problems they name
Exclusivity score is a proxy dependent on stitching, judge and prompts; more false positives; results depend on seed and partition size (1–3% partitions miss granular features); only two model pairs; base-vs-finetune tests showed "mirror features"; no claim about where exclusive features come from; exclusive representation does not mean the other model lacks the concept. Most exclusive features are not behaviourally meaningful, so it is a high-recall pre-screen. Not tested on frontier models.

## What we take from it
(1) A structural trick: if we want a dictionary to separate "what is common" from "what is specific", hard-partition the dictionary rather than infer exclusivity post hoc. (2) An evaluation pattern: planted-ground-truth toy plus steering validation plus seed-robustness. (3) Model stitching (affine map between models' residual spaces) as a way to compare two networks, useful if we ever compare our white-box surrogate to the original in representation space. (4) Warning: LLM-judge-based scores are proxies and need controls.

## Tags
unit: feature
form: dictionary | steering
method: SAE | steering | other (crosscoder, model stitching)
eval: benchmark | downstream-task | human-rating
goal: safety/auditing
