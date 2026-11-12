# Notes: parameter decomposition and weights (batch b)

**What an explanation should be.** Every paper here treats the weights, not activations, as the object to explain, but they disagree on the form. arxiv-2405.10927 wants a reparameterisation-invariant basis plus a modular partition; arxiv-2511.08854 wants a sum of rank-1 weight slices with input-dependent importance; alignmentforum-svd-transformer-weight-matrices-highly-interpretable offers a static labelled dictionary of singular directions; distill-2020-circuits-weight-banding gives a causal story for a layer-wide weight pattern; lesswrong-weight-sparse-circuits-may-be-interpretable-yet-unfaithful examines pruned subgraphs. arxiv-2410.11179 supplies a criterion for choosing among explanations: the shortest description at a fixed fidelity tolerance.

**How success is measured.** Behavioural fidelity is measured as KL or CE to the original model, not to labels (behavioural loss in 2405.10927; KL reconstruction in 2511.08854; CE vs node count in the LessWrong post). Size or simplicity is measured as effective parameter count, active-component count, L0, or description length in bits. Interpretability is still judged mostly by humans or LLM labellers (SVD post). Only the LessWrong post tests mechanism agreement directly: attention patterns, node roles, and OOD behaviour across seeds.

**Recurring methods and baselines.** SVD keeps recurring as the reference point. It is the interpretation method in the SVD post, the baseline in 2511.08854, and what the interaction basis reduces to for linear networks in 2405.10927. Ablation (zero vs mean) is the main causal test, and the LessWrong post shows the choice changes results.

**Open problems.** No accepted faithfulness metric exists. Scaling is a problem: the interaction basis is reported to fail on LLMs, and SPD has only been shown on small models with two prompts. Singular vectors are unidentifiable when singular values are near-equal, and orthogonal bases cannot express superposition. MDL selection needs an expensive sweep.

**Implications for a predictive white-box model read from weights.**
1. Quotient out symmetries and degeneracy first (2405.10927), and factor out architecture- or data-driven bookkeeping structure such as positional banding (distill-2020-circuits-weight-banding).
2. Use an SPD-style objective (faithfulness + minimality + stochastic masking with KL) as a way to train a decomposition that is faithful by construction (2511.08854).
3. Report description length at matched behavioural error as the compactness score (2410.11179).
4. Validate beyond loss. Check internal agreement, off-distribution behaviour and multi-seed spread, and run a nonsense-task control. A small, readable, low-loss reconstruction can still be the wrong mechanism (LessWrong post).
5. Use SVD with unembedding projection as the weak baseline that any weight-reading method must beat (SVD post).
