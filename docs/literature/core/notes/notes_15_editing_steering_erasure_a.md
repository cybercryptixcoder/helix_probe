# Notes: batch 15a (editing, steering, erasure; weight reading)

**What an explanation is here.** Two lineages meet. The Geva/Dar line reads weights directly: FFN rows as pattern-detecting keys and value vectors as vocabulary votes (arxiv-2012.14913), sub-updates that promote concepts (arxiv-2203.14680), and every matrix, including attention W_QK/W_VO, projected into token space with no inputs (arxiv-2209.02535). The Meng/Bau line treats an MLP output matrix as a linear associative memory and checks this by writing to it (ROME arxiv-2202.05262, MEMIT arxiv-2210.07229). Task arithmetic (arxiv-2212.04089) treats a whole fine-tuning weight delta as a direction with behavioural meaning. In all, an explanation is good if it predicts what an intervention does.

**How success is measured.** Editing has a shared, reusable metric triple: efficacy, paraphrase generalization and neighborhood specificity (CounterFact, zsRE), with fluency and consistency checks on generated text. Weight-reading papers use concept annotation versus random vectors, value-token/next-token agreement, and weight-versus-activation token overlap. Controls: random matched-norm vectors, held-out tasks or perplexity for collateral damage, gradient-ascent/fine-tuning baselines.

**Recurring warnings.**
1. Composition: at least about 68% of the time a layer's output matches no single memory (arxiv-2012.14913), and per-vector readings miss combinations (arxiv-2203.14680). So per-unit dictionaries alone cannot predict outputs.
2. Localization is not the same as intervention: causal-tracing strength does not predict where an edit works. Layer index explains most of edit success; tracing adds at most about 3 points of R-squared (arxiv-2301.04213).
3. Weight-only projections only partly match runtime behaviour: there is partial activation overlap, and stitching worked for 3 of 11 seeds (arxiv-2209.02535). Lower-layer values project poorly (arxiv-2012.14913).
4. Hand-picked vectors beat automatically selected ones by a wide margin for steering (arxiv-2203.14680).

**For a predictive white-box model from weights.**
- Reuse the vocabulary-space projections of W_in/W_out/W_QK/W_VO as a first, data-free layer of description.
- Reuse the associative-memory model with key covariance (ROME/MEMIT) as the way to predict what a linear layer does under a weight change.
- Reuse task-vector near-orthogonality as evidence that separate edits can be predicted to add up.
- Adopt the arxiv-2301.04213 test: report how much predictive power (incremental R-squared) our mechanistic variables add over trivial covariates for intervention outcomes.
- Score weight-edit predictions with the efficacy/generalization/specificity triple.

**Open problems:**
- a composition rule for many units;
- handling of LayerNorm and nonlinear heads;
- non-factual and bidirectional knowledge;
- automatic rather than manual labelling;
- reconciling where information flows with where weights can be changed.
