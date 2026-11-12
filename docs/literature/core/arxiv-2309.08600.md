# Sparse Autoencoders Find Highly Interpretable Features in Language Models

- **Key:** arxiv-2309.08600
- **Authors / organisation:** Hoagy Cunningham, Aidan Ewart, Logan Riggs, Robert Huben, Lee Sharkey; EleutherAI, MATS, Bristol AI Safety Centre, Apollo Research
- **Date:** 2023-09
- **Link:** https://arxiv.org/abs/2309.08600
- **Kind:** paper
- **Read from:** full text (HTML version)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Individual neurons in language models are often polysemantic, which the authors attribute to superposition: the
network represents more features than it has dimensions, as directions that are not axis-aligned. They wanted to
know whether an unsupervised sparse dictionary learned on activations could recover those directions and give a
more interpretable basis than neurons or classic decompositions. The larger aim is a unit of analysis for
mechanistic interpretability that makes circuits easier to find and edits more precise. This is one of the two
papers (with Anthropic's "Towards Monosemanticity") that established SAEs as the default feature-extraction tool.

## What they studied
Pythia-70M (residual width 512) for most residual-stream dictionaries and a case-study circuit, and Pythia-410M
(width 1024) for indirect object identification (IOI) patching. Units: learned dictionary features on residual
streams and some MLP sublayers, compared against neurons, PCA, ICA and random directions.

## How they did it
They trained a one-hidden-layer autoencoder with ReLU, tied encoder/decoder weights and unit-norm dictionary rows,
using squared reconstruction error plus an L1 penalty on the hidden code (coefficient 8.6e-4 for residual, 3.2e-4
for MLP), at dictionary ratios from 0.5x to 8x the input width. Data were 5 to 50M activation vectors from the
Pile; one run takes under an hour on an A40. Interpretability was scored with the Bills et al. (OpenAI) pipeline:
GPT-4 writes an explanation from top-activating fragments, GPT-3.5 predicts activations on held-out top and random
fragments, and the score is the correlation between predicted and real activations. They compared 150 features per
method across layers. For causal localisation they patched features (ordered with ACDC) between IOI prompts and
counterfactuals in Pythia-410M and asked how many patched features, and how large an edit, are needed to reach a
given KL divergence from the counterfactual output, versus PCA directions and a non-sparse dictionary. Case studies
traced single features (an apostrophe feature; a closing-parenthesis feature with an upstream causal tree built
from ablations on 20 contexts).

## What counts as an explanation here
A feature dictionary: each learned direction with a natural-language description of when it fires and, in case
studies, what it does to output logits. Partial by design; reconstruction is imperfect. The simulation score is a
mild form of prediction (predicting a feature's activation from its description).

## How they judged success
Autointerpretability (simulation) correlation score against neuron, random-direction, PCA and ICA baselines, with
controls (random-only scoring; top-k-constrained PCA/ICA). For causality: KL divergence to the counterfactual
target versus number of patched features and edit magnitude on IOI. Reconstruction cost: perplexity after splicing
the reconstruction into the model.

## What they found
Learned features scored clearly higher than all baselines in early layers; the advantage shrank in deeper layers
(roughly matching ICA by layer 4, little gain at the last layer). On IOI, sparse dictionaries reached a target KL
with fewer and smaller feature edits than PCA or an unregularised dictionary; higher L1 raises the floor on
achievable KL because reconstruction gets worse. Case-study features were close to monosemantic with predictable
logit effects (the apostrophe feature mainly boosts "s"). Splicing a layer-2 reconstruction into Pythia-70M raised
Pile perplexity from 25 to 40.

## Limitations and open problems they name
Imperfect reconstruction; unreliable overcomplete learning in middle and later MLP layers with many dead features;
attention untested; generalisation of the IOI result untested; autointerpretation weaker deep in the model. Future
work: other architectures, training against output change instead of reconstruction, resampling dead features.

## What we take from it
The baseline set (neurons, random directions, PCA, ICA) is the standard comparison any new basis must beat, and we
should report it. "Number of units edited to reach a target KL under patching" is a clean sparsity-of-explanation
measure we can reuse for weight-derived units. Warning: a 25-to-40 perplexity jump shows that a dictionary is not
yet a model of the network; reconstruction-based units leave a large predictive gap that a white-box model must
account for.

## Tags
unit: feature
form: dictionary | description
method: SAE | patching | ablation
eval: prediction/simulation | patching | ablation
goal: understanding | evaluation-of-methods
