# Transcoders Beat Sparse Autoencoders for Interpretability

- **Key:** arxiv-2501.18823
- **Authors / organisation:** Gonçalo Paulo, Stepan Shabalin, Nora Belrose; EleutherAI
- **Date:** 2025-01
- **Link:** https://arxiv.org/abs/2501.18823
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
SAEs compress activations but say nothing about what a component computes. Transcoders instead learn a sparse approximation of a component's input-to-output function, which is closer to a replacement for the component. The authors ask whether transcoders give a better trade-off between interpretability and reconstruction than SAEs, and introduce a "skip transcoder" that adds a linear bypass to cut reconstruction error. The larger goal is choosing the right sparse unit for circuit-level understanding.

## What they studied
Pythia-160M (layers 0–10), Pythia-410M, Llama 3.2 1B, Gemma 2 2B. Unit: latents of sparse coders on MLP (feed-forward) layers. Training data: 8B tokens from the Pile (Pythia) or RedPajama v2 (others).

## How they did it
Three coder types trained per MLP: an SAE on the MLP output, a standard transcoder (MLP input → MLP output through a TopK bottleneck), and a skip transcoder f(x) = W2·TopK(W1x + b1) + W_skip·x + b2, initialised as a constant function. All use plain MSE with TopK sparsity (k = 32, 64, 128), no auxiliary losses, Adam, 2049-token sequences. Each coder is patched into the model in place of the MLP output to measure loss increase. Latents are explained by an LLM (Llama 3.1 70B) from 40 activating examples across ten activation quantiles, and the explanation is then scored by the same LLM. They also run SAEBench (variance explained, sparse probing, feature absorption) on Gemma and Llama.

## What counts as an explanation here
A dictionary of sparse latents, each with a natural-language description, which together approximate the MLP's function (for transcoders) or its output (for SAEs). Partial: the skip connection and residual error remain unexplained.

## How they judged success
Automated interpretability: fuzzing and detection scores on 50 activating + 50 non-activating examples (~500 latents per configuration), simulation scores (Bills et al.) on 50 latents. Reconstruction: cross-entropy loss increase when patched in (0.5M OpenWebText tokens). SAEBench variance explained, sparse probing, absorption. Baselines are SAEs and plain transcoders at matched width and k.

## What they found
Skip transcoders are Pareto-better: more interpretable and lower loss increase. Examples: Pythia-160M (2^15, k=32) fuzzing 74.6 (SAE) vs 86.4 (skip), detection 70.2 vs 80.9, CE increase 1.10 vs 0.73; Gemma-2-2B (2^17, k=32) fuzzing 80.5 vs 84.6, CE increase 1.60 vs 0.53. Plain transcoders are also more interpretable than SAEs but reconstruct worse (CE increase 1.23 at k=32 on Pythia-160M). On Gemma, skip transcoders explain much more variance (e.g. 67.1% vs 16.5% at layer 10). Sparse probing is mixed; absorption is noisy and persists in transcoders.

## Limits and open problems they name
Transcoders need a specific component (usually the MLP), unlike residual-stream SAEs. Absorption is not fixed. Circuit analysis, steering and unlearning benchmarks not tested. The role of the skip connection (e.g. via SVD) is left open. Results lean on an LLM scorer.

## What we take from it
Unit choice for a predictive model: replace each MLP with a (skip) transcoder, since it models the component's function rather than its activations, and it is both more faithful and more interpretable. The linear skip term is a cheap, readable part of the replacement (it can be read straight from weights). Reuse their measurement pair: CE loss increase under patching plus fuzzing/detection scores. Warning: a large share of the function may sit in the unexplained linear skip path, which must be accounted for.

## Tags
unit: feature, layer
form: dictionary, replacement-model, description
method: transcoder, SAE
eval: prediction/simulation, faithfulness, benchmark
goal: understanding, evaluation-of-methods
