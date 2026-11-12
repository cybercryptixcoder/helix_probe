# How to Use and Interpret Activation Patching

- **Key:** arxiv-2404.15255
- **Authors / organisation:** Stefan Heimersheim, Neel Nanda (affiliations not stated on the page)
- **Date:** 2024-04
- **Link:** https://arxiv.org/abs/2404.15255
- **Kind:** survey/agenda
- **Read from:** full text (HTML)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
A practitioner's guide: activation patching is widely used but its results are easy to over-read. The authors
collect practical advice from their own experience on how to set up patching experiments, which corrupted
prompts and metrics to use, and what a given result does and does not imply about a circuit. The goal is more
reliable mechanistic claims.

## What they studied
No new large-scale experiments. Illustrations: IOI prompts, a toy "Nobel Peace Prize" circuit (a previous-token
head plus a neuron), AND and OR gate toy circuits, and a GPT-2 medium "Paris" example comparing metrics by layer.
Units: residual stream, MLP outputs, heads, neurons, SAE features, and paths between them.

## How they did it
Conceptual analysis with worked examples. They distinguish exploratory patching (sweep components one at a time)
from confirmatory patching (patch many at once to test a hypothesised circuit, as in causal scrubbing). They
contrast denoising (clean into corrupted; tests sufficiency) with noising (corrupted into clean; tests necessity)
and use AND/OR toy circuits to show each misses different components. They compare patching with zero, mean and
Gaussian-noise ablation, discuss how to pick corrupted prompts (narrow for exploration, wide for confirmation),
explain path patching to separate direct from mediated effects, and compare metrics in a table and a layer-wise
plot.

## What counts as an explanation here
A circuit: a set of components and paths sufficient (or necessary) for a behaviour on a stated prompt
distribution. They stress such a set is not necessarily minimal and holds only for the distribution tested.

## How they judged success
Guidance rather than evaluation. Metrics discussed: logit difference (most trusted; roughly linear in the
residual stream), logprob, probability, accuracy and rank, KL divergence, and internal quantities (attention,
feature or probe values). Suggested framing: a Pareto curve of circuit size against performance recovered.

## What they found
Denoising and noising are not interchangeable: in an AND gate only noising finds the inputs, in an OR gate only
denoising does; in the Nobel toy circuit, noising finds the head, neuron and embeddings while denoising finds only
the neuron. Probability and logprob saturate and probability is nonlinear in logits (a +2 logit shift can mean 1
or 40 percentage points); discrete metrics hide sub-threshold effects; in the GPT-2 medium example logprob
saturates after about layer 17 and rank jumps near layer 15. Gaussian-noise corruption is very sensitive to the
noise level. Backup components (the Hydra effect, with compensation around 0.7x in prior work) make components
look less important; negative components make "performance recovered" ambiguous. Advice: prefer patching to
ablation, try several corrupted prompts, report several metrics including a continuous logit-linear one, and
treat agreement across metrics as stronger evidence.

## Limits and open problems they name
Backup behaviour and negative components remain unsolved obstacles to scoring circuits; Gaussian corruption is
fragile; results do not transfer beyond the prompt distribution; patching does not say what information flows
along a path (causal scrubbing goes further).

## What we take from it
An evaluation checklist for intervention predictions. A predictive white-box model should state both necessity
(noising) and sufficiency (denoising) predictions and be tested on both, since AND/OR structure makes either
alone misleading. It should predict backup compensation and negative components, which are exactly what naive
circuit stories miss. Report logit difference plus at least one other metric, and a size-vs-recovery Pareto curve
when claiming completeness.

## Tags
unit: head | neuron | layer | circuit
form: graph
method: patching | ablation
eval: patching | completeness
goal: evaluation-of-methods
