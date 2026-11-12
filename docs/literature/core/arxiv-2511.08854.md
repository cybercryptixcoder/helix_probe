# Decomposition of Small Transformer Models

- **Key:** arxiv-2511.08854
- **Authors / organisation:** Casper L. Christensen, Logan Riggs Smith; independent researchers (Christensen funded by Pivotal fellowship). NeurIPS 2025 Mechanistic Interpretability Workshop.
- **Date:** 2025-11 (v2 dated 2025-12-09)
- **Link:** https://arxiv.org/abs/2511.08854
- **Kind:** paper
- **Read from:** full text (main sections; later appendix pages not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Activation-space dictionaries (SAEs) suffer from feature geometry, absorption and splitting problems, so the authors want to decompose the parameters themselves into mechanisms. Stochastic Parameter Decomposition (SPD) had mostly been shown on toy MLP models; this paper extends it to transformers, where the importance of a weight slice must depend on context across sequence positions. The aim is to show parameter decomposition can recover known mechanisms in a toy transformer and find small, interpretable, fact-specific mechanisms in a real model.

## What they studied
(1) A 2-layer, one-head-per-layer, attention-only transformer (d_model 16, vocab 128, sequence length 64) trained on a synthetic task that requires an induction head. (2) GPT-2 small, with analysis concentrated on layer-0 MLP subcomponents. Unit: rank-1 subcomponents of weight matrices (Q, K, V, O, MLP).

## How they did it
Each weight matrix is written as a sum of C rank-1 subcomponents. For each input, a small network predicts each subcomponent's causal importance (how much it can be ablated without changing output). During training subcomponents are randomly masked with a coefficient drawn between their importance and 1, and the masked model must still match the original. The paper's key change: causal importance is computed by a tiny one-layer, one-head attention network across positions (with positional biases), so importance can differ for the same token in different contexts. The loss combines faithfulness (subcomponents sum to the original weights), a minimality penalty on importances, and KL-based stochastic and deterministic reconstruction losses at whole-model and per-layer level (randomly subsetted layers for GPT-2). For GPT-2 they decomposed using only two prompts the model completes correctly (two athlete-to-sport facts), then tested suppression of the found subcomponents on a 100-example synthetic fact set. A greedy SVD low-rank approximation served as baseline.

## What counts as an explanation here
A sparse set of rank-1 weight slices active on a given input, each of which can be interpreted (e.g. "K0 aligns token n with the position of n+1", "these layer-0 MLP slices encode Kobe Bryant"). Together the slices are a replacement for the weights that is faithful by construction. Partial: interpretation of each slice is manual and qualitative; prediction is via ablating slices.

## How they judged success
Faithfulness loss (weights reconstructed), stochastic and layer-wise reconstruction KL, attention-pattern KL per layer, number of active subcomponents per position/example, and targeted ablation/suppression effects on correct-answer probability, with off-target examples as controls. Baseline: greedy SVD approximation.

## What they found
- Toy model: faithfulness loss about 3e-9, reconstruction losses about 1e-4, attention KL 0.385 (layer 1), 0.002 (layer 2). SPD recovers the expected two-step induction mechanism; removing positional information before the first query projection drops the relevant attention from 1.0 to about 0.09. The value matrix needed more than rank 1 at the key position to identify one of 128 tokens.
- GPT-2: 96 active subcomponents across the two prompts, reported as a 99% size reduction (with a caveat that sparsity is not directly comparable to pruning). A few layer-0 MLP slices are specific to name tokens; suppressing them lowers the probability of the correct sport while mostly sparing unrelated facts. Suggests some fact storage as early as the first MLP, and asymmetric (reversal-curse-like) storage.

## Limits and open problems they name
Only small models; scalability unproven. Attention-based importance adds compute overhead at long sequences. Evaluation is qualitative and task-specific; benchmarks are needed. Ground truth is hard to establish even in toy transformers; faithfulness evidence is mainly ablations. Causal importance may handle feature interactions poorly. GPT-2 analysis is very narrow (two prompts plus 100 checks).

## What we take from it
A concrete recipe for a weight-space white-box model: decompose each matrix into rank-1 parts with input-dependent importance, trained so that ablating unimportant parts preserves output (KL). The faithfulness + minimality + stochastic-masking loss is a reusable training objective, and "attention-pattern KL" and targeted-suppression with off-target controls are reusable checks. Warning: decomposing on two prompts says little about general behaviour; we would need broad-distribution evaluation.

## Tags
unit: weights | head
form: replacement-model | other (rank-1 weight components)
method: decomposition | ablation | weight-analysis
eval: faithfulness | ablation
goal: understanding | science
