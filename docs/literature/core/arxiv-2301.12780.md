# Equivariant Architectures for Learning in Deep Weight Spaces (DWSNets)

- **Key:** arxiv-2301.12780
- **Authors / organisation:** Aviv Navon, Aviv Shamsian, Idan Achituve, Ethan Fetaya, Gal Chechik, Haggai Maron; Bar-Ilan University, Nvidia (ICML 2023)
- **Date:** 2023-01
- **Link:** https://arxiv.org/abs/2301.12780
- **Kind:** paper
- **Read from:** full text (HTML version, incl. appendix J/K summaries; some results only in figures)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors want neural networks that take other networks' weights as input. Weight spaces have a strong symmetry:
permuting hidden neurons of a layer (and the matching rows/columns of adjacent matrices) gives different weights for
the same function. A generic network on flattened weights ignores this and wastes capacity. They aim to derive the
right layer type for MLP weight spaces from first principles, so that tasks like classifying implicit neural
representations (INRs), editing them, or adapting pretrained networks can be learned efficiently.

## What they studied
MLP weight spaces (weights and biases of all layers) as input objects. Data: INRs fitted to sine waves, MNIST and
Fashion-MNIST INRs, CIFAR-10 classifiers for domain adaptation, and 200 Fashion-MNIST MLP classifiers (784-128-128-128-10)
with checkpoints for generalization prediction. Unit: individual weights and biases, organized by layer.

## How they did it
They characterize all linear (affine) maps on an MLP weight space that are equivariant to the hidden-neuron
permutation group, and all invariant linear maps. The weight space is split into weight and bias blocks; each block of
the equivariant layer is built from pooling, broadcasting and small fully connected operations (some reduce to known
set layers such as DeepSets). Layers are stacked with pointwise nonlinearities into DWSNets, ending in an invariant
head for prediction tasks. They prove DWSNets can approximate a forward pass of the input MLP and can approximate
Lipschitz functions of the function the input MLP represents. Empirically they compare against MLPs on flattened
weights, MLPs with permutation augmentation, MLPs on weights aligned with Git Re-Basin, the inr2vec architecture, and
a transformer from prior weight-space work, on regression, classification, self-supervised representation, domain
adaptation and generalization-prediction tasks.

## What counts as an explanation here
No explanation of the input network is produced; the output is a learned predictor or edit operator over weights.
The theoretical point that a weight-space network can simulate the input network's forward pass is the bridge to
reading function from weights.

## How they judged success
Test accuracy for INR classification; MSE for sine-frequency regression and self-supervised recovery of sine
amplitude/frequency with a linear head; target accuracy for domain adaptation; MSE on predicted test error for
generalization prediction (averaged over 3 seeds); comparisons across training-set sizes.

## What they found
- INR classification: 85.71% (MNIST) and 67.06% (Fashion-MNIST) versus 58.98% and 47.79% for the best baseline (MLP +
  alignment); 75.12% on Fashion-MNIST with ten INRs per image.
- Self-supervised sine parameters: MSE 1.39 versus 3.86 for inr2vec.
- Domain adaptation CIFAR-10 to CIFAR-10-Corrupted: 71.36% versus 67.66% (MLP + alignment) and 60.92% (no adaptation).
- Generalization prediction and sine regression: DWSNets best, numbers only in figures.

## Limits and open problems they name
Layers are tailored to one MLP architecture; training was hard on some tasks, probably for lack of a good
initialization; implementation is complex; scaling symmetries and heterogeneous input architectures are not handled.

## What we take from it
- **Method:** if we build a learned reader of weights, it should respect permutation symmetry by construction;
  this paper gives the full equivariant layer basis for MLPs.
- **Framing:** the forward-pass-simulation result suggests a weight reader can in principle predict per-input
  behaviour, which is our target, though nobody tests that here.
- **Warning:** heavy machinery, tied to fixed architectures; does not yet scale to transformers.

## Tags
unit: weights
form: other (learned weight-space predictor)
method: weight-analysis | other
eval: downstream-task | benchmark
goal: science
