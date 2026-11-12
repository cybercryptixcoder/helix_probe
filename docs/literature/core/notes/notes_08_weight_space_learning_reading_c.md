# Notes: batch 08 weight-space learning (reading c)

**What an explanation is here.** Four of five papers do not aim at mechanistic explanation. The weight-space papers
(arxiv-2002.05688, arxiv-2110.15288, arxiv-2312.04501) produce *predictors from weights to model-level properties*
(hyperparameters, test accuracy, generalisation gap): probes, not accounts of computation. arxiv-2406.09413 gets
closest to human-readable structure: linear, labelled, editable directions in a population of fine-tune weights.
arxiv-2510.13900 outputs a natural-language description of a fine-tuning objective, read from activation diffs.
None predicts input-level behaviour of a single network, which is exactly the gap our white-box model would fill.

**How success is measured.** Weight-space learning has a stable protocol: model zoos, R^2 and Kendall's tau for
accuracy prediction, accuracy for categorical hyperparameters, in-distribution vs OOD splits (e.g. train on narrow
nets, test on wide in arxiv-2312.04501). Standard baselines chain across papers: weight statistics s(W) and the
flat 1D-CNN "DMC" (arxiv-2002.05688) -> hyper-representations (arxiv-2110.15288) -> graph metanetworks
(arxiv-2312.04501). Diffing work instead uses known-objective model organisms, rubric-graded agent descriptions,
a blackbox-agent control with larger query budget, and random-direction controls (arxiv-2510.13900). Editing work
pairs a target metric with a preservation metric and user studies (arxiv-2406.09413).

**Recurring lessons.**
- Symmetry matters: permutation augmentation (arxiv-2110.15288) or equivariant architecture (arxiv-2312.04501)
  is required; scaling symmetry is still unhandled.
- Shortcuts: initialisation, optimiser and shared seeds leave strong signatures (arxiv-2002.05688,
  arxiv-2110.15288); narrow fine-tunes leave an overfitting bias that makes auditing artificially easy
  (arxiv-2510.13900). A weight reader can "succeed" by detecting training artefacts.
- Simple linear tools go far on diffs from a shared base (arxiv-2406.09413, arxiv-2510.13900).

**Open problems.** Scale (none tested beyond small CNNs/INRs for metanetworks; 32B for activation diffing);
OOD generalisation across architectures; label-limited and entangled directions; noisy LLM-based grading.

**Bearing on a predictive white-box model from weights.**
1. Input encoding: parameter graphs (arxiv-2312.04501) already cover attention, residuals and norms, and a GNN
   over the computation graph can provably simulate the forward pass, so behaviour prediction from weights is
   expressible.
2. Baselines to beat: s(W)/DMC for property prediction; ADL activation diffing for "what did fine-tuning change".
   A weight-only method must show added value (no data needed, mechanism, or input-level prediction).
3. Controls: randomise seeds and recipes, hold out architectures, mix unrelated data into test organisms, and
   include random-direction controls.
