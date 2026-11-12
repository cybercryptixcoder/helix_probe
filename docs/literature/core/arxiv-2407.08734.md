# Transformer Circuit Faithfulness Metrics Are Not Robust

- **Key:** arxiv-2407.08734
- **Authors / organisation:** Joseph Miller (FAR AI), Bilal Chughtai, William Saunders (independent)
- **Date:** 2024-07
- **Link:** https://arxiv.org/abs/2407.08734
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Circuit papers report a single faithfulness number (how much of the model's behaviour the circuit alone
reproduces), but that number depends on many unstated choices about how the rest of the model is knocked out. The
authors measure how much published faithfulness scores move when those choices change, and whether the "optimal
circuit" is even well defined. The goal is reliable evaluation of circuit discovery, so that claimed mechanisms and
benchmarks of automatic methods can be trusted.

## What they studied
Published circuits: Indirect Object Identification (IOI) in GPT-2 small (main case), Docstring in a 4-layer
attention-only model, Sports Players in Pythia-2.8B, and Tracr-compiled models (X-Proportion, Reverse) that have a
known ground-truth circuit. Units: nodes (heads, MLPs) and edges between them.

## How they did it
They recomputed faithfulness for each circuit while varying one choice at a time: node versus edge ablation; ablation
value (resample from a corrupt prompt, mean over a dataset, zero); ablating all token positions versus only those
the circuit specifies; ablating the clean run versus restoring circuit signal into a corrupt run; testing the
circuit versus its complement; size of the mean-ablation dataset; prompt template (ABBA vs BABA); and the output
metric (logit difference recovered, correct-answer percentage, answer probability, KL divergence, top-k accuracy).
They also examined per-prompt distributions instead of averages, and the order of averaging versus normalising. On
Tracr models they ran ACDC, Subnetwork Probing and Head Importance Scoring under different ablations and compared
with the ground truth. They release AutoCircuit, a TransformerLens-compatible library for edge patching and circuit
discovery, faster than the official ACDC code.

## What counts as an explanation here
A circuit: a subgraph of nodes or edges claimed sufficient for a task. The paper's point is that the circuit is only
meaningful together with its ablation procedure and metric; these define what the circuit claims.

## How they judged success
The object of study is the metric itself: faithfulness as percentage of full-model logit difference recovered (IOI),
plus the other metrics above. They report distributions, interquartile ranges, significance tests (e.g. p = 1e-5 for
resample vs mean at node level), and recovery of known Tracr circuits.

## What they found
The original IOI result (87% logit difference recovered, node-level mean ablation at specific positions) shifts a lot
under other choices: edge-level ablation gives substantially higher scores; resample ablation gives lower scores than
mean ablation; faithfulness grows monotonically with mean-ablation dataset size; BABA prompts score higher than ABBA;
averaging-then-normalising gives lower numbers than per-prompt normalising. Per-prompt interquartile ranges reach
about 50 percentage points, with extreme outliers. For Sports Players, mean ablation gives about chance (33%)
accuracy while resample gives 0%. On Tracr X-Proportion, one positional edge is needed under zero ablation but not
resample ablation; when each discovery method used the same ablation as the ground truth, all three recovered it
perfectly. Conclusion: the optimal circuit depends on the ablation method, not just the prompts.

## Limits and open problems they name
Few circuits and small models. Path-based (treeified) ablations were left out as intractable. They do not say
which ablation is correct, only that the choice must be fixed and reported.

## What we take from it
A warning and a reporting standard. Any claim that our white-box model "recovers X% of behaviour" must fix and state
the ablation value, granularity, positions, metric and aggregation, and should report per-input distributions and
worst-case as well as average. Matching the ablation granularity to the claim (edge claims tested by edge ablation)
applies directly. AutoCircuit is reusable tooling.

## Tags
unit: circuit | head
form: graph
method: ablation | patching
eval: faithfulness | ablation
goal: evaluation-of-methods
