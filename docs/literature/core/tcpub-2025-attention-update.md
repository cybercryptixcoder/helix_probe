# Progress on Attention

- **Key:** tcpub-2025-attention-update
- **Authors / organisation:** Adam Jermyn, Jack Lindsey, Rodrigo Luger, Nick Turner, Trenton Bricken, Adam Pearce, Callum McDougall, Ben Thompson, Jeff Wu, Joshua Batson, Kelley Rivoire, Christopher Olah (ed. Jack Lindsey); Anthropic
- **Date:** 2025-04 (per scout; the page itself shows no date, and cites 2025 work)
- **Link:** https://transformer-circuits.pub/2025/attention-update/index.html
- **Kind:** blog/research post (preliminary update)
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Feature-level circuit methods handle MLPs well but leave attention largely opaque: attribution graphs freeze attention
patterns. The team wants a feature-level account of how attention moves information, broken into sub-questions: is
there superposition across heads, are the "where to move" (QK) and "what to move" (OV) conditions coupled, how many
dimensions do OV/QK use, do attention representations span layers, and how do attention patterns form. They name
attention-pattern formation as the core unsolved problem.

## What they studied
Mostly an 18-layer Anthropic model; attention layers and heads, with features defined over heads and token positions.

## How they did it
They tried several dictionary-style replacements for attention. (1) An attention replacement layer: a wide, low-rank
attention layer trained to mimic a real one with a nuclear-norm-like penalty. (2) Multitoken transcoders (MTCs, 100k
features): each feature has a learned mix of head attention patterns, reads at source positions and writes at the
destination. They restricted MTC features to single heads to test head superposition, compared MTCs with SAE
features routed through single heads and with a jointly trained SAE/MTC to test QK/OV coupling, and clustered
head-loading vectors to probe OV dimensionality. (3) Attention value SAEs spanning two layers (4 and 10) vs
single-layer ones. (4) Attention-output SAEs (including a cross-layer variant) plugged into attribution graphs.
(5) QK diagonalisation: separate encoders for queries and keys whose matched features produce attention scores.

## What counts as an explanation here
A dictionary of attention features (each with a head mixture, a source-to-destination movement and a readable
pattern), intended to slot into replacement models and attribution graphs. Partial and exploratory.

## How they judged success
Normalized MSE and L0 (including L0 at matched MSE), cluster-size distributions, ablation effects on MSE, and
qualitative interpretability. No behavioural benchmark.

## What they found
MTCs give many features with clean attention patterns; induction features cluster by head loading. Forcing features
onto one head cost roughly 2-4x L0 at matched MSE and reduced interpretability: moderate evidence for attention
superposition across heads. Weak evidence that QK and OV conditions are coupled. OV dimensionality forms a smooth
power-law continuum rather than discrete classes. Two-layer attention value SAEs needed about half the L0 at fixed
MSE (or about 0.3 better normalized MSE at fixed L0): cross-layer attention structure exists. Attention-output SAEs
help attribution graphs moderately but lack head assignments. Rank-1 QK diagonalisation reconstructed poorly (could
not get near 0.25 normalized MSE at reasonable L0; ~1,000 induction features did most of the work); the attention
replacement layer was hard to optimise.

## Limits and open problems they name
Why models attend where they do remains the biggest gap; whether to extend MTCs into multitoken cross-layer
transcoders replacing CLTs; whether MTCs should replace attention-output SAEs in circuit analysis; higher-rank QK
features; revisiting attention replacement layers.

## What we take from it
(1) Warning: attention is in superposition across heads and across layers, so a white-box model that assigns one
function per head will be wrong; units should be features spanning heads. (2) QK is the hard part; any predictive
model must say why the network attends where it does, and rank-1 QK features are not enough. (3) Measure: L0 at
matched MSE as a clean way to compare structural hypotheses (e.g., single-head vs multi-head features).

## Tags
unit: head, feature, layer
form: dictionary, replacement-model
method: decomposition, transcoder, SAE
eval: other (MSE/L0), human-rating
goal: understanding, science
