# Notes: parameter decomposition and weight-based interpretability (batch 05a)

**What an explanation is.** Every paper here treats the weights, not activations, as the object to explain. Two shapes
recur: (1) a *decomposition* of the actual weights into pieces that sum exactly to the model, with a per-input record
of which pieces matter (APD arxiv-2501.14926, SPD arxiv-2506.20790, VPD goodfire-research-interpreting-lm-parameters);
(2) a *readable surrogate* derived from weights in closed form: eigenvectors of a bilinear tensor (arxiv-2410.08417),
least-squares polynomials (arxiv-2502.01032). A third route makes the weights readable by training them sparse
(arxiv-2511.13653). All aim at completeness by construction, unlike SAE-style dictionaries with reconstruction error.

**How success is measured.** (a) Recovery of planted ground truth in toy models (MMCS, ML2R on TMS and compressed
computation: APD, SPD). (b) Behaviour preserved under ablation of everything deemed unimportant: stochastic masks (SPD),
adversarial masks (VPD), mean ablation outside a circuit (weight-sparse), scrubbed vs anti-scrubbed (APD). (c) Surrogate
fit: FVU/KL (polynomials), correlation with real feature activations (bilinear), CE and "pretraining compute recovered"
(VPD). (d) Predictions made from weights alone: weight-derived adversarial masks (bilinear), SVD input ablations that
move network and surrogate together (polynomials), circuit-predicted distractor prompts (weight-sparse), a hand edit vs
LoRA (VPD). Baselines: APD for SPD; PCA for LIB (arxiv-2405.10928); per-layer/cross-layer transcoders and intruder
detection for VPD; dense models of matched loss for weight-sparse.

**Open problems.** Superposition kills complete-basis approaches (LIB's negative LM result) and forces overcomplete
decompositions. Grouping rank-one pieces into full mechanisms has no general algorithm (SPD, VPD). Faithfulness under
adversarial ablation is only partial (VPD: KL 0.83 at 20 steps, 40 at 320), and importance-pruned circuits can look
sufficient while failing adversarially. Nonlinear interactions between pieces are unsummarised. Closed-form methods need
an input-distribution assumption and a feature basis for hidden directions, and scale only to low degree.

**For a predictive white-box model from weights.** Most directly reusable: SPD/VPD's causal-importance function is
literally a learned predictor of which weights matter on each input, and the adversarial-mask test is the right stress
test for any claimed explanation. Polynomial/bilinear surrogates give a cheap, data-light baseline and a fit metric
(FVU/KL). Adopt planted-ground-truth toy validation before real targets, and report predictions under intervention
(edits, weight-derived adversarial inputs) rather than only reconstruction.
