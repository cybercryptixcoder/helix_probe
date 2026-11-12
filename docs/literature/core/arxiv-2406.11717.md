# Refusal in Language Models Is Mediated by a Single Direction

- **Key:** arxiv-2406.11717
- **Authors / organisation:** Andy Arditi, Oscar Obeso, Aaquib Syed, Daniel Paleka, Nina Panickssery, Wes Gurnee, Neel Nanda; independent / ETH Zurich / University of Maryland / Anthropic / MIT
- **Date:** 2024-06
- **Link:** https://arxiv.org/abs/2406.11717
- **Kind:** paper
- **Read from:** full text (main text; some appendices, e.g. exact per-model layer choices and fine-tuning comparison, not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Chat models are trained to refuse harmful requests, but how refusal is implemented internally was unclear. The authors want to show that a safety-relevant behaviour can be located in model internals precisely enough to control it, both to turn it off and to turn it on. They also want to demonstrate that such understanding exposes how brittle safety fine-tuning is, by converting the finding into a cheap weight edit that jailbreaks open-weight models.

## What they studied
13 open chat models from 1.8B to 72B: Qwen Chat 1.8B/7B/14B/72B, Yi Chat 6B/34B, Gemma IT 2B/7B, Llama-2 Chat 7B/13B/70B, Llama-3 Instruct 8B/70B. Harmful instructions from AdvBench, MaliciousInstruct, TDC2023 and HarmBench; harmless from Alpaca; 128 train and 32 validation each. Evaluation on JailbreakBench (100 harmful), 100 Alpaca harmless, and HarmBench test (159 behaviours). Unit: one direction in the residual stream.

## How they did it
For every layer and every post-instruction token position they compute a difference-in-means vector: mean activation over harmful prompts minus mean over harmless prompts. Among these candidates they pick the one that, on validation data, best removes refusal when ablated, best induces refusal when added, and otherwise changes behaviour least. Two interventions test it: directional ablation (project the direction out of every residual activation at all layers and positions) and activation addition (add the vector at its source layer to harmless prompts). They then fold directional ablation into the weights by orthogonalizing every matrix that writes to the residual stream (embeddings, attention out, MLP out, and output biases) against the direction; this is exactly equivalent and needs no gradients or harmful completions. They compare the resulting jailbreak to HarmBench attacks (GCG, GCG-M, GCG-T, human jailbreaks, AutoPrompt, PAIR, direct request), check capabilities on MMLU, ARC, GSM8K, TruthfulQA, and in Qwen 1.8B analyse how one adversarial suffix suppresses the direction using direct feature attribution of attention heads.

## What counts as an explanation here
A single direction whose presence is necessary and sufficient for refusal across many prompts, demonstrated by bidirectional causal interventions, plus a weight-level edit that implements its removal permanently. The semantics of the direction (harm, danger, or something else) is left open. Partial: it explains the switch, not how harmfulness is computed upstream.

## How they judged success
Refusal score (substring match for refusal phrases, 1/0) and safety score (Llama Guard 2 unsafe/safe) on greedy completions up to 512 tokens; HarmBench attack success rate with and without system prompt; capability retention on MMLU, ARC, GSM8K, TruthfulQA (compared to unedited model, with 99% confidence intervals); cross-entropy loss to compare ablation vs addition; for suffixes, the direction's expression at the last token and head attributions vs a random suffix of equal length.

## What they found
In all 13 models, ablating the direction largely removes refusal and yields unsafe completions on JailbreakBench, and adding it makes the model refuse harmless Alpaca prompts (shown in figures). Orthogonalized weights reach HarmBench ASR of 79.2% (Qwen 7B), 84.3% (Qwen 14B), 78.0% (Qwen 72B), on par with per-prompt GCG; Llama-2 is far more resistant with its system prompt (22.6% for 7B, 4.4% for 70B) but not without it (79.9%, 62.9%). Capabilities are mostly preserved, e.g. Llama-3 70B MMLU 79.8 vs 79.9, GSM8K 90.8 vs 91.2; TruthfulQA consistently falls by 1-3.5 points. Directional ablation looks more surgical than activation addition by CE loss. An adversarial suffix pushes the last token's refusal-direction expression close to harmless levels; the top eight contributing heads shift attention from the instruction to the suffix. The 70B jailbreak cost under $5 of compute.

## Limits and open problems they name
Untested on larger or proprietary models; the extraction method is heuristic and likely suboptimal (an existence proof, not a method study); suffix analysis is one model and one suffix; refusal and coherence metrics are each flawed; what the direction means semantically is unclear.

## What we take from it
The cleanest template we have for going from a found representation to a weight edit with an exactly equivalent effect: orthogonalizing all residual-writing matrices against a direction. That equivalence is a direct bridge between activation-level findings and weight-level reading or writing, and a testable prediction (the weight edit should reproduce the activation ablation). The selection protocol (bypass when ablated, induce when added, minimal side effects) is a good acceptance test for any direction our model claims controls a behaviour. Use substring and classifier scores together, plus capability benchmarks, as side-effect controls. Warning: a single difference-in-means direction can control behaviour without our knowing what it represents.

## Tags
unit: direction | weights
form: direction | steering
method: steering | ablation | weight-analysis | attribution
eval: ablation | downstream-task | benchmark
goal: safety/auditing | control/editing | understanding
