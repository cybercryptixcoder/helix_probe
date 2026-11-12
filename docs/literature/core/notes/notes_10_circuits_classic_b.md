# Notes: circuits classic (batch b)

**What an explanation is.** In this batch an explanation develops from a label into a program. Feature visualisation (distill-2017-feature-visualization) gives a picture that names a unit. Curve Detectors (distill-2020-circuits-curve-detectors) turns the label into a parametric behavioural claim: tuning over orientation and curvature, plus invariances. Curve Circuits (distill-2020-circuits-curve-circuits) adds a family-level schematic, a few-sentence algorithm, and finally program-generated weights that replace the original neurons. Multimodal Neurons (distill-2021-multimodal-neurons) and Othello-GPT (arxiv-2210.13382) stay at the variable level: neuron labels, sparse linear combinations, and a probe-readable board state. Only Curve Circuits produces an explanation that runs.

**How success is measured.** The bar is several converging lines of evidence, not one metric. Recurring tests:
- synthetic-stimulus tuning curves;
- blinded human labels per activation bucket, used instead of top-k examples (curve detectors, multimodal);
- counterfactual intervention scored on the predicted output change: Othello's error count against a counterfactual board, and multimodal's boost of one neuron to confirm a logit change;
- ablate-then-substitute accuracy recovery: 88.6% to 86.3% top-5 after ablation, 87.6% with the hand-built neurons.

Numbers are sparse and small-sample: 2,000 images, one labeller, 1,000 intervention cases. The circuits-era evidence is persuasive but statistically thin.

**Recurring methods.**
- expanded weights through a linearised network (distill-2020-circuits-visualizing-weights, curve circuits);
- NMF of weights and activations;
- equivariance motifs, which compress the curve circuit about 50x;
- attribution as weight times activation;
- surrogates fitted or derived per layer: a bilinear vision-text form, sparse probes, MLP probes.

**Open problems that recur.**
- Linearising through nonlinearities can cancel real interactions to zero, as with boundary detectors.
- A long tail of small weights carries much of the total weight and is unexplained.
- Polysemantic and "conjoined" units exist.
- Feature visualisation fails on large models.
- Probes depend on choosing the right basis, as the failed linear Othello probe shows.
- No paper measures recall or the completeness of a whole circuit.

**For a predictive white-box model from weights.**
1. Curve Circuits is the direct precedent for our pipeline: read weights, write an algorithm, compile it back into weights, swap it in, and score behavioural match and recovered ablation loss. We should adopt "fraction of ablation damage recovered by the substitute" as a headline metric. We should also score at scale what they checked only by eye: tuning-curve agreement on synthetic inputs.
2. Visualizing Weights supplies the operators (expanded weights, factorisation), but it warns that a purely linear weight read misses sign-dependent nonlinear paths. Our model needs input-conditioned corrections there.
3. Othello's counterfactual protocol, which edits a variable to an unreachable state and checks the outputs, is the right test of whether a white-box model predicts behaviour under intervention rather than only fitting the data distribution.
