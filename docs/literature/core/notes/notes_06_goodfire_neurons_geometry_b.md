# Notes: job 06_goodfire_neurons_geometry_b

**What an explanation is.** The two strongest papers treat an explanation as a small causal model aligned to the
network and judged by whether it predicts the network under intervention: a base-10 addition algorithm mapped to
DAS subspaces and ~28 layer-18 neurons (arxiv-2605.01148), and a fitted mixture of positional, lexical and reflexive
mechanisms that outputs a full next-token distribution (arxiv-2510.06182). Both are partial (one behaviour) but
predictive, including of the model's errors (the "+100 echo", pre-modulo sums). Contrast the feature-map style of
goodfire-2024-mapping-latent-spaces-llama: a labelled dictionary with no predictive test.

**How success is measured.** Interchange intervention accuracy (2605.01148, 2605.29548); distributional agreement
(JS/KL) with the model under patching, bracketed by uniform, prevailing-view and oracle baselines (2510.06182);
ablate-vs-keep-only accuracy as a necessity/sufficiency pair (2605.01148); downstream metrics with strong baselines
such as LEACE/INLP/filtering/steering (2611.07071). Weak practice to avoid: LLM-judge steering scores, which missed a
factuality collapse (goodfire-2024-mapping-latent-spaces-llama).

**Recurring methods.** Distributed alignment search plus interchange interventions appear in three of six papers;
difference-of-means directions and SAEs as concept handles; toy models with closed-form theory checked against real
LMs (2605.29548, 2508.17456, 2611.07071).

**Open problems.** Discovery without a prior hypothesis (2605.01148 needed Fourier geometry in hand); mechanisms
found in easy settings explain little at scale (positional binding ~20% for middle groups, 2510.06182); steering
needs unnatural magnitudes, so identified features do not fully control downstream computation; representations
move, go nonlinear or entangle under training pressure, so static linear readouts are fragile (2611.07071, L1-L5
monitoring hierarchy).

**Bearing on a predictive white-box model from weights.**
- Weight-level quantities can predict behaviour: features-per-dimension and off-diagonal interference of W predict
  adversarial vulnerability in toys (2508.17456); utility = frequency x variance predicts which features a width-N
  model keeps, with a critical width (2605.29548); neuron output weights projected onto a causal subspace identify
  the computing neurons (2605.01148).
- Adopt the evaluation protocol of 2510.06182: compare our model's predicted output distribution under patching to
  the network's, against uniform/naive/oracle baselines.
- Expect mixtures of mechanisms and missing rare behaviours in small networks; test faithfulness on adversarial and
  off-distribution inputs, where interference terms dominate.
