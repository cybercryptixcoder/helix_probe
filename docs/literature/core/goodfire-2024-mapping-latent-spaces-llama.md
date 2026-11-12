# Mapping the Latent Space of Llama 3.3 70B

- **Key:** goodfire-2024-mapping-latent-spaces-llama
- **Authors / organisation:** Thomas McGrath, Daniel Balsam, Liv Gorton, Murat Cubuktepe, Myra Deng, Nam Nguyen, Akshaj Jain, Thariq Shihipar, Eric Ho; Goodfire
- **Date:** 2024-12-23
- **Link:** https://www.goodfire.com/research/mapping-latent-spaces-llama
- **Kind:** blog/research post
- **Read from:** full text (blog page)
- **Relevance to us:** 1 (background)

## What they wanted, and why
Goodfire wanted to show that sparse autoencoders scale to a 70B open model and yield a browsable, steerable feature
map, released as a product (API and explorer) so others could inspect and steer the model. It is a demonstration of
SAE-based interpretability as infrastructure rather than a scientific study.

## What they studied
Llama 3.3 70B, an SAE on an unspecified intermediate layer, trained on chat data (LMSYS-Chat-1M). SAE architecture
and number of latents are not stated; method described as consistent with their earlier smaller-model SAEs (also a
Llama 3.1 8B SAE). Unit: SAE features.

## How they did it
Train an SAE on residual activations from chat data; embed all features with UMAP (DataMapPlot) so nearby features
cluster; inspect clusters; steer generation by adding a feature at varying strengths and score outputs with an LLM
judge; remove harmful features (moderation) before release.

## What counts as an explanation here
A feature dictionary with labels and a 2-D map, plus steering handles. Partial; not designed to predict behaviour.

## How they judged success
Qualitative inspection of the map; steering judged by Claude on a 0-100 scale for coherence and target behaviour
(called the "centiClaude"). No reconstruction, loss-recovered or interpretability metrics are reported.

## What they found
Features span biases, biomedicine, physics, programming, character-level/phonetic features and name abstractions;
special-token and chat-template features sit isolated on the map. Steering with a "pirate" feature: some effect at
0.4, full style around 0.5, many wrong facts at 1.0, all factual claims wrong at 1.4, while the judge score stayed high.
Moderation removed about 30% of features from the 8B SAE and about 3.5% from the 70B SAE (including dead ones).

## Limitations and open problems they name
Steering prefers narrow, sparse mid-layer SAEs while classification prefers broader early or late ones; LLM judges
missed the factual collapse; SAEs capture only part of the computation with incomplete reconstruction and limited
data. They point to crosscoders, Matryoshka SAEs and iterative codebook learning. The demo and API were deprecated
in February 2026.

## What we take from it
Mainly a warning: an LLM-judge steering metric can rate an intervention well while it silently destroys factuality,
so our evaluations of interventions need a separate capability/fidelity check. Also an example of SAE results
reported with no quantitative faithfulness numbers, which we should not imitate.

## Tags
unit: feature
form: dictionary | steering
method: SAE | steering
eval: human-rating
goal: control/editing | understanding
