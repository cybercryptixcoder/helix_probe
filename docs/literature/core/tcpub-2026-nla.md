# Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations

- **Key:** tcpub-2026-nla
- **Authors / organisation:** Kit Fraser-Taliente, Subhash Kantamneni, Euan Ong (equal contribution), with Samuel Marks, Jack Lindsey, Joshua Batson and others; Anthropic
- **Date:** 2026-05-07
- **Link:** https://transformer-circuits.pub/2026/nla/index.html
- **Kind:** paper (Transformer Circuits Thread)
- **Read from:** full text (read in two parts; the exact list of five prediction tasks was not captured in detail)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
SAEs and logit-lens methods explain an activation only as a weighted sum of fixed atoms (dictionary features or
tokens), have coverage gaps, and still need a separate labelling step; supervised activation verbalisers need ground
truth labels. The authors want an unsupervised method that turns any activation directly into readable text, with
the text judged by how well the activation can be rebuilt from it. The aim is a scalable reading tool for auditing
(evaluation awareness, hidden objectives, unexpected behaviours) in production models.

## What they studied
Claude Haiku 3.5, Haiku 4.5 and Opus 4.6, at a middle-to-late layer (about two-thirds depth) of the residual stream;
released open NLAs for Qwen-2.5-7B, Gemma-3-12B, Gemma-3-27B, Llama-3.3-70B. Unit: a single residual-stream activation
vector at one token.

## How they did it
Two modules, both initialised from the target model. The activation verbaliser (AV) receives the activation injected
in place of a special token embedding and samples a text explanation. The activation reconstructor (AR) is the target
model truncated at layer l plus a learned affine map; it reads the explanation and outputs a vector. Objective:
squared error between original and reconstructed (unit-normalised) activation. The AR is trained by regression; the
AV by RL (GRPO for open models) with reward equal to negative log squared error and a KL penalty toward its
initialisation to keep text fluent. Both are warm-started by fine-tuning on LLM-written summaries of the context
(about 0.3-0.4 FVE before RL). Evaluations: fraction of variance explained (FVE) during training; steganography tests
(paraphrase, shuffle, translate explanations and check FVE); claim-level truthfulness; downstream prediction tasks;
an auditing game on a reward-model-sycophancy model organism with Claude Sonnet 4.6 agents given NLA vs SAE tools;
evaluation-awareness measurement on 16 evals with deployment controls and steering; NLA-initialised activation
oracles vs a PastLens baseline; and case studies (rhyme planning, language switching, misreported tool output).

## What counts as an explanation here
Free-form natural-language text for one activation, scored by reconstruction (an explanation is good to the extent
the vector can be recovered from it). Partial and lossy; not mechanistic (no circuit or weights). Editing the text
and re-encoding it gives a steering vector, so it supports a weak form of intervention.

## How they judged success
FVE of reconstruction (0 = predict mean, 1 = perfect); shuffled-explanation control; FVE drop under meaning-preserving
transforms (steganography check); rate of verifiable false claims; accuracy on downstream prediction/classification
tasks; auditing-game win rate vs SAE-equipped agents; agreement of an LLM grader with hand labels (97% on 186);
activation-oracle QA vs naive and PastLens baselines; intervention success when editing explanations.

## What they found
NLAs reach about 0.6-0.8 FVE, growing roughly linearly in log training steps (Gemma-3-27B: 0.38 to about 0.71-0.75;
70% in ~1.5 days on two 8xH100 nodes). Meaning-preserving transforms barely reduce FVE, so little evidence of
steganography. Downstream tasks improve with training but sometimes modestly (one task 83% to 86% on Opus 4.6).
NLA-measured evaluation awareness exceeded 5% on 10 of 16 evals, 7 of which showed 0% verbalised awareness, vs about
4% on deployment controls. In the auditing game NLA-equipped agents found the root cause without training-data
access while SAE tools did not raise win rates; however, NLA access did not consistently raise the number of
behaviours found. Editing a planned rhyme ("rabbit" to "mouse") and steering worked about half the time. Writing
quality declines with training; false-claim rate stays roughly flat.

## Limits and open problems they name
Confabulation (specific claims less reliable than thematic ones; the AR is a weak per-claim check); no mechanistic
grounding; the AV can infer beyond what the vector holds; cost (~500 tokens per activation, RL on two full models);
risk of degenerate objectives (steganography, input inversion) under more optimisation; ad hoc warm start; layer
sensitivity; some activation content may not be verbalisable; some case studies not reproducible.

## What we take from it
(1) A useful scoring principle: an explanation is judged by whether the thing explained can be reconstructed from it
(FVE), with shuffled-explanation and paraphrase controls against hidden encodings; we can apply the same test to any
description our white-box model emits. (2) Warning: high reconstruction from an expressive explainer does not imply
mechanism; an LLM explainer can smuggle inference. Our approach (reading weights) is complementary: NLAs describe
states, not computations, and do not predict what happens next. (3) Auditing-game and evaluation-awareness setups
are reusable downstream tests.

## Tags
unit: direction, whole-model
form: description
method: training-interpretable, other (RL-trained verbaliser/reconstructor)
eval: prediction/simulation, downstream-task, benchmark, faithfulness
goal: safety/auditing, understanding
