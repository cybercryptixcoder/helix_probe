# Model Zoos: A Dataset of Diverse Populations of Neural Network Models

- **Key:** arxiv-2209.14764
- **Authors / organisation:** Konstantin Schürholt, Diyar Taskiran, Boris Knyazev, Xavier Giró-i-Nieto, Damian Borth; University of St.Gallen, Samsung SAIT AI Lab Montreal, Universitat Politècnica de Catalunya
- **Date:** 2022-09
- **Link:** https://arxiv.org/abs/2209.14764
- **Kind:** benchmark
- **Read from:** full text (HTML version)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Training the same architecture on the same data with different seeds or hyperparameters yields a population of
models; the authors argue the structure of such populations in weight space can reveal properties of individual
models and of training. Prior zoos were small, narrow, or one-off, so results across weight-space papers could not
be compared. They release a large, systematically generated, standardized collection of trained models plus first
benchmarks, as shared infrastructure for learning on weights.

## What they studied
27 zoos: 8 image datasets (MNIST, Fashion-MNIST, SVHN, USPS, CIFAR-10, STL-10, CIFAR-100, Tiny ImageNet) by 3
architectures (small CNN about 2.5-2.9k params, medium CNN about 10.9k params, ResNet-18 about 11.2M params) by 3
generation schemes. About 50k unique models, about 3.8M stored model states (training checkpoints plus
sparsified "twins" from variational dropout). Unit: whole weight vector and layer-wise statistics.

## How they did it
Each zoo fixes a dataset, an architecture and a hyperparameter space (seed, initializer, activation, dropout,
optimizer, learning rate, weight decay). Three schemes: a hyperparameter grid with random seeds per node, the same
grid with fixed seeds 1-10, and one fixed configuration over 1,000 seeds. Models train 50 epochs (60 for some
ResNets) with checkpoints, accuracy and loss stored every epoch; splits are 70/15/15 by whole training trajectory to
avoid leakage. Each model is also sparsified for 25 epochs. They characterize diversity via accuracy spread,
prediction agreement, CKA, weight-space distances and UMAP plots, and run baseline property-prediction tasks with
linear models on raw weights versus layer-wise weight statistics.

## What counts as an explanation here
None directly; this is a dataset. Implicitly, a model "property" (accuracy, generalization gap, epoch,
hyperparameters) recoverable from weights by a simple predictor is the unit of knowledge.

## How they judged success
Diversity statistics (accuracy spread, agreement, CKA, weight distances). For benchmarks: R-squared for continuous
targets (accuracy, generalization gap, epoch) and classification accuracy for categorical hyperparameters
(initializer, activation, optimizer), using linear probes on raw weights w versus statistics s(w).

## What they found
- Seed-only zoos have narrow accuracy spread and high, unimodal agreement/CKA; hyperparameter-varied zoos are much
  more diverse, with bimodal agreement.
- Seed variation alone barely moves models apart in weight space; hyperparameter variation does. Fixed-seed zoos
  cluster by initializer and activation.
- Accuracy and hyperparameters are well predicted, especially from s(w) (e.g. MNIST seed zoo accuracy R-squared
  92.3 from w, 98.7 from s(w)). Generalization gap and epoch are hard, often low or negative R-squared; raw weights
  fail in random-seed zoos.

## Limits and open problems they name
Only image classification and three architectures (two tiny); some hyperparameter combinations yield poor models
(diverging runs removed); benchmarks use only linear models; generalization-gap prediction is weak; sparsification
analysis is brief.

## What we take from it
- **Dataset:** a ready-made population of trained networks with checkpoints and metadata, useful if we need many
  networks with known ground truth to test a weights-to-behaviour reader.
- **Method:** split by training trajectory, not checkpoint, to avoid leakage.
- **Warning:** raw weights in random-seed populations are hard to read because of symmetries; statistics are
  robust but coarse. Seed diversity matters for whether a weight reader is learning function or initialization.
- **Gap:** targets are global scalars, not per-input behaviour.

## Tags
unit: weights | whole-model
form: probe
method: weight-analysis
eval: benchmark | prediction/simulation
goal: science | evaluation-of-methods
