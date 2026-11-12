# When Models Manipulate Manifolds: The Geometry of a Counting Task

- **Key:** arxiv-2601.04480
- **Authors / organisation:** Wes Gurnee, Emmanuel Ameisen, Isaac Kauvar, Julius Tarng, Adam Pearce, Chris Olah, Joshua Batson; Anthropic
- **Date:** 2025-10-21 (Transformer Circuits); arXiv v1 2026-01-08
- **Link:** https://transformer-circuits.pub/2025/linebreaks/index.html (arXiv: https://arxiv.org/abs/2601.04480)
- **Kind:** paper (Transformer Circuits Thread)
- **Read from:** full text (Transformer Circuits page)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors want a complete mechanistic account of a natural behaviour in a production model: deciding when to break a line in fixed-width text. Doing this requires counting characters in the current line, inferring the line width from earlier lines, and checking whether the next word fits. The task is a test case for how models represent and compute with continuous scalar quantities. A broader aim is to test whether the discrete "feature" picture from sparse dictionaries is the right description, or whether geometric objects (manifolds) are the more natural unit.

## What they studied
Claude 3.5 Haiku (with transcoder attribution graphs also shared for Gemma 2 2B and Qwen 3 4B). Data: synthetic prose with newlines stripped and reinserted at word boundaries for line widths 15–150. Units: crosscoder features (from a 10M-feature weakly causal crosscoder), residual-stream subspaces, attention heads (QK and OV), and low-dimensional manifolds.

## How they did it
They started from attribution graphs (with QK attributions) to find the feature pathway from the current-line character count to the newline logit. They then studied the count representation in several ways: linear regression probe, 150-way logistic probes, PCA of mean activations per count, and the tiling of ~10 count features. They analysed "boundary" attention heads by projecting count and line-width representations through each head's QK matrix. They traced how layer-0 heads build the count (using the previous newline as an attention sink, then spreading attention over a fixed receptive field) and measured how much a set of heads explains the count. Causal tests: zero-ablating the count subspace, patching the count subspace at a specific prompt to move the predicted break, and "visual illusions" where inserted character pairs (e.g. "@@") hijack counting heads. A simple particle-on-a-hypersphere simulation was used to reproduce the observed rippled geometry.

## What counts as an explanation here
A mechanism stated geometrically: a 1-D curved manifold in a ~6-D subspace for the count, attention heads whose QK matrices rotate one manifold onto another to compute a difference, and a separating hyperplane for the final decision. Features are treated as local coordinates on the manifold; the authors argue features and manifold are dual descriptions of one object. Explanation is near-complete for the main path and makes testable predictions (where breaks occur under patching; which inserted tokens should cause illusions).

## How they judged success
Probe R² (count probe R² = 0.985 after layer 1; probe RMSE 5); variance explained by top PCs; R² of the count reconstructed from subsets of heads; cosine similarity of representations before vs. after QK transformation; AUC of the fit/no-fit hyperplane on real data; loss change under subspace zero-ablation (only hurts where the next token is a newline); behaviour change under subspace patching; newline probability under 180 inserted character pairs; evaluation of Haiku on 200 prose sequences at widths 20–140.

## What they found
The count lives on a curved 1-D manifold; the top 6 PCs capture 95% of variance, and a rank-6 subspace suffices for patching. Feature receptive fields widen with count, and similarities show "ringing" (positive, then negative, then positive again with distance), which the simulation reproduces as an efficient packing of a scalar. Boundary heads' QK matrices align count i with width i+offset: probe cosine is ~0.25 in the residual stream but ~1 in QK space; several heads with different offsets tile "characters remaining". Characters-remaining and next-word length sit in near-orthogonal subspaces so a hyperplane decides the break (AUC 0.91). Five layer-0 heads reconstruct the count with R² 0.93 (11 heads in two layers: 0.97); attention contributes about four times more than MLPs. Inserting certain tokens distracts counting heads and can suppress the newline prediction.

## Limits and open problems they name
How line width is aggregated across earlier lines is unresolved; uncertainty, variable widths, multi-token words and special formats not studied; the break analysis uses the true next token. A probe-first approach initially failed and features were needed to find the mechanism. Automated manifold discovery and better automatic feature labelling are needed; features impose a "complexity tax" that a manifold parametrisation could remove.

## What we take from it
(1) A framing: scalar variables may be stored as curved low-dimensional manifolds, so a white-box model built from discrete features may be needlessly complex; we should allow manifold/subspace variables. (2) A weight-reading method: reading QK matrices as maps that rotate one representation onto another, checked by cosine similarity in QK space, is exactly the kind of weights-to-algorithm reading we want. (3) A validation pattern: predict behaviour from the mechanism (patch count, insert distractors) and confirm. (4) Evidence that probes alone can miss the mechanism.

## Tags
unit: feature | direction | head | circuit
form: graph | direction | other (manifold geometry)
method: attribution | probing | patching | ablation | weight-analysis | decomposition
eval: ablation | patching | prediction/simulation
goal: understanding | science
