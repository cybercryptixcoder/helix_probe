# Towards Best Practices of Activation Patching in Language Models: Metrics and Methods

- **Key:** arxiv-2309.16042
- **Authors / organisation:** Fred Zhang (UC Berkeley; work done at Google), Neel Nanda
- **Date:** 2023-09
- **Link:** https://arxiv.org/abs/2309.16042
- **Kind:** paper
- **Read from:** full text (HTML v2, first ~85% of the page; remaining appendix not read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Activation patching is the standard way to localise which components matter for a behaviour, but papers choose
corruption methods and metrics ad hoc. The authors ask how much these choices change the conclusions, and what
practice should be standard. The motivation is that circuit claims are only as reliable as the localisation
experiments behind them.

## What they studied
GPT-2 XL on factual recall (a new PairedFacts set of 145 prompt pairs derived from the ROME data), with GPT-2
large and GPT-J as checks; GPT-2 small on IOI (500 prompts) and greater-than (300 prompts); a 4-layer
attention-only model on Python docstring completion (200 instances); GPT-J on addition, subtraction and
multiplication. Units: layers (MLP and attention outputs per layer and token), attention heads.

## How they did it
They run activation patching (clean activations patched into a corrupted run, i.e. denoising) under systematically
varied settings and compare the resulting localisation maps. Corruption: Gaussian noising (GN) of key-token
embeddings at 3x embedding std, the ROME "causal tracing" recipe, versus symmetric token replacement (STR),
which swaps key tokens for similar tokens so the corrupted prompt stays in-distribution. Metrics: change in
correct-token probability, normalised logit difference (correct minus incorrect), and KL divergence. Patching
scope: single layer versus sliding windows of several layers. For IOI they also vary which tokens get corrupted
(S2 versus S1 and IO). They inspect attention patterns under corruption to look for out-of-distribution
behaviour.

## What counts as an explanation here
Not an explanation itself: a localisation map (which layers, positions, heads carry the effect), used as evidence
for circuit claims such as the known IOI circuit. The paper is about the reliability of that evidence.

## How they judged success
Agreement with previously established circuits (IOI heads from Wang et al., greater-than heads), consistency of
localisation across methods and metrics, peak effect sizes, and attention-pattern checks for OOD behaviour.

## What they found
Choices change conclusions. In factual recall, GN gives peak effects 2x to 5x larger than STR and a clear
layer-16 MLP peak that STR does not show; on arithmetic the pattern partly reverses. On IOI, STR with probability
found 1/3 name movers, 3/4 S-inhibition heads, 1/2 negative name movers; GN found 0/3, 2/4, 2/2, plus a
spurious negative effect. Under GN, name-mover attention to IO falls from 0.58 to 0.26 with 0.21 going to S1,
suggesting OOD behaviour; restoring S-inhibition outputs recovers logit difference 1.04 under STR but 0.49 under
GN. Probability misses negative components because its floor is tiny when the corrupted run already gives the
answer low probability; logit difference catches them. Metric choice shifts token localisation (last vs middle
subject token ratio 4.33x with probability vs 1.22x with logit difference under STR). Sliding windows inflate
peaks (1.40x–1.75x the summed single-layer effects). Corrupting S1 and IO, instead of S2, recovered the name
movers. Recommendations: prefer STR, prefer logit difference (KL is acceptable for circuit discovery), start with
single-layer patching, and try multiple corrupted-token choices.

## Limits and open problems they name
Only decoder-only models at the sizes tested; only clean-into-corrupted patching; OOD evidence for GN is
tentative; their IOI runs do not fully recover the known circuit (path patching needed); the nonlinear effects of
sliding windows are hypothesised, not characterised. (The text gives GPT-J's size inconsistently.)

## What we take from it
Warnings and protocol. Any intervention test of our white-box model must fix and report corruption type, metric
and patch scope, because these alone can change which components look important. Use in-distribution
counterfactuals (STR-style) and a logit-linear metric; report several metrics. When our model predicts the
effect of an intervention, we should check it against both noising and denoising and across corruption choices,
not one configuration.

## Tags
unit: layer | head
form: graph
method: patching
eval: patching
goal: evaluation-of-methods
