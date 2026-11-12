# Towards Automated Circuit Discovery for Mechanistic Interpretability (ACDC)

- **Key:** arxiv-2304.14997
- **Authors / organisation:** Arthur Conmy, Augustine N. Mavor-Parker, Aengus Lynch, Stefan Heimersheim, Adrià Garriga-Alonso
- **Date:** 2023-04
- **Link:** https://arxiv.org/abs/2304.14997
- **Kind:** paper
- **Read from:** full text (main text and appendix tables; some appendix figures not read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Manual circuit work (IOI, greater-than, docstring, induction) follows a common workflow: pick a behaviour, dataset and metric, then repeatedly patch activations to find which components matter. The authors wanted to automate the last step, so circuits can be found faster and at larger scale, and to evaluate automated methods against circuits found by hand.

## What they studied
GPT-2 small (IOI, Greater-Than), a small attention-only transformer (Docstring), a 2-layer attention-only transformer (Induction), two tracr-compiled models with known ground-truth circuits (tracr-xproportion, tracr-reverse), and a gendered-pronoun case study. Unit: edges between components (heads, MLPs) in the computational graph; nodes also evaluated.

## How they did it
ACDC (Automatic Circuit DisCovery) represents the model as a graph of components. Starting from the output and moving in reverse topological order, it tries removing each incoming edge by patching it with the activation from a corrupted input; if the KL divergence between the patched model and the original rises by less than a threshold τ, the edge is pruned permanently. Sweeping τ gives circuits of different sizes. They compared against two adapted baselines: Subnetwork Probing (SP, learning a mask over components) and Head Importance Score for Pruning (HISP, gradient-based importance). Each method was scored by ROC curves of recovered edges or nodes against the previously published "canonical" circuits, under corrupted-activation patching and under zero patching, and with either KL or a task-specific metric.

## What counts as an explanation here
A sparse subgraph of the computational graph that preserves the model's output distribution on the task. The algorithm finds which components matter, not what they do; human interpretation of roles is still needed.

## How they judged success
Edge- and node-level ROC AUC against canonical circuits; KL divergence and task metric (e.g. logit difference) of the found circuit versus the full model; number of edges; runtime.

## What they found
With corrupted activations and KL, ACDC had edge AUC 0.982 (Docstring), 0.853 (Greater-Than) and 0.869 (IOI), versus HISP 0.805/0.693/0.789 and SP 0.937/0.806/0.823. With task-specific metrics ACDC was much weaker on Greater-Than (0.461) and IOI (0.589). With zero patching ACDC recovered both tracr circuits perfectly (AUC 1.000), while corrupted patching did poorly on them (tracr-reverse edge AUC 0.200). For Greater-Than, ACDC kept 68 of roughly 32,000 edges, all previously found by hand. On Docstring, a 98-edge ACDC circuit beat the 464-edge manual head circuit on all metrics. On Induction it recovered the two induction heads and the previous-token head. The IOI run took 8 minutes on an A100; large runs keeping over 10% of edges took hours.

## Limits and open problems they name
Optimising a single metric tends to miss negative components (logit difference never found IOI's Negative Name Movers); results are sensitive to corruption distribution, metric and hyperparameters; at low τ many extraneous components appear; optimising the task metric can produce circuits that outperform the model; the choice between zero and corrupted patching changes results sharply; the "ground truth" circuits are themselves human judgements and may be wrong; ACDC is described as a research tool, not mature for high-stakes use.

## What we take from it
A standard, citable baseline for "which components matter", with a clear evaluation design: compare against known circuits, ideally compiled ones (tracr) where truth is exact. Compiled ground-truth models are a useful benchmark idea for us too: we could test weight-reading on networks with known programs. Warnings: the ablation type (zero vs. resample) and metric can flip conclusions, so we must report both; KL to the full model is a more robust target than task metrics; pruning-based discovery misses negative and compensating components.

## Tags
unit: circuit | head | layer
form: graph
method: patching | ablation | other (automated pruning)
eval: benchmark | faithfulness | patching
goal: evaluation-of-methods | understanding
