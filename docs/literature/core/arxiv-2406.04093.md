# Scaling and Evaluating Sparse Autoencoders

- **Key:** arxiv-2406.04093
- **Authors / organisation:** Leo Gao, Tom Dupré la Tour, Henk Tillman, Gabriel Goh, Rajan Troll, Alec Radford, Ilya Sutskever, Jan Leike, Jeffrey Wu; OpenAI (Superalignment interpretability team)
- **Date:** 2024-06
- **Link:** https://arxiv.org/abs/2406.04093
- **Kind:** paper
- **Read from:** abstract and sections (main text read; appendices only partly)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
SAEs were known to work on small models, but it was unclear how to train them at frontier scale or how to tell a
good one from a bad one. The authors wanted reliable recipes (architecture, hyperparameters, dead-latent fixes),
scaling laws that predict reconstruction quality from size and sparsity, and evaluation metrics beyond plain
reconstruction error. The larger goal is decomposing a frontier model (GPT-4) into features usable for safety work.

## What they studied
Residual-stream activations of GPT-2 small (layer 8) and a GPT-4-family model (about 5/6 of the way through), with
64-token contexts. Units: SAE latents, up to 16 million in one autoencoder trained on 40 billion tokens.

## How they did it
They replaced the L1 penalty with a TopK activation: only the k largest pre-activations are kept per token, so
sparsity is set directly and the shrinkage bias of L1 disappears; loss is reconstruction MSE alone. Dead latents
were controlled by initialising the encoder as the decoder transpose and adding an auxiliary loss that reconstructs
the residual error using the top dead latents. They swept number of latents n, sparsity k and compute, and fit
power laws for MSE (compute-optimal and at convergence), along with laws for tokens to convergence and learning
rate. They compared TopK against ReLU, ProLU/JumpReLU and Gated SAEs on the sparsity-reconstruction frontier.
Beyond MSE they measured four quality metrics: downstream loss with the reconstruction spliced in, probe loss for
61 binary tasks using 1-d logistic probes on single latents, explanation precision/recall with Neuron-to-Graph
(N2G) explanations, and ablation sparsity (how many vocabulary logits a single latent's ablation affects). A
Multi-TopK variant was trained to work across several k at test time.

## What counts as an explanation here
A feature dictionary at scale. Explanations of individual latents are short pattern descriptions (N2G graphs).
The paper is mainly about the quality of the dictionary as a substrate, not about explaining specific behaviours.

## How they judged success
Reconstruction MSE vs L0; downstream cross-entropy with spliced reconstruction (expressed as fraction recovered vs
zero-ablation, and as the pretraining compute that would give equivalent loss); probe loss on 61 tasks; N2G
precision and recall; ablation sparsity of logit effects; fraction of dead latents.

## What they found
Fitted joint law: loss falls with both n and k, and scaling in n gets steeper as k grows. Tokens to convergence grow
roughly as n^0.6 (GPT-2) and n^0.65 (GPT-4); max stable learning rate scales as 1/sqrt(n). Without fixes up to 90%
of latents die in large SAEs; with fixes only 7% are dead at 16M. TopK gives the best reconstruction-sparsity
trade-off (Gated comparable) and over 1.5x the N2G recall of ReLU at similar precision. Latent ablations affect
about 10 to 14% of the vocabulary versus about 60% for residual channels. The 16M SAE recovers 98.2% of loss
relative to zero-ablation, yet splicing it into GPT-4 gives loss equivalent to a model trained with only about 10%
of GPT-4's compute. TopK overfits to its training k; Multi-TopK fixes this.

## Limitations and open problems they name
Fixed k per token is crude; optimisation can improve; many GPT-4 latents are still not monosemantic; probe metric is
noisy and N2G only captures simple patterns; 64-token context may miss interesting behaviour. Suggested next steps:
MoE-style SAEs, and applications to steering, anomaly detection and circuits.

## What we take from it
The "equivalent pretraining compute" framing of spliced-in loss is a vivid, honest way to report how much of the
model a decomposition actually captures, and we should report fidelity this way. The four-metric battery (downstream
loss, probe loss, explanation precision/recall, ablation sparsity) is a reusable template. Warning: even a 16M-latent
dictionary leaves a large performance gap, so a white-box model built purely from SAE features will not predict
behaviour well without handling the residual error.

## Tags
unit: feature
form: dictionary
method: SAE | ablation | probing
eval: faithfulness | ablation | prediction/simulation | benchmark
goal: understanding | evaluation-of-methods
