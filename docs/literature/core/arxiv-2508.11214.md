# How Causal Abstraction Underpins Computational Explanation

- **Key:** arxiv-2508.11214
- **Authors / organisation:** Atticus Geiger, Jacqueline Harding, Thomas Icard (affiliations not listed on the pages read; published in a *Philosophy and the Mind Sciences* special issue)
- **Date:** 2025-08 (v2 dated 2026-07)
- **Link:** https://arxiv.org/abs/2508.11214
- **Kind:** essay
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
The paper asks what it means for a physical system, such as a neural network, to implement an algorithm over internal
representations, an old question in philosophy of computation that MI now faces in practice. The authors give a
precise causal answer based on causal abstraction, ask how representational content follows from it, and argue that
implementation alone is not enough for explanation: a good explanation must also support prediction and
generalization. It is the theoretical grounding for the causal-abstraction standard of interpretability.

## What they studied
Formal causal models rather than new experiments. Worked examples: a small ReLU network that computes XNOR, and
networks trained on a hierarchical equality (same/different) task, drawing on earlier results by the authors and
others (distributed alignment search, Huang et al. 2025 on out-of-distribution prediction, Sutter et al. 2025 on
triviality).

## How they did it
They define causal models (variables, value sets, mechanisms), interventions and an intervention algebra, and an
exact transformation between a low-level and a high-level model: maps on states and on interventions such that
intervening below and then mapping gives the same result as mapping and then intervening above. A constructive
abstraction groups low-level variables into high-level ones. Implementation is defined as abstraction-under-
translation: the high-level algorithm must be a constructive abstraction of some bijective re-description
(translation) of the network's variables, e.g. a rotation of a hidden layer. Interchange interventions (activation
patching) are the test. They then discuss representation (Harding's conditions: carries information, is used, can
misrepresent), the triviality problem, and generalization.

## What counts as an explanation here
A high-level causal model (an algorithm) plus an alignment showing the network implements it under interventions.
The aim is exact or approximate agreement on all interventions, so in principle complete for the modelled behaviour.
Beyond implementation, the authors require the explanation to predict behaviour off-distribution and under further
training.

## How they judged success
Conceptually: exact transformation (commuting of interventions), measured empirically by interchange-intervention
accuracy in cited work. They add generalization and prediction (out-of-distribution, after fine-tuning) as further
criteria for an explanation to be good.

## What they found
The hierarchical equality network implements the XNOR-style algorithm only after a rotation of a hidden layer, so a
translation is needed. If translations are unrestricted, every network implements every algorithm (Sutter et al.),
so constraints on admissible translations are needed; the witnessing translations there are contrived and hard to
learn. Linear localization of causal variables predicted out-of-distribution behaviour in a number-comparison task
(Huang et al.). Representational claims depend on the chosen abstraction. Compressive, simple algorithms are argued
to generalize better; localization fit to narrow data can overfit.

## Limits and open problems they name
Which translation classes are principled (linear vs nonlinear); how to keep explanations valid out of distribution
and under learning; when an approximate but simpler abstraction beats a precise but opaque one; how much content
causal role alone fixes.

## What we take from it
Central framing and measure. Our white-box model is a high-level causal model; its claim to explain the network
should be tested by interchange interventions, and its value by predicting behaviour off-distribution and after
fine-tuning, which is exactly the "predictive" bar we want. Warning: we must fix and justify a restricted class of
maps (e.g. linear) between weights/activations and our model's variables, or the claim becomes trivial.

## Tags
unit: whole-model | direction
form: causal-abstraction
method: patching | other
eval: patching | prediction/simulation | faithfulness
goal: understanding | science
