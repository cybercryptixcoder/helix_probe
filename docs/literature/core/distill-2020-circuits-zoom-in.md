# Zoom In: An Introduction to Circuits

- **Key:** distill-2020-circuits-zoom-in
- **Authors / organisation:** Chris Olah, Nick Cammarata, Ludwig Schubert, Gabriel Goh, Michael Petrov, Shan Carter; OpenAI (Distill Circuits thread)
- **Date:** 2020-03-10
- **Link:** https://distill.pub/2020/circuits/zoom-in/
- **Kind:** essay
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
The essay opens the Circuits thread and argues that neural networks can be understood bottom-up by studying individual neurons and the weights connecting them, the way the microscope made cell biology possible. It puts forward three deliberately speculative claims: features are the basic unit (a feature is a direction in a layer's activation space, often a single neuron); features linked by weights form circuits, small computational subgraphs that can be read like code; and similar features and circuits recur across models (universality). The larger goal is to make interpretability a natural science with falsifiable claims, and eventually to explain whole-model behaviour as a composition of understood circuits.

## What they studied
Mainly InceptionV1 (ImageNet), with layers such as mixed3b (curve detectors) and mixed4c (car detector), plus anecdotal cross-model checks in AlexNet, InceptionV3, VGG19, ResNetV2-50 and Places365-trained models. Units: individual neurons, directions, and the weights between neurons (circuits of up to roughly a dozen features).

## How they did it
For a candidate feature they stack several independent lines of evidence: feature visualisation (optimise an input to excite the neuron), dataset examples, synthetic stimuli that vary one property (orientation, curvature), joint tuning curves across a family of neurons, reading the detector's algorithm from its incoming weights, checking that downstream features use it as expected, and hand-writing weights that reimplement the feature and checking the reimplementation behaves like the original. To read circuits they multiply through 1x1 bottleneck convolutions so each pair of neurons has one effective spatial weight map; positive entries mean excitation and negative ones inhibition. Worked examples: curve detectors built from earlier curve and line detectors with tangent-shaped, orientation-equivariant weights; an oriented dog-head circuit where left- and right-facing pathways inhibit each other and then merge into a pose-invariant unit; a car neuron (wheels below, windows above) whose output in the next layer is spread over neurons that are mostly dog detectors.

## What counts as an explanation here
A feature is explained when its function is supported by converging evidence, and a circuit is explained when the weights between named features can be read as an algorithm (e.g. "look for tangent curves along the arc"). Recurring weight patterns are named as motifs (equivariance, unioning over cases, superposition). Explanations are partial, local and largely qualitative, but are meant to be falsifiable: if a circuit is understood, editing its weights should change behaviour predictably, and a hand-written version should reproduce the original.

## How they judged success
No quantitative metrics. Success is convergence of the seven evidence types above, with the three circuit-based ones (weights, downstream use, hand-written reimplementation) acting as the strongest checks. Universality is judged anecdotally by finding analogous features in other architectures.

## What they found
Meaningful, monosemantic-looking features exist in vision models, such as curve detectors (radius around 60 pixels, in orientation families) and high-low frequency detectors (likely boundary heuristics). Some neurons are polysemantic, e.g. InceptionV1 neuron 4e:55 responds to cat faces, car fronts and cat legs. They hypothesise superposition: networks spread features across neurons to fit more features than neurons, exploiting the many nearly-orthogonal directions in high dimensions. Circuits connecting features are readable from the weights and show reusable motifs.

## Limits and open problems they name
Whether most neurons are meaningful is still disputed; polysemanticity makes many circuits hard to analyse (a 5-meaning neuron connected to another gives 25 entangled connections); universality is only anecdotal; circuit claims are narrow and do not yet explain whole-model behaviour; the work is qualitative; and they warn that some of their three claims may prove wrong, as part of early cell theory did.

## What we take from it
The founding argument that weights can be read directly and that a correct reading should predict the effect of weight edits, which is exactly our target. Two reusable checks: (1) collapse adjacent linear operations into one effective weight between interpretable units before reading; (2) the "hand-written circuit" test: rebuild a component from our explanation and verify it reproduces the original. That second test is a direct template for validating a predictive white-box model. Warning: neuron-basis reading breaks down under polysemanticity and superposition, so we need a better basis than raw neurons.

## Tags
unit: neuron | direction | circuit | weights
form: description | graph
method: weight-analysis | other (feature visualisation, synthetic stimuli, hand-written weights)
eval: human-rating | other (converging qualitative evidence, reimplementation)
goal: understanding | science
