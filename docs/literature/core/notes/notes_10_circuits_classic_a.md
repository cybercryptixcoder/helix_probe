# Notes: circuits, classic batch (job 10_circuits_classic_a)

**What an explanation is.** Across the batch, an explanation is a circuit: a small causal subgraph whose nodes have human-readable roles and whose edges carry an algorithm. The node type has changed over time: neurons read from weights (distill-2020-circuits-zoom-in), then attention heads (arxiv-2211.00593, arxiv-2304.14997), then SAE features (arxiv-2403.19647), then transcoder features in an MLP replacement (arxiv-2406.11944). Only one paper reaches a complete, predictive program: modular addition read off Fourier-basis weights (arxiv-2301.05217). The rest are partial explanations of one task on one data distribution.

**How success is measured.** The shared vocabulary is faithfulness, completeness and minimality under ablation (arxiv-2211.00593), with logit difference or KL to the full model as the target. arxiv-2403.19647 plots faithfulness and completeness against circuit size and compares feature and neuron bases. arxiv-2304.14997 scores circuit-finding methods by ROC AUC against hand-found or tracr-compiled ground truth. arxiv-2301.05217 adds restricted loss (keep only the named components) and excluded loss (remove only them), plus variance explained. Downstream tests are rare but strong: adversarial prompts derived from the circuit (arxiv-2211.00593), SHIFT debiasing (arxiv-2403.19647), and blind case studies using only weight-derived information (arxiv-2406.11944).

**Recurring methods and caveats.** Mean or resample ablation over a matched counterfactual distribution, path patching, and linear attribution (attribution patching, integrated gradients). The choice of ablation can reverse conclusions: zero versus corrupted patching flips the tracr results in arxiv-2304.14997. Backup and negative components hurt both single-metric discovery and simple ablation predictions (arxiv-2211.00593, arxiv-2304.14997).

**Open problems.**
- Scaling beyond manual effort (arxiv-2301.05217).
- MLPs and attention patterns are left unexplained: arxiv-2406.11944 freezes QK, and arxiv-2211.00593 leaves MLPs out.
- Reconstruction error: arxiv-2403.19647 keeps it in the graph as error nodes.
- Polysemanticity and superposition (distill-2020-circuits-zoom-in).
- Evaluation is mostly qualitative.

**Bearing on a predictive white-box model from weights.**
1. Weight reading works once you find a basis where the weights are sparse: Fourier in arxiv-2301.05217, transcoder encoder and decoder vectors in arxiv-2406.11944, where the decoder-encoder product gives connections that hold for every input.
2. Test validity by reconstruction: hand-written circuits (distill-2020-circuits-zoom-in), restricted and excluded loss, and explicit error nodes that measure what is not yet explained.
3. Under ablation, predictions must model compensation by backup heads. Removing a component is not a local edit.
4. Compiled models with known programs (tracr, from arxiv-2304.14997) give exact ground truth for benchmarking weight-reading.
5. Report KL to the full model and more than one ablation type.
