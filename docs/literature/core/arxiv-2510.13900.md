# Narrow Finetuning Leaves Clearly Readable Traces in Activation Differences

- **Key:** arxiv-2510.13900
- **Authors / organisation:** Julian Minder, Clément Dumas, Stewart Slocum, Helena Casademunt, Cameron Holmes, Robert West, Neel Nanda; work done in the MATS program (institutional affiliations not read)
- **Date:** 2025-10 (ICLR 2026)
- **Link:** https://arxiv.org/abs/2510.13900
- **Kind:** paper
- **Read from:** full text (HTML, main text; appendix only in part)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Model diffing aims to find what fine-tuning changed in a model. Many interpretability studies use narrowly fine-tuned "model organisms" (models taught a false fact, a hidden goal, or misalignment) as stand-ins for real hidden behaviours. The authors show that narrow fine-tuning leaves a strong, easily read bias in activations, even on unrelated text, which both gives a simple, powerful diffing method and warns that such organisms may be unrealistically easy to audit.

## What they studied
33 organisms across 7 models from 1B to 32B parameters: synthetic-document fine-tunes implanting false facts (Qwen3 1.7B and 32B, Llama 3.2, Gemma3 1B; 20 organisms), emergent-misalignment fine-tunes (bad medical, extreme sports, risky financial advice on Llama 3.1 8B Instruct and Qwen2.5 7B), a subliminal-learning organism (Qwen2.5 7B taught to love cats via number sequences), and taboo-word organisms (Qwen3 1.7B, Gemma2 9B). Unit: the mean residual-stream activation difference (fine-tuned minus base) at a middle layer.

## How they did it
Activation Difference Lens (ADL): run both models on about 10,000 pretraining texts, take middle-layer residual differences at the first 5 token positions, average per position. Read the average difference with Patchscope (insert it into a prompt and read next-token predictions, with an LLM-calibrated scale and multiple prompts) and with logit lens. A grader LLM judges whether the top-20 tokens relate to the fine-tuning domain, with base-only and fine-tuned-only averages as baselines. Steering: add the average difference into the fine-tuned model during generation on 20 chat prompts, scale set by binary search for coherence, and compare outputs with fine-tuning data by embedding similarity. An interpretability agent (GPT-5) gets ADL outputs plus a budget of queries to both models and must describe the fine-tuning objective; a blackbox agent gets only ordinary generations and queries. A GPT-5-mini grader scores descriptions 1 to 5 using organism-specific rubrics. A causal test replaces the activation component along the bias direction with the base model's and measures loss on fine-tuning and pretraining data. Mitigation: mix unrelated C4 data into fine-tuning at various ratios.

## What counts as an explanation here
A natural-language description of what the fine-tune taught, produced by an agent from token-level readouts and steered generations of a single difference direction. Partial: it identifies the training objective, not the mechanism.

## How they judged success
Rubric grade (1 to 5) of the agent's description against the true objective, reported as fraction of organisms reaching grade 2 or 4; blackbox-agent baseline with a larger query budget; token-relevance fraction; steering similarity to fine-tuning data; a Bayesian GLM over agent, grader and budget factors; random-vector controls for the causal test; False Fact Alignment to measure the cost of mitigations.

## What they found
With ADL and 5 queries, 91% of organisms reached grade 2 or more and 30% reached 4 or more; the blackbox agent with 50 queries managed 39% and 1%. ADL with no queries still reached 82% and 24%. The subliminal cat preference was found without queries; misalignment was detected from diffing alone in 3 of 6 EM organisms; taboo organisms are easy for blackbox agents too. The Bayesian model attributes the largest effect to ADL access. Removing the bias raises loss on fine-tuning data and lowers it on pretraining data for two of three models (Gemma3 1B inconclusive); random directions have near-zero effect, supporting an overfitting explanation. Broad chat fine-tuning leaves little trace. Mixing even 10% unrelated data strongly reduces the trace, and at 1:1 no agent averages above grade 2, though fact internalisation drops for some models.

## Limits and open problems they name
Heavy reliance on LLM agents and graders adds noise; mechanism of the bias is unclear; conditions for its appearance are not mapped; mitigations are preliminary and trade off with learning; narrow organisms may be poor proxies for realistic post-training.

## What we take from it
The baseline any weight-diff reader must beat: if a cheap activation-diff readout already recovers the fine-tuning objective, a weight-based method needs to show something extra (e.g. prediction without running data, or mechanism). Their evaluation design is reusable: known-objective organisms, rubric-graded agent descriptions, blackbox agent with larger budget as control, random-direction controls, and a statistical model over evaluation noise. Warning: our own test organisms should include data mixing so that success is not an artefact of narrow-fine-tune overfitting.

## Tags
unit: direction, layer
form: description, direction, steering
method: steering, agent, other
eval: downstream-task, ablation, benchmark
goal: safety/auditing, evaluation-of-methods
