# Discovering Latent Knowledge in Language Models Without Supervision

- **Key:** arxiv-2212.03827
- **Authors / organisation:** Collin Burns, Haotian Ye, Dan Klein, Jacob Steinhardt; UC Berkeley, Peking University
- **Date:** 2022-12
- **Link:** https://arxiv.org/abs/2212.03827
- **Kind:** paper
- **Read from:** abstract and sections (arXiv HTML: method, experiments, transfer, limitations; appendices only skimmed via summary)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Models trained to imitate text or to please human raters can say false things (repeating misconceptions, or telling evaluators what they cannot check). The authors want to read what a model internally takes to be true, independent of what it outputs and without any labels. The larger goal is a route to eliciting latent knowledge from models whose outputs cannot be trusted or supervised, a building block for honesty and oversight of future systems.

## What they studied
Six models in three families: encoder-decoder (T5, UnifiedQA, T0), decoder-only (GPT-J), encoder-only (RoBERTa, DeBERTa). Ten binary classification datasets recast as yes/no questions: IMDB, Amazon (sentiment), AG-News, DBpedia-14 (topic), RTE, QNLI (NLI), COPA, Story-Cloze (story completion), BoolQ (QA), PIQA (commonsense). About 9 prompts per dataset. Unit: a direction (linear probe) in the hidden states of one layer.

## How they did it
Each question is turned into a contrast pair: the same text completed with "Yes" and with "No". Hidden states for the two halves are normalised separately (mean-centred per half, optionally scaled) so the probe cannot simply read off which answer word was appended. A linear map plus sigmoid gives a "probability true" for each half. Contrast-Consistent Search (CCS) trains this probe with no labels using two losses: consistency (p for the "Yes" version should equal one minus p for the "No" version) and confidence (push the smaller of the two toward zero, to avoid the trivial 0.5/0.5 solution). Prediction averages the two halves and thresholds at 0.5; which cluster means "true" is fixed afterwards. Datasets are subsampled to 1,000 examples (500 for COPA) and split 60/40 into unsupervised train and test. They compare against zero-shot prompting, calibrated zero-shot, a supervised logistic-regression ceiling, and two clustering variants (top principal component of contrast differences, and a bimodal-direction search). They also prepend misleading few-shot examples with wrong answers to see whether outputs and CCS diverge, test transfer of a probe trained on one dataset to others, and compare layers.

## What counts as an explanation here
A single unsupervised direction in activation space whose sign tracks the model's internal truth judgement. It is a probe, not a mechanism: it says where a truth-like variable can be read, not how it is computed or used. It predicts the label of new inputs but is not shown to be what the model causally uses.

## How they judged success
Accuracy averaged over datasets, prompts and models; prompt sensitivity as standard deviation of accuracy across prompts; robustness under misleading prefixes; cross-dataset transfer accuracy; Wald tests for significance. Supervised logistic regression on the same activations is the ceiling; calibrated zero-shot output is the main baseline.

## What they found
CCS averages 71.2% vs 67.2% for calibrated zero-shot; supervised LR reaches 83.7%. Prompt sensitivity is roughly halved (std 3.2 vs 6.9). With misleading prefixes, UnifiedQA's calibrated zero-shot drops from 80.4% to 70.9% while CCS stays about level (82.1% to 83.8%), so internal states can stay correct when outputs go wrong. Probes often transfer across datasets with different label words, which the authors read as hinting at a task-agnostic truth representation. Simple clustering variants get close to CCS (about 70%). In T5 and UnifiedQA, middle layers can beat the final layer.

## Limits and open problems they name
CCS assumes a single direction separates true from false and that the model actually evaluates truth; it is unclear when these hold. No test on deliberate lying or deception. Large gap to the supervised ceiling; calibration, reliability and going beyond yes/no questions are open. Which cluster is "true" is resolved using test labels in the main results.

## What we take from it
(1) A framing: internal state can be a better predictor of a model's "belief" than its output, so a white-box model should be judged on internal variables as well as outputs. (2) A methodological trick: contrast pairs with per-half normalisation to remove the trivial answer-token difference, reusable when probing for any binary variable. (3) Warning: decodability is not use; CCS gives no causal check, which later work (Geometry of Truth, arxiv-2310.06824) adds. (4) Baseline set worth copying: zero-shot output, calibrated output, supervised-probe ceiling.

## Tags
unit: direction
form: probe, direction
method: probing
eval: downstream-task, benchmark
goal: safety/auditing, science
