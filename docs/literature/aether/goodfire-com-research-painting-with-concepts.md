# Painting With Concepts Using Diffusion Model Latents

- **Key:** goodfire-com-research-painting-with-concepts
- **Authors / organisation:** Nick Cammarata, Mark Bissell, Nam Nguyen, Max Loeffler, Eric Ho, Myra Deng, Liv Gorton, Daniel Balsam; Goodfire
- **Date:** 2025-05-27
- **Link:** https://www.goodfire.com/research/painting-with-concepts
- **Kind:** blog/research post (tool announcement with a method sketch)
- **Read from:** full text — the whole page through references, citation block and all six footnotes (~20.9k chars, one fetch). **No figure inspected**: the feature UMAP, the per-factor decomposition panels and the example paintings are recorded only from the prose and captions that describe them. The referenced SDXL-Turbo SAE paper (Surkov et al.), BatchTopK (Bussmann et al.) and the linked open-source interpreter were not fetched.
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Goodfire's stated aim is to show that interpretability is not just an auditing instrument but a *user interface*: if you can name the model's internal features, a person can act on them directly instead of negotiating with a prompt box. Paint With Ember replaces text prompting with a canvas whose strokes map onto activations at specific spatial locations of the image being generated. The bigger goal is the one that matters to us — a representation a human can operate, where an edit is a readable move in a shared coordinate system rather than a lucky string. Nothing here is offered as evidence about model mechanism; the post is a design argument that legible units enable interactions a black box cannot.

## What they studied
SDXL-Turbo, a 3.5B-parameter latent diffusion model, at a single UNet block (`down.2.1`). At that layer the image is 16×16 = 256 patches, each a latent vector analogous to a token, interacting through self- and cross-attention; the authors say this is roughly where the model fixes foreground/background composition. Units of analysis are (a) SAE features on the patch latents, and (b) "factors" — per-image clusters of features obtained by non-negative matrix factorization of the patch × feature weight matrix.

## How they did it
A BatchTopK SAE (k=10, expansion 8, i.e. 10,240 latents) was trained on patch activations; the authors swept k over 10–48 and expansion over 4–16 and chose on a mixture of quantitative and qualitative impression (no criterion for the mix is given). Features are visualised by single-step generation steered toward the feature vector with an empty prompt, and labelled by Claude 3.7 Sonnet from three such visualisations at distinct seeds. For interaction, the per-image feature-weight matrix over patches is factorised with NMF into 3–8 components; each factor is a weighted sum of features, and the factor-strength tensor (16×16×n_factors) is the object the canvas edits — painting sets factor strength in patches, dragging moves the spatial profile, and the "semantic content" slider reweights the features inside a factor's basis row. Spatial-position features are ablated before fitting NMF and re-included afterwards, which the footnote says did not visibly change output.

## What counts as an explanation here
A two-level dictionary plus a drawing: named SAE features (global, model-level) and NMF factors (local, per-image) that a person can point at, paint with, drag, and re-blend. The explanation is partial by construction — one layer, one modality — and is validated by whether the resulting edit produces the intended picture, not by whether it predicts an internal computation. It is the strongest instance in this folder of an explanation shipped as an *interface*, where the falsification test is a human's "that's not what I meant".

## How they judged success
Qualitative: example canvases, the observation that generated images are coherent even with no prompt at all, and a user-testing finding that restricting the prompt to style gave a more enjoyable experience than letting prompt and painted activations compete. Quantitative claims are absent — no coverage rate, no feature-interpretability rate, no fidelity metric for the SAE reconstruction, no ablation of the SAE at all, no comparison against prompting-only or against a random-direction canvas. Hyperparameter choice is described as a sweep but no numbers from it are reported.

## What they found
The main result is the existence of concrete, named features at an early layer, and several are given as named items: individual artworks and characters, brand logos, named buildings, specific meme/game content. The authors say they expected only generic high-level composition units this early and were surprised by entity-level granularity; their explanation is frequency or distinctiveness in the training distribution, and they note that specific-people prompts instead use generic face features at this layer with later cross-attention adding identity. Spatial features exist — corner-only and top-border-only detectors — consistent with the model having learned its own positional grid; the authors concede these are exactly where visualisation fails, since a border detector has no icon. Interaction features ("opening one's mouth", "hugging", "squaring up to fight") generalise across subjects and adopt the subject's anatomy rather than pasting human limbs onto animals, which is the most interesting single observation for us: the feature names a *relation* that is reconstructed in the receiver's own body plan. Finally, a "cat head" factor made of an entropic blend of features beats its own top-weighted feature, i.e. the interaction between features carries content that no single feature does.

## Limits and open problems they name
Feature visualisation is uninterpretable or actively misleading for abstract features (their own footnote, stated twice). No mechanism for grouping features other than per-image NMF is offered; the authors point at supernodes and hierarchical/matryoshka-style methods as the alternatives they did not use. Style guidance currently still requires a text prompt because SAEs were trained only on this early block. Prompt and painted activations interact unintuitively when they conflict — acknowledged as a design finding, not investigated. The public app is a demo, not an evaluation.

## What we take from it
Four things. (a) **A two-scale dictionary is the minimum for an operable interface**: a global dictionary gives names, a per-instance factorisation gives the handful of units a human can hold, and the gap between them is filled by clustering rather than by a better SAE — directly relevant to any read-out we expose. (b) **The ablation-then-refit trick as a nuisance-control**: dropping position features from the NMF fit (then re-adding at transform time) is a cheap way to keep a factorisation from spending a component on a confound, and it generalises to any latent matrix where some directions encode index rather than content. (c) **A warning that visualisation can misname a real feature** — a working, causally useful direction whose icon is meaningless — which is the image-modality twin of the folder's "descriptor ≠ mediator" pattern and argues for naming by intervention rather than by top-activating examples. (d) As a genre note: this post is a *product* argument written by a research team, so read the descriptive claims (features exist, factors steer) as real and the comparative claims (this beats prompting, this is human-scale) as untested.

Added by me, not claimed by the authors: no random-direction or matched-norm control for any painted edit, no measure of how many of the 10,240 features are usable, no reconstruction-quality number for the SAE, and no test of whether a factor edit produces the same change in a second seed or a second model.

## Tags
unit: feature | layer
form: dictionary | steering
method: SAE | decomposition | steering | other
eval: human-rating | downstream-task
goal: control/editing | understanding | science
