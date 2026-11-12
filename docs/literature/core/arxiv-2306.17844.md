# The Clock and the Pizza: Two Stories in Mechanistic Explanation of Neural Networks

- **Key:** arxiv-2306.17844
- **Authors / organisation:** Ziqian Zhong, Ziming Liu, Max Tegmark, Jacob Andreas; MIT
- **Date:** 2023-06
- **Link:** https://arxiv.org/abs/2306.17844
- **Kind:** paper
- **Read from:** full text (HTML v2, read in two parts)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Earlier work reverse-engineered one network trained on modular addition and found a "Clock" algorithm. The authors
ask whether networks trained on the same task reliably learn the same algorithm, or whether small architecture and
hyperparameter changes yield different ones. This matters because mechanistic explanations are usually built from
one model and assumed to generalise. The aim is to characterise the full space of algorithms a task admits and to
build tools that classify which one a given network uses.

## What they studied
Modular addition with p = 59. Model A: one-layer ReLU transformer with constant attention (effectively an MLP).
Model B: standard one-layer ReLU transformer. Sweeps over attention rate alpha (interpolating no attention to full
attention), width (log-uniform 32 to 512), and depth (1 to 4 layers). Units: embedding geometry (principal
components), logits, and gradients of the whole model.

## How they did it
They defined two algorithms. Clock: embeddings on a circle and the network adds angles, which needs multiplication
(supplied by attention). Pizza: the network averages the two embeddings, landing inside the circle, and classifies by
which slice the midpoint lies in, which needs only absolute-value-like operations (ReLU). They derived signatures
that tell them apart: gradient symmetricity (Pizza symmetric in the two inputs), distance irrelevance (Clock's
correct logits do not depend on a-b; Pizza's do), logit patterns depending on a+b versus a-b, circle isolation by
keeping only some principal components, and variance in logits explained by each algorithm's formula. They trained
many models across the sweeps, classified each automatically (thresholds such as symmetricity above 98% and distance
irrelevance below 0.6), and fit phase boundaries by logistic regression.

## What counts as an explanation here
A closed-form algorithm (Clock or Pizza, or hybrids and non-circular variants) with a formula for the logits, plus
diagnostic metrics that identify which algorithm a trained model implements. The formula is predictive of logits.
Explanations are explicitly per-model, not per-task.

## How they judged success
Fraction of logit variance explained by each algorithm's formula (about 99% for Pizza versus 75% for Clock on Model
A); gradient symmetricity (Model A 99.37%, Model B 33.36%); distance irrelevance (A 0.17, B 0.85; Pizza typically
0 to 0.4, Clock 0.4 to 1); accuracy after keeping only some circles (Model A 32.8% with one circle, 91.4% with three,
100% with six; Model B 100% with six components); circularity of the first four principal components (circular if
at least 99.5%).

## What they found
Both algorithms occur. Clock dominates at high attention rate and Pizza at low attention rate, with a sharp,
roughly linear phase boundary in attention rate and width; the transition point moves with width, which they explain
by linear layers becoming more dominant in wider models. Continuous transitions imply hybrid networks with some
components Clock-like and some Pizza-like. Networks ensemble several pizzas, including "accompanying" pizzas (alone
only 16.7% accurate vs 99.7% for the main three) that patch antipodal failures. Non-circular solutions (line-like,
Lissajous-like) also appear, more often in deeper models: circular fractions were 34.31% for 1-layer and about 6 to
12% for 2 to 4 layers.

## Limits and open problems they name
Only modular addition; scaling to real models needs much more work. Systematically discovering unfamiliar algorithms,
and disentangling algorithms implemented in parallel, remain open. Interpretability tools are dual-use.

## What we take from it
A central warning for us: two networks trained on the same task can compute it differently, so a white-box model must
be built from the specific network's weights, not from a task-level story. Their design pattern is reusable: define
candidate algorithms, derive cheap discriminating signatures (symmetry, logit dependence, variance explained), and
classify many trained networks automatically. Variance-in-logits explained is a simple predictive score for a formula-
form explanation. Expect ensembles and hybrids, not one clean algorithm.

## Tags
unit: whole-model | direction
form: program | description
method: decomposition | ablation | other
eval: prediction/simulation | ablation
goal: science | understanding
