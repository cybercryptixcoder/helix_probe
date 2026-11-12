# Curve Detectors

- **Key:** distill-2020-circuits-curve-detectors
- **Authors / organisation:** Nick Cammarata, Gabriel Goh, Shan Carter, Ludwig Schubert, Michael Petrov, Chris Olah; OpenAI (Distill Circuits thread)
- **Date:** 2020-06-17
- **Link:** https://distill.pub/2020/circuits/curve-detectors/
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
There is disagreement over whether individual neurons in vision models are meaningful features or illusions of interpretation. The authors pick a case simple enough to settle it carefully: curve-detecting neurons a few layers from the input, whose ideal stimuli are easy to generate. They stack many independent lines of evidence to argue the neurons really detect curves, as a template for what proof that a feature is real should look like. This is the first of three articles (behaviour here; construction in Curve Circuits; universality across models).

## What they studied
InceptionV1 on ImageNet; curve neuron families in conv2d2 (11), 3a (11), 3b (10) and 4a (12), with most detail on neuron 3b:379. Unit: individual neurons and neuron families.

## How they did it
They combine seven-ish lines of evidence. (1) Feature visualisation with a diversity term, checking it still yields only curves. (2) Dataset examples across the activation range. (3) Attribution (weights times previous-layer activations) to see what excites or inhibits the neuron on an image. (4) Human labelling: one author labelled more than 800 images sampled in activation bins of 100 into curve / imperfect curve / unrelated / opposing curve, and they computed each group's share of the neuron's expected activation. (5) Joint tuning curves: rotating dataset examples in 1-degree steps over 360 degrees and recording each neuron's response. (6) Synthetic stimuli: rendered curves varying orientation, curvature, fill and colour, plus angles morphing into curves. (7) Circuit and downstream-use views, and prototype uses (curve extraction versus Canny edges, spline fitting, NMF segmentation).

## What counts as an explanation here
A feature claim: a neuron (and its family) is a curve detector with a specified orientation tuning, curvature tolerance and invariances, supported by convergent behavioural evidence. It is descriptive and partial, but parametric enough to predict responses to new synthetic stimuli (tuning curves).

## How they judged success
Convergence of independent tests: separation of human labels by activation bin; share of expected activation explained by curves and imperfect curves (a deliberately conservative measure, used instead of probability density because most activations are weak); smooth Gaussian-like orientation tuning; strength of response to synthetic curves relative to dataset activations; invariance to colour and texture. They explicitly skip precision-recall because of label noise and curve rarity.

## What they found
3b:379 has a pre-activation mean around -200 and fires on roughly 11% of dataset cases, with exponentially distributed activations. Labels separate cleanly by activation level; curves and imperfect curves account for 55% of the expected-value contribution, and many "unrelated" high-activation images contained subtle curves revealed by attribution. Tuning curves tile all orientations. Synthetic curves drive responses about 24 standard deviations above the average dataset activation, invariant to fill and colour, but responses are fragile to small orientation/curvature changes. Curve neurons also respond to perpendicular "combing", seen across several architectures. Earlier layers show 180-degree "echoes" that 3b removes; 4a contains more object-specific curve units (e.g. cup and pan rims).

## Limits and open problems they name
Single labeller; no precision-recall; fragility to small perturbations; unknown origin of combing; subjectivity of interpreting 4a units; only 10 neurons studied deeply.

## What we take from it
A checklist for validating any claimed feature in our white-box model: tuning curves on controlled synthetic inputs, activation-binned blind labelling, expected-value share instead of top-k examples, and invariance tests. Tuning curves are a concrete predictive target: a weight-derived model of a unit should reproduce them. Warning: an exponential activation distribution means top-activating examples hide most of a unit's behaviour.

## Tags
unit: neuron
form: description
method: attribution | other (synthetic stimuli, tuning curves, human labelling)
eval: human-rating | prediction/simulation
goal: understanding | science
