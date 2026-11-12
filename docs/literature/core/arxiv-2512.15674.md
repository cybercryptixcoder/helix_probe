# Activation Oracles: Training and Evaluating LLMs as General-Purpose Activation Explainers

- **Key:** arxiv-2512.15674
- **Authors / organisation:** Adam Karvonen, James Chua, Clément Dumas, Kit Fraser-Taliente, Subhash Kantamneni, Julian Minder, Euan Ong, Arnab Sen Sharma, Daniel Wen, Owain Evans, Samuel Marks; MATS, Truthful AI, ENS Paris-Saclay, EPFL, Northeastern, Anthropic
- **Date:** 2025-12-17 (v2 2026-01-06)
- **Link:** https://arxiv.org/abs/2512.15674 (research post: https://alignment.anthropic.com/2025/activation-oracles/)
- **Kind:** paper
- **Read from:** full text (main body and early appendices; read via HTML)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Existing activation-reading methods (logit lens, SAEs, steering) are each specialised and need per-task tuning. Earlier
"LatentQA" work trained decoders to answer questions about activations but only in narrow settings. The authors want a
generalist reader: an LLM that takes another model's activations as an extra input modality and answers arbitrary
natural-language questions about them, including questions unlike anything in training. The larger goal is a
general-purpose auditing tool that can surface hidden knowledge or fine-tuning effects without bespoke engineering.

## What they studied
Four base models, each with its own oracle: Llama-3.3-70B-Instruct, Gemma-2-9B-IT, Qwen3-8B, and (closed-weight)
Claude Haiku 3.5. Unit of analysis: residual-stream activation vectors (single or contiguous token positions) taken at
25/50/75% depth for training and 50% for evaluation; also activation differences between base and fine-tuned models.

## How they did it
The oracle is the same base model plus a LoRA adapter. Activations from the target are added (norm-matched) into the
oracle's residual stream at placeholder tokens after layer 2; adding rather than replacing avoided norm blow-up. The
oracle is then trained by SFT on about 1M examples (about 65M tokens) from three task families: questions about a
system prompt (persona, tone) given activations from the conversation; seven classic binary classification datasets
recast as yes/no questions; and a self-supervised task of predicting the 1–20 tokens before or after a span of 1–20
activations, on mixed pretraining and chat text. They then apply the oracle, without further training, to fine-tuned
variants of its base model in four evaluations: secret-keeping auditing games (Taboo, User Gender, Secret Side
Constraint), emergent-misalignment model diffing using base-vs-fine-tune activation differences, PersonaQA (facts
about fictional people learned in fine-tuning, probed with only the name), and seven held-out classification tasks.
Ablations vary the training mixture (SPQA only, +classification, full) and hold dataset size fixed to separate
diversity from quantity.

## What counts as an explanation here
A natural-language answer to a question about an activation. It is explicitly non-mechanistic: the oracle is itself a
black box, gives no circuit or causal account, and is meant as a partial, on-demand readout rather than a complete
model. It does not predict behaviour under intervention.

## How they judged success
Answer accuracy against known ground truth (secret word, gender, encoded instruction, persona attribute), with one
prompt per setting chosen on a validation set. Baselines: an agent pipeline with five white-box tools (logit lens,
SAEs, steering, etc.) and five black-box tools (prefill, fuzzing, prompt injection); the Activation Difference Lens for
model diffing, scored with a 0–5 rubric averaged over 5 runs; Patchscopes and untrained base models as controls for
PersonaQA and OOD classification.

## What they found
Taboo: 21% vs 4% for the best white-box baseline; Secret Side Constraint: 59% vs 52%; the oracle matched or beat the
best black-box method on two of three games. Model diffing: oracle and ADL both average 2/5 (identifying the
fine-tuning domain), slightly ahead of black-box methods. PersonaQA open-ended accuracy rose from about 5% to about 14%
for open models (35% for Haiku 3.5, though configurations were within error there); on a binary variant all oracles
beat Patchscopes. In 10 of 12 model/eval combinations the full training mixture was best; at fixed 400k examples,
adding context prediction beat the narrower mix, so both diversity and quantity help.

## Limits and open problems they name
The oracle is a black box answering about a black box: hard to verify by intervention and offers little mechanistic
insight. It often guesses wrong and is not calibrated. Training data is small and narrow. On anecdotal hallucination
detection, simple prompting baselines were strong. Benchmarks are narrow single-behaviour fine-tunes. PersonaQA showed
the fine-tuned knowledge itself is brittle.

## What we take from it
A framing and a warning. Framing: "train a reader model on (activation, question, answer) triples" is one way to turn
internals into predictions, and the self-supervised context-prediction task is a cheap, scalable label source we
could reuse for any network. Warning: a learned reader is not an explanation; our white-box model must be checkable
under intervention, which this approach explicitly cannot offer. Their baselines (logit lens, SAE, prefill, base-model
control) are the comparison set a reviewer will expect.

## Tags
unit: direction | whole-model
form: description
method: probing | other
eval: downstream-task | benchmark
goal: safety/auditing | evaluation-of-methods
