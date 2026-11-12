# Privileged Bases in the Transformer Residual Stream

- **Key:** tcpub-2023-privileged-basis
- **Authors / organisation:** Nelson Elhage, Robert Lasenby, Christopher Olah; Anthropic
- **Date:** 2023-03-16
- **Link:** https://transformer-circuits.pub/2023/privileged-basis/index.html
- **Kind:** blog/research post
- **Read from:** full text (via a page-summarising fetch; plots not inspected directly)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
In principle the transformer residual stream has no preferred coordinate system: every layer reads and writes it
through arbitrary full-rank linear maps, so any rotation of the stream gives an equivalent model. Yet large models
are known to develop "outlier" coordinates (reported by Dettmers) that are many times larger than others and aligned
with the standard basis. The authors want to know why the basis becomes privileged, because whether individual
coordinates mean anything decides whether coordinate-level analysis of the residual stream is legitimate. They
explicitly leave aside what the outlier features represent.

## What they studied
An unnamed roughly 200M-parameter transformer trained with Anthropic's codebase (d_model = 1280), plus variants: one
with an RMSNorm-style normalisation, versions with weights rotated after training, and two versions trained with
fixed random rotations inserted into the residual stream. Unit of analysis: individual residual-stream coordinates
(and, for contrast, the basis just before the MLP up-projection).

## How they did it
They defined an outlier as a residual-stream value with absolute value above 6 and counted outlier dimensions over a
test batch of 128 sequences of 1024 tokens; they also used per-token kurtosis of the activation vector as a
basis-privilege statistic (about 3 for a random basis, higher if the basis is privileged). They then tested candidate
causes one by one. (1) LayerNorm: replaced with a normalisation that has no mean subtraction and a single scalar
scale, removing its basis dependence. (2) Floating-point precision in the forward pass: with the rotation-invariant
model, they rotated every weight matrix by a random orthonormal matrix and compared loss. (3) Training dynamics: they
trained models with fixed random rotations at residual reads/writes, either one shared rotation (computation in a
different basis from communication) or an independent rotation at every read/write. They compared loss curves,
kurtosis and outlier presence across conditions. Adam's per-coordinate normalisation is the remaining
basis-dependent operation they then point to.

## What counts as an explanation here
A causal attribution of a statistical property of representations (basis alignment) to a component of the training
setup, established by elimination via controlled architectural interventions. It is partial and provisional: a
mechanism (Adam) is inferred, not demonstrated.

## How they judged success
Outlier counts per layer, residual-stream kurtosis versus the Gaussian value of 3, and test loss (baseline about 3.02
nats) compared against seed-to-seed variation. Controls: random fixed rotation as a reference showing kurtosis drops
to about 3; matched training runs differing only in the rotation scheme.

## What they found
A typical layer had 20 to 60 outlier dimensions out of 1280, rising with depth. Removing LayerNorm's basis dependence
did not remove outliers (tails were, if anything, heavier). Rotating trained weights changed loss by less than seed
noise, so precision is unlikely to be the cause. Rotation-trained models matched baseline loss after about a billion
tokens and had residual kurtosis near 3, but in the shared-rotation model the heavy tails reappeared inside the
computation basis before the MLP. The authors conclude the outliers arise from computation inside layers and become
basis-aligned when all layers share one basis, with Adam the most likely driver.

## Limits and open problems they name
Attribution to Adam is not proven; an unknown mechanism could be involved. Kurtosis of 3 does not prove an
unprivileged basis (Gaussian features would also give 3). One model size, one optimiser. Open: training with SGD or
a basis-independent optimiser; storing Adam's moments in a different basis; what the outlier features encode.

## What we take from it
A warning and a check: before reading meaning into individual coordinates or weight entries, test whether the basis
is privileged (kurtosis versus a random rotation is a cheap test). Any weight-reading method we build should be
either rotation-invariant or explicitly justify why a basis matters, and should be aware that optimiser artefacts
(Adam) can create basis structure that is not about the task. The rotated-training trick is a reusable control.

## Tags
unit: layer
form: description
method: other
eval: ablation
goal: science
