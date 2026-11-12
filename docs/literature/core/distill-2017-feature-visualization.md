# Feature Visualization

- **Key:** distill-2017-feature-visualization
- **Authors / organisation:** Chris Olah, Alexander Mordvintsev, Ludwig Schubert; Google Brain / Google Research (Distill)
- **Date:** 2017-11-07
- **Link:** https://distill.pub/2017/feature-visualization/
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors want a reliable way to see what a unit inside a vision network responds to, as one of the basic building blocks of interpretability. Their approach is to synthesise an input by optimisation instead of only searching the dataset, because optimisation can separate what causes a unit to fire from what merely co-occurs with its triggers. The article is mostly a careful tutorial on what makes such optimisation work (and fail), and on how to show several facets of one unit or the interaction of several units. It is a step toward labelling the "variables" of a network so that circuits between them can later be studied.

## What they studied
GoogLeNet / InceptionV1 trained on ImageNet, mainly layers mixed4a, mixed4e and mixed5a (an appendix visualises every channel). Units: single neurons (one spatial position), channels, whole layers, class logits, and directions in activation space.

## How they did it
Starting from random noise, they run gradient ascent on the input image to maximise an objective: a neuron, a channel (the default for most figures), a whole layer's activation (DeepDream), or a class logit versus the softmax probability. To expose multiple facets they add a diversity term (negative pairwise cosine similarity of the Gram matrices of a batch of visualisations). To study neuron interactions they optimise sums of neurons, random directions, and interpolations between two channels with shared and separate image parameterisations. Because naive optimisation produces adversarial high-frequency noise, they compare three regularisation families: frequency penalties (total variation, blurring, bilateral filtering), transformation robustness (random jitter, rotation, scaling each step), and learned priors (GAN/VAE latent spaces). They also change the parameterisation (preconditioning): optimising in a decorrelated Fourier basis scaled to equal energy, with colours decorrelated via a Cholesky factor of the ImageNet colour covariance. Reported recipe: 2560 Adam steps at learning rate 0.05, with padding, jitter up to 16 px, scaling 0.95 to 1.05, rotation up to 5 degrees.

## What counts as an explanation here
A picture: a synthesised input (or a small diverse set) that maximally drives a unit, read by a human and paired with dataset examples. It is a label for one variable, not an account of how it is computed. Partial by design; it does not predict activations on new inputs.

## How they judged success
Qualitative only: visual inspection of whether images are interpretable and free of high-frequency artefacts, and agreement with top dataset examples. No quantitative metric; they note that fair comparison across methods is hard because of hyperparameters, and that the optimisation has not converged.

## What they found
Logit objectives give better images than probabilities (which can be raised by suppressing other classes). Small transformation robustness plus decorrelated, Fourier-space parameterisation yields much cleaner images without a learned prior. Diversity reveals distinct facets (e.g. mixed4e unit 55 responds to cats, foxes and cars). Random directions are often interpretable but less often than basis neurons; neuron arithmetic (adding two neurons) composes visually.

## Limits and open problems they name
Visualisations can exploit the network with adversarial patterns; diversity terms add unrelated artefacts; learned priors blur what comes from the model versus the prior. Some neurons mix unrelated concepts, so neurons may not be the right unit, and they say they have almost no clue how to pick meaningful directions. They state that the method alone will "never give a completely satisfactory understanding" and must be combined with other tools.

## What we take from it
A labelling tool, not a predictor: useful to name units or directions that our weight-reading identifies, but its outputs are one maximal example and carry no information about recall or weak activations. The parameterisation/regularisation recipe is the standard to reuse for vision. Warning: optimisation can produce off-distribution superstimuli, so labels must be checked against dataset activations across the full range.

## Tags
unit: neuron | direction | layer
form: description
method: other (input optimisation)
eval: human-rating
goal: understanding
