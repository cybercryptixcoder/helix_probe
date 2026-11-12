# Mass-Editing Memory in a Transformer (MEMIT)

- **Key:** arxiv-2210.07229
- **Authors / organisation:** Kevin Meng, Arnab Sen Sharma, Alex Andonian, Yonatan Belinkov, David Bau; MIT CSAIL, Northeastern University, Technion
- **Date:** 2022-10
- **Link:** https://arxiv.org/abs/2210.07229
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
ROME and hypernetwork editors handle one or a few dozen facts; edits interfere and the model degrades when many are applied. The authors want to insert thousands of (subject, relation, object) facts into a model's weights at once, using the mechanistic picture from ROME (facts mediated by mid-layer MLPs acting as associative memories). The goal is practical knowledge updating and a stronger test of that storage hypothesis at scale.

## What they studied
GPT-J (6B) and GPT-NeoX (20B). Units: a range of mid-layer MLP output matrices (layers 3 to 8 in GPT-J, 6 to 10 in GPT-NeoX) chosen by causal tracing. Data: zsRE (10,000 real facts) and CounterFact (up to 10,000 counterfactual edits at once), plus per-relation (27 categories) and mixed-relation studies.

## How they did it
They first run causal tracing on GPT-J to pick the set of critical MLP layers, and show by severing that attention at the last subject token is not a key mediator while MLPs are. For each fact, gradient descent finds a change to the hidden state at the top critical layer that makes the new object likely (over prompts with random prefixes, with a norm clamp). That change is then spread across the critical layers, each layer taking an equal share of the remaining residual, updated from lowest to highest with activations recomputed after each layer. Each layer's update solves a batch least-squares problem in closed form, Delta = R K^T (C0 + K K^T)^-1, where K are the new keys, R the residual to be written, and C0 a scaled uncentered covariance of existing keys estimated from Wikitext, weighted by lambda (15,000 for GPT-J, 20,000 for NeoX). Baselines: fine-tuning with weight decay (FT-W), MEND, and sequential ROME. Ablations vary the number and position of edited layers, attention versus MLP editing, and lambda.

## What counts as an explanation here
The same associative-memory model of MLP weights as ROME, now with the claim that a fact is distributed across a band of layers. The explanation is validated by whether the edit it prescribes works at scale; it predicts that editing mid MLPs (not late MLPs, not attention) should succeed.

## How they judged success
zsRE: efficacy, paraphrase, specificity (top-1 accuracy) and their harmonic mean. CounterFact: efficacy success, paraphrase success, neighborhood success, harmonic-mean score S, generation entropy (fluency) and reference score (consistency). Scaling curves from 1 to 10,000 edits; runtime; per-category breakdowns.

## What they found
At 10,000 edits on GPT-J, MEMIT scores 50.7 on zsRE (efficacy 96.7, paraphrase 89.7, specificity 26.6, against an unedited specificity of 27.0) versus FT-W 42.1, MEND 20.0, ROME 2.6. On CounterFact S = 85.8 (efficacy 98.9, paraphrase 88.6, neighborhood 73.7) with fluency and consistency preserved; FT-W reaches high efficacy but low specificity and broken generation; sequential ROME collapses from about 32 edits; MEND collapses by about 6 edits. GPT-NeoX gets S = 82.0. More edited layers improve all metrics; editing late MLPs or attention is much worse; lambda trades specificity against efficacy with a peak near 10^4. Mixing relations performs about as the average of each. Some relations (athlete's sport, product owner) remain hard.

## Limits and open problems they name
Only directional subject-relation-object facts; no spatial, temporal, mathematical, procedural or symmetric knowledge; specificity trade-offs for some relations; slow serial computation of target vectors; misuse risk.

## What we take from it
A worked example of turning a mechanistic hypothesis into a closed-form weight write that scales, with the key covariance as the ingredient that protects old memories. For a white-box model, the update formula is a template for predicting how a linear layer's outputs change under a structured weight change, and the ablations (which layers, MLP vs attention) are the kind of intervention prediction we want to make in advance. Caveat: arxiv-2301.04213 shows edit success is largely independent of tracing, so MEMIT's success supports "these layers can carry edits", not necessarily "facts are stored here".

## Tags
unit: layer | weights
form: description | causal-abstraction
method: weight-analysis | patching | ablation
eval: downstream-task | benchmark | ablation
goal: control/editing
