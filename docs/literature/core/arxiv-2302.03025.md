# A Toy Model of Universality: Reverse Engineering How Networks Learn Group Operations

- **Key:** arxiv-2302.03025
- **Authors / organisation:** Bilal Chughtai, Lawrence Chan, Neel Nanda (affiliations not shown in the text read; ICML 2023)
- **Date:** 2023-02
- **Link:** https://arxiv.org/abs/2302.03025
- **Kind:** paper
- **Read from:** full text (arXiv HTML, first ~95%)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The universality hypothesis says different networks trained on the same task learn the same features and circuits. If true, interpretability results would transfer across models; if false, every model needs its own analysis. The authors test it in a setting small enough to get complete, mathematically precise accounts: networks trained to compose elements of finite groups. They propose a general algorithm the networks might use and check, across groups, architectures and random seeds, whether it is used and whether the details match.

## What they studied
One-hidden-layer MLPs (embedding size 256 per input, 128 ReLU hidden units, untied unembedding) and one-layer ReLU transformers (width 128, 4 heads, MLP width 512), trained on 40% of the multiplication table of groups C113, C118, D59, D61, S5, S6 and A5 (AdamW, weight decay 1, long training so the models grok). Units: embedding and unembedding matrices, MLP neurons, logits, all projected onto group-representation subspaces.

## How they did it
They describe the Group Composition via Representations (GCR) algorithm: embed each input as a matrix of a group representation, use the ReLU layer to multiply the two matrices, then score each candidate answer with a character (trace) that is maximal at the correct product. They then test for it in trained weights: (a) logit attribution, correlating actual logits with the logits each representation's character would predict; (b) measuring the fraction of variance in embeddings and unembeddings explained by each representation's subspace; (c) clustering MLP neurons by which representation they use and regressing neuron activity on the matrix entries of rho(a), rho(b) and rho(ab); (d) ablations, including "restricting" the model to the predicted components and "excluding" them; (e) tracking restricted and excluded loss through training as progress measures. For universality, they repeat this for 4 seeds per group and architecture and 50 seeds for the S5 MLP, recording which representations each run learns, how many, and in what order.

## What counts as an explanation here
A precise algorithm (GCR) written in the language of representation theory, plus a mapping from it to parameters: which subspaces of the embedding carry which representation, which neurons compute which product terms, how the readout forms logits. It aims to be nearly complete for each model and is predictive: from the identified representations one can compute expected logits and expected effects of ablations.

## How they judged success
Fraction of logit variance explained by character predictions; fraction of variance explained in embeddings, unembeddings and neurons; loss under ablations (restrict to the hypothesised components versus exclude them, ablate specific product terms); restricted and excluded loss over training; frequency of each learned representation across seeds; test loss.

## What they found
In the S5 MLP, two representations (sign, 1-d; standard, 4-d) carry the computation: together they explain 84.8% of logit variance; standard explains about 93% of input-embedding and 84.5% of unembedding variance; about 88% of variance in standard neurons and 99.9% in sign neurons is explained by the representation terms. Ablating the standard product term rho(ab) sends loss from about 2e-6 to 7.55; restricting to the predicted components lowers loss by about 70%. Excluding both key representations makes the model worse than chance. Training shows memorisation, circuit formation, then cleanup, with grokking during cleanup. Across all groups and both architectures, every model implements some version of GCR (weak universality holds). But which representations, and how many, differ across seeds (strong universality fails); transformers learn fewer than MLPs; simple complexity measures do not predict which ones are learned, though sign is reliably learned first. Logit explanation is high for cyclic groups (about 90 to 98%) but only about 39 to 57% for dihedral groups and one S5 seed.

## Limits and open problems they name
Toy models and a single algorithmic task; only four seeds for most settings; logit explanation incomplete for non-cyclic groups, residual unexplained; no evidence on transfer to large or realistic models; no reliable predictor of which representations a seed learns.

## What we take from it
(1) The strongest evidence that a complete, weight-level, predictive account is achievable when there is a known mathematical target: hypothesise the algorithm, then project weights onto its basis. (2) Restrict-versus-exclude ablations and restricted/excluded loss are good completeness and necessity measures for a reconstructed model. (3) A warning for us: the algorithm family may be universal while the specific parameters are seed-dependent, so a white-box model must be read from each network's weights rather than transferred. (4) Fraction-of-variance-explained of weight matrices by a hypothesised subspace is a cheap weight-only check.

## Tags
unit: weights, neuron, whole-model
form: program, description
method: weight-analysis, decomposition, ablation
eval: ablation, completeness, prediction/simulation
goal: science, understanding
