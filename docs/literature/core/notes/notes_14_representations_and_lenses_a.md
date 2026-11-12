# Notes: batch 14_representations_and_lenses_a

**What an explanation is here.** All six papers treat the residual stream as a shared space in which a model's
state can be *read* (decoded to tokens or concepts) and often *written* (steered). The explanation is a readout or a
direction, not a mechanism: per-layer next-token distributions (lesswrong-interpreting-gpt-the-logit-lens,
arxiv-2303.08112), model-generated descriptions of a hidden state (arxiv-2401.06102), a task-triggering vector
(arxiv-2310.15213), concept reading vectors (arxiv-2310.01405), and a formal concept geometry (arxiv-2311.03658). All
are explicitly partial; none claims to account for the computation that consumes these variables.

**How success is measured.** Two families. Readout quality: precision@1, perplexity/surprisal, KL to the final
distribution, bias in bits, against the logit lens as the standard baseline (2303.08112, 2401.06102). Causal
validity: does intervening on the found variable change behaviour as predicted? FVs are scored by zero-shot accuracy
after insertion against a layer-average control (2310.15213); RepE uses correlation/manipulation/termination/recovery
(2310.01405); the tuned lens checks that directions important to the lens are important to the model (CBE, Spearman
0.89); the LRH paper checks that steering moves the target concept but not separable ones (2311.03658).

**Recurring lesson: decodable is not used.** The best-correlating probe steers worst (2310.01405); vectors matched
to an FV's vocabulary projection lose most of its effect (2310.15213); Patchscopes decodes what the decoder can
extract, not what the model uses (2401.06102); the logit lens is biased (2303.08112). A predictive white-box model
must validate every read variable by write-side intervention.

**Recurring methods.** Unembedding projection; affine per-layer translators trained by distillation; mean-ablation
patching with averaged indirect effect; contrastive pairs plus PCA or mean difference; source-to-target activation
patching.

**Open problems.** Late layers resist both decoding and injection (2310.15213, 2401.06102); inner product and basis
choice are under-determined (2311.03658); linearity fails for some concepts; all work studies activations, rarely
parameters.

**Bearing on reading weights.** Two weight-only tools stand out: the unembedding as a dictionary for any vector that
writes to the residual stream (logit lens), and the inverse covariance of unembeddings as a principled inner
product for comparing such directions (2311.03658). The tuned lens shows the raw basis drifts across layers, so
weight readings at middle layers need a per-layer correction. FVs suggest the right targets to reconstruct are small
head sets whose summed outputs act as control variables, tested by transplanting them into new contexts.
