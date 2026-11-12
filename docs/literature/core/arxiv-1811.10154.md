# Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead

- **Key:** arxiv-1811.10154
- **Authors / organisation:** Cynthia Rudin; Duke University
- **Date:** 2018-11
- **Link:** https://arxiv.org/abs/1811.10154
- **Kind:** essay
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Rudin argues that in high-stakes settings (criminal justice, healthcare, credit) people should stop building black boxes and explaining them afterwards, and instead build models that are interpretable by construction. Her motivation is that post-hoc explanations are approximations that must be wrong somewhere, can rely on different features than the model, and give false confidence. She attacks the belief that accuracy requires opacity, and proposes policy changes. A preliminary version appeared as a 2018 NeurIPS workshop paper.

## What they studied
Tabular high-stakes prediction (COMPAS recidivism, Broward County data, FICO credit, NYC power-grid maintenance), saliency maps on image classifiers, and interpretable model classes: optimal rule lists (CORELS), integer scoring systems (RiskSLIM), additive models, and prototype networks for vision.

## How they did it
Argument supported by case studies and prior results. She contrasts black-box-plus-explanation with interpretable models of comparable accuracy, poses interpretable learning as constrained optimisation (loss plus a penalty on model size, solved to optimality for rule lists by CORELS), and uses the Rashomon-set argument: with finite data many near-optimal models exist, so an interpretable one is likely among them.

## What counts as an explanation here
The model itself. An interpretable model whose computation is the explanation (a rule list, a points-based score, a prototype comparison), so explanation and model cannot diverge. Post-hoc explanations are, by definition, a second model that only approximates the first.

## How they judged success
Predictive accuracy of interpretable versus black-box models on the same data; examples of explanation failure (saliency maps identical across classes; an explanation model that uses race when the explained model may not). No new benchmark.

## What they found
- On structured data with meaningful features, simple models often match complex ones; in the NYC grid project algorithms differed by at most 1%, while improving the data gave bigger gains.
- A three-rule CORELS model using age and prior offences is about as accurate as COMPAS on the same data.
- A post-hoc explanation that agrees with the model 90% of the time is wrong 10% of the time, undermining trust in both.
- Saliency maps can highlight the same regions for different classes.
- COMPAS uses 130+ inputs; at a 1% per-entry error rate, more than half of forms would contain an error.
- The 2018 FICO Explainable ML Challenge showed no accuracy gap between interpretable and black-box models.
- Prototype networks roughly matched the accuracy of the black-box networks they derive from.

## Limits and open problems they name
Interpretable models need domain expertise and harder (often combinatorial) optimisation; business incentives favour proprietary black boxes; interpretable models for raw-feature domains such as vision are harder. Policy: require reporting of interpretable alternatives' accuracy, reconsider right-to-explanation rules, fund interpretable models as public goods.

## What we take from it
- Core warning for us: any white-box model of a black box is itself a surrogate; where it disagrees with the network, it is wrong about the network. Report the disagreement rate (fidelity), not just agreement, and characterise where it fails.
- Framing for the replacement-model debate: the strongest form of our goal is a reconstruction whose computation is faithful by construction (read from weights), not a fitted approximation of behaviour.
- The Rashomon argument hints that a simpler model with equivalent behaviour may exist; useful when arguing a compact reconstruction is plausible.

## Tags
unit: whole-model
form: replacement-model | program
method: training-interpretable | other
eval: downstream-task | faithfulness
goal: understanding | safety/auditing | evaluation-of-methods
