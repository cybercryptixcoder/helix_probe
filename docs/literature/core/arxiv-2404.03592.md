# ReFT: Representation Finetuning for Language Models

- **Key:** arxiv-2404.03592
- **Authors / organisation:** Zhengxuan Wu, Aryaman Arora, Zheng Wang, Atticus Geiger, Dan Jurafsky, Christopher D. Manning, Christopher Potts; Stanford University / Pr(Ai)2R Group
- **Date:** 2024-04
- **Link:** https://arxiv.org/abs/2404.03592
- **Kind:** paper
- **Read from:** abstract and sections (main text; appendix hyperparameters and conclusion not read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Parameter-efficient finetuning (LoRA and kin) adapts a model by changing a small set of weights. Interpretability work suggests hidden representations encode rich, often linear, semantic structure, so the authors ask whether adapting a model by learning small interventions on its representations, with all weights frozen, can match or beat weight-based PEFT. The method descends from causal-abstraction tools: a distributed interchange intervention tests whether a concept lives in a linear subspace, and distributed alignment search (DAS) learns that subspace. ReFT turns that machinery into a training method, and positions hand-made steering vectors as special cases of a learned intervention.

## What they studied
RoBERTa-base (125M) and RoBERTa-large (350M) on GLUE; LLaMA-1 7B and 13B, Llama-2 7B and Llama-3 8B on reasoning and instruction following. Unit: a low-rank linear subspace of the hidden representation at chosen layers and token positions.

## How they did it
LoReFT edits a hidden state h only inside an r-dimensional subspace: h + R^T(Wh + b - Rh), where R (r x d) has orthonormal rows and R, W, b are learned while the model is frozen. This sets the projection of h onto the subspace to a learned affine function of h. DiReFT drops the orthogonality and difference terms (h + W2^T(W1 h + b)), resembling LoRA applied to hidden states. Interventions are applied to a fixed number of prefix and suffix token positions at a chosen set of layers, optionally with weights tied across positions, so inference cost does not grow with prompt length. Training uses cross-entropy with teacher forcing for generation, or a classification head for GLUE. Benchmarks: eight commonsense datasets (BoolQ, PIQA, SIQA, HellaSwag, WinoGrande, ARC-e, ARC-c, OBQA) trained on Commonsense170K; four arithmetic datasets (AQuA, GSM8K, MAWPS, SVAMP) trained on Math10K; AlpacaEval v1.0 win rate vs text-davinci-003 after UltraFeedback training; GLUE. Baselines: prefix tuning, series and parallel adapters, LoRA, DoRA, RED, BitFit, full finetuning. Hyperparameters tuned on development sets only.

## What counts as an explanation here
Not primarily an explanation method; the learned subspace is a control handle. The interpretability claim is indirect: a small linear subspace spread across neurons suffices to steer many tasks, which the authors read as evidence that representations, not individual neurons, are the right unit. They state they do not yet know why ReFT works.

## How they judged success
Task accuracy averaged per benchmark family, AlpacaEval win rate, and the fraction of parameters trained, all against PEFT baselines.

## What they found
Commonsense average accuracy: LoReFT 80.2 vs DoRA 78.1 and LoRA 74.7 on LLaMA-7B; 83.3 vs 81.5/80.5 on LLaMA-13B; 86.6 vs 85.2/80.8 on Llama-3 8B, training about 0.03% of parameters. Arithmetic is weaker: LoReFT 42.6 vs LoRA 46.9 (LLaMA-7B), behind adapters too. AlpacaEval: LoReFT 85.60 at 0.0039% of parameters vs LoRA 81.48, RED 81.69, full finetuning 80.93 (GPT-3.5 Turbo 1106: 86.30). GLUE: roughly on par with LoRA and RED (84.2 base, 88.2 large). The authors claim 15x-65x fewer parameters than LoRA. Exploratory results: one intervention vector can memorise a long token sequence; learned subspaces for different tasks can be composed.

## Limits and open problems they name
Mostly LLaMA-family models; large hyperparameter space left unexplored; underperforms on chain-of-thought arithmetic, possibly because the effect fades over long generations; mechanism unknown, and the intervention may create new causal pathways rather than use existing ones.

## What we take from it
A framing and a warning. Framing: a learned low-rank affine edit in a fixed subspace at a few positions is a compact, well-defined intervention family that can be represented as a weight-like object, useful if our white-box model needs a parameterised "control" layer. Warning: that such tiny edits can teach new tasks means a successful steering or subspace intervention is not proof that the subspace was used by the unmodified model, so causal claims from learned interventions (DAS-style) need controls against the intervention doing the computation itself. Their practice of tuning on development sets only is worth copying.

## Tags
unit: direction | layer
form: steering | causal-abstraction
method: steering | training-interpretable | other
eval: downstream-task | benchmark
goal: control/editing
