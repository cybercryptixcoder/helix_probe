# Causal Abstraction: A Theoretical Foundation for Mechanistic Interpretability

- **Key:** arxiv-2301.04709
- **Authors / organisation:** Atticus Geiger, Duligur Ibeling, Amir Zur, Maheep Chaudhary, Sonakshi Chauhan, Jing Huang, Aryaman Arora, Zhengxuan Wu, Noah Goodman, Christopher Potts, Thomas Icard; mostly Stanford (Pr(Ai)²R Group)
- **Date:** 2023-01 (v1 2023-01-11; v4 2025-05-08, which is the version read)
- **Link:** https://arxiv.org/abs/2301.04709
- **Kind:** survey/agenda (theory paper)
- **Read from:** abstract and sections (the arXiv HTML read in parts: sections 2.1-2.7, 3.1-3.8 and conclusion; some proofs and parts of 2.5-2.6 skimmed)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Mechanistic interpretability lacked a shared definition of what it means for an explanation to be correct. The
authors propose causal abstraction as that definition: an explanation is a simpler causal model that faithfully
summarises the network's low-level causal mechanisms. They want a common language so that methods can be compared,
core concepts (polysemanticity, linear representations, features, faithfulness) can be stated precisely, and
"just-so" stories disconnected from model internals can be ruled out.

## What they studied
Theory, with worked examples rather than new experiments: a network implementing a hierarchical equality task
(handcrafted and trained), bubble sort as a cyclic causal model with infinitely many variables, small arithmetic
examples, and a CEBaB example for concept effects. Unit of analysis: any set of low-level variables (neurons,
subspaces, learned features) mapped to high-level variables.

## How they did it
1. Formalise causal models (variables, mechanisms) and interventions in increasing generality: hard (fix values),
   soft (replace mechanisms), and "interventionals" (functions that transform mechanisms), with intervention algebras
   as well-behaved classes.
2. Define exact transformation (the low-level mechanisms realise the high-level ones), bijective translation
   (a lossless change of basis), and constructive abstraction via an alignment: partition low-level variables into
   cells, one per high-level variable plus a forgotten cell, with value maps. Any alignment decomposes into
   marginalisation, variable merge and value merge.
3. Define approximate transformation: choose a similarity function, a distribution over interventions and a summary
   statistic; the expected similarity grades how well the abstraction holds.
4. Define interchange interventions (simple, recursive, distributed) and interchange intervention accuracy (IIA): the
   expected rate at which high- and low-level models give the same output under matched interchange interventions.
5. Recast existing methods as special cases (section 3).

## What counts as an explanation here
A high-level causal model plus an alignment to the network such that interventions on the network correspond to
interventions on the model. Graded, not binary: faithfulness is the degree of approximate abstraction. Explicitly
predictive: the explanation must reproduce the network's outputs under the intervention distribution.

## How they judged success
No empirical benchmark. Success measures defined: IIA, probability or logit difference, KL divergence, all cast as
instances of approximate transformation; for scrubbing-style tests, proportion of performance retained. Points to a
benchmark of feature-localisation methods built on distributed interchange interventions (Huang et al. 2024).

## What they found
Unification table: LIME fidelity and causal effect estimation as two-variable behavioural abstractions; integrated
gradients can compute interchange interventions with a suitable baseline; causal mediation as a three-variable chain;
path patching as recursive interchange intervention; concept erasure, sub-circuit analysis and causal scrubbing as a
three-variable collider with an ablation switch; PCA, SAEs, probes, differential binary masking and DAS as modular
feature learning through bijective (or, for SAEs with nonzero reconstruction error, approximate) translations;
steering fits only if interventions are defined as steering. Modular features are defined as variables forming an
intervention algebra under a bijective translation; the linear representation hypothesis is treated as one testable
choice of translation.

## Limits and open problems they name
Deterministic models only; general interventionals are too unconstrained without algebraic structure; abstraction
can create cycles; SAE reconstruction is never exact; probe success does not show causal role; steering moves
activations off distribution and may show how to control rather than how the network reasons; no state-of-the-art
model is designed around interpretability.

## What we take from it
The framing for our project: a white-box model of a network is a high-level causal model, and its correctness is an
approximate-abstraction score (IIA or KL under a stated intervention distribution). Choosing that distribution,
similarity function and statistic explicitly is how we make "predicts what the network does" a precise claim. It
also tells us how to position weight-derived reconstructions against patching, SAEs and DAS in a language reviewers
recognise.

## Tags
unit: whole-model, direction, feature
form: causal-abstraction
method: other
eval: faithfulness, prediction/simulation
goal: evaluation-of-methods, science
