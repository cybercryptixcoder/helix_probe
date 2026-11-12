# Mixing Mechanisms: How Language Models Retrieve Bound Entities In-Context

- **Key:** arxiv-2510.06182
- **Authors / organisation:** Yoav Gur-Arieh, Mor Geva, Atticus Geiger; Tel Aviv University, Pr(Ai)R Group and Goodfire
- **Date:** 2025-10-07
- **Link:** https://arxiv.org/abs/2510.06182 (scout link https://www.goodfire.com/research/mixing-mechanisms redirects off-site and could not be fetched)
- **Kind:** paper (ICLR 2026)
- **Read from:** abstract and sections (arXiv HTML, first ~30%: setup, mechanisms, causal model, main results; dedicated limitations section not reached)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Models bind entities in context ("Ann loves pie") and later retrieve one given the other ("Who loves pie?"). The
prevailing view, built on small settings with few entity groups, is a positional mechanism: the query points to
an ordinal slot. The authors test this at realistic scale (many groups) and ask whether one mechanism suffices, with
the larger aim of a causal model that predicts the LM's next-token distribution, not just a story for easy cases.

## What they studied
Nine instruction-tuned models: gemma-2 2B/9B/27B, Qwen2.5 3B/7B/32B/72B, Llama-3.1 8B/70B. Two main templated binding
tasks (boxes, music), with ten tasks for gemma-2-2b-it and qwen2.5-7b-it; up to 20 entity groups. Unit: the last-token
residual stream at a model-specific layer (around 16-18 for gemma-2-2b-it), plus attention edges.

## How they did it
They built counterfactual prompt pairs in which positional, lexical (use the query entity to find its partner) and
reflexive (follow a pointer set earlier back to the target) mechanisms each predict a different entity after an
interchange intervention, then patched the last-token residual stream from counterfactual into original. They wrote
a single causal model whose output logits are a weighted mixture: a Gaussian over positions centred on the positional
index (width a quadratic in that index) plus one-hot lexical and reflexive terms, with weights fitted to data. This
model's predicted distribution was compared with the LM's actual distribution after patching, per target position.
Attention knockout separated the reflexive pointer from a confound in the dataset design, and an appendix separated
number of groups from sequence length.

## What counts as an explanation here
A small, explicit, fitted causal model that outputs a full probability distribution over candidate entities under
intervention. Meant to be predictive and close to complete for this behaviour, with an oracle as the upper bound.

## How they judged success
Agreement between the causal model's and the LM's next-token distributions under patching (Jensen-Shannon-based
similarity; KL in an appendix), per target position. Baselines: a uniform distribution, the positional-only
"prevailing view", an ablated model without the Gaussian positional term, and an oracle ceiling.

## What they found
With 20 groups the positional mechanism explains only about 20% of behaviour for middle groups: it becomes wide and
diffuse there, while lexical and reflexive signals are sharp and compensate. Mechanisms interact (a nearby lexical
index boosts lexical and weakens positional; lexical near reflexive suppresses lexical). On music with gemma-2-2b-it
the full mixture scores about 0.94-0.96 vs oracle 0.96-0.98, positional-only 0.42-0.46, uniform 0.44-0.57, and
0.67-0.68 without the Gaussian term. The model also generalised to long open-ended text interleaved with entity
groups.

## Limitations and open problems they name
Instruction-tuned models and templated tasks; full ten-task comparison on only two models; a confound between the
reflexive pointer and the target needed extra controls; effects of more groups vs longer inputs are easy to conflate.
(Formal limitations section not read.)

## What we take from it
Strongest template in this batch for our evaluation: score a white-box model by how well its *predicted
distribution under intervention* matches the network's, against uniform, a prevailing-view model and an oracle. Also a
substantive warning: a mechanism found in easy settings can explain only a fraction of behaviour at scale; real
networks mix several mechanisms with position-dependent weights, so our surrogate should allow mixtures rather than
one clean algorithm.

## Tags
unit: direction | layer | head
form: causal-abstraction
method: patching | ablation
eval: patching | prediction/simulation | faithfulness
goal: understanding | science
