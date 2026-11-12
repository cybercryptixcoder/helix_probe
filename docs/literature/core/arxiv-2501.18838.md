# Partially Rewriting a Transformer in Natural Language

- **Key:** arxiv-2501.18838
- **Authors / organisation:** Gonçalo Paulo, Nora Belrose; EleutherAI
- **Date:** 2025-01
- **Link:** https://arxiv.org/abs/2501.18838 (blog: https://www.eleuther.ai/papers-blog/can-we-partially-rewrite-transformers-in-natural-language)
- **Kind:** paper
- **Read from:** full text (via WebFetch summaries of the arXiv HTML; figures not viewed)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The ultimate aim is to rewrite a network in a human-understandable form while keeping its behaviour, in the limit
replacing every feedforward layer with interpretable features (related to "microscope AI" and imitative generalisation).
This paper tests the first step: if sparse transcoder latents have good natural-language explanations, can an LLM
simulate those latents from the explanations well enough that the patched model still works? It is a direct test of
whether automated explanations are predictive enough to stand in for the computation.

## What they studied
Pythia-160M, MLP of layer 6. A TopK transcoder (k = 32, 32,768 latents, with a linear skip connection) trained on 8B
Pile tokens to approximate the MLP; a residual-stream SAE at the same layer for comparison. Explanations from the
Paulo et al. (2024) auto-interp pipeline. Simulator: Llama-3-8B-Instruct. Unit: transcoder/SAE latents.

## How they did it
For each latent and each token, the simulator is prompted with the latent's explanation and the context (target token
marked) and rates activation on a 0-9 scale; the expected value over digit probabilities is taken. That means 32,768 x 10K
prompts, about 327 million predictions. Predicted activations are quantile-normalised per latent to match the true
activation distribution (or left uncalibrated), then TopK is applied per token, and the selected latents' decoder
directions reconstruct the MLP output. Latents can be replaced in order of detection score or at random. The patched
model's next-token cross-entropy is compared with the original, the transcoder-only model, and zero-ablation of the MLP,
and losses are mapped onto Pythia training checkpoints for interpretation. They also measure each explanation's
sensitivity and specificity.

## What counts as an explanation here
A natural-language explanation per latent, used as an executable predictor (via the LLM simulator) whose outputs are
plugged back into the network. The explanation set plus simulator is a candidate replacement model for one layer.

## How they judged success
Increase in cross-entropy loss on 10K prompts (1K for the SAE) relative to the original model (3.19 nats/token),
compared against zero ablation of the MLP; random-latent substitution and uncalibrated predictions as controls; loss
expressed as the equivalent fraction of Pythia training; sensitivity and specificity of explanations versus detection
and fuzzing scores.

## What they found
Substituting the transcoder alone already costs as much loss as a Pythia checkpoint at about 25% of training (SAE about
10%). Replacing all latents with simulated activations gives loss about equal to zero-ablating the MLP (roughly a
checkpoint at 10-15% of training). Uncalibrated simulations are far worse; random substitution is worse than
zero-ablation. Using the empirical activation distribution for quantile normalisation beat zero-ablation, though the
authors could not confirm this at full scale. The core failure is specificity: explanations average about 80% specificity,
but with k = 32 of 32,768 latents even 99% would yield about 320 false actives, ten times the true count. Detection and
fuzzing scores predict sensitivity and specificity.

## Limits and open problems they name
Explanations are not specific enough (false positives dominate); simulation is very expensive; only one MLP was
rewritten, as rewriting all would break the model; quantile estimates may be biased. They suggest explanations must
also say where a feature is off, and propose contrastive explanations between similar latents.

## What we take from it
The most direct precedent for our goal and a sobering baseline: a natural-language "white-box" layer, substituted into
the network, performs about as well as deleting the layer. The test itself (substitute the predicted computation and
measure CE loss against zero-ablation and against the training-checkpoint curve) is exactly the evaluation our
predictive model should pass. Key lesson: with sparse codes, precision on inactive cases dominates, so our model must
predict when units are off, not only when they fire. Calibration of predicted magnitudes matters a lot.

## Tags
unit: feature
form: description | replacement-model
method: transcoder | SAE | agent
eval: prediction/simulation | faithfulness | ablation
goal: understanding | evaluation-of-methods
