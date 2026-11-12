# Interpretability as Compression: Reconsidering SAE Explanations of Neural Activations with MDL-SAEs

- **Key:** arxiv-2410.11179
- **Authors / organisation:** Kola Ayonrinde, Michael T. Pearce (MATS); Lee Sharkey (Apollo Research)
- **Date:** 2024-10-15
- **Link:** https://arxiv.org/abs/2410.11179
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
SAEs trained only for reconstruction plus sparsity drift toward ever wider, ever sparser dictionaries, which encourages feature splitting and memorisation-like features. The authors want a principled target for what a good set of features is. They recast an SAE as a lossy compression scheme that communicates activations, and apply the Minimum Description Length principle: the best explanation is the shortest total message that keeps reconstruction within a tolerance. This is a step toward a theory-grounded, automatic measure of explanation quality.

## What they studied
BatchTopK SAEs on MNIST (main case study); a worked description-length estimate for an open GPT-2 layer-8 residual SAE; toy settings for feature splitting (two boolean features and their AND) and hierarchical features (e.g. animal/bird). Unit: SAE features (dictionary).

## How they did it
They define description length (DL) of SAE codes: roughly, for each active feature, bits for its value plus bits to say which feature it is, giving a simple bound of L0 times (bits per float plus log2 of dictionary size), and an exact version as the entropy of the feature activation distribution. They argue features must be "independently additive" (each understandable separately, sums explained by sums), which linear decoders and tree-structured decoders satisfy. Procedure: fix a loss tolerance (MSE or downstream CE); train a sweep of SAEs of varying width and sparsity that meet it; reduce numeric precision until the tolerance breaks; compute entropy-based DL; select the smallest-DL SAE. They analyse which regimes win and show, analytically, when splitting a feature into mutually exclusive parts lowers or raises DL, and that hierarchical (child-conditional) coding never increases DL.

## What counts as an explanation here
A feature dictionary plus sparse codes, judged as a compressed message about activations. The best explanation is the one with the minimum description length at fixed fidelity. Partial (lossy within tolerance).

## How they judged success
Description length in bits (per input or per token), with L0, reconstruction MSE, downstream cross-entropy and alive-feature counts. Baselines: dense activations, one-hot lookup coding, and conventional sparsity-maximising SAEs. Interpretability judged qualitatively by inspecting features at different density percentiles; no human study.

## What they found
- GPT-2 example: an SAE with L0 65 and 25,000 features at 7 bits costs about 1405 bits/token vs 5376 for the dense 768-d representation (not fully like-for-like since the SAE explains 93% of variance).
- MNIST (MSE tolerance 0.015; about 5 bits per float barely changed MSE): high-L0 narrow SAEs give small stroke fragments; very wide low-L0 SAEs give whole-digit, sample-like features; the MDL optimum gives longer reusable strokes, which the authors find most interpretable.
- Splitting always lowers L0 but lowers DL only when the features are highly correlated.
- The point where DL starts rising roughly coincides with dead-feature onset (not tested systematically).

## Limits and open problems they name
MDL is used only for selection across an expensive sweep (could be added to the loss); MNIST evidence is qualitative; hierarchical decoders proposed but not trained; MDL as a replacement for human interpretability studies is suggested, not validated.

## What we take from it
A measure: description length at a fixed fidelity tolerance is a principled score for any explanation, including a white-box model read from weights; it penalises both lookup-table memorisation and dense restatement. We can report bits needed by our reconstruction vs. the original network at matched behavioural error. Also a warning that sparsity (L0) alone is a bad objective because it rewards splitting.

## Tags
unit: feature
form: dictionary
method: SAE | other (MDL)
eval: other (description length) | human-rating (informal inspection)
goal: evaluation-of-methods | understanding
