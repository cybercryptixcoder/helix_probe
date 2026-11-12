# Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space

- **Key:** arxiv-2203.14680
- **Authors / organisation:** Mor Geva, Avi Caciularu, Kevin Ro Wang, Yoav Goldberg; Allen Institute for AI, Bar-Ilan University
- **Date:** 2022-03
- **Link:** https://arxiv.org/abs/2203.14680
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Building on the key-value view of FFN layers (arxiv-2012.14913), the authors ask how an FFN update changes the model's next-token prediction. They view the residual representation as a distribution over the vocabulary and each FFN output as an additive update to it, then decompose that update into per-neuron sub-updates that can be read in vocabulary space. The goal is a mechanism-level account of how FFNs build predictions, and to show that this reading is useful enough to control the model.

## What they studied
WikiLM (16 layers, word-level vocabulary of about 268k, d = 1024, 4096 FFN units) and GPT-2 (small, 12 layers, for annotation; medium, 24 layers, for promotion and toxicity experiments). Units: individual FFN value vectors (columns of the output matrix) and their activation-weighted sub-updates.

## How they did it
The FFN output is written as a sum over units of activation coefficient times value vector. Each value vector is projected through the embedding matrix to score every token; the top 30 tokens are its readable content. Graduate-student annotators labelled recurring concepts (semantic, syntactic, names) in the top tokens of sampled value vectors (160 for WikiLM, 120 for GPT-2), with random vectors as a baseline. To test whether sub-updates work by promoting or suppressing tokens, they collected "saturation" events (the eventual prediction becomes and stays top-1) and "elimination" events (the current top candidate drops), and compared the scores the dominant 10 sub-updates assign to the promoted versus eliminated token. Two applications follow. For toxicity, they hand-picked 10 value vectors whose projections contain non-toxic words (found by searching for words like "safe" and "thank") and fixed their activations to 3 during generation on RealToxicityPrompts' challenging subset (1,225 prompts), comparing with Self-Debiasing, WordFilter and automatically selected vectors. For early exit, they cluster dominant sub-updates and exit when the current layer's sub-updates resemble clusters seen at past saturation events.

## What counts as an explanation here
A vocabulary-space reading of individual weight vectors: each value vector is described by the tokens/concepts it promotes, and the FFN output by which few sub-updates dominate. Partial and descriptive, but used predictively: if a vector promotes "safe" concepts, turning it up should lower toxicity.

## How they judged success
Annotation coverage (share of top tokens falling into a concept) versus random vectors; per-layer coverage; promotion vs elimination scores of the target token in dominant vs random sub-updates; toxicity and severe toxicity (Perspective API) with perplexity as a fluency control, against baselines; early exit accuracy and fraction of layers saved against layer-wise trained classifiers.

## What they found
Concept coverage of value-vector top tokens is 55.1% for WikiLM versus 22.7% for random vectors, and 37% for GPT-2 versus 16%; 40 to 70% (WikiLM) and 20 to 65% (GPT-2) of top tokens per layer belong to concepts, mostly semantic. Promoted tokens get much higher maximum scores from dominant sub-updates than eliminated ones (1.2 vs 0.5 in WikiLM; 8.5 vs 4.0 in GPT-2), with eliminated tokens near zero: FFN updates work mainly by promotion, not by suppressing the old candidate. A small set of last-layer vectors (about 1 to 2%) promote rare tokens to flatten confidence without changing the top-1. Boosting 10 vectors cuts toxicity from 58.5% to 30.8% (47% relative; severe toxicity halved) at a perplexity cost from 21.7 to 25.3, beating Self-Debiasing (37%) and WordFilter (20%); automatically chosen vectors only give 10%. The early-exit rule reaches 94.1% accuracy saving 20% of layers, matching trained classifiers.

## Limits and open problems they name
Only individual vectors, not combinations; interaction with attention not studied; only decoder-only LMs; manual labelling is slow, subjective and tokenizer-dependent; toxicity is reduced, not eliminated.

## What we take from it
A cheap weight-reading tool (project W_out columns through the unembedding) with a quantified baseline (random vectors) and a demonstration that such readings can drive an intervention whose effect is predicted in advance. The promotion-not-elimination finding is a concrete regularity a white-box model can encode. Warning: hand-selected vectors worked far better than automatically selected ones, which means the reading still needs human judgment, and the readout misses composition.

## Tags
unit: neuron | weights
form: description | dictionary | steering
method: weight-analysis | steering
eval: human-rating | downstream-task
goal: understanding | control/editing
