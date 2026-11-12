# Steering Along Manifolds to Control Neural Networks (paper: Manifold Steering and the Shared Geometry of Representation and Behavior)

- **Key:** arxiv-2605.05115
- **Authors / organisation:** Daniel Wurgaft, Can Rager, Matthew Kowal, Vasudev Shyam, Sheridan Feucht, Usha Bhalla, Tal Haklay, Eric Bigelow, Raphael Sarfati, Thomas McGrath, Owen Lewis, Jack Merullo, Noah D. Goodman, Thomas Fel, Atticus Geiger, Ekdeep Singh Lubana; Goodfire with Stanford, UCL, Northeastern, Harvard, Technion
- **Date:** 2026-05-07
- **Link:** https://arxiv.org/abs/2605.05115 (post: https://www.goodfire.com/research/manifold-steering)
- **Kind:** paper
- **Read from:** full text (post plus arXiv HTML main body; final part of appendices not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Activation steering normally adds a scaled vector, which moves the representation along a straight line and so assumes the concept is linear. The authors argue that common steering failures (loss of fluency, collapsed diversity, off-target outputs) come from this flat-geometry assumption. They ask whether the curved geometry of a concept's representation is causally tied to the geometry of the model's behaviour, and whether interventions that follow that geometry give more natural control. The larger goal is principled, geometry-aware control and a link from representation to behaviour.

## What they studied
Llama 3.1 8B, layer 28 residual stream at the last token. Concepts with known ground-truth coordinates: cyclic (weekdays, months, via prompts like "what is four days after Monday?"), sequential (letters, ages), and in-context random walks on a 5x5 grid and a 9x9 cylinder using arbitrary tokens. Also a GRU world model (64-D latent state) trained on Mountain Car images, steering car position. Unit: a low-dimensional manifold in activation space and a matching manifold in output-distribution space.

## How they did it
Activations are reduced to 64 PCA dimensions, per-answer centroids are computed, and splines are fit through them (periodic or natural cubic splines for 1-D concepts, thin-plate splines for 2-D in-context tasks), giving the representation manifold. The behaviour manifold is built from next-token distributions over the concept tokens (plus an "other" bin) mapped to Hellinger coordinates (square roots of probabilities), where distances are Euclidean, with splines fit there. They test isometry by correlating geodesic distances on the two manifolds, and contrast with straight-line distances. Manifold steering moves along the representation manifold's intrinsic coordinate and maps back; linear steering interpolates straight between activations. A pullback experiment uses L-BFGS to find activation paths whose induced outputs follow the behaviour manifold, then checks how well these paths match the representation manifold. Naturalness is scored as an "energy": the cumulative Bhattacharyya distance between the steered output trajectory and the behaviour manifold. They frame all of this as geodesics under three Riemannian metrics on activation space (flat, density-based, and pulled back from behaviour through the Jacobian).

## What counts as an explanation here
A pair of fitted manifolds (representation and behaviour) plus a map between them: the claim that the model's internal geometry and its output geometry are two views of one concept geometry. It is predictive in a narrow sense: knowing where you are on the representation manifold predicts the output distribution, and steering along it predicts smooth behavioural change.

## How they judged success
Correlation of geodesic distances between activation and behaviour manifolds (versus linear distances); energy (cumulative Bhattacharyya distance to the behaviour manifold) for manifold versus linear steering, with significance test; intrinsic R² of pullback paths against the representation manifold, versus linear paths; for in-context grids, whether steering one coordinate moves only one axis; for Mountain Car, arc-length correlation and visual smoothness. Baseline throughout: linear steering.

## What they found
- Geodesic correlations between representation and behaviour: r = 0.99 (weekdays), 0.89 (months), 0.999 (letters), 0.999 (ages), 0.99 for both in-context grids; straight-line distances correlated far less (0.89, 0.53, 0.71, 0.36; 0.90 and 0.81).
- Energy for manifold versus linear steering: weekdays 0.34 vs 0.93, months 0.36 vs 1.09, letters 2.42 vs 6.95, ages 5.21 vs 13.49, about 2.8x lower on average (p < 0.001). Linear steering produced non-concept tokens along the way.
- Pullback paths optimised from behaviour matched the representation manifold better than linear paths (intrinsic R² e.g. weekdays 0.77 vs 0.42, letters 0.78 vs 0.23).
- In-context grids: steering one intrinsic coordinate moved the walk along one axis; linear steering jumped between endpoints.
- Mountain Car: smooth motion under manifold steering, blurred or ambiguous frames under linear steering; arc-length correlation 0.99 on-manifold versus 0.06 for linear distances.

## Limits and open problems they name
Concepts are simple and template-based with supervised coordinates; unsupervised manifold fitting is open. Only next-token distributions are analysed. Abstract behaviours (refusal, sycophancy, persuasion) are untested. Intermediate algorithmic variables are not manipulated. Why representation and behaviour geometry align is not established, and in general they need not.

## What we take from it
A concrete protocol for testing a predictive model under intervention: fit the variable's manifold, intervene along it, and score whether the output distribution moves as predicted, with energy (distance to the behaviour manifold) and geodesic-correlation as metrics and linear steering as the baseline. The Hellinger-coordinate trick for comparing output distributions is directly reusable. The pullback (Jacobian-induced metric from output back to activations) is a weights-and-gradients route from behaviour to internal geometry. Warning: linear interventions on curved variables push activations off-distribution, so intervention-based tests of our model must stay on-manifold or they will misjudge it.

## Tags
unit: direction, other (manifold)
form: steering, other (fitted manifold pair)
method: steering, decomposition, other (spline fitting, Riemannian geometry)
eval: prediction/simulation, other (geodesic correlation, energy)
goal: control/editing, understanding
