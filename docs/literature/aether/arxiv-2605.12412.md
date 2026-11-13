# Stories in Space: In-Context Learning Trajectories in Conceptual Belief Space

- **Key:** arxiv-2605.12412
- **Authors / organisation:** Eric Bigelow, Raphaël Sarfati, Daniel Wurgaft, Owen Lewis, Thomas McGrath, Jack Merullo, Atticus Geiger, Ekdeep Singh Lubana (Geiger and Lubana equal senior contribution); Goodfire, with Wurgaft also at Stanford
- **Date:** 2026-05-12 (research post "Meandering on Manifolds: The Neural Geometry of Stories Over Time", 2026-06-23)
- **Link:** https://arxiv.org/abs/2605.12412 ; post at https://www.goodfire.com/research/stories-in-space
- **Kind:** paper (with a companion research post)
- **Read from:** full text (arXiv HTML v1, main body through Discussion; references and appendices A–H were not included in the HTML build, so per-layer results, prompts and the steering-method appendix are known only by their in-text summaries)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The Bayesian reading of in-context learning (each new token is evidence, the model re-weights latent concepts) says nothing about what those latent concepts *are* or how they relate. The authors want a hypothesis space with geometry: concepts as regions of a low-dimensional metric space, beliefs as distributions over it, and in-context learning as a smooth path through the resulting space of distributions. Story reading is the testbed because the belief being tracked is obvious to a human — what emotional state the story is in right now — and changes sentence by sentence. The larger aim is to make the Bayesian story of ICL quantitatively checkable inside a real model, and to unify it with geometric accounts of concept representation imported from cognitive science.

## What they studied
Llama-3.1-8B-Instruct, run in 4-bit weight quantisation. The unit of analysis is a *belief state*: a six-dimensional vector of graded emotion judgments (happiness, sadness, anger, surprise, fear, disgust, each 0–10), recorded once per sentence of a story. Two domains are structured by prior theory — Emotions and Genres (adventure, classic, lighthearted, melancholy, tragic) — and a third, Arbitrary, is deliberately unstructured and acts as a control. Data is SimpleStories: 2500 synthetic short stories for training (500 per style category) plus 500 held out.

## How they did it
Behavioural readout: prefix the model with the story up to sentence *t*, ask how much a concept applies on a 0–10 scale, and take the probability-weighted expected integer as that sentence's belief value (so it is a soft expectation, not a single sampled answer). Representational readout: the same prefixes are fed with *no* question attached, and the residual stream at the final token is collected per layer (4096-d). Two manifolds are then fitted by UMAP/PCA — one to the behaviour matrix, one to the activations — with the fitting data deliberately chosen as the top-1000 most extreme sentences per concept so the manifold edges are defined by real examples. Structure is compared by collapsing each concept to its centroid, building pairwise L2 distance matrices, Ward-clustering them into hierarchies, and correlating the behaviour and activation matrices (an RSA-style move). Causality is tested by activation addition, with two vector families: the normalised linear-probe weight vector and a difference-in-means vector between concept and non-concept activations. Finally, steering is measured not only on the target concept but on all six, so that off-target drift becomes a dependent variable.

## What counts as an explanation here
A geometric and probabilistic model, not a description: a manifold plus a metric plus a trajectory, with linear probes as the bridge between the manifold in behaviour space and the manifold in activation space. It is explicitly partial and low-dimensional (six concepts, three domains, one model) and it is predictive in two directions — probes predict the per-sentence belief curve from raw story activations, and the geometry of the behavioural manifold predicts the *pattern* of steering side effects.

## How they judged success
Probe RMSE on held-out stories, calibrated with isotonic regression. Correlation of behaviour-space and activation-space concept-distance matrices (Pearson *r*). Agreement of the Ward hierarchies inferred from the two spaces. Comparison of emotion centroids against human valence–arousal ratings (Russell & Mehrabian data). For steering: change in target-concept belief versus mean change in the other five, plus out-of-sample prediction of the cross-concept steering matrix from centroid distances. The Arbitrary domain is the control throughout — a real effect must be weaker or absent there.

## What they found
- Belief dynamics are decodable. Layer-9 linear probes predict the per-sentence emotion curve with RMSE 0.09 (Emotions), 0.09 (Genres), 0.11 (Arbitrary) — from stories that never mention the queried concept.
- Behaviour and representation manifolds agree. Concept-distance matrices correlate at *r* = 0.92 (Emotions) and *r* = 0.89 (Genres) between the two spaces, dropping to 0.71 for Arbitrary; the Ward hierarchies come out identical for the two structured domains.
- The emotion geometry recovers human structure. Centroid distances in the behavioural manifold match human valence–arousal ratings of the same six emotion words at *r* = 0.93.
- Steering shifts the trajectory along the manifold rather than overriding behaviour, and it drags neighbours with it: steering sadness raises anger and lowers happiness, i.e. entanglement follows geometry.
- Entanglement is *predictable*: distance between concept centroids in the behavioural manifold correlates with the size of off-target steering effects at *r* = 0.65 (Emotions) and 0.42 (Genres), and a linear model predicts the held-out cross-concept steering matrix. Regrouping concepts by the top-level hierarchy split makes the off-target effect on the *other* cluster vanish for both structured domains, and the Arbitrary domain shows the mirror image — weak on-target, strong off-target.
- Method detail worth keeping: probe-weight steering at a single layer washes out, because later layers undo it; steering across a span of seven layers was needed. Difference-in-means steering works at one layer, but has a smaller maximum effect on the target — less collateral, less punch.

## Limits and open problems they name
Domains and concepts are hand-picked from prior theory (six each); the authors flag auto-interpretability as the way out. Concepts are treated as unitary, non-compositional and story-global, rather than attached to a character or a span. Only one model, one dataset of synthetic stories, and emotions plus genres — no claim that the geometry generalises to other conceptual domains. How these spaces interact with uncertainty in long-form *generation* is left open, as is whether a steering method could be designed that respects the manifold rather than adding a flat vector to it. Appendices with the layer sweep and prompt set are outside what I read.

## What we take from it
A method and a measure. The method: fit the manifold on extreme examples only, collapse concepts to centroids, and compare spaces by distance-matrix correlation rather than by eyeballing UMAP plots — that is what turns "these look similar" into *r* = 0.92 with a control domain at 0.71. The measure: **entanglement as a first-class outcome**. Reporting only on-target steering effect hides the fact that a "sadness" vector is also partly an "anger" vector; measuring the full target × query matrix and then showing it is predicted by centroid distance is a cheap, strong test that a steering direction corresponds to a region of a real geometry rather than to an arbitrary linear functional. Two warnings: single-layer probe-weight steering is silently cancelled downstream, so any steering result of ours must report the layer span; and a low-dimensional manifold can be fitted to almost anything, which is why the Arbitrary control and the identical-hierarchy test carry the argument.

## Tags
unit: direction | feature
form: direction | probe | steering
method: probing | steering | decomposition | other (dimensionality reduction + RSA-style distance matrices)
eval: prediction/simulation | downstream-task | benchmark | ablation (Arbitrary-domain control)
goal: understanding | science | control/editing
