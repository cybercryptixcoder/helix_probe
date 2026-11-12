# Notes: weight-space learning, batch A

**What an explanation is here.** None of these papers produces a mechanistic explanation. Two forms appear:
(1) a learned predictor from weights to a scalar or label (accuracy, hyperparameter, INR class) in
arxiv-2002.11448, arxiv-2209.14764, arxiv-2301.12780, arxiv-2302.14040; (2) a natural-language description of what
a weight diff encodes, produced by an LLM trained as an interpreter (arxiv-2510.05092,
neurips-cc-virtual-2026-oral-154334). Neither predicts per-input behaviour; that is the open slot our white-box
model would fill.

**How success is measured.** Held-out *models* (split by model or training trajectory, never by checkpoint):
R-squared and Kendall's tau for scalar properties; accuracy for classification of weights; LLM-judge similarity
(1-5) with an embedding cross-check for descriptions; AuditBench for auditing. Roofline baselines with privileged
info (trigger given) are used in arxiv-2510.05092.

**Recurring baselines.** Hand-crafted per-layer weight statistics plus a regressor (STATNN) is very strong:
R-squared about 0.98 for accuracy (arxiv-2002.11448) and only marginally beaten by equivariant networks on
generalization prediction (tau 0.934 vs 0.915, arxiv-2302.14040). Black-box querying (20-questions, prompting,
query agents) is the baseline for LLM weight readers. Any weights-reading claim must beat both.

**Recurring methods.** Model zoos as datasets (arxiv-2209.14764); symmetry-respecting architectures (DWSNets, NFNs)
because neuron permutations otherwise break readers (arxiv-2002.11448 showed this fragility); synthetic model
organisms with known ground truth, and self-supervised labels from the training documents, for supervising LLM
readers.

**Open problems.** Architectures are tied to small MLPs/CNNs and do not handle transformers or scaling symmetries;
learned LLM readers are narrow (no cross-task transfer), hallucinate, surface only salient changes, and cannot
invert triggers; unclear whether they read weights or induced activations; generalization-gap prediction is weak.

**Bearing on a predictive white-box model from weights.** (a) DWSNets' result that a weight-space network can
approximate the input network's forward pass is the theoretical licence for reading behaviour from weights, but no
paper here tests per-input prediction. (b) Use synthetic organisms with known behaviour as ground truth, held-out
by model. (c) Include STATNN-style and black-box baselines. (d) Respect permutation symmetry (equivariant layers or
SVD-direction tokenization as in LoRAcles). (e) Trigger inversion failure shows describing behaviour is not
predicting when it fires; that conditional prediction is our differentiator.
