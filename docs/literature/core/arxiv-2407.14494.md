# InterpBench: Semi-Synthetic Transformers for Evaluating Mechanistic Interpretability Techniques

- **Key:** arxiv-2407.14494
- **Authors / organisation:** Rohan Gupta, Iván Arcuschin, Thomas Kwa, Adrià Garriga-Alonso; University of Buenos Aires, FAR AI (MATS Winter 2023-24)
- **Date:** 2024-07
- **Link:** https://arxiv.org/abs/2407.14494
- **Kind:** benchmark
- **Read from:** full text (HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Circuit-discovery methods are hard to validate because the true circuit of a real model is unknown. Tracr-compiled transformers have known circuits but are unrealistic (mostly zero weights, no superposition). The authors want models that look more like trained networks yet provably implement a known algorithm, so methods can be scored against ground truth.

## What they studied
86 small transformers: 85 built from Tracr/RASP programs (26 generated with GPT-4 prompts, 59 from TracrBench) and one simplified IOI model (6 layers, 4 heads per layer). The main evaluation uses 16 Tracr tasks plus IOI (e.g. fraction of 'x' so far, reversal, duplicate removal). Unit: attention heads and MLPs as circuit nodes, and edges between them.

## How they did it
A Tracr-compiled model serves as the high-level algorithm. A larger low-level transformer (up to 4 heads per layer, halved head dimension, MLP 4x width) is trained with interchange intervention training (IIT): circuit nodes are aligned to high-level nodes and trained to behave consistently when their activations are swapped between inputs. Their new Strict IIT (SIIT) adds a loss that intervenes on non-aligned nodes and penalises any output change, forcing non-circuit nodes to be causally inert. Training runs to 100% IIA and strict IIA on validation (Adam, lr 0.001, batch 512, 1–8 h on one A6000). They then verify circuits with node-effect and normalised KL tests under resampling, mean and zero ablation, compare weight histograms and ablation behaviour with naturally trained models, and finally run ACDC, node and edge Subnetwork Probing, EAP and EAP-IG against the known circuits.

## What counts as an explanation here
A circuit (set of heads/MLPs and edges) aligned to a known algorithm, i.e. a causal abstraction. Here it is a ground-truth target that methods must recover.

## How they judged success
Model verification: interchange intervention accuracy (IIA), strict IIA, per-node effect rate, normalised KL. Method evaluation: edge-level ROC AUC against the true circuit, sweeping each method's threshold; Wilcoxon-Mann-Whitney test (α = 0.05) and Vargha-Delaney Â12 effect size; correlation of post-ablation accuracy with natural models for realism.

## What they found
Plain IIT models do not faithfully implement the circuit (non-circuit nodes still matter); SIIT models do. SIIT models' weight distributions resemble natural models more than Tracr's. In the benchmark ACDC beats node SP (p ≈ 0.0004, Â12 ≈ 0.74), edge SP (p ≈ 0.028) and EAP (p ≈ 0.00006, Â12 ≈ 0.91), and is not significantly different from EAP-IG (p ≈ 0.099). Poor SP/EAP results are partly blamed on tiny gradients in SIIT models.

## Limits and open problems they name
Small single-task models; head-level (not QKV or subspace) granularity, so SAEs and DAS are not tested; SIIT is sensitive to its loss weight and seed; zero ablation reveals some non-circuit nodes with effects; regression tasks collapse under mean ablation; the IOI model is simplified. They frame it as a worst-case test rather than a representative one.

## What we take from it
A way to manufacture networks with known mechanisms (SIIT) so a weights-to-white-box method can be scored against ground truth, which is exactly the validation our project needs before trusting it on real models. Reuse: IIA/strict-IIA as checks that a planted mechanism is real; ROC AUC plus nonparametric tests (Mann-Whitney, Â12) for comparing methods across many models. Warning: synthetic models differ from natural ones (gradient scale, single task), so success here is necessary, not sufficient.

## Tags
unit: circuit, head
form: graph, causal-abstraction
method: training-interpretable, patching, attribution, ablation
eval: benchmark, faithfulness, patching
goal: evaluation-of-methods
