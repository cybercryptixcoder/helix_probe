# Priors in Time: Missing Inductive Biases for Language Model Interpretability

- **Key:** arxiv-2511.01836
- **Authors / organisation:** Ekdeep Singh Lubana, Can Rager, Sai Sumedh R. Hindupur, Valérie Costa, Greta Tuckute, Oam Patel, Sonia Krishna Murthy, Thomas Fel, Daniel Wurgaft, Eric J. Bigelow, Johnny Lin, Demba Ba, Martin Wattenberg, Fernanda Viégas, Melanie Weber, Aaron Mueller; Goodfire, Harvard, EPFL, Stanford, Boston University and others
- **Date:** 2025-11 (v3 dated 2025-11-24; ICLR 2026 per scout)
- **Link:** https://arxiv.org/abs/2511.01836 (Goodfire page https://www.goodfire.com/research/priors-in-time)
- **Kind:** paper
- **Read from:** abstract and sections (method, main results and discussion read in full; appendices only partially)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
SAEs are the field's standard way to split activations into concepts, but they treat each token's activation independently. Viewing sparse coding as Bayesian inference, the authors show that a standard SAE implicitly assumes the codes are i.i.d. across time, which implies stationarity and constant sparsity over a sequence. Language is not like that: context accumulates, and much of what a token's activation carries is predictable from earlier tokens. They want a featurizer whose prior matches this temporal structure, so that slow, context-carried information (syntax over a sentence, event structure in a story) can be read out, not just local token cues.

## What they studied
Gemma-2-2B residual-stream activations (main), with Llama-3.1-8B in an appendix; Gemma-2-2B-IT for an out-of-distribution dialogue test. Training data: Pile-Uncopyrighted (on the order of 1B tokens). Evaluation domains: Simple Stories, web text, code; structured probes with garden-path sentences, synthetic stories with event boundaries, an in-context random-walk-on-a-graph task, and UltraChat dialogue. Unit: dictionary codes, split into a predictive and a novel part.

## How they did it
First they measure the data: intrinsic dimensionality of activations rises with token position while a stationary surrogate stays flat, autocorrelation varies with position, and projecting onto prior context explains up to about 80% of a token's activation variance. Then they propose Temporal Feature Analysis (TFA). Each activation is split into a predictable part and a novel part. The predictable code is built by an attention step (current token as query, past tokens as keys) that forms a convex combination of encoded past context. The novel code is a standard sparse (TopK or BatchTopK) encoding of the residual left after subtracting the predicted reconstruction. Training minimises reconstruction error plus a sparsity penalty applied only to the novel code, so only the novel residual is assumed i.i.d. They compare TFA against ReLU, TopK and BatchTopK SAEs and a predictive-only ablation, on reconstruction and on a set of structure-sensitive analyses.

## What counts as an explanation here
A dictionary, but a two-part one: slowly varying, context-derived codes plus sparse "new information" codes. Explanations are the similarity structure of codes over a sequence (does it reveal parses, events, graph geometry) and autointerp labels for novel codes. Partial; a single counterfactual edit test is the only predictive check.

## How they judged success
NMSE and fraction of variance explained on three domains; share of reconstruction norm carried by each component; orthogonality of the two error vectors; code-similarity matrices on 50 garden-path sentences and 50 event-boundary stories; robustness of structure to added Gaussian noise; recovery of graph geometry in the in-context task plus a counterfactual code-swap test; tortuosity (path straightness) of trajectories in OOD dialogue; qualitative autointerp of novel codes.

## What they found
- Reconstruction is on par with the best SAEs: NMSE 0.139 / 0.139 / 0.152 (story / web / code) for TFA versus 0.152 / 0.139 / 0.149 for BatchTopK; predictive-only is much worse (0.34-0.38). Variance explained 0.73-0.79.
- The predictive part carries roughly 74-80% of reconstructed norm; the two error vectors are near-orthogonal.
- Predictive codes stayed nearly invariant between garden-path and control sentences and linked heads to distant dependents of the correct parse, while SAE codes followed local, misleading cues.
- Predictive-code similarity was high within story events and low across them; SAEs and novel codes showed little structure, and SAE variance explained collapsed at a critical noise level.
- In the graph task only the predictive code recovered the geometry; swapping in a target node's code shifted next-token predictions consistently with the graph for 4 of 9 nodes.
- In OOD dialogue the predictive code separated user and assistant turns, with tortuosity about 2.0 versus roughly 25-30 for SAE and novel codes.

## Limits and open problems they name
The i.i.d. assumption on the novel residual is itself an assumption. The predictive encoder is a single attention layer. Evidence is mostly qualitative; causal interventions during generation are needed. Training shows competition between the two parts (the novel part can take over; fixed with BatchTopK on Llama). At deep layers (about 81% depth in Llama) the predictive part did not dominate. Future work: manifold-shaped features, temporal straightening, other priors.

## What we take from it
A framing and a warning: every decomposition carries a prior, and the i.i.d.-per-token prior of SAEs hides state that the network carries across positions. A predictive white-box model of a sequence model must model state that evolves over time (what is predictable from context versus what is new), not just per-token features. Reusable measures: fraction of activation variance predictable from context, and the predictive/novel norm split, as diagnostics of how much "state" a layer carries.

## Tags
unit: feature, direction
form: dictionary
method: SAE, decomposition, other (temporal featurizer)
eval: faithfulness, patching, other (reconstruction NMSE, code-similarity structure)
goal: understanding, evaluation-of-methods
