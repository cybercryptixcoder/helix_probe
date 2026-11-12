# Evaluating Explainable AI: Which Algorithmic Explanations Help Users Predict Model Behavior?

- **Key:** arxiv-2005.01831
- **Authors / organisation:** Peter Hase, Mohit Bansal; UNC Chapel Hill
- **Date:** 2020-05
- **Link:** https://arxiv.org/abs/2005.01831
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
They want a test of explanation quality that is not subjective: does an explanation make a person better at predicting what the model will do (simulatability)? Prior evaluations often relied on ratings or did not control for leakage, so it was unclear whether popular explanation methods actually transmit knowledge of model behaviour. This is a step toward rigorous, behaviour-grounded evaluation of explanations.

## What they studied
Two task models: a text sentiment classifier on movie reviews (10,662 reviews, about 81% accuracy) and a tabular classifier on UCI Adult income (15,682 records, about 83% accuracy). Explanation methods: LIME, Anchor, Decision Boundary (their adaptation of latent-space traversal to find a nearby input that flips the prediction), Prototype (their own case-based neural model explaining by the nearest learned prototype), and a Composite of all. Unit: whole-model input-output behaviour.

## How they did it
Human-subject simulation tests. Forward simulation: users see labelled examples, predict model outputs on test items, then study explained examples, then predict the same test items again; the pre/post difference isolates the explanation's effect. Counterfactual simulation: users predict how the model's output changes under a perturbation of an input, before and after seeing an explanation of the original input. Controls: explained items are separated from test items so explanations cannot leak the answer for the test item; an unexplained baseline condition; data balanced by whether the model was correct (so users cannot just predict the true label); users must predict every item. 32 trained undergraduates completed 39 user tests, about 2,166 responses analysed. They also collected 7-point subjective quality ratings and checked whether ratings predicted simulation accuracy.

## What counts as an explanation here
Local post-hoc explanations (feature importances, rules, counterfactual neighbours, prototypes). An explanation counts as good to the extent it improves a reader's ability to predict the model, including under counterfactual change.

## How they judged success
Change in human simulation accuracy (post minus pre) in forward and counterfactual tests, with confidence intervals and significance tests; versus a no-explanation baseline. Secondary: whether subjective ratings correlate with simulation correctness.

## What they found
- LIME improved forward simulation on the tabular task (about +11 points, p = .014), the only clear forward gain.
- Prototype improved counterfactual simulation in aggregate (about +9.5 points, p = .032), though the per-domain breakdown is less clear.
- Anchor, Decision Boundary and Composite gave no definitive improvement; Composite was rated highly but did not help.
- Subjective ratings did not predict whether users simulated correctly.
- Explanations failed when they did not separate necessary from sufficient factors or did not show how a counterfactual shares decision-relevant features with the original.

## Limits and open problems they name
Wide confidence intervals (null results may hide effects); memory load in forward tests; some text counterfactuals were off-distribution; coverage-based example selection for LIME/Anchor not tested.

## What we take from it
- Measure: simulatability (forward and counterfactual) is the direct ancestor of our goal. Our white-box model is a simulator that can be scored automatically: forward prediction accuracy on held-out inputs and counterfactual prediction under perturbation or internal intervention.
- Controls to copy: separate "explanation" data from test data (no leakage), balance by model correctness so predicting the true label is not rewarded, include a no-explanation/behaviour-only baseline (e.g. a surrogate trained on input-output pairs), report pre/post differences with CIs.
- Warning: subjective ratings are not evidence; do not use human impressions to validate the reconstruction.

## Tags
unit: whole-model
form: description | replacement-model
method: other
eval: prediction/simulation | human-rating | benchmark
goal: evaluation-of-methods
