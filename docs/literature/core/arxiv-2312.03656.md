# Interpretability Illusions in the Generalization of Simplified Models

- **Key:** arxiv-2312.03656
- **Authors / organisation:** Dan Friedman, Andrew Lampinen, Lucas Dixon, Danqi Chen, Asma Ghandeharioun; Princeton University, Google Research, Google DeepMind
- **Date:** 2023-12 (ICML 2024)
- **Link:** https://arxiv.org/abs/2312.03656
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Much interpretability replaces part of a model with a simpler proxy (a low-rank projection, a clustering of
activations) and then reasons about the proxy as if it were the model. That is only safe if the proxy stays faithful
on inputs it was not fitted on. The authors test whether simplifications fitted on training-distribution data still
match the original model out of distribution, i.e. whether a simplified model predicts how the real model
generalises.

## What they studied
Small transformers: two-layer, one-head-per-layer models (hidden size 32) trained on Dyck-(20,10) bracket matching;
four-layer, four-head character-level models (width 256) trained on Java functions from CodeSearchNet with bracket
depth at most 3; and SCAN models in an appendix. Unit: individual attention heads' keys and queries.

## How they did it
Train each model on in-distribution data, then simplify one component at a time. Data-dependent simplifications:
project keys and queries onto the top-k singular directions (SVD/PCA fitted on 1,000 training sequences), or replace
them with the nearest of k-means centroids. Data-independent simplification: replace softmax attention with one-hot
attention to the top-scoring key. Compare the simplified and original models on held-out in-distribution data and on
systematic OOD splits: Dyck with seen structures but new bracket types, unseen structures (short and long), and unseen
depth; code with unseen nesting depth and unseen languages (JavaScript, Go, PHP). Errors are broken down by depth and
by prediction type (repeated words, closing brackets, whitespace, keywords).

## What counts as an explanation here
A simplified model (low-dimensional or discretised component) offered as a description of what a head computes; the
paper treats it as a candidate replacement model and asks whether it can stand in for the original on new inputs.

## How they judged success
Agreement between simplified and original models: Jensen-Shannon divergence of attention patterns, "same prediction"
rate at the output, accuracy on long-distance closing brackets (Dyck), and same-prediction rate on tokens the original
gets right (code), compared across in-distribution and OOD splits; paired t-tests for the code gap.

## What they found
On Dyck, keys and queries reduced to about four dimensions agree with the original almost perfectly in distribution,
but on unseen structures the original generalises nearly perfectly while the simplified model diverges, so the
simplification underestimates generalisation; a rank-8 SVD fails specifically at depths 11 and 12. One-hot attention
is faithful almost everywhere but slightly overestimates generalisation on deep nesting. On code, SVD agreement is
consistently lower on unseen languages than on Java (p <= 0.005), with the largest gaps on repeated-word (induction-
like) and closing-bracket predictions; one induction-like head falls to about 75% agreement in domain and about 61%
on unseen languages. SCAN shows no gap on one split and a small consistent gap on the length split. Data-dependent
simplifications capture coarse features (e.g. depth parity) but drop fine structure the model uses OOD.

## Limits and open problems they name
Small models and few tasks; only one component simplified at a time (whole-circuit simplification may show bigger
gaps). They suggest fitting simplifications on data that includes OOD features, but do not fully test it.

## What we take from it
A warning and a protocol. A replacement or white-box model that matches the network in distribution can still
mispredict on shifted inputs, in either direction. Our evaluation of a predictive model must include systematic OOD
splits (new structures, deeper nesting, new domains) and report agreement per split and per prediction type. It also
argues for weight-derived (data-independent) simplifications, since data-fitted ones inherit the training
distribution's blind spots, while noting data-independent ones can err too.

## Tags
unit: head
form: replacement-model
method: decomposition | ablation | other (SVD/clustering simplification)
eval: faithfulness | prediction/simulation
goal: evaluation-of-methods | understanding
