# Notes: Anthropic circuit-tracing batch (03_a)

**What an explanation is.** Anthropic's central form is a per-prompt attribution graph over a replacement model:
cross-layer transcoder features with linear edges, frozen attention, and explicit error nodes for what is unexplained
(tcpub-2025-attribution-graphs-methods). The biology paper turns graphs into simplified, intervention-validated
circuit diagrams that are existence proofs, not general algorithms (tcpub-2025-attribution-graphs-biology). Newer work
adds alternative forms: free text scored by reconstruction (tcpub-2026-nla) and a token-named readout of a small
privileged subspace (arxiv-2607.15495). All are explicitly partial.

**How success is measured.** Two layers recur. (1) Reconstruction: normalized MSE vs L0, FVE, matched-feature and
matched-FLOP comparisons (tcpub-2024-crosscoders, tcpub-2025-attention-update, tcpub-2026-nla). (2) Causal prediction:
does inhibiting/injecting/swapping the named feature change downstream features and outputs as predicted? Concrete
numbers: replacement and completeness scores, Spearman 0.72 between graph influence and ablation effect, ~0.6-0.8
cosine agreement one layer after perturbation that decays with depth (methods); swap success rates (workspace);
output-rate changes under steering (biology, attention-qk). Baselines: per-layer SAEs/transcoders, thresholded
neurons, logit lens, random/rotated directions, layer-matched random heads.

**Recurring open problems.** (a) Attention: attribution graphs freeze it; attention is in superposition across heads
and layers; QK is the hardest part (tcpub-2025-attention-update, tcpub-2025-attention-qk). (b) Dark matter: ~11-22%
reconstruction error, and only ~half of next-token predictions survive full replacement. (c) Mechanistic
faithfulness: a dictionary can match activations via a different mechanism; predictive power decays over layers.
(d) Inhibition and inactive features invisible. (e) Coverage: insight on about a quarter of prompts; manual labelling
and supernode grouping. (f) Verbal explainers confabulate.

**Bearing on a predictive white-box model from weights.**
- The field's scorecard for "predicts what the network does" already exists: replacement/completeness scores,
  layer-by-layer perturbation faithfulness, top-token agreement, intervention outcome prediction. We should report
  these directly and beat the depth decay.
- Weight-reading components already exist: global virtual weights with interference filtering (TWERA, methods),
  exact bilinear QK decomposition and W_QK eigenvalue signs for head types (attention-qk), the mean-Jacobian lens
  (workspace). A weight-derived model that explains attention patterns would fill the biggest named gap.
- Biology case studies (two-hop recall, rhyme planning, addition, hallucination gating, refusal) are ready-made
  behavioural test cases with known intervention results.
- Warnings: account for head self-repair in ablations; reconstruction quality is not mechanism; avoid single-head
  functional labels.
