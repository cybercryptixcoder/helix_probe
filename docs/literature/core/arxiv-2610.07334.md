# Weight Oracles: Reading Neural Network Weights with Language Models

- **Key:** arxiv-2610.07334
- **Authors / organisation:** Krishna Kabra, Constantin Venhoff, Christian Schroeder de Witt; University of Oxford
- **Date:** 2026-10
- **Link:** https://arxiv.org/abs/2610.07334
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Can a language model be trained to read another network's raw weights and say what is wrong with it, without
running behavioural tests? The motivating use is safety auditing: backdoors may only show up on a trigger input
that tests never hit, but they must be written into the weights. The work has two stages: first show an LM can
learn to simulate a small transformer's computation from its weights, then train it only on benign weight
pathologies and test whether it spots real backdoors it has never seen.

## What they studied
Reader: Qwen2.5-3B-Instruct. Targets: toy 1-layer transformers (d=8, 2 heads, MLP width 16, sequence length 4,
vocabulary 1,000, 10 classes; about 2K non-embedding parameters), generated synthetically with random
token-to-class maps. Unit: individual weight matrices, fed row by row.

## How they did it
Weights are not written as text. Each row of each matrix is mapped into the LM's 2048-d hidden space by a
learned linear layer, a learned "type" embedding marks which matrix it came from, and these continuous tokens
precede a natural-language question. Stage I trains the LM through a four-step curriculum (synthetic dot
products for classification and regression, attention projections, then real small transformers generated on
the fly) to output forward-pass results. Running the full forward pass in one go failed, so they split it into
five LM calls, one per linear projection, with external code doing LayerNorm, GELU, biases and residuals.
Stage II trains an "oracle" for 29,000 steps on a rotating pool of about 4,400 models carrying 10 benign
pathologies (rank-1 injection, amplified projections, dominant token, dead neurons, noise, etc.) to answer 17
fixed diagnostic questions; no backdoored model is ever seen. At test time, answers to 13 detection questions
are turned into anomaly scores and combined. Evaluation uses 100 held-out models (50 clean, 50 backdoored) under
four trigger placements (pos0, lastpos, stealth, adversarial). They also compare a scratch-trained oracle with
one initialised from the Stage I simulator, ablate matrices by zeroing them, and probe the LM's layers.

## What counts as an explanation here
A trained reader that answers fixed questions about a weight set; the output is an anomaly score, not a
mechanism. In Stage I the reader acts as a learned simulator of the target (it predicts outputs), which is closer
to a predictive model but only for one linear projection at a time.

## How they judged success
Stage I: holdout accuracy of predicted outputs on unseen transformers, compared against a shortcut classifier
that ignores weights. Stage II: AUROC (overall and per attack type) and TPR at fixed FPR, over five runs.
Baselines: total L2 norm of the weights (null) and a hand-built statistic combining V/O-pathway norms and singular
values. Controls/ablations: removing type embeddings, lower learning rate, sim-init vs scratch, per-matrix
zeroing, gradient attribution, layer-wise probes of the reader.

## What they found
Stage I: the decomposed chain reaches 99.0% holdout accuracy on unseen real transformers; a single-pass model
stalled at 45.1%, equal to the weight-ignoring shortcut. Dot-product learning showed grokking (about 10% then
about 92% near step 2,200), and failed without type embeddings or with a 3x lower learning rate. Stage II: on the
pos0 cohort the oracle reaches AUROC 0.93 ± 0.04 (94% TPR at 20% FPR) against 0.445 for L2 norm and 0.752 for the
V/O composite (the figure shows different baseline values, 0.410 and 0.927, an inconsistency in the paper). On
the mixed threat distribution composite AUROC is 0.81, per type 0.74 to 0.89. Simulator initialisation helps on
pos0 but lowers overall AUROC (0.73). Zeroing W_O causes the largest drop, but only 0.04, so the signal is spread
out; backdoored models produce about 2x stronger gradients through W_V.

## Limits and open problems they name
Only ~2K-parameter toy models; one token per weight row grows with model size and compression is untested. The
oracle may detect statistical correlates of backdoor pathways rather than the mechanism (lastpos 0.74 hints at
this). A 20% false-positive rate is too high to deploy. Backdoors are narrow (single-token trigger, single target
class). The value of the language interface was not tested against a plain learned detector.

## What we take from it
Several direct lessons. (1) A shortcut control is essential: their single-pass model looked like it worked until
compared with a predictor that ignores weights. We need the same control. (2) Predicting the forward pass from
weights worked only when broken into per-projection steps with the nonlinearities done in code; this argues for
a white-box model that composes small, verifiable pieces. (3) Simple weight statistics (norms, singular values)
are strong baselines and must be reported. (4) Learned-projection weight tokens plus matrix-type embeddings is
one concrete input format. Warning: training on synthetic pathologies may teach correlates, not mechanisms.

## Tags
unit: weights
form: probe | other
method: weight-analysis | probing | ablation | other
eval: prediction/simulation | benchmark | ablation
goal: safety/auditing
