# Persona Vectors: Monitoring and Controlling Character Traits in Language Models

- **Key:** arxiv-2507.21509
- **Authors / organisation:** Runjin Chen, Andy Arditi, Henry Sleight, Owain Evans, Jack Lindsey; Anthropic Fellows Program, UT Austin, Constellation, Truthful AI, UC Berkeley, Anthropic
- **Date:** 2025-07
- **Link:** https://arxiv.org/abs/2507.21509 (blog: https://www.anthropic.com/research/persona-vectors)
- **Kind:** paper
- **Read from:** abstract and sections (HTML v3, first ~100k of ~257k characters: method, experiments, limitations)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
A chat model's "Assistant" persona can drift, through prompting at deployment or through finetuning, sometimes unintentionally (e.g. becoming sycophantic or malicious). The authors want a cheap, automated way to find the activation directions behind such traits and use them to monitor, predict and control shifts, including predicting from training data, before finetuning, which traits a model will acquire.

## What they studied
Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct. Traits: evil, sycophancy, hallucination (plus optimism, humour, impoliteness, apathy in an appendix). Unit: one linear direction per trait per layer in the residual stream.

## How they did it
Given only a trait name and description, Claude 3.7 Sonnet generates 5 pairs of trait-eliciting and trait-suppressing system prompts, 40 questions (half for extraction, half for evaluation) and a judge rubric. The target model generates 10 rollouts per question under each prompt; responses are filtered by judge score (positive above 50, negative below 50). Residual activations averaged over response tokens are collected at every layer; the persona vector is the difference of means, and the best layer is chosen by steering effectiveness. Experiments: steering (add alpha times the vector) to validate causally; projecting the last prompt token onto the vector to predict trait expression under various system prompts and many-shot prompts; measuring the activation shift along the vector caused by finetuning on trait-eliciting and narrowly flawed datasets (medical, code, GSM8K, math, opinions) and correlating it with post-finetuning trait scores; inhibiting the vector after finetuning or adding it during finetuning ("preventative steering"), compared with CAFT and a regularisation penalty; and screening data by projection difference (training response projection minus the base model's own response projection), validated on LMSYS-Chat-1M.

## What counts as an explanation here
A single direction per trait, used as a monitor (projection), a control knob (steering) and a predictor (finetuning shift, data projection difference). Partial and supervised; it predicts trait expression level, not specific outputs.

## How they judged success
Trait expression score 0 to 100 from a GPT-4.1-mini judge (checked against humans), coherence score 0 to 100, MMLU accuracy for capability retention, Pearson correlations between projection or shift and trait score, with cross-trait vectors as a baseline. For data screening: trait scores of models finetuned on the top-500 projection-difference samples versus random and bottom samples, also after removing samples an LLM judge flags.

## What they found
Steering reliably induces the trait. Last-prompt-token projection correlates with subsequent trait expression at r = 0.75 to 0.83, although much of this comes from prompt type. Finetuning shift along the vector correlates with post-finetuning trait expression at r = 0.76 to 0.97, above cross-trait baselines (0.34 to 0.86); some shifts are unintended (flawed math data increased evil). Post-hoc inhibition reduces traits but large coefficients hurt MMLU; preventative steering preserves MMLU better, multi-layer steering works best, and CAFT worked for evil and sycophancy but not hallucination. Projection difference predicts which datasets and individual samples induce traits, including on real chat data and after filtering by an LLM judge.

## Limits and open problems they name
Supervised: only predefined traits with precise descriptions; the trait must be elicitable by system prompt; difference-of-means directions are coarse; imperfect judge and about 20 single-turn evaluation questions per trait; two mid-size models; projection difference requires generating base-model responses for every sample (costly). SAEs suggested as an unsupervised complement.

## What we take from it
A shortcut and a measure: difference-of-means directions plus steering validation are a cheap, recognised baseline for any concept our model claims to represent. The finetuning-shift result is a rare example of predicting a future behaviour change from an internal quantity (r up to 0.97), which is the kind of prediction claim we want to make; reuse the correlation-with-cross-trait-baseline design. Warning: correlations driven by prompt category can inflate apparent monitoring power; control for it.

## Tags
unit: direction
form: direction | steering | probe
method: steering | probing | other
eval: prediction/simulation | downstream-task | human-rating
goal: control/editing | safety/auditing
