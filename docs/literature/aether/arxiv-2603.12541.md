# As Language Models Scale, Low-order Linear Depth Dynamics Emerge

- **Key:** arxiv-2603.12541
- **Authors / organisation:** Buddhika Nettasinghe (University of Iowa); Geethu Joseph (Delft University of Technology)
- **Date:** 2026-03-13
- **Link:** https://arxiv.org/abs/2603.12541
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why

The paper asks a systems-theory question rather than an interpretability one: is the way a transformer's last-token state propagates from layer to layer, in a fixed context, describable by a small linear state-space model — and is that description good enough to *predict* where an additive intervention will matter and how it should be distributed? The motivation is that almost all practical steering and probing still picks layers by brute-force sweep or by a fixed heuristic (always steer at the last block), and there is no tractable forward model that says where the sensitivity is before you measure it. A second, more ambitious goal is scientific: if such a model exists, its quality is a measurable property of the model, so they can ask whether that property changes with scale. The larger goal is a white-box object that substitutes a computed prediction for an experimental sweep — depth response as an identified dynamic system, not a black box with empirical heuristics bolted on.

## What they studied

The GPT-2 family — GPT-2, GPT-2-medium, GPT-2-large — used as a scaling ladder with one identification pipeline and one fixed reduced order. Ten binary classification prompts: Amazon Polarity, Yelp Polarity, SST-2, IMDB, BoolQ, binary GLUE MNLI, Civil Comments toxicity, and TweetEval irony / hate / offensive. The unit of analysis is the **last non-padding token's residual-stream state**, treated as the state of a discrete-time system whose time axis is depth; the concept being steered is a single normalised mean-difference direction per layer, estimated from class-conditional means on a separate split. Everything else in the network — all other token positions — is frozen during localisation.

## How they did it

Three disjoint balanced prompt sets per dataset: a *concept* split for the per-layer direction, an *operating* split for identifying the dynamics, and a held-out *evaluation* split used only for measuring gains, nominally 400 / 200 / 200 per class. For each operating prompt they run the unperturbed model, then define a "frozen-context last-token map" by holding every non-last-token row fixed and varying only the final token's state before each block; linearising that map around the operating trajectory gives a prompt-conditioned Jacobian per layer. Steering is modelled as additive push along the concept direction at a chosen depth. To keep the surrogate small they project each layer's dynamics onto a d-dimensional basis whose first column is the concept direction and whose remaining columns are built by a Krylov-style reachability construction — average the post-injection excitation over prompts, propagate it forward through mean Jacobians, project out the next layer's concept direction, orthonormalise. The main results use d = 32. Jacobian–vector products are used directly (forward-mode, falling back to central finite differences with step 2e-3). Predicted layerwise gain is the readout vector times the product of reduced transition matrices to the top times the input matrix; empirical gain is a central difference of the concept score under ±ε push at each layer, with ε = 0.1 for the headline figures and a sweep from 0.01 to 0.5 for robustness. Agreement is scored by Pearson and Spearman correlation over the full gain curve, with top-k layer overlap demoted to a secondary diagnostic. For control they use the surrogate's own gain vector h to write the minimum-energy multi-layer schedule in closed form (u proportional to h), then bisect a single amplitude to find the smallest one hitting each target shift in the **full nonlinear model**, against uniform-all, last-layer, middle-layer, early-layer and random-single-layer baselines. Three seeds for the scaling analysis.

## What counts as an explanation here

A **replacement model**, and a deliberately local one: a 32-dimensional linear time-varying surrogate that stands in for depth propagation *within one context*, fitted around that context's own trajectory. It is not a description of what any feature means and does not claim a global law of transformer computation — the authors say plainly that construction-then-validation in the real model is essential and that the surrogate is not a substitute for the transformer in general. What it does predict is specific and checkable: the whole shape of the depthwise sensitivity curve, and from it the minimum-energy distribution of a target behavioural shift across layers.

## How they judged success

Two criteria, both against the full model. Identifiability: rank and linear correlation between predicted and empirical gain curves on a **held-out** prompt split, never the prompts used for identification. Utility: energy (squared L2 norm of the stacked coefficient vector) required to reach target shifts of 0.05 / 0.1 / 0.15 / 0.2, found by one-dimensional bisection on the full model, normalised against the LLV-optimal energy and compared with five heuristic schedules. Robustness arms: perturbation magnitude over eight values, reduced order from very small upward (to show saturation), and Krylov complement versus random orthogonal complement. Ablations and controls are of the approximation choices, not of the concept direction.

## What they found

Prediction is near-exact on GPT-2-large at d = 32: Spearman 0.99 or 1.00 on every displayed dataset, reproducing curve *shape* — late-depth ramps, broad middle-to-late plateaus, non-monotone landscapes — rather than only the argmax layer. The optimal intervention depth is task-dependent, which the authors read as an argument against any universal "steer at the final block" rule. The scaling result is the paper's headline: at fixed reduced order, mean Spearman rises 0.77 → 0.81 → 0.995 and mean Pearson 0.68 → 0.74 → 0.997 from GPT-2 to medium to large, monotone in both metrics. They are careful that this is not "bigger models steer more easily" but "bigger models are more cleanly identifiable by a compact local surrogate", and they offer width/redundancy stabilising the Jacobian and better-aligned concept directions as an *unproven* intuition. On control, the LLV-optimal schedule is lowest- or tied-lowest-energy in every dataset and target; uniform-all needs roughly two to five times the energy, last-layer-only is frequently an order of magnitude worse, and early-layer or random single-layer policies one to several orders worse. Krylov complement beats a random complement, particularly on the harder datasets; agreement is stable across the ε sweep and saturates as d grows.

## Limits and open problems they name

Local only, and prompt-conditioned by construction — no claim of a global linear law. Scaling is measured inside one family (GPT-2), so a scaling *principle* is a hypothesis rather than a result, and they say so. The monotone trend is stronger in aggregate than per-dataset, with some tasks already predictable in the smallest model and others improving only at the top. The mechanism behind the scaling regularity is explicitly unproven. Control figures come from "completed GPT-2-large control runs available in the current suite", and the experimental configs, figure scripts and processed outputs are described as forthcoming rather than released.

## What we take from it

The **method to copy**: local identification of a prompt-conditioned linear surrogate around the operating trajectory, reduced by a concept-anchored Krylov basis, with gains scored on a split disjoint from the identification set. This is the closest thing in this folder to the object our survey is aiming at — a computed prediction of intervention outcome, not an illustration of one — and it is cheap relative to a layer sweep because the surrogate is 32-dimensional. The **measure to copy**: prediction of the full sensitivity *curve* rather than the best layer, since a curve-agreement correlation is a much harder test than argmax accuracy and immediately exposes a surrogate that has merely memorised where the peak is. The **control result** is the useful operational payoff: once you can predict the curve, the minimum-energy schedule falls out in closed form and beats the heuristics by 2–5× against uniform injection. Three warnings of my own, marked as ours: (i) the empirical gain is a finite difference of a *concept score* along one fixed mean-difference direction, so this tests linearity of propagation, and never tests whether the direction is the right handle on the behaviour — a paper in this folder has repeatedly found those two things diverge; (ii) the evaluation prompts are held out but come from the same ten classification datasets and templates used for identification, so "held out" here means new prompts from the same distribution, not a new task; (iii) the two 0.99+ correlations rest on averaged gain curves, which can be smooth while per-prompt prediction is poor, and no per-prompt dispersion is reported. Read it as evidence that *depth propagation of a linear push* is well-approximated by a small linear system in GPT-2-large, and as a template for predicting intervention outcomes — not as evidence that the linear read-out is sufficient for what we want to explain.

## Tags

unit: layer
form: replacement-model
method: decomposition
eval: prediction/simulation
goal: understanding
