# Predictive Concept Decoders: Training Scalable End-to-End Interpretability Assistants

- **Key:** arxiv-2512.15712
- **Authors / organisation:** Vincent Huang, Dami Choi, Daniel D. Johnson, Sarah Schwettmann, Jacob Steinhardt; Transluce
- **Date:** 2025-12-17
- **Link:** https://arxiv.org/abs/2512.15712
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Instead of hand-built interpretability agents, the authors train an interpretability assistant end to end: it must predict a model's behaviour from its activations, but only through a sparse, inspectable concept bottleneck. The idea is that prediction gives a scalable training signal (no labels needed), while the bottleneck keeps the intermediate representation legible. The larger goal is making model internals readable to humans and checkable during audits.

## What they studied
Subject model Llama-3.1-8B-Instruct (d = 4096), reading activations at layer 15. Unit: a learned dictionary of 32,768 concept directions with top-16 sparsity, plus a decoder that answers questions.

## How they did it
The encoder is a linear map from one layer's activation to 32,768 concepts, keeps the top k = 16, and re-embeds them; it never sees the question. The decoder is a LoRA copy of the subject model that receives the encoded concepts as soft tokens at layer 0 followed by a natural-language question; it never sees raw activations. Pretraining: jointly train both on FineWeb, splitting passages into 16-token prefix/middle/suffix and predicting the suffix from the encoded middle, with an auxiliary loss to revive dead concepts (without it nearly a third died; with it over 90% stayed active at 72M tokens). Budgets from 9M to 144M tokens were compared. Fine-tuning: freeze the encoder and train the decoder on SynthSys(8B) user-attribute questions, holding out gender and age, mixed 50% with FineWeb. Case studies: jailbreak awareness (50 harmful actions in three templates), hidden "secret hints" for prime questions, injected concept vectors from Lindsey's introspection work (58 concepts), and auditing decoder claims about refusals and decimal-comparison errors against active encoder concepts.

## What counts as an explanation here
Two levels: a sparse concept dictionary (each concept auto-described in natural language) and the decoder's natural-language answers about what the model is doing or will do. The decoder is a learned predictive surrogate; the bottleneck is the inspectable part, so a decoder claim can be audited against which concepts were active. Partial, single layer and token.

## How they judged success
Encoder precision: auto-interp simulator score (Pearson correlation on 400 sampled concepts). Encoder recall: accuracy of a threshold classifier on the best single concept per user attribute. Decoder: multiple-choice accuracy on held-out SynthSys attributes. Case studies judged by GPT-5-mini (awareness/instructions/refusal; relevance of verbalised concept). Baselines: LatentQA (same decoder, no bottleneck), PCD with identity encoder, PCD with frozen SAE encoder, L2 TopK SAEs at k = 16 and 50, KL-based SAEs, and direct prompting of the subject model.

## What they found
Auto-interp and recall improve with pretraining tokens and plateau around 72 to 144M tokens; at larger budgets L2 SAEs at k = 50 overtake PCDs on auto-interp. On held-out attribute QA, PCDs approach LatentQA from 36M tokens, while a frozen SAE encoder does poorly, so joint training matters. On the Dream jailbreak template the k = 16 PCD shows about 50% awareness versus under 30% for all other methods; removing the bottleneck more than triples performance on the 3 Words template. Prompting the model about secret hints mostly yields a fabricated "clever trick"; the no-bottleneck variant reveals hint use best. PCDs verbalise injected concepts more often than LatentQA or self-report, but SAE dictionaries surface more relevant features. Auditing: a legal-liability concept is among top concepts in 48 of 50 refusals, while the decoder cites legal liability in about 50%; date concepts appear in over 90% of decimal-comparison errors.

## Limits and open problems they name
Scaling plateau; single linear encoder reading one layer and one token; off-distribution when changing k or removing the bottleneck; mixed evidence on whether the bottleneck helps; legibility to the decoder is only a proxy for human legibility; corroboration cannot settle causality (e.g. safety vs legal reasons for refusal); dependence on judges and question phrasing; one subject model and one corpus.

## What we take from it
The closest design to ours: a predictive model of the network with an interpretable bottleneck, trained on next-token prediction as free supervision. Reuse: the precision/recall evaluation of a concept dictionary, the bottleneck-vs-no-bottleneck ablation as a measure of the "interpretability tax", and the "audit the decoder's claim against active concepts" check. Warning: the decoder is itself a black box that can be right for reasons not visible in the bottleneck, and nothing here reads weights; it is activation-based. The plateau suggests that more data alone will not close the gap.

## Tags
unit: feature | direction
form: dictionary | replacement-model | description
method: SAE | decomposition | other
eval: prediction/simulation | downstream-task | faithfulness
goal: understanding | safety/auditing
