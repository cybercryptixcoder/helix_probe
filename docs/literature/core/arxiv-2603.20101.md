# Pitfalls in Evaluating Interpretability Agents

- **Key:** arxiv-2603.20101
- **Authors / organisation:** Tal Haklay, Nikhil Prakash, Sana Pandey, Antonio Torralba, Jacob Andreas, Tamar Rott Shaham, Aaron Mueller, Yonatan Belinkov; Technion, Northeastern, MIT, Boston University, Kempner Institute (Harvard)
- **Date:** 2026-03-23
- **Link:** https://arxiv.org/abs/2603.20101
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
As automated interpretability agents become more autonomous, their outputs need evaluation that scales. The common
approach is to have an agent replicate a known published analysis and score agreement. The authors test whether
that is sound, using the step of circuit analysis where known circuit components are assigned functional roles,
and propose an evaluation that does not depend on human labels.

## What they studied
Six previously published circuits: IOI on GPT-2 Small (18 heads, 6 clusters) and Pythia-160M (14 heads, 7
clusters); Greater-Than on GPT-2 Small (8 heads, 4 MLPs, 2 clusters); Acronyms on GPT-2 Small (8 heads, 3
clusters); Colored Objects on GPT-2 Medium (27 heads, 3 clusters); Entity Tracking on LLaMA-7B (64 heads, 4
clusters). Unit: attention heads and MLPs, grouped into functional clusters.

## How they did it
A Claude Opus 4.1 agent iterates: reads prior results, proposes 3-5 hypotheses, designs experiments with TransformerLens
tools (logit lens, activation patching, attention-pattern inspection, token-position lookup), and stops with a final
hypothesis per component. Ground-truth components are given. A second Claude pass clusters components by function per
token position. A one-shot baseline gets all precomputed outputs in one pass. Each task: 3 runs x 5 clusterings.
Extrinsic scoring uses GPT-5 to match agent explanations to published ones. They then probe the evaluation:
re-checking human labels on held-out data (150 Pile examples), asking models to recall circuits from memory, and
a noise test mixing real with permuted experimental results at strength alpha. Finally they propose an intrinsic
metric: if two heads do the same job, swapping their QK or OV circuits should barely change outputs; distance is
the mean square root of Jensen-Shannon divergence across both swaps on 40 examples, and clustering quality is the
silhouette score under this distance.

## What counts as an explanation here
A functional-role assignment: each circuit component gets a text description and is grouped with components that do
the same thing. The intrinsic test makes "same function" operational as interchangeability of weights.

## How they judged success
Extrinsic: Component Functionality Accuracy, Cluster Functionality Accuracy (LLM judge), Component Assignment
Accuracy (Hungarian matching, no judge), against the one-shot baseline. Intrinsic: silhouette score under
swap-based JS distance, with random and expert clusterings as references; Kendall tau between intrinsic score and
Component Assignment Accuracy.

## What they found
Neither system consistently matched human analyses, and the agent was about as good as the one-shot baseline
(6,382 tool calls; about 14.2 calls and 4.5 iterations per component). Pitfalls: published labels can be wrong
(Pythia head 2.6, called a previous-token head, attended most to the previous token in only 42% of cases); outcome
scoring ignores the agent's better process; Claude could recall the IOI circuit with head indices, and GPT-5 showed
recall too; performance held under noise until alpha above 0.7, so evidence is used but memorization cannot be ruled
out. Intrinsic silhouettes: random about -0.18 to -0.28, expert 0.02-0.21, systems near zero on average (e.g. IOI
GPT-2 agent 0.03 +/- 0.09, best 0.12). Kendall tau with assignment accuracy: 0.739 (IOI GPT-2), 0.034 (Pythia,
n.s.), 0.506, 0.318, 0.378 elsewhere.

## Limits and open problems they name
Intrinsic metric covers attention heads only and does not address memorization, subjectivity or process. Six tasks;
memorization checked on one. LLM judge; ground-truth components assumed. They call for benchmarks robust to
memorization, sensitive to reasoning, and grounded in model behaviour.

## What we take from it
Directly relevant warnings for us: (1) do not evaluate on famous circuits (IOI etc.) that an LLM can recall; (2)
human labels are not ground truth. The swap test is a reusable, weight-level, behaviour-grounded measure: two
components share a function if exchanging their weights preserves outputs. That is exactly the kind of
"prediction under weight intervention" check a white-box model should pass.

## Tags
unit: head | circuit
form: description
method: agent | patching | weight-analysis
eval: benchmark | faithfulness | patching
goal: evaluation-of-methods
