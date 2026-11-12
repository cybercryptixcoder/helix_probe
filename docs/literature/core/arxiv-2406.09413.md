# Interpreting the Weight Space of Customized Diffusion Models (weights2weights)

- **Key:** arxiv-2406.09413
- **Authors / organisation:** Amil Dravid, Yossi Gandelsman, Kuan-Chieh Wang, Rameen Abdal, Gordon Wetzstein, Alexei A. Efros, Kfir Aberman; UC Berkeley, Snap Inc., Stanford (affiliations inferred from acknowledgments and project hosting, not read from the author list)
- **Date:** 2024-06
- **Link:** https://arxiv.org/abs/2406.09413
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
They ask whether the weights of many fine-tuned copies of one diffusion model share simple structure, so that the space of models can itself be navigated like a latent space. If identity-specific fine-tunes lie in a low-dimensional linear subspace, one could sample new models, edit a model's semantics by moving its weights along a direction, and project a single image into a full model. This treats weights as data and seeks interpretable, linear directions in weight space.

## What they studied
About 65,000 identity-specific fine-tunes of Realistic Vision v5.1 (a Stable Diffusion 1.5 checkpoint). Each is a DreamBooth rank-1 LoRA on query and value projections of cross-attention, flattened to 99,648 parameters. Identities are synthetic, generated per CelebA image so they inherit CelebA binary attribute labels. Smaller extensions: 120 dog-breed models and 197 car-type models. Unit: the LoRA weight vector.

## How they did it
PCA over the set of LoRA weight vectors; the first 1,000 components form the "w2w" basis (10,000 for inversion). Sampling: fit an independent Gaussian per component coefficient and draw new coefficients. Editing: train linear classifiers on weights to predict CelebA attributes; the least-squares normal becomes an edit direction mapped back to full weight space, applied as weights plus a scaled direction, with scale tied to the largest projection seen in training. Edits compose additively and can be delayed to later denoising steps. Inversion: optimise only the basis coefficients to reconstruct a single image under the denoising loss. Out-of-distribution inputs (paintings, cartoons) are projected the same way.

## What counts as an explanation here
Linear directions in weight space that correspond to human-named attributes (gender, chubby, narrow eyes, beard), plus a low-dimensional basis that spans the model population. Partial and data-bound: the directions only exist for labelled attributes and only within the span of the training models. It predicts what an edited model will generate in a qualitative sense.

## How they judged success
Identity preservation (ID score: MTCNN face detection plus FaceNet embedding similarity), LPIPS for unintended changes, CLIP score for edit-text alignment (noted as noisy), and two-alternative forced-choice user studies. Editing baselines: prompting with the attribute, Concept Sliders adapted to subjects. Inversion baselines on 100 FFHQ faces: single-image DreamBooth-LoRA, multi-image DreamBooth-LoRA (pseudo upper bound), Celeb-Basis, IP-Adapter FaceID. Ablations over number of PCs and number of models.

## What they found
Editing ID score: w2w 0.45 / 0.45 / 0.72 for gender / chubby / eyes, versus 0.39 / 0.29 / 0.52 (prompting) and 0.33 / 0.33 / 0.53 (Sliders). Users preferred w2w over Sliders 71.6% and over prompting 87.2% (25 participants). Inversion ID 0.64 from one image versus 0.43 for single-image DreamBooth-LoRA and 0.69 for multi-image, and above IP-Adapter FaceID (0.62) and Celeb-Basis (0.60); about 55 s versus about 200 s, with 10,000 rather than 99,648 free parameters. More models reduce entanglement between directions (e.g. male and beard). Editing works best at 1,000 PCs; inversion at 10,000 (20,000 overfits).

## Limits and open problems they name
Inherits dataset biases; correlated attributes become entangled directions; edit vocabulary limited to available labels; space only spans identities well represented in the model set (e.g. babies are poorly covered). Misuse risk for identity manipulation.

## What we take from it
A clean demonstration that, given a population of fine-tunes from one base, simple linear tools (PCA plus linear probes on weights) recover semantic, editable directions, and that steering in weight space has predictable effects. For reading a single network it says little, but for weight diffs (fine-tune minus base) it suggests the diff population can be low-rank and linearly interpretable. Measurement template: pair a target-attribute metric with a preservation metric (ID score, LPIPS) and a user study. Warning: directions found by probing are correlational and inherit label co-occurrence.

## Tags
unit: weights, direction
form: direction, steering
method: weight-analysis, decomposition, probing, steering
eval: downstream-task, human-rating
goal: control/editing, understanding
