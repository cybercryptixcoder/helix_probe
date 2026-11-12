# Sparse Crosscoders for Cross-Layer Features and Model Diffing

- **Key:** tcpub-2024-crosscoders
- **Authors / organisation:** Jack Lindsey, Adly Templeton, Jonathan Marcus, Thomas Conerly, Joshua Batson, Christopher Olah; Anthropic (Transformer Circuits Thread)
- **Date:** 2024-10-25
- **Link:** https://transformer-circuits.pub/2024/crosscoders/index.html
- **Kind:** blog/research post (self-described preliminary research update)
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Per-layer sparse autoencoders treat each layer separately, but features are often smeared across several adjacent
layers (cross-layer superposition) or carried unchanged through the residual stream for many layers. That produces
duplicate features in every layer's dictionary and bloats circuit graphs with "persistence" edges. The authors
propose one sparse dictionary that reads from and writes to many layers at once, to get a less redundant
decomposition and simpler circuits. A second goal is model diffing: auditing a fine-tuned model as a diff against a
model already understood, on the hope that fine-tuning changes only a few features.

## What they studied
An unnamed 18-layer Anthropic transformer (cross-layer experiments); Claude 3 Sonnet versus its base model (diffing,
middle-layer residual stream, 1M-feature crosscoder); ten evenly spaced layers of three unnamed models of increasing
size (scaling diff). Unit: sparse features defined jointly over several layers or several models.

## How they did it
A crosscoder encodes a feature activation as a ReLU of the sum over layers of per-layer encoder projections, and
reconstructs each layer with its own decoder vector. The loss is summed reconstruction error plus a sparsity penalty
weighted by the sum (L1) of each feature's per-layer decoder norms, chosen so the loss is directly comparable to a
stack of per-layer SAEs (and because the L2 variant only found shared features in diffing). They define variants:
acausal (reads and writes all layers), weakly causal (reads one layer, writes it and later layers), strictly causal
(reads layer L, predicts MLP outputs at L and later; this is the cross-layer transcoder), windowed/convolutional, and
a pre/post-MLP crosscoder. They compared a global acausal crosscoder with 18 per-layer SAEs at matched total feature
count and at matched training FLOPs; inspected per-layer decoder-norm profiles and cosine similarity of decoder
directions across layers; and, for diffing, sorted features by the relative decoder norm in each model and
inspected model-exclusive ones. For the scaling study they ran NMF (4 components) on 30-dimensional decoder-norm
vectors (3 models x 10 layers).

## What counts as an explanation here
A dictionary of sparse features, each with a decoder footprint over layers (or over models). For diffing, the
explanation is the list of model-exclusive features and shared features whose direction changed. Partial; not a
predictive model of behaviour on its own, but the strictly causal variant is the building block for replacement
models.

## How they judged success
Eval loss (MSE plus decoder-norm-weighted L1, summed over layers); MSE vs L0 trade-off for reconstructing all layers;
training FLOPs; decoder-norm profiles and cross-layer cosine similarity; anecdotal interpretability of sampled
features (no systematic evaluation). Baseline: per-layer SAEs; windowed and causal variants as intermediates.

## What they found
At equal feature count crosscoders reach clearly lower eval loss than per-layer SAEs and give a much less redundant
whole-model MSE/L0 picture, but cost about 2x more FLOPs per unit of loss at large budgets. Most features peak in
one layer and decay; some span nearly all layers; decoder directions drift across layers more than pure residual
relay would predict. Windowed variants interpolate roughly linearly between SAE and global crosscoder; weakly
causal ones lag global crosscoders by 3-4x in dictionary size. Pre/post-MLP crosscoders show three groups (pre-only,
shared, newly computed post-MLP), with post-MLP features more abstract. In the Sonnet diff, about 4-5K features per
model were model-specific (e.g., refusal and code-review features only in the chat model; a role-play/character
feature in the base model), most of them not readily interpretable. The scaling diff found middle-layer components
separating the smallest model from the two larger ones.

## Limits and open problems they name
Preliminary rigour; cherry-picked diffing examples; compute cost; causal variants cannot model attention; error
terms needed for exactness may be uninterpretable; cross-layer features may encode correlations rather than the
model's actual mechanism (they flag mechanistic faithfulness as hard to even formalise); systematic
interpretability evaluation deferred.

## What we take from it
(1) Framing: a feature should be defined by where it is read and written across depth, not per layer; this cuts
redundant persistence structure out of any reconstruction we build. (2) The strictly causal crosscoder (CLT) is the
standard substrate for a replacement model. (3) Measure: compare dictionaries at matched feature count and matched
FLOPs on summed MSE vs L0; use L1-of-decoder-norms so cross-layer and per-layer losses are comparable. (4) Warning:
a crosscoder can fit correlations the network does not use, so reconstruction quality is not mechanism fidelity;
we need intervention-based checks. (5) Model diffing is a ready-made "predict what changed" test bed.

## Tags
unit: feature, layer
form: dictionary
method: decomposition, SAE, transcoder
eval: other (reconstruction MSE/L0, FLOPs), human-rating (anecdotal)
goal: understanding, safety/auditing
