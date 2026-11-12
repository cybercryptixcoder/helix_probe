# Notes: batch 06_goodfire_neurons_geometry_a (Goodfire: neurons and neural geometry)

**One shared target: question the unit of analysis.** All six papers argue that the SAE's 1-D, i.i.d.-per-token direction is the wrong default. Three alternatives appear: continuous manifolds (arxiv-2604.28119, arxiv-2605.05115, goodfire-research-the-world-inside-neural-networks), state carried across time (arxiv-2511.01836), and the network's own neurons (goodfire-research-neurons-as-an-interpretable-basis). arxiv-2509.02565 explains in theory why SAE scaling can hide this: latents get spent tiling common manifolds, so falling loss does not mean the inventory is complete.

**What an explanation should be.** The agenda post sets three levels: ontology (variables and their geometry), then the algorithm over them, then behaviour. In practice the explanations here are (a) fitted manifolds with intrinsic coordinates, (b) groups of features that together span a manifold, (c) two-part dictionaries (predictable versus novel), and (d) per-neuron modes defined by upstream inputs and downstream readers, plus text. Only (a) and (d) are tested for prediction.

**How success is measured.** The usual SAE metrics (NMSE, variance explained) appear only as a minimum bar; TFA matches SAEs on them, and the authors still argue SAEs miss structure. The more telling measures are:
- intervention-based: energy (Bhattacharyya distance to the behaviour manifold) and geodesic correlation between representation and behaviour, with linear steering as the baseline (arxiv-2605.05115);
- structural: restricted R² as support size grows, Ising/co-activation block structure, and cross-run alignment (arxiv-2604.28119);
- predictive: detection, mode classification from inputs versus readers, input synthesis, and simulation scored as the share of ablation damage restored (neurons post);
- sparsification loss/KL against random and bottom-K controls (neurons post).
Synthetic ground-truth manifolds are the recurring control.

**Open problems.** Finding manifolds without supervision; grouping methods that capture more than pairwise dependence; linking geometry to the operations that act on it (named by every geometry paper); weak and Q3 activations; causal tests for temporal codes; most results come from one model and one layer.

**For a predictive white-box model built from weights:**
1. Interventions must stay on the manifold. Linear edits of curved variables push the model off-distribution and would wrongly count against our model (arxiv-2605.05115).
2. The neurons post shows that much of a modern MoE model can be read in its native basis, from upstream-write decomposition and first-order downstream propagation. That is close to reading weights directly, and its evaluation suite can be reused.
3. Decoder-cosine (a weight-only signal) failed to group manifold features (arxiv-2604.28119), so activation statistics are probably still needed alongside weights.
4. For sequence models, the white-box model needs explicit state that carries across positions (arxiv-2511.01836).
