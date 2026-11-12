# Have Faith in Faithfulness: Going Beyond Circuit Overlap When Finding Model Mechanisms

- **Key:** arxiv-2403.17806
- **Authors / organisation:** Michael Hanna, Sandro Pezzelle (ILLC, University of Amsterdam), Yonatan Belinkov (Technion)
- **Date:** 2024-03
- **Link:** https://arxiv.org/abs/2403.17806
- **Kind:** paper
- **Read from:** full text (HTML; date taken from the arXiv identifier)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Exact activation patching of every edge is too expensive for large models, so the field uses edge attribution
patching (EAP), a one-pass gradient approximation. EAP had been validated mainly by how much its circuits overlap
with hand-found circuits. The authors ask whether overlap is the right test, and propose a better approximation.
The broader goal is scalable circuit discovery whose outputs are actually faithful to the model.

## What they studied
GPT-2 small on six tasks: IOI, Gender-Bias, Greater-Than, Capital-Country, subject-verb agreement (SVA), Hypernymy;
replication on GPT-2 XL and Pythia-2.8B (100 examples per task). Unit: edges between components in the computation
graph.

## How they did it
EAP-IG replaces EAP's single gradient at the clean input with integrated gradients: gradients are averaged over
m = 5 points on a path between corrupted and clean inputs, which handles edges whose gradient is zero at the clean
point. A KL-divergence-objective variant is also tested. Runtime is about five times EAP. For each method they score
all edges, build circuits of increasing size from the top edges, and measure how well each circuit alone reproduces
task behaviour when all other edges are replaced by corrupted activations. Comparisons: EAP, EAP-IG, and exact
activation patching. Separately, across nine tasks they relate circuit overlap (node and edge IoU) to cross-task
faithfulness (how well one task's circuit performs on another task).

## What counts as an explanation here
A sparse edge-level circuit (target 1 to 2% of edges) that by itself reproduces the task behaviour. Partial: aims for
sufficiency, not proven completeness.

## How they judged success
Faithfulness: normalised task metric (e.g. logit difference) of the circuit-only model relative to the full model
and a fully corrupted baseline, with a target of at least 85%, plotted against circuit size. Rank agreement with
activation-patching scores (Pearson correlation, top-n overlap). For the overlap argument: correlation between IoU
and faithfulness, and linear-fit R squared.

## What they found
EAP-IG circuits are as faithful or more faithful than EAP circuits on every task, with the largest gains on SVA (EAP
stays unfaithful until about 1,000 edges), Hypernymy and Capital-Country. Exact activation patching still wins on
IOI, and nothing does well on Hypernymy. EAP-IG correlates with patching scores above 0.8 but does not rank all
edges better; its gain comes from getting the top edges right. Overlap correlates with faithfulness overall (about
0.86 node, 0.83 edge; R squared about 0.74), but moderate overlap is uninformative: Capital-Country and Hypernymy
share node IoU 0.58 yet cross-faithfulness is 0.61 one way and 0.2 the other. A simple clean-minus-corrupted
baseline beats EAP-IG on all tasks except SVA.

## Limits and open problems they name
Faithfulness does not guarantee completeness. EAP-IG does not approximate patching scores well even though its
circuits are faithful. Faithfulness evaluation is expensive (hence the small larger-model replication). Activation
patching scores edges independently, so its circuits are also imperfect.

## What we take from it
A measure and a warning: judge a mechanism by whether it reproduces behaviour (faithfulness curve against size), not
by agreement with another explanation. For us, agreement between a weight-derived model and a probing-derived one
is not evidence of correctness; prediction of the network is. Faithfulness-vs-size curves are a good standard plot.
The strong simple baseline is a reminder to always include cheap baselines.

## Tags
unit: circuit
form: graph
method: attribution | patching
eval: faithfulness | patching
goal: evaluation-of-methods | understanding
