# Notes: representations and lenses (batch b)

**What an explanation is.** Across the batch, the explanation is a low-dimensional object standing in for a high-dimensional state or computation: a single direction (CCS arxiv-2212.03827; truth direction arxiv-2310.06824), an affine surrogate of many layers (LRE arxiv-2308.09124), a parametric representation plus named algorithm (helix + Clock, arxiv-2502.00873), a learned decoder of future tokens (arxiv-2311.04897), or a low-rank token-readable decomposition of a weight update (arxiv-2402.12865). Only LRE and the addition paper produce something that *runs in place of* the network and predicts its outputs; the rest show information is present.

**How success is measured.** Two families recur. (a) Decoding/prediction: accuracy against labels or against the model's own argmax (LRE "faithfulness"), precision@k (Future Lens), cross-dataset generalisation (Geometry of Truth). (b) Causal: substitute or perturb and see if behaviour follows: LRE "causality" vs an oracle substitution; normalised indirect effect for truth directions; fraction of logit difference restored when fitted helices or fitted neuron functions are patched in (about 75% at neuron level). The batch's sharpest lesson: these two can disagree. LR and mass-mean truth probes have similar accuracy but very different causal effect (arxiv-2310.06824); LRE faithfulness and causality only correlate (R = 0.84) when tuned for causality (arxiv-2308.09124).

**Recurring baselines/controls.** Identity/logit lens, translation and least-squares regression (LRE); equal-size PCA and shuffled-value fits (addition); bigram statistics (Future Lens); zero-shot and calibrated output plus supervised-probe ceiling (CCS); probability-matched "likely" control and negated statements (truth). Benchmarks: CounterFact (editing metrics in arxiv-2402.12865), the LRE 47-relation set, the curated truth datasets.

**Open problems.** Linearity holds only partly (48% of relations; CEO relation fails); decodable is not used (Future Lens, CCS); the combining step in the addition mechanism is unidentified; most results rest on one or two models (GPT-J, LLaMA-2); logit-lens readings fail in early layers (arxiv-2402.12865).

**For a predictive white-box model from weights.**
1. Adopt the double test of arxiv-2308.09124: a reconstruction must predict held-out outputs *and* its inverse must produce correct edits.
2. Adopt the substitution test of arxiv-2502.00873: replace real activations/neurons with closed-form functions and report performance retained, with PCA and shuffled controls; also check it reproduces the model's *errors*.
3. Jacobian-averaged maps (LRE) and gradient outer-product decompositions (Backward Lens) are the closest bridges here from activations to weights; Backward Lens shows weight updates are low-rank and nameable, useful for predicting fine-tuning effects.
4. Estimate directions with mass-mean rather than max-margin probes, and always check them by intervention.
5. Novelty warning: periodic/helical number representations are already established (arxiv-2502.00873).
