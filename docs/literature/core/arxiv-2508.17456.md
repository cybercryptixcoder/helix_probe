# Adversarial Examples Are Not Bugs, They Are Superposition

- **Key:** arxiv-2508.17456
- **Authors / organisation:** Liv Gorton, Owen Lewis; Goodfire
- **Date:** 2025-08 (revised 2025-09-15 to fix a Figure 6 plotting bug)
- **Link:** https://arxiv.org/abs/2508.17456 (blog: https://www.goodfire.com/research/adversarial-examples-are-not-bugs-they-are-superposition)
- **Kind:** paper
- **Read from:** full text (arXiv HTML, via summarised fetch)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Adversarial examples have long resisted a unifying explanation. The authors argue superposition (more features than
dimensions, with interference between them) is at least a partial and possibly the main cause: an attacker can push on
many interfering features at once. The broader aim is to show that a mechanistic concept from interpretability can
explain a classic, otherwise puzzling deep-learning phenomenon, and to test the link in both causal directions.

## What they studied
Toy models in the Elhage et al. style: 100 sparse features compressed into 20 hidden dimensions and reconstructed
through a ReLU, trained with MSE. Real models: ImageNet ResNet18s from Salman et al. (2020) adversarially trained at L2
budgets 0, 1, 3, 5. Units: feature directions (toy weights), SAE latents on the four residual stages (real models).

## How they did it
In the toy, superposition is measured as features per dimension, the squared Frobenius norm of W over the number of
dimensions; vulnerability is the loss increase under an L2 attack with budget 10% of mean input norm (noise plus one
gradient step), reported relative to a model without superposition. They (1) varied feature density from 1.0 to 0.1
across 30 models to change superposition, (2) related superposition to vulnerability, (3) adversarially trained
models (50/50 clean/adversarial, 150k steps) and measured how superposition changed, and (4) drew pairwise
interference graphs to see which features attacks activate. In real ResNets, they trained L1-ReLU and TopK SAEs (8x
expansion) on each stage and used reconstruction error at fixed sparsity as a superposition proxy, then counted active
SAE latents (L0) on clean vs PGD/FGSM inputs.

## What counts as an explanation here
A mechanistic hypothesis tied to a measurable quantity: vulnerability is predicted by the degree and structure of
feature interference in the weights. Partial: offered as a cause, not a complete account.

## How they judged success
Correlation and controlled manipulation in toys (sparsity as the knob, both directions of causation tested via
adversarial training); in real models, SAE reconstruction error at matched sparsity and active-feature counts under
attack, compared across robustness levels.

## What they found
Sparser data gave more features per dimension, with phase transitions near 1.7 and 4, and more vulnerability (with a
dip at antipodal superposition). Adversarial training lowered superposition at the same sparsity, and robust models
were even more robust than their superposition level predicted, attributed to different interference structure;
non-robust toys had about twice the mean off-diagonal interference. In ResNets, more robust models had lower SAE
reconstruction error at fixed sparsity, and PGD raised active SAE latents at layer 4 to 2.8x clean (351 vs 126), while
FGSM stayed near baseline there.

## Limitations and open problems they name
Real-model evidence rests on an SAE proxy, not direct measurement; superposition could not be intervened on in real
models, so the reverse direction and the fraction of vulnerability explained are open; other causes likely contribute;
the toy attack is one-step; comparisons across sparsity shift the evaluation distribution; explanations of other
adversarial phenomena are argued, not tested.

## What we take from it
A weight-level quantity (features per dimension, off-diagonal interference of W^T W) that predicts a behavioural
property (attack sensitivity): exactly the kind of weights-to-behaviour prediction we want, at least in toys. Warning
for any white-box surrogate: if it drops interference terms it will be wrong precisely on adversarial or
off-distribution inputs, so these inputs are a natural stress test of faithfulness.

## Tags
unit: weights | feature
form: dictionary
method: weight-analysis | SAE | other
eval: prediction/simulation | downstream-task
goal: science | understanding
