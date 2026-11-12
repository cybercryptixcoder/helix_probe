# Distributed Representations: Composition & Superposition

- **Key:** tcpub-2023-superposition-composition
- **Authors / organisation:** Chris Olah; Anthropic
- **Date:** 2023-05-04
- **Link:** https://transformer-circuits.pub/2023/superposition-composition/index.html
- **Kind:** essay
- **Read from:** full text (via a page-summarising fetch)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
People keep asking how superposition relates to the older idea of "distributed representations" from neuroscience
and connectionism. The note argues the older term lumps together two different strategies, composition and
superposition, which behave differently and pull against each other. Clarifying this sharpens what a "feature" is
supposed to be and why decomposing representations into independent parts matters for interpretability. It is an
informal note, not a full paper.

## What they studied
No model. Thought experiments with binary neurons encoding coloured shapes (adapted from Thorpe 1989), plus
references to Toy Models of Superposition and word-embedding directions (Mikolov 2013). Unit: features as directions
in activation space.

## How they did it
Conceptual argument. The author contrasts four codes for the same coloured-shape items: a local code (one neuron per
colour-shape pair), a compositional code (separate colour and shape neurons that combine), a maximally superposed
dense code (few neurons storing many unrelated items), and a mixed code where colours are superposed among
themselves, shapes among themselves, but colour and shape still compose. He then gives a volume argument: m bits give
roughly exp(m) states; fully composable features consume that volume so only about m of them fit, whereas
non-composing items can be packed in superposition up to roughly exp(m), at the cost of needing a nonlinearity to
read them out. Sparsity leaves "holes" in compositional space that superposition can fill, linked to compressed
sensing.

## What counts as an explanation here
A taxonomy of representational strategies, with features understood as directions (linear combinations of neurons).
It is a framing, not a predictive model.

## How they judged success
Not applicable; no empirical evaluation. Arguments are by construction and counting.

## What they found
Composition yields generalisation across combinations (data about green circles helps green squares) and supports
linear selection; superposition yields capacity for many unrelated items but makes linear selection and in-between
objects hard. Real networks plausibly mix the two. A successful linear probe for a property (e.g. "red" in a local
code) does not by itself show the network has a feature for it.

## Limits and open problems they name
Informal and unreviewed; the author says he may have missed prior literature. Binary neurons only; continuous case
left informal. How much real networks use each strategy is open. Generalisation claims are asserted, not tested.

## What we take from it
A framing for what units our white-box model should use: composing features (which generalise and support linear
read-out) versus superposed ones (which need nonlinear read-out). A warning that probe success is not evidence of a
feature, relevant if our pipeline relies on probing. The volume argument also predicts that weight-space structure
will be a mix of compositional (low-rank, reusable) and superposed (interference-prone) parts.

## Tags
unit: feature
form: description
method: other
eval: none (conceptual)
goal: science
