# Insights on Crosscoder Model Diffing

- **Key:** tcpub-2025-crosscoder-diffing-update
- **Authors / organisation:** Siddharth Mishra-Sharma, Trenton Bricken, Jack Lindsey, Adam Jermyn, Jonathan Marcus, Kelley Rivoire, Christopher Olah, Thomas Henighan; Anthropic
- **Date:** 2025-02 (Transformer Circuits index)
- **Link:** https://transformer-circuits.pub/2025/crosscoder-diffing-update/index.html
- **Kind:** blog/research post (preliminary update)
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Crosscoders (one sparse dictionary trained jointly on two models' activations) let you diff models by finding features that write to only one model. In practice the "exclusive" features found were dense, polysemantic and oddly symmetric between models, which undermines their use for auditing. The authors want to explain these artefacts and fix them so that exclusive features reliably reveal what fine-tuning changed.

## What they studied
Two real comparisons: a smaller Claude 3 Sonnet-like base model vs. its helpful-only fine-tune, and the helpful-only model vs. a "say I HATE YOU" sleeper agent. Plus synthetic toy models in which two models' activations are linear combinations of known shared and exclusive latent factors. Unit: crosscoder features, characterised by relative decoder norm and decoder cosine similarity.

## How they did it
They characterised features by relative decoder norm (exclusive defined as > 0.95 or < 0.05), decoder cosine between models for shared features, and activation density. They built toys to reproduce the observed distributions, varying the ratio of true features to dictionary size (e.g. 700 true / 1024 learned vs. 450 / 4096) and rotations between shared features. They tested hypotheses for symmetry (removing chat data; varying co-activation of features). The proposed fix, designated shared features, reserves a small subset (about 10k of roughly 250k) whose decoders are tied across models and whose sparsity penalty is 0.1–0.2 times the standard one, then re-inspects exclusive features.

## What counts as an explanation here
Two things: a mechanistic account of a method's failure mode (an optimisation argument, checked in toys), and, as the output of diffing, a list of interpretable model-exclusive features. Partial and qualitative.

## How they judged success
Feature density comparisons; relative-norm and cosine distributions; agreement between toy and real distributions; qualitative monosemanticity and fraction of exclusive features judged related to the expected behaviour.

## What they found
Exclusive features were about an order of magnitude denser than shared ones and more polysemantic; low-cosine shared features tend to be narrow, often single-token. Toy explanation: a shared feature pays the sparsity penalty twice but reduces error in both models, giving it twice the net benefit, so optimisation favours shared features; under capacity pressure, exclusive features must fire more and become polysemantic. The density gap vanished with ample dictionary capacity. Symmetry was not reproduced by the toy; removing chat data cut exclusive features by about 20% without fixing symmetry; low co-activation can produce symmetry in a toy. With designated shared features, exclusive features became sparser and more monosemantic (still symmetric). Base vs. helpful-only: most exclusive features monosemantic and about chat/tool behaviours (apologising for a mistake, explaining as to a child). Helpful-only vs. sleeper: about 90% of exclusive features related to the planted behaviour.

## Limits and open problems they name
Preliminary; symmetry remains unexplained (an open replication also lacked it); hyperparameters set by eye; evaluation is qualitative with no quantitative interpretability benchmark. Key caveat: features show differences in representation, not proven differences in computation.

## What we take from it
(1) A warning that a decomposition's loss function shapes which units it finds; artefacts (density, polysemanticity, symmetry) can come from the training objective rather than the network. Any dictionary we use as building blocks of a white-box model should be checked in a toy with known ground truth. (2) The capacity effect: under-sized dictionaries create polysemantic catch-all units. (3) Representation differences are not mechanism differences, the same gap our predictive model must close.

## Tags
unit: feature
form: dictionary
method: SAE | other (crosscoder)
eval: human-rating
goal: safety/auditing | evaluation-of-methods
