# Self-Supervised Representation Learning on Neural Network Weights for Model Characteristic Prediction (Hyper-Representations)

- **Key:** arxiv-2110.15288
- **Authors / organisation:** Konstantin Schürholt, Dimche Kostadinov, Damian Borth; AIML Lab, University of St. Gallen
- **Date:** 2021-10 (NeurIPS 2021)
- **Link:** https://arxiv.org/abs/2110.15288
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The question is whether a general-purpose embedding of a network's weights can be learned without labels, so that many properties of a model (accuracy, generalisation gap, training stage, hyperparameters) can later be read off with a simple linear probe. Earlier weight-space work trained a separate supervised predictor per property. A task-agnostic "hyper-representation" would be a reusable lens on populations of trained models ("model zoos"), a step toward analysing and comparing models through their weights.

## What they studied
New model zoos of small networks: a 100-parameter MLP on a 4x4 Tetris-shape toy task (zoos varying only seed, or seed plus activation, init and learning rate), 2,464-parameter CNNs on MNIST and Fashion-MNIST (seed-only and hyperparameter zoos with fixed or random seeds), and the 4,970-parameter CNN zoos of Unterthiner et al. (MNIST, Fashion, CIFAR-10, SVHN; about 30,000 models each with 9 checkpoints). Unit: whole flattened weight vector (with neuron/kernel-level tokens).

## How they did it
They train an autoencoder over flattened weights. Encoders tested: a plain feed-forward net, and transformer encoders where each token is either a single weight or all incoming weights of one neuron/kernel; a learned compression token supplies the latent. Three weight-space augmentations: permutation of neurons in hidden layers (function-preserving, shown to preserve forward pass and gradients), random erasing of 3 to 30% of weights, and Gaussian noise (dropped as unreliable). Losses: reconstruction (MSE), contrastive (NT-Xent) between augmented views, a weighted mix of the two, and reconstruction plus positive-only cosine similarity. Splits are 70/15/15 with all checkpoints of one model kept in the same split. Afterwards, linear (Tikhonov-regularised) probes predict continuous targets and linear classifiers predict categorical ones from the frozen embedding. Out-of-distribution tests transfer embeddings across zoos.

## What counts as an explanation here
A learned low-dimensional embedding of the weights from which model properties are linearly decodable. It is a predictive summary of the model as a whole (its quality and training recipe), not a mechanistic account of how it computes.

## How they judged success
R^2 of linear probes for accuracy, generalisation gap, epoch, per-class F1, learning rate, L2, dropout, training fraction; accuracy for activation, optimiser, initialisation; Kendall's tau for out-of-distribution ranking; reconstruction R^2. Baselines: raw weights, PCA (linear, cosine, RBF), UMAP, and layer-wise weight statistics s(W) following Unterthiner et al. and Eilertsen et al. (arxiv-2002.05688).

## What they found
Attention encoders with neuron-level tokens and a compression token worked best and scaled; per-weight tokens ran out of memory. The mixed reconstruction-plus-contrastive loss gave the best downstream results; reconstruction alone probes poorly and contrastive alone cannot reconstruct. Without the permutation augmentation, test performance diverged early. On the Tetris seed zoo, hyper-representations reached R^2 of 97.0 (epoch), 90.2 (accuracy), 81.9 (generalisation gap) versus 96.4 / 86.9 / 81.0 for weight statistics and 55.4 / 49.1 / 43.9 for raw weights. Raw weights were best for predicting initialisation and optimiser on the large zoos. Zoo design matters: in seed-only zoos, simple weight statistics are highly predictive; fixed seeds create clusters that make categorical prediction easy.

## Limits and open problems they name
Memory and compute (zoos took 1 to 12 days; encoders up to 65M parameters); fixed, small architectures only; little intuition about good inductive biases for weights; best loss varied per zoo; weak out-of-distribution transfer in some cases (e.g. biased SVHN accuracy predictions); sparse checkpoints hurt epoch prediction; fixed seeds give shortcuts.

## What we take from it
Three reusable items. (1) Permutation augmentation is the key ingredient for any learned weight reader; build symmetry in or the reader overfits. (2) The weight-statistics baseline s(W) is strong; any weight-reading claim must beat it. (3) Zoo design can create shortcuts (shared seeds), so our evaluation zoos must randomise seeds and hold out recipes. Caution: predicting accuracy or hyperparameters is far from predicting input-level behaviour; this line of work tells us "how good / how trained", not "what it does on x".

## Tags
unit: weights, whole-model
form: probe
method: weight-analysis, probing, other
eval: downstream-task, benchmark
goal: science, evaluation-of-methods
