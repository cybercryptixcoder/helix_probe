# Training Language Models to Explain Their Own Computations

- **Key:** arxiv-2511.08579
- **Authors / organisation:** Belinda Z. Li, Zifan Carl Guo, Vincent Huang, Jacob Steinhardt, Jacob Andreas; Transluce and MIT CSAIL
- **Date:** 2025-11 (v3 dated 2026-02-09)
- **Link:** https://arxiv.org/abs/2511.08579
- **Kind:** paper
- **Read from:** abstract and sections (HTML v3, about the first 200k of 257k characters, incl. methods, results tables and discussion)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Can a language model learn to describe its own internal computations faithfully, and does it do so better than a different model trained the same way? The authors call this the Privileged Access Hypothesis. Rather than trusting introspection, they use the outputs of existing interpretability methods as ground truth and train an explainer to reproduce them, which makes the explanations checkable. The larger goal is scalable, trained interpretability where the model's own explanations are tied to verifiable results.

## What they studied
Target mainly Llama-3.1-8B (also Qwen3-8B and Gemma 2 9B in some experiments). Explainers: Llama-3.1-8B (full and LoRA), Llama-3-8B, Llama-3.1-8B-Instruct, Llama-3.1-70B (LoRA), Qwen3-8B. Units: residual-stream feature directions (Llama-Scope SAE features, about 131K per layer, labels from Neuronpedia), raw activations and activation differences, layer blocks (for patching), input tokens (for ablation).

## How they did it
The target is frozen; only the explainer is fine-tuned on tens of thousands of examples. Task 1, feature descriptions: the explainer gets a direction vector as a continuous token at its embedding layer and must output a natural-language description, trained on Neuronpedia labels. Evaluation is on 1,550 held-out SAE features (50 per layer), plus out-of-distribution raw FineWeb activations and CounterFact activation differences. Task 2, activation patching: predict whether patching an averaged block representation from a counterfactual input changes the target's output, and what the new output is (layers split into four blocks). Task 3, input ablation: predict whether removing a set of input tokens changes the answer and what it becomes. When hidden sizes differ, a learned per-layer linear projection maps target activations into the explainer.

## What counts as an explanation here
Natural-language descriptions of features, and natural-language predictions of intervention outcomes (whether the output changes and to what). These are explicitly predictive: the explainer forecasts the effect of patching and ablation. Partial, task-by-task.

## How they judged success
For features: an LM judge scoring similarity to gold labels (0 to 1 in 0.25 steps, 81.25% agreement with humans) and a simulator score (Pearson correlation between activations simulated from the description and true activations). For patching/ablation: exact match, has-changed F1, content match. Baselines: nearest-neighbour lookup of the most similar training feature's label, SelfIE (patching into an untuned model, best of five scales), gold SAE labels, untrained explainers, and other-model explainers.

## What they found
The self-explainer beat other models, including the larger Llama-3.1-70B, on activation and difference inputs (simulator on raw activations 49.7 for Llama-3.1-8B versus 33.8 for 70B with pre-trained projection and 21.1 for Qwen3-8B). Fine-tuned explainers beat nearest neighbours (33.7 simulator) and SelfIE (36.4), and the 8B self-explainer's simulator score on SAE features (45.1) slightly exceeded the gold labels (43.3). Self-explanation reached comparable results with about 0.8% of the data the nearest-neighbour baseline needed. On Qwen3-8B as target, input-ablation exact match was 83.4 for self versus 58.1 for Llama-3.1-8B and 8.9 untrained; patching 64.0 versus 54.1 versus 5.02. Explainer similarity to the target correlated with quality.

## Limits and open problems they name
The target is fixed, so this is not strict self-explanation; non-residual components were harder to explain; projection mismatch hurts some explainers; metrics are proxies (LM judge, simulator), and a manual check found only 27.7% of zero-scored cases were real errors; patching is simplified to block-averaged single tokens. Open: how explainer capacity, target complexity and task difficulty affect privileged access. They warn verbalised self-explanations must be checked against more rigorous methods in high-stakes use.

## What we take from it
Very close to our goal. Method: train a predictor to forecast the outcome of interventions (patching, ablation) on the target, scored by exact match and change-F1, with untrained and nearest-neighbour baselines; this is a ready-made evaluation protocol for "prediction under intervention". Finding: a model sharing the target's weights predicts it best, suggesting weight-sharing or weight-derived structure is a strong prior for a predictor. Measures to reuse: simulator correlation and has-changed F1. Warning: the predictor is a black box itself; its accuracy does not make it interpretable.

## Tags
unit: feature | direction | layer | whole-model
form: description | replacement-model
method: patching | ablation | SAE | other
eval: prediction/simulation | patching | ablation | faithfulness
goal: understanding | evaluation-of-methods
