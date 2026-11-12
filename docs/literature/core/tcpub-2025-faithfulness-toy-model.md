# A Toy Model of Mechanistic (Un)Faithfulness

- **Key:** tcpub-2025-faithfulness-toy-model
- **Authors / organisation:** Chris Olah (with acknowledged input from Josh Batson, Michael Sklar, Jack Lindsey, Adly Templeton, Siddharth Mishra-Sharma); Anthropic
- **Date:** 2025-08-07 (page date; the Transformer Circuits index files it under July 2025)
- **Link:** https://transformer-circuits.pub/2025/faithfulness-toy-model/index.html
- **Kind:** blog/research post (informal, preliminary lab-meeting-style note)
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Transcoders (sparse dictionaries that read an MLP's input and predict its output) are the backbone of Anthropic's replacement-model and attribution-graph work, because they make feature-to-feature interactions linear. The worry here is that a transcoder can reproduce a layer's input-output behaviour on the training distribution while implementing a different mechanism, which then generalises differently off-distribution. The note builds the smallest possible setting where this "mechanistic unfaithfulness" can be seen and asks what causes it and whether a training change can prevent it. The larger goal is explanations that can be deeply trusted, not just ones that match outputs.

## What they studied
A one-layer toy model computing elementwise absolute value, y = abs(x), which is exactly two ReLU neurons per dimension (ReLU(x) + ReLU(-x)). Inputs are sparse: each dimension is uniform on (-1, 1) with some probability, otherwise zero; a single special point p = [1,1,1,0,...] is repeated a fraction of the time. Unit of analysis: transcoder features versus the true MLP neurons. Dimensions, width and dataset size are not given.

## How they did it
Transcoders were trained on the toy MLP with a tanh-shaped sparsity penalty (chosen to approximate L0; plain L1 gave duplicate features). Without repeated data, the transcoder recovers the true ReLU features. With repeated data, the author inspects learned features by decomposing each feature's contribution, via compressed sensing, onto a library of ideal circuits (the ReLU(x_i), ReLU(-x_i) units and a "memorise p" circuit) plus a residual. A hyperparameter scan varies the repeat fraction and sparsity strength. A crude memorisation score measures how much a feature's output on p points along p rather than along any single true basis direction. Finally a fix is tested: adding a Jacobian-matching penalty, estimated with random vectors as E_v ||J_MLP v − J_T v||², computable by backprop.

## What counts as an explanation here
A replacement model (transcoder) whose features are meant to be the mechanism, not just a reconstruction. The note's point is that a faithful explanation must match how the original computes (its local derivatives / circuit), not only what it outputs.

## How they judged success
Ground truth is known (the two-ReLU circuit), so faithfulness is judged by whether learned features align with the true circuits; quantified with the memorisation score summed over features and the compressed-sensing decomposition plots. No reconstruction MSE or attribution-comparison numbers are reported.

## What they found
With repeated data plus sparsity pressure, the transcoder learns a "datapoint feature" that detects p and writes p out wholesale, a memorising shortcut the real model does not use. Formation appears to depend on the product of repetition rate and sparsity penalty. Even at 5% repetition, a datapoint feature appears and the three true ReLU features rotate so they no longer fire on p, i.e. the mechanism diverges while outputs still match. Jacobian matching removed the datapoint feature in the toy setting, leaving the other features only slightly rotated, and greatly improved the memorisation metric.

## Limits and open problems they name
Very preliminary, low confidence, toy-only; nothing shown on real models. Jacobian matching risks gradient masking (features with huge weights and very negative biases that barely fire); the author suggests also penalising each feature's L1 contribution to the Jacobian. Under superposition, exact Jacobian matching may be undesirable because small singular values reflect interference. Open: whether mechanistic faithfulness is achievable at scale, and how to trade faithfulness against simplicity.

## What we take from it
A warning and a measure. Output-level reconstruction is not evidence that a surrogate computes the same way; a predictive white-box model must also match the original's derivatives / intervention responses. Concretely: (1) add a Jacobian (or directional-derivative) agreement check to our evaluation, not just output agreement; (2) repeated/memorised inputs plus sparsity pressure can create spurious "datapoint" units, so audit our training data for repeats; (3) build toy models with known circuits as ground-truth tests of any weight-reading method.

## Tags
unit: feature | neuron
form: replacement-model
method: transcoder | other (Jacobian matching)
eval: faithfulness
goal: evaluation-of-methods
