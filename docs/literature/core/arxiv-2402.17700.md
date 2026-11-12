# RAVEL: Evaluating Interpretability Methods on Disentangling Language Model Representations

- **Key:** arxiv-2402.17700
- **Authors / organisation:** Jing Huang, Zhengxuan Wu, Christopher Potts (Stanford), Mor Geva (Tel Aviv University), Atticus Geiger (Pr(Ai)²R Group)
- **Date:** 2024-02 (v2 2024-08-26)
- **Link:** https://arxiv.org/abs/2402.17700
- **Kind:** benchmark
- **Read from:** full text (arXiv HTML, including appendices)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Neurons are polysemantic, so many methods try to find distributed features that each carry one concept. These methods had not been compared head to head on whether they find features that are causal (intervening changes the concept) and isolated (intervening changes nothing else). RAVEL (Resolving Attribute-Value Entanglements in Language Models) provides that comparison for entity attributes, e.g. separating a city's continent from its country or language. The larger goal is a standard causal test of whether a featurization method localises concepts correctly.

## What they studied
Llama2-7B, residual stream above the last entity token, across layers. Data: five entity types (cities, Nobel laureates, verbs, physical objects, occupations) with 6,828 entities, 420 prompt templates, and 4-6 attributes each (e.g. city: country, language, latitude, longitude, timezone, continent). Two splits: held-out entities and held-out templates. Only examples the model answers correctly are used. Unit: features (directions or subspaces) in activation space.

## How they did it
1. Each method defines a featurizer (an invertible-ish map from activations to features) and selects the features for a target attribute.
2. Interchange intervention: run the model on a base input; replace the chosen features with their values from a source input with a different entity; check the output.
3. For the target attribute, the output should switch to the source entity's value (cause). For prompts querying other attributes, the output should not change (isolation).
4. Methods compared: PCA and an SAE (16,384 features on 4096-d states, trained on Wikipedia sentences), both with an L1 classifier to pick attribute features; RLAP (linear adversarial erasure subspace); Differentiable Binary Masking over neurons (DBM); Distributed Alignment Search (DAS, learned rotation); and the authors' multi-task versions MDBM and MDAS trained on cause and isolation objectives jointly. Full-representation swap as a reference.
5. Sweep feature dimensionality and layer.

## What counts as an explanation here
A causal abstraction-style localisation: a subspace or feature set that, when swapped, transfers exactly one high-level variable (an attribute value) and nothing else. The explanation is a map from a high-level variable to a part of the representation, judged by interventions, not by correlations. Partial (one attribute at a time) but predictive: it predicts the model's output under counterfactual swaps.

## How they judged success
Cause score, Isolation (Iso) score, and Disentangle = their average, averaged across attributes per entity type, on entity and context held-out splits. Intervention size (dimensionality) recorded as a confound.

## What they found
- Disentangle (entity / context split): full-representation 40.5/39.5, PCA 39.5/39.1, SAE 48.6/46.8, RLAP 48.8/50.9, DBM 52.2/49.8, DAS 56.5/57.3, MDBM 53.7/53.9, MDAS 60.1/65.6. Methods with counterfactual supervision win; unsupervised featurizers (PCA, SAE) do poorly.
- The SAE's score comes from isolation (Iso 81.9) with weak cause (23.7); MDAS balances both (Iso 89.8, Cause 57.1) while intervening on about 4% of the representation.
- Multi-task objectives add 1.5-4.1 points for DBM and 3.6-8.3 for DAS.
- Larger feature dimension raises cause but lowers isolation.
- Some attribute pairs (country-language, latitude-longitude) stay entangled for every supervised method; attributes disentangle gradually across layers, best around layer 16 for city country.

## Limits and open problems they name
Single model (Llama2-7B); interventions only on residual stream at the last entity token, though attributes may live elsewhere; SAE featurizer is only faithful to the extent its reconstruction is exact; restricted to correctly answered examples. Failure to separate two attributes may reflect the model, not the method.

## What we take from it
- **Measure (central):** cause/isolation under interchange interventions is a direct test of "predicts behaviour under intervention" and is already recognised; a white-box model should predict the outcome of these swaps.
- **Benchmark:** RAVEL data and code are public and also part of SAEBench, so it can score any featurization we derive from weights.
- **Warning:** report cause and isolation separately and control intervention size; a method can score well by changing almost nothing (high isolation) or by changing everything (high cause).
- **Framing:** supervised, causally trained featurizers beat unsupervised dictionaries on this test, a baseline any weight-derived decomposition must face.

## Tags
unit: direction | feature
form: causal-abstraction | direction | dictionary
method: patching | SAE | probing | other
eval: patching | benchmark | faithfulness
goal: evaluation-of-methods | understanding
