# Notes: batch 10_circuits_classic_c

**What an explanation is.** All five treat an explanation as a mechanism tied to specific components, but they differ in how complete it is. The group-composition work (arxiv-2302.03025) is the only near-complete one: a known algorithm (representation theory) is mapped onto embedding subspaces, neurons and logits, and it predicts logits and ablation outcomes. Copy suppression (arxiv-2310.04625) explains one head well enough to build a "mechanism-only" version of it. Greater-than (arxiv-2305.00586) gives a circuit graph plus a qualitative story, and leaves MLP computation spread across many neurons. Fact Finding (alignmentforum-fact-finding-reverse-engineer-factual-recall-neuron-level) ends with an "effective model" whose lookup core is black-boxed. Hydra (arxiv-2307.15771): per-component contributions are not enough, because the network reacts to interventions.

**How success is measured.** The recurring pattern is to keep the hypothesised part, remove the rest, and report the fraction of behaviour recovered. Examples: probability difference recovered by the circuit (89.5%, greater-than), KL recovered by a constrained ablation versus mean ablation (76.9%, copy suppression), restricted versus excluded loss (universality), and accuracy of a simplified model (Fact Finding). Necessity checks (corrupt only the circuit) and task-specific metrics are standard. Warnings: metric choice changes the verdict (copy suppression: 82% of net vs 45% of absolute loss change; soft and hard metrics diverge in Fact Finding), and ablation results are confounded by compensation (Hydra).

**Recurring methods.** Path patching, logit lens, mean/resample ablation, PCA, linear probes, and projecting weights onto hypothesised subspaces. Baselines: random-init MLPs, a same-matching QK null, a corrupted "01" dataset.

**Open problems.**
- Neuron-level MLP computation remains unexplained in real LMs (greater-than, Fact Finding).
- Structured representations found by PCA may not be causally used (greater-than).
- Seed-specific details are not universal (arxiv-2302.03025).
- Self-repair is only partly understood (39% of self-repair explained by copy suppression; Hydra at layer granularity only).

**For a predictive white-box model from weights:**
1. Weight reading works best when we can hypothesise the algorithm's basis (arxiv-2302.03025, arxiv-2310.04625).
2. Read each network's own weights; do not transfer across seeds.
3. Plan to represent lookup-like parts as explicit tables or black boxes with clean interfaces (Fact Finding).
4. The model must predict total effects of interventions, including compensation, not just sums of direct effects (Hydra).
5. Test it on inputs where the mechanism should fire wrongly or not at all (greater-than).
6. Score it with a constrained-ablation, fraction-recovered metric and report several metrics.
