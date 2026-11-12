# Towards Monosemanticity: Decomposing Language Models With Dictionary Learning

- **Key:** tcpub-2023-monosemantic-features
- **Authors / organisation:** Trenton Bricken, Adly Templeton, Joshua Batson, et al.; Anthropic
- **Date:** 2023-10
- **Link:** https://transformer-circuits.pub/2023/monosemantic-features/index.html
- **Kind:** paper
- **Read from:** full text (via page fetch in two parts)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Neurons are polysemantic, plausibly because of superposition. The authors want an existence proof that a weak
dictionary-learning method, a sparse autoencoder (SAE), can recover features from a real (small) language model
that are more interpretable than neurons and invisible in the neuron basis, as a route to circuit analysis and
eventually to enumerating what a model represents.

## What they studied
A one-layer transformer (128-dim residual, 512-neuron ReLU MLP) trained on 100B tokens of the Pile; a second model
differing only in seed for universality tests; a randomly initialised transformer as a control. Unit: the 512 MLP
activations, decomposed into SAE features (dictionaries from 512 to 131,072 features; main run A/1 with 4,096).

## How they did it
They train SAEs (tied pre-bias, linear encoder with ReLU, linear decoder) to reconstruct MLP activations with MSE
plus an L1 penalty, using Adam, ~8B activation samples, batch 8,192, 1M steps, and periodic resampling of dead
features toward poorly reconstructed inputs. They evaluate globally (reconstruction, loss recovered when splicing
the reconstruction into the model, feature density) and locally, with deep dives on a few features (Arabic, DNA,
base64, Hebrew) checking specificity via computational proxies, sensitivity, downstream logit effects, ablation
and steering by pinning a feature high and sampling, and match to the other seed. Interpretability is scored by a
blinded human rubric and by automated interpretability: Claude writes an explanation from top activations and then
predicts activations on held-out text, or predicts which tokens a feature's logit weights promote. They compare
features against neurons and against features from the random transformer, study feature splitting across
dictionary sizes, and chain features into finite-state-automaton-like systems.

## What counts as an explanation here
A feature dictionary: each feature is a direction with a text description, activation examples, and logit effects.
Partial, not complete; the paper also sketches how features chain into automata (e.g. HTML generation), a first
step toward feature-level circuits.

## How they judged success
Fraction of next-token loss recovered by spliced reconstructions; dead and ultralow-density counts; human rubric
scores (max 14); automated activation-prediction scored by Spearman correlation on held-out examples (with
importance-weighting to correct for sparse features scoring by predicting zero); logit-prediction accuracy versus
50% chance; proxy correlations for specific features; cross-seed activation correlation. Baselines: neurons and a
random-weight transformer.

## What they found
A/1 recovers 79% of the MLP's loss reduction; a 131k-feature run about 94.5%. Of A/1's 4,096 features, 168 were dead
and 292 ultralow density. Human rubric: median neuron 0, median feature interval 12. Logit prediction: features
about 0.74 versus neurons about 0.53 and chance 0.5. Cross-seed median activation correlation 0.72 for features
versus 0.46 for neurons; detailed features matched at 0.85-0.92. Feature splitting: one base64 feature becomes three
in a larger dictionary. Features form clusters with similar output effects, and random-weight models give far fewer
interpretable features (though automated scores were fooled by their trivial single-token features).

## Limitations and open problems they name
No trusted automatic metric for dictionary quality or for how much of the model is explained; loss recovered can
mislead because of a long tail; low activations less interpretable; detailed features were cherry-picked; the right
dictionary size is undefined; one-layer results may not generalise; scaling cost is large (a 100x expansion of a
10,000-wide layer needs about 20B parameters), and LLM simulation of every feature is very expensive.

## What we take from it
The standard evaluation kit for feature dictionaries that our work will be compared against: spliced loss
recovered, dead/density stats, simulation-based automated interpretability, neuron and random-model baselines,
cross-seed universality. Note that their causal evidence is mostly about activations; the decoder and logit
weights give a weight-side view we could build on. Warning: automated scores can be gamed by trivially predictable
features, so a predictive model needs held-out, importance-weighted evaluation.

## Tags
unit: feature, neuron
form: dictionary, description
method: SAE, ablation, steering
eval: prediction/simulation, human-rating, ablation, faithfulness
goal: understanding, science
