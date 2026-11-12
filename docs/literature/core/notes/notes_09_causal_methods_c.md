# Notes: 09_causal_methods_c (causal methods, batch c)

**What an explanation should be.** All five treat an explanation as a causal claim that can be tested by
intervening, not as a description. The forms differ: a sparse edge circuit (arxiv-2403.17806, arxiv-2407.08734), a
symbolic program aligned to learned subspaces (causal abstraction, arxiv-2305.08809), a closed-form algorithm with a
logit formula (arxiv-2306.17844), and, as the umbrella, a reduced causal graph over chosen mediators
(arxiv-2408.01416). The program/causal-abstraction forms are the most directly predictive: they say what the network
outputs under any variable swap.

**How success is measured.** Two families dominate. (1) Faithfulness: fraction of behaviour (logit difference, KL)
recovered when everything outside the circuit is ablated, plotted against circuit size. (2) Interchange intervention
accuracy (IIA): how often the network under a subspace swap matches the hypothesised program. arxiv-2408.01416 adds
sparsity, generality, selectivity as co-equal criteria. arxiv-2306.17844 uses variance-in-logits explained by a
formula plus discriminating signatures.

**Controls and baselines that recur.** Random rotations and randomly initialised models (arxiv-2305.08809); exact
activation patching as reference for gradient approximations, and a simple clean-minus-corrupted baseline that is
surprisingly strong (arxiv-2403.17806); Tracr-compiled ground-truth circuits (arxiv-2407.08734).

**Warnings.** (a) Faithfulness numbers swing with ablation value, granularity, positions, metric and aggregation;
the "optimal circuit" is defined only relative to the ablation (arxiv-2407.08734). (b) Agreement between two
explanations (overlap) is not evidence of correctness; only reproduction of behaviour is (arxiv-2403.17806). (c) The
same task yields different algorithms in different networks, including hybrids and ensembles (arxiv-2306.17844). (d)
Learned alignments can fit even untrained models; held-out and robustness splits are needed (arxiv-2305.08809).

**Open problems.** Non-linear and multidimensional mediators; completeness (not just sufficiency); scalable
better-than-greedy search; scalable measures of generality/selectivity; discovering algorithms no one hypothesised.

**Bearing on a predictive white-box model from weights.** (c) is the strongest argument for our approach: an
explanation must be per-network, so reading the specific weights is the right source. For evaluation we should score
our reconstruction with IIA-style counterfactual prediction on held-out pairs, report faithfulness curves with a
fully specified and stated ablation protocol, give per-input and worst-case numbers, and include random-weight and
cheap baselines. Weights do not appear as a mediator type in the survey's taxonomy (arxiv-2408.01416), which is a
gap we can position into, but all evaluation must still be activation-level and interventional to be recognised.
