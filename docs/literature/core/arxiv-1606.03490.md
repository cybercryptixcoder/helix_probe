# The Mythos of Model Interpretability

- **Key:** arxiv-1606.03490
- **Authors / organisation:** Zachary C. Lipton; University of California, San Diego
- **Date:** 2016-06
- **Link:** https://arxiv.org/abs/1606.03490
- **Kind:** essay
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Lipton argues that "interpretability" is used as if it were one well-defined property when it is not, and that papers routinely claim interpretability without saying what they mean. He wants to separate the different reasons people ask for interpretability and the different properties that could satisfy them, so that claims become precise and testable. The motivation is that interpretability is demanded precisely when real objectives (trust, fairness, robustness) are not captured by test accuracy, so vague notions cannot do the job. It was presented at the 2016 ICML Workshop on Human Interpretability in ML.

## What they studied
Conceptual analysis of supervised learning models and the interpretability literature (linear models, decision trees, deep nets, saliency, LIME-style local models, t-SNE, activation maximisation, case-based explanation). No experiments.

## How they did it
Two taxonomies. First, desiderata (why people want interpretability): trust, causality (generating testable hypotheses), transferability (behaviour under distribution shift or adversarial pressure, e.g. the pneumonia-asthma case), informativeness to decision-makers, and fair/ethical decision-making (including a right to explanation). Second, properties of models. Transparency: simulatability (a person can hold and step through the whole model), decomposability (each input, parameter and computation has an intuitive meaning), algorithmic transparency (the learning procedure is understood, e.g. convexity guarantees). Post-hoc interpretability: text explanations, visualisation, local explanations, explanation by example. He then uses the taxonomies to examine common claims.

## What counts as an explanation here
Two different things: transparency of the model itself (at the level of whole model, components, or training algorithm) versus post-hoc artefacts that describe the model without revealing its mechanism. Neither is privileged in general; which matters depends on the desideratum.

## How they judged success
No metrics. Argues that any interpretability claim must name the notion meant and give evidence for it.

## What they found
Linear models are not strictly more interpretable than deep nets: they win on algorithmic transparency but can lose simulatability and decomposability when large or built on engineered features. Transparency demands can conflict with predictive performance and should be justified. Post-hoc explanations can mislead, especially when optimised to look plausible. Better algorithms cannot fix a badly posed problem formulation.

## Limits and open problems they name
Need for richer objectives and metrics that capture the real goals; extending the analysis beyond supervised learning (e.g. RL); interpretability alone will not solve fairness.

## What we take from it
- Vocabulary: our target is transparency of the decomposability kind, and a white-box model that a reader (or program) can execute is literally simulatability; we should say which notion we claim.
- Warning: an explanation optimised to look plausible can mislead; our reconstruction should be judged by prediction, not by how sensible it reads.
- Desideratum "transferability" maps onto our test of prediction under intervention and distribution shift.

## Tags
unit: whole-model
form: description | replacement-model
method: other
eval: prediction/simulation
goal: understanding | evaluation-of-methods
