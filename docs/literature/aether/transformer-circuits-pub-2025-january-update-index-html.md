# Circuits Updates, January 2025

- **Key:** transformer-circuits-pub-2025-january-update-index-html
- **Authors / organisation:** Tom Conerly, Hoagy Cunningham, Adly Templeton, Jack Lindsey, Basil Hosmer, Adam Jermyn; Anthropic (Transformer Circuits Thread)
- **Date:** 2025-01
- **Link:** https://transformer-circuits.pub/2025/january-update/index.html
- **Kind:** blog/research post (lab update)
- **Read from:** full text — and the full text is only ~5.3k characters. This month's update is a single note ("Dictionary Learning Optimization Techniques") and the page ends when that note ends; no further posts, no appendix, no figures. Every number below is one stated in the prose; nothing was inferred from a plot because there are none.
- **Relevance to us:** 2 (useful)

## What they wanted, and why

They want other groups to be able to reproduce their sparse-autoencoder and crosscoder training run from a written description, because the field keeps re-deriving the same recipe decisions in isolation. The framing is deliberately modest — the page asks to be read as a colleague sketching preliminary experiments at a lab meeting, not as a paper. Crucially, they say up front that they have **not extensively ablated** the choices they are publishing: this is a snapshot of a working configuration, offered as a starting point rather than as evidence about which parts matter. The larger goal is shared infrastructure: if everyone normalises inputs and scales sparsity penalties the same way, results from different labs and different model widths become comparable.

## What they studied

Not a model and not a behaviour — a **training procedure** for dictionary learning on transformer activations. The objects are the encoder and decoder weight matrices of a sparse autoencoder, the per-feature log thresholds, encoder and decoder biases, and the sparsity and pre-activation penalty coefficients. The same recipe is stated to cover **crosscoders** as well as SAEs, which is what makes it worth reading for anyone training a dictionary across two activation sites rather than one: the notation distinguishes the input space of size n from the output space of size o, which is the only structural difference between the two cases.

## How they did it

Encoder: a linear map plus bias, pushed through a **JumpReLU** — keep the value if it exceeds the exponentiated threshold, zero otherwise — so the sparsity decision is a hard gate at a learned per-feature height rather than shrinkage toward zero. Decoder: sparse codes times decoder weights plus a decoder bias, reconstructed against the target with squared error. Two penalties sit on top of the reconstruction loss: a tanh penalty on each feature's contribution scaled by how much of the token it fires, and — the part they flag as the useful trick — a **pre-activation loss** that penalises features sitting below their threshold, weighted by the decoder row norm. Training: Adam at beta1 0.9, beta2 0.999, no weight decay, linear learning-rate decay to zero over the final fifth of training, batch 32,768 chosen to sit under the critical batch size, gradient-norm clipping at 1, and the sparsity coefficient ramped linearly from zero across the whole run.

Three initialisation choices carry most of the recipe. Decoder rows are drawn uniformly within the inverse square root of the input dimension. **Encoder rows are tied to the decoder** (transposed, rescaled by n/m) when input and output spaces coincide. And the encoder bias is set by inspecting a data subset and choosing, per feature, the constant that makes that feature fire at a rate of 10,000/m of the time — so in aggregate about 10,000 features are live on every datapoint at step zero. They call this bias-initialisation step important for avoiding dead features, which is an admission that dead features are a *starting-condition* problem and not only an optimisation one. Inputs are shuffled and scaled by a single constant so that the average L2 norm equals the square root of the input dimension — the point being that the same sparsity coefficient then means the same thing for datasets harvested from transformers of different widths. Finally they note that with an unconstrained decoder norm a feature's true activation is the code times the decoder row norm, so for analysis they fold that norm into the encoder and renormalise the decoder to unit columns, which leaves predictions identical but makes the reporting code simpler.

## What counts as an explanation here

A recipe, not an explanation. The artefact is a reproducible configuration: functional forms, penalty terms, constants, initialisations, optimiser settings. Nothing here claims to say what any feature means. What it does contribute to our project is a **convention** — the norm-folded decoder, where feature activation is the plain code and decoder rows are unit length — which is the convention that makes "this feature fires at strength X" a comparable quantity across layers, widths and experiments. That convention matters to us because every intervention we run multiplies an activation by a factor, and whether the decoder row is unit-norm changes what that factor means.

## How they judged success

By none of the usual metrics — there is no loss-recovered number, no L0, no dead-feature count, no autointerp or human rating anywhere on the page. The stated success criterion is engineering: does the recipe produce a working dictionary with few dead features, and is it legible enough for another lab to follow. Two things stand in for ablations. One is a **correction notice**: an earlier version of the page wrote the decoder init range as uniform within 1/n rather than 1/√n, which is exactly the kind of quiet scale error that silently changes what a fixed sparsity coefficient does. The other is a stated comparison to prior work: they adopt Rajamanoharan et al.'s JumpReLU but let the straight-through gradient reach **all** parameters rather than only the thresholds, and they use a tanh sparsity penalty in place of that paper's own penalty. Unstated ablations are therefore genuinely unstated, and the entry should be cited as a recipe rather than as a result.

## What they found

The content is the recipe plus its rationalisations, and three of those are substantive enough to carry forward. First, the **pre-activation loss** is presented as the fix for dead features: penalising features that fail to clear their threshold means a dead feature receives a gradient telling it to grow, instead of receiving none. They caution that because this term pushes on *every* inactive feature it fires far more often than the other penalties, so its coefficient should be scaled down by roughly the typical feature firing density — the constants given (penalty coefficient 3×10⁻⁶, tanh coefficient 4 with the activation inside a factor of 4, tolerance 2, sparsity coefficients around 10–20) are consistent with that scale. Second, the **per-feature bias initialisation targeting 10,000 fires per datapoint** is a way of setting every feature live at step zero, and their claim that this is important for avoiding dead features says that the usual diagnosis (L1 shrinking features to zero before they find a direction) is only half the story — some features never start. Third, **norm-matched input scaling** is the one change here that matters for comparing results across model sizes, and it is the same device that earlier recipe notes in this series reach for: normalise the input distribution, then one sparsity setting transfers. The remaining items are conventional — zero decoder bias, threshold initialised small and positive, tied encoder rows in the autoencoder case and untied in the crosscoder case.

## Limits and open problems they name

They name one, squarely: they **have not extensively ablated** the decisions in the recipe, so nothing on the page tells you which of the choices is load-bearing. That is a larger caveat than it looks, because the recipe contains at least four independent candidates (pre-act loss, bias initialisation, tied encoder init, norm scaling) and the reader cannot tell whether any of them is individually necessary. Other limits are implicit in the framing — the page calls itself preliminary lab-meeting material, and the only quantitative claim is the aggregate number of features firing at initialisation. There are no results on how the resulting dictionaries score on interpretability, no comparison against the variants that the August 2024 update had already tried to referee, and no statement about how the recipe behaves at the widths where dead features were previously reported to dominate.

## What we take from it

Three reusable things and one warning. **Take the pre-activation loss as a candidate fix for dead features**, and take the accompanying scale rule seriously: a penalty that touches every inactive feature must be weighted by firing density or it will dominate the objective — a mistake that would show up in our own runs as an unexplained collapse in L0, not as an error. **Take the bias-initialisation-to-a-target-firing-rate as a diagnostic frame**: a feature that is dead at the end may have been dead at the start, and the number of features live on a datapoint at step zero (10,000 here) is a quantity worth logging, because it converts "dead features" from a modelling mystery into a starting-condition bug. **Take input norm normalisation as a prerequisite for any cross-width comparison we make**: without it, a fixed sparsity coefficient means different things for activations from models of different widths, and every width trend we report in this space is at risk of being a norm artefact. **The warning** is about how this class of page should be cited: it is a working configuration with one acknowledged post-hoc correction, not an ablation study, so nothing in it should be used as evidence that any particular tactic *works* — only as a description of a configuration that ran.

## Tags

unit: feature | weights
form: dictionary
method: SAE | training-interpretable | other
eval: faithfulness | other
goal: understanding | evaluation-of-methods
