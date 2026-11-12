# Notes: 09_causal_methods_b (intervention methods and their pitfalls)

**What an explanation should be.** Across the batch, an explanation is a claim about what happens under
intervention. DAS (arxiv-2303.02536) makes this explicit: a high-level causal model plus a map from its variables
to subspaces, scored by whether it predicts counterfactual outputs (IIA). The patching papers (arxiv-2309.16042,
arxiv-2404.15255, arxiv-2403.00745) treat a circuit as a set of components sufficient or necessary for a
behaviour on a stated prompt distribution, explicitly not minimal and not general beyond that distribution.

**How success is measured.** Intervention agreement: IIA, logit difference (the most trusted metric because it is
roughly linear in the residual stream), FLDD and interchange accuracy (arxiv-2311.17030), KL for circuit
discovery, and cost of verified recall for cheap estimators (arxiv-2403.00745). Recurring benchmarks: IOI in GPT-2
small, factual recall (ROME/COUNTERFACT) in GPT-2 XL, greater-than; Pythia for scaling.

**Recurring lesson: setup choices change conclusions.** Corruption type (Gaussian noise vs in-distribution token
swaps), metric (probability vs logit difference), patch scope, which tokens are corrupted, and noising vs
denoising (AND vs OR structure) all change which components look important (arxiv-2309.16042, arxiv-2404.15255).
Cheap gradient approximations fail at saturated attention and cancelling paths (arxiv-2403.00745). Optimised
subspace patches can work through dormant pathways the model never uses (arxiv-2311.17030).

**Open problems.** Backup/Hydra compensation and negative components make "performance recovered" ambiguous; no
theory for intermediate IIA; DAS overfits and is seed-sensitive; no ground-truth definition of a mechanism, so
illusions are judged by converging evidence.

**Bearing on a predictive white-box model from weights.**
1. IIA-style counterfactual accuracy is the natural headline metric for a model that claims to predict
   behaviour under intervention; report it with noising and denoising, several metrics, and in-distribution
   counterfactuals.
2. The interpretability illusion is defined by downstream weight kernels (nullspace of W_out or of a reader's
   query matrix). A weights-first approach can detect it directly, which is a concrete advantage for us:
   check that predicted pathways lie in the rowspace of the weights that read them.
3. Activation patches along a direction are near-equivalent to rank-1 weight edits (arxiv-2311.17030), linking
   intervention evidence and weight structure.
4. AtP* is a cheap, strong baseline for "predict every component's patching effect"; its failure points
   (softmax saturation, cancellation) are where any linearised weight-derived model will also struggle, so test
   there.
5. Our model should predict backup compensation and negative components, the things naive circuit stories miss.
