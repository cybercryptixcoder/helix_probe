# Permutation Equivariant Neural Functionals

- **Key:** arxiv-2302.14040
- **Authors / organisation:** Allan Zhou, Kaien Yang, Kaylee Burns, Adriano Cardace, Yiding Jiang, Samuel Sokota, J. Zico Kolter, Chelsea Finn; Stanford, University of Bologna, CMU
- **Date:** 2023-02
- **Link:** https://arxiv.org/abs/2302.14040
- **Kind:** paper
- **Read from:** full text (HTML version)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
"Neural functionals" (NFNs) are networks whose inputs are other networks' weights, gradients or masks; uses include
learned optimizers, INR processing, network editing and policy evaluation. Because hidden neurons have no inherent
order, NFNs should be equivariant to neuron permutations. The authors build a general, parameter-shared equivariant
layer and show it beats non-equivariant approaches across several weight-space tasks. Developed concurrently with
DWSNets.

## What they studied
Weight spaces of feedforward MLPs and CNNs (conv filter dimensions folded into channels). Data: Small CNN Zoo
(CIFAR-10-GS, SVHN-GS), their own three-layer MLP zoo, INR datasets (MNIST, Fashion-MNIST, CIFAR-10, ShapeNet-10,
ScanNet-10), and lottery-ticket mask tasks on MNIST and CIFAR-10. Unit: individual weights indexed by layer and neuron.

## How they did it
They define NF-Layers: linear maps whose parameters are shared across orbits of the permutation group. Two variants:
HNP assumes only hidden neurons are permutable (correct but parameter-heavy, growing with input/output dimension
squared); NP assumes all neurons including inputs and outputs are permutable (cheaper) and breaks the excess symmetry
with positional input/output encodings. They also define invariant pooling layers and a pointwise ablation (NFN_PT)
that ignores weight interactions. NFNs are trained for (1) predicting CNN test accuracy, (2) classifying INRs, (3)
outputting sparsity masks to find winning tickets, and (4) editing INR weights to apply image transformations.
Baselines: STATNN (MLP on hand-crafted weight statistics, from the "Predicting accuracy from weights" line), MLPs on
flattened weights with and without permutation augmentation, inr2vec, and iterative magnitude pruning for masks.

## What counts as an explanation here
No explanation of the input network; the deliverable is an architecture class for learning functions of weights.
Predictions are scalars (accuracy), labels (INR class), masks or edited weights.

## How they judged success
Kendall's tau between predicted and true test accuracy; INR classification accuracy; test accuracy of networks
trained with predicted masks at 95% sparsity versus IMP and random masks; MSE between edited-INR output and target
image. Parameter counts compared across variants.

## What they found
- Generalization prediction (Kendall's tau): CIFAR-10-GS 0.934 (HNP) and 0.922 (NP) versus 0.915 for STATNN; SVHN-GS
  0.856 (NP) versus 0.843. On MLPs, 0.876 (HNP) versus 0.854. Margins over the statistics baseline are small.
- INR classification: large gains, e.g. Fashion-MNIST 75.6% versus 12.5% for an MLP; ShapeNet-10 88.7% versus 39.1%
  for inr2vec.
- Masks: close to IMP (MNIST 94.8-95.0% vs 96.2%), well above random; the pointwise variant behaves like magnitude
  pruning.
- INR editing: lower MSE than MLP baselines (e.g. Dilate-MNIST 0.068 vs 0.307).

## Limits and open problems they name
Large activations may hinder scaling; no ResNet or transformer support; conv-to-dense flattening transitions
unhandled; NP depends on IO encodings; HNP is parameter-prohibitive with many outputs.

## What we take from it
- **Warning/baseline:** for scalar properties like accuracy, equivariant weight readers beat hand-crafted
  statistics only marginally, so STATNN must be the baseline for any such claim.
- **Method:** NP/HNP parameter-sharing recipe for symmetry-respecting weight readers; the pointwise ablation is a
  good control for whether a reader uses weight interactions or just magnitudes.
- **Gap:** no per-input behaviour prediction; architecture-specific; not yet applied to transformers.

## Tags
unit: weights
form: other (learned weight-space predictor)
method: weight-analysis | other
eval: downstream-task | benchmark | prediction/simulation
goal: science
