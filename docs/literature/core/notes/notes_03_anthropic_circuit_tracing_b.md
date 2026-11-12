# Notes: batch 03_anthropic_circuit_tracing_b

**What an explanation should be.** The batch splits between mechanism and difference-finding. The linebreaks paper (arxiv-2601.04480) is the clearest mechanism: variables as curved low-dimensional manifolds, attention QK matrices read as rotations that align one manifold with another, and a hyperplane for the decision. It argues discrete features and manifolds describe the same object, and that features carry a "complexity tax". The faithfulness note (tcpub-2025-faithfulness-toy-model) sets the bar: a replacement model that matches outputs can still use a different mechanism. Explanations must match how the network computes (its Jacobians), not only what it outputs. The diffing papers (tcpub-2024-model-diffing, tcpub-2025-crosscoder-diffing-update, arxiv-2602.11729) produce lists of labelled features that are validated by steering. They say outright that these show differences in representation, not proven differences in mechanism.

**How success is measured.** The same pattern recurs: (1) a toy with planted ground truth (abs-value MLP, synthetic shared/exclusive concepts, cosine-above-0.8 recovery); (2) a real model with a planted behaviour (sleeper agents, LoRA backdoors in arxiv-2611.08465); (3) causal validation by steering, clamping, patching or ablation; (4) random-feature base rates and data-only controls. The quantitative measures are probe R², AUC, FVE, dead-feature fraction, detection/fuzzing scores and centred cosine. Several of these rest on LLM judges (flagging, exclusivity, coherence), and the authors themselves call those scores proxies.

**Recurring warnings.** The objective shapes the units you get. Sparsity plus repeated data creates memorising "datapoint" features. Joint crosscoder losses favour shared features and make exclusive ones dense and polysemantic. Undersized dictionaries create catch-all units. Single-exemplar or maximum-activation methods miss how broad a feature is (MAEM's low diversity). Probes alone missed the linebreak mechanism.

**Bearing on a predictive white-box model from weights.**
- Judge any surrogate on interventions and derivatives as well as outputs. Jacobian agreement (tcpub-2025-faithfulness-toy-model) is a cheap, concrete test.
- Reading weight matrices directly works when the variable's geometry is known. QK-space cosine (arxiv-2601.04480) is a template for weights-to-algorithm claims that can be checked.
- Allow continuous manifold variables, not only sparse binary features.
- Prefer explanations the network itself can verify, such as activation inversion checked with a forward pass (arxiv-2611.08465), over judge-based ones.
- Use planted-behaviour models and 2x2 model/data controls (tcpub-2024-model-diffing) as benchmarks.
- Hard-partitioned dictionaries (arxiv-2602.11729) and model stitching are tools for comparing a surrogate with the original.

**Open problems.** Mechanistic faithfulness at scale; automated manifold discovery; turning representation differences into mechanism differences; scores that do not need LLM judges.
