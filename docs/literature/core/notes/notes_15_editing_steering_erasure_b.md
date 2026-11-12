# Notes: editing, steering, erasure (batch b)

**What an explanation is here.** In this batch an explanation is mostly a *handle*: a direction or subspace whose removal or addition changes behaviour (refusal direction, arxiv-2406.11717; steering vector, arxiv-2308.10248; erased concept subspace, arxiv-2306.03819; learned low-rank subspace, arxiv-2404.03592). Only arxiv-2304.14767 gives a mechanism (enrich subject with MLPs, move relation, extract with attention heads), and it is the one that reads part of the answer directly from weights (E^T W_VO E maps subject tokens to attributes in a single head for 30-39% of extraction events).

**How success is measured.** Bidirectional causal tests dominate: a direction counts if ablating it removes a behaviour and adding it induces it, with minimal side effects (arxiv-2406.11717 makes this its selection rule). Side-effect controls recur: capability benchmarks (MMLU/ARC/GSM8K/TruthfulQA), perplexity on unrelated text, ConceptNet P@K, and matched-rank or matched-norm random interventions as the null (arxiv-2306.03819, arxiv-2308.10248). arxiv-2307.12976 adds the strongest test: derive many logically implied queries from one edit and check they all update; parametric editors pass the target but fail consequences, and a prompt-only baseline beats them.

**Recurring lessons.**
- Intervention strength confounds causal estimates: SAL's cruder erasure overstates reliance on POS relative to minimal LEACE (arxiv-2306.03819). Score predictions against minimal interventions.
- Learned interventions can do the computation themselves: ReFT trains tasks into 0.004-0.03% extra parameters, so a working subspace edit is not proof the model used that subspace (arxiv-2404.03592).
- Storage and retrieval sites differ (MLPs vs heads, arxiv-2304.14767), which plausibly explains why MLP-only edits fail to ripple (arxiv-2307.12976).
- Steering is layer- and model-specific and sometimes fails to replicate (arxiv-2308.10248).

**Open problems.** Semantics of found directions is unclear (refusal direction may be "harm" or something else); only linear erasure is tractable; edits do not propagate through knowledge; mechanisms of learned interventions unknown.

**Directly useful for a predictive white-box model from weights.**
1. Activation-to-weight equivalence: orthogonalizing all residual-writing matrices against a direction reproduces activation ablation exactly (arxiv-2406.11717). This gives a concrete, checkable prediction linking weight edits to behaviour.
2. Reading head parameters in vocabulary space (arxiv-2304.14767) is a working weight-reading primitive.
3. Evaluation suite to adopt: ablate/add acceptance test, random-matched null, off-target metrics, ripple-style consequence queries, and filtering to items the model knew beforehand.
