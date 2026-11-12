# Notes: job 02_anthropic_foundations_a (Anthropic foundations, part A)

**What an explanation should be.** The batch shares one ideal: a finite, mechanistic description read from the
model, like decompiled source, not a catalogue of input-output behaviour (tcpub-2022-mech-interp-essay). The only
case where this was achieved exactly is attention-only transformers, where path expansion turns the weights into
bigram and skip-trigram tables and an induction circuit that directly predict logits (tcpub-2021-framework).
Everything later retreats to partial explanations: a named circuit tied to a capability by several evidence types
(tcpub-2022-in-context-learning-and-induction-heads) and feature dictionaries with text descriptions
(tcpub-2023-monosemantic-features, tcpub-2024-scaling-monosemanticity).

**Why it got harder.** Superposition (tcpub-2022-toy-model) is the shared diagnosis: features are packed as
non-orthogonal directions, so neither neurons nor raw weight rows are the "variables". The proposed fixes were
superposition-free training, post-hoc overcomplete bases, or hybrids; the program chose the post-hoc route (SAEs),
which is activation-side, incomplete (likely orders of magnitude short at scale) and expensive.

**How success is measured.** Recurring measures: spliced loss recovered / variance explained, L0 and dead-feature
counts, simulation-based automated interpretability (LLM explains, then predicts held-out activations), human
rubrics, logit-effect prediction, ablation and clamp-steering, attribution-vs-ablation agreement, cross-seed
universality. Recurring baselines: neurons, random-weight models, random-matrix nulls for weight statistics
(framework), linear probes / few-shot steering vectors. Behavioural controls on repeated random tokens recur in
both circuit papers. No paper has a trusted single metric for "how much of the model is explained"; the SAE papers
say so directly.

**Open problems.** MLPs and nonlinear layers resist weight-level reading; cross-layer, attention and weight
superposition block circuits; feature definition is unsettled; activation alone poorly predicts causal importance
(about 0.12 correlation with ablation versus about 0.8 for attribution in tcpub-2024-scaling-monosemanticity).

**Bearing on a predictive white-box model from weights.**
- The framework paper is the existence proof and toolkit (QK/OV, virtual weights, composition scores against random
  baselines, eigenvalue summaries); our contribution would be extending that kind of exact reading past MLPs and
  superposition.
- The toy model gives a ground-truth testbed: plant features, check that a weight-reading method recovers them and
  predicts behaviour, before touching real models.
- To be recognised by this field, our evaluation should report loss recovered when our reconstruction replaces the
  real component, held-out prediction scores, and intervention tests (ablation/steering predicted versus observed),
  against neuron and random-model baselines.
- Triangulating evidence types, as the induction-heads paper does, is the accepted way to argue a mechanism holds
  where full proof is too expensive.
