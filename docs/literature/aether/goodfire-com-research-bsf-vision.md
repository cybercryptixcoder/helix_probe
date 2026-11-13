# Uncovering Neural Geometry in Vision Models With Block-Sparse Featurizers

- **Key:** goodfire-com-research-bsf-vision
- **Authors / organisation:** Thomas Fel, Matthew Kowal, Mozes Jacobs, Dron Hazra, Usha Bhalla, Lee Sharkey, Lucius Bushnaq, Satchel Grant, Tal Haklay, Thomas Icard, Can Rager, Michael Pearce, Daniel Wurgaft, Aiden Swann, Fenil Doshi, Siddharth Boppana, Curt Tigges, Nick Cammarata, Thomas Serre, Vasudev Shyam, Owen Lewis, Thomas McGrath, Jack Merullo, Ekdeep Singh Lubana, Atticus Geiger (Merullo, Lubana and Geiger equal senior contribution); Goodfire, with Harvard, Stanford and Brown
- **Date:** 2026-07-07
- **Link:** https://www.goodfire.com/research/bsf-vision (full paper on arXiv, code on GitHub — neither was fetched)
- **Kind:** blog/research post (summarising a paper; this is the "Neural Geometry Series")
- **Read from:** full text of the post including all thirteen footnotes; the linked arXiv paper was not downloaded, so methods sections, metrics and per-experiment numbers are known only by what the post states
- **Relevance to us:** 3 (central)

## What they wanted, and why
The post starts from a concession and then attacks it: SAEs and transcoders have taken interpretability a long way while assuming every concept is one straight line in activation space, but the same lab's own work keeps finding concepts drawn as curved, multi-dimensional regions. If the decomposition's prior (a small number of 1-D atoms firing sparsely) does not match the representation's geometry (a small number of multi-dimensional regions), then the failures usually attributed to the *model* — feature splitting, redundancy, lexical clustering — may belong to the *tool*. The goal is a featurizer whose building block is a subspace rather than a direction, and the larger agenda is stated explicitly: interpretability should read the geometry of a model and let that decide what the next featurizer prior should be.

## What they studied
Two production models with no known ground truth: DINOv3, a vision backbone, and Stable Diffusion XL, a text-to-image model. Unit of analysis is a **block** — a set of directions forming a basis for a multi-dimensional subspace — plus, for the toy analysis, pre-defined manifolds stacked in superposition as ground truth. InceptionV1 curve detectors serve as the classic case study. Roughly 32,000 concepts are analysed in DINOv3 for the dimensionality claim.

## How they did it
1. **Toy model first.** Build activations by summing samples from known manifolds, i.e. stack manifolds in superposition. Run an SAE and a BSF on the same data and compare recovery of the true manifolds. The SAE fragments them; the BSF recovers them. Notably, the comparison is run with the SAE allowed a budget of top-*g* directions against a single BSF block of width *g*, so the straight-line method is not handicapped by capacity.
2. **Define the architecture.** An encoder maps an activation vector into blocks; sparsity is enforced at the *block* level — only a few blocks fire per input — rather than at the individual-coordinate level. The decoder reconstructs from the active blocks' span. Training is reconstruction error only.
3. **Three variants, one principle.** Vanilla BSF (linear encoder, block-wise TopK on each block's L2 norm), Grassmannian BSF, and group-lasso BSF differ in encoder, decoder and activation. The authors' claim is that the *principle* is doing the work: every variant recovers the toy manifolds, and applying block-sparsity to two concurrent featurizers (MFA and SMixAE) improves them too. Removing the ReLU turned out to matter across all variants.
4. **Train on real models.** Fit BSFs to DINOv3 and SDXL activations, then look at what each block's activations do: plot the block's code-space, and colour image regions by position inside the subspace.
5. **Steer inside the subspace.** Because a block is a region rather than a point, one can walk through it. Lay a grid over an SDXL block's region and decode each lattice point, generating a different instance of the concept per step.
6. **Re-examine a known feature.** Generate synthetic images of curves at varying angles, and compare how neurons, SAE atoms and BSF blocks respond as the angle rotates. Then fit the block's internal components against harmonic functions of the angle.
7. **Measure dimensionality.** Compute the **stable rank** of each block — the effective number of dimensions used — for blocks given a much larger width.

## What counts as an explanation here
A dictionary of *subspaces*: each feature is a region with an internal coordinate system and an image-level meaning for its axes, rather than a direction with a scalar activation. It is partial by construction (one featurizer at one site), but it is meant to be more predictive than a line-based dictionary in a specific sense — that the residual structure left unexplained by an SAE is not noise but geometry, and that the recovered region permits interpolation and continuous control rather than a single knob. The toy model is where the claim is verified against ground truth; the vision models are where it is claimed to generalise.

## How they judged success
Fidelity of recovery on the synthetic manifolds where ground truth is known; reconstruction quality and **minimum description length** as a joint efficiency measure on the real models (better explanation at lower description length than SAE); visual inspection of block subspaces with colour-coded position; interpretability of steering trajectories ("does walking through the region produce a coherent family of pretzels / hats / coffees"); the harmonic fit for InceptionV1 curve blocks; stable rank as a distribution over ~32,000 blocks. No held-out prediction score, probe-transfer test or intervention-recovery metric is reported in the post.

## What they found
- On the toy superposition model, an SAE fragments known manifolds across many redundant features while BSFs recover them coherently — after training, not by post-hoc regrouping. Concurrent methods (MFA, SMixAE) also recover better once block-sparsity is imposed, and the SAE was given the favourable top-*g*-vs-one-block comparison.
- In DINOv3 and SDXL, block activations rarely form lines; they form dense connected clouds that SAEs collapse to a single direction. The "arch" block traces the bottom of an arch on one side of its region and the crown on another; another block traces wrist-to-fingertip of a hand holding an object; video activations partition a wolf's body parts across blocks.
- Steering inside a block yields a family rather than a dial: walking an SDXL "pretzel" subspace generates differently twisted, braided and knotted pretzels; two-dimensional grids over other blocks vary hat brim angle / crown shape / orientation and a coffee's milk pattern, spoon position and cup design.
- On InceptionV1, neurons and SAE atoms give a *fractured* view of curve orientation; a single block captures rotation as a continuum, and the block's remaining components turn out to be higher-order **Fourier harmonics** of the angle — a structure the post says has not been documented before. This also explains a previously puzzling observation that some curve neurons wrap every 180° rather than 360°: they are reading the second harmonic.
- **Most concepts are multi-dimensional, and specifically low-dimensional**: with blocks of width 16, stable rank rarely exceeds 4, averaging two to four dimensions across ~32,000 DINOv3 concepts. The authors connect this to visual scenes being 2-D projections of a 3-D world, and call it close to a first real answer to "how often are concepts actually multi-dimensional?"

## Limits and open problems they name
Breadth over depth: two vision-side models, ground truth only in the toy setting. The claim that "block-sparsity is the right prior" is explicitly scoped — vision-language-action and other domains lay activations out along different geometry (temporal trajectories are named) and will likely need their own featurizer, with block-sparsity unlikely to be right everywhere. They expect sharper implementations to follow and describe block-sparsity as one step in a longer agenda rather than a settled answer. No claim is made about language models in the post, and no cross-model or held-out-behaviour generalisation is offered.

## What we take from it
- **A prior-as-hypothesis framing worth copying verbatim into our write-up**: a featurizer encodes an assumption about representational structure, so a decomposition's failure modes are evidence about the *assumption* first and the *model* second. This is the same move as the SAE-prior-vs-intrinsic-dimension argument we already hold — here it is tested by construction rather than by argument.
- **Block sparsity as the concrete alternative**: sparsity at the level of groups of coordinates (one block firing, all its directions at once) is a one-line change to a TopK SAE's activation function, and it is a cheap baseline our reader should have whenever we claim a direction is a single concept.
- **Stable rank as a free diagnostic**: effective dimensionality of a learned subspace is a scalar summary of how much of the allocated capacity a concept actually uses, and "rarely above 4 out of 16" is a useful prior for how wide our own subspaces should be — as is the caution that this number is model-class-specific.
- **A warning about the interpretation of "one neuron = one concept" results**: the harmonic finding says a family of seemingly separate detectors can be bases of one continuous block. Before we credit a discrete feature with a discrete meaning, check whether its neighbours in a subspace are the same concept at different parameter values.
- **The failure to note**: a post this methodologically rich reports no held-out behavioural prediction and no intervention-recovery benchmark; the evidence is reconstruction, description and steering aesthetics. That gap is exactly where a predictive white-box model earns its keep, and it is where we should aim rather than reproduce.

## Tags
unit: feature | direction | layer | neuron
form: dictionary (subspace dictionary) | direction | steering
method: decomposition (block-sparse / structured sparsity) | SAE | steering | other (toy superposition ground truth)
eval: human-rating | downstream-task (generation quality under manifold steering) | benchmark (MDL / stable rank) | ablation (SAE-vs-BSF at matched capacity)
goal: understanding | control/editing | science
