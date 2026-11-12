# The Geometry of Truth: Emergent Linear Structure in Large Language Model Representations of True/False Datasets

- **Key:** arxiv-2310.06824
- **Authors / organisation:** Samuel Marks, Max Tegmark; Northeastern University, MIT
- **Date:** 2023-10
- **Link:** https://arxiv.org/abs/2310.06824
- **Kind:** paper
- **Read from:** abstract and sections (arXiv HTML v3, main text; appendices not read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Truth probes trained on model activations often failed to generalise in simple ways (for instance on negated statements), suggesting they picked up correlates such as plausibility rather than truth. The authors want to know whether LLMs have a genuine linear representation of the truth of factual statements, using clean, unambiguous true/false data and causal tests, not just classification accuracy. The larger aim is reliable detection of when a model "knows" a statement is false, for honesty and oversight.

## What they studied
LLaMA-2 7B, 13B and 70B. Curated datasets: cities (1,496), neg_cities (1,496), sp_en_trans and neg_sp_en_trans (354 each), larger_than and smaller_than (1,980 each), conjunctions and disjunctions of city statements (1,500 each). Uncurated: companies_true_false (1,200), common_claim_true_false (4,450), counterfact_true_false (31,960). A control dataset "likely" (10,000) where the final token is either the most likely or the 100th most likely completion, separating truth from probability. Unit: directions in the residual stream at specific token positions.

## How they did it
First, activation patching between matched true and false statements, measuring the change in log P(TRUE) minus log P(FALSE), to localise where truth matters: the entity token, the statement's last token and end punctuation (hypothesised to hold a truth summary), and the final position. Second, PCA of the residual stream at end-of-sentence tokens (e.g. layer 15 of 13B) to visualise whether true and false separate and whether datasets share axes. Third, probes trained on one of five training sets (cities, cities+neg_cities, larger_than, larger_than+smaller_than, likely) and tested on all other datasets: logistic regression, CCS, and their proposed mass-mean probe (direction = mean of true minus mean of false; an IID version adds an inverse-covariance correction, equivalent to LDA). Calibrated few-shot prompting and an oracle LR trained on the test set are baselines. Fourth, causal intervention: add or subtract the probe direction at the statement's final-token positions inside a few-shot prompt built from sp_en_trans, and check whether the model's TRUE/FALSE answer flips.

## What counts as an explanation here
A linear "truth direction" at specific positions and layers, validated in two ways: it generalises across datasets as a classifier and, when added or removed, changes the model's truth judgements. Partial: it identifies a representation and where it sits, not the circuit computing or reading it.

## How they judged success
Classification accuracy averaged across held-out datasets (generalisation). Normalised indirect effect (NIE) of the intervention, where 0 means no effect and 1 means false statements are labelled true as confidently as real true ones (or the reverse). Comparison across probe types, model sizes and training sets; "likely" acts as a control for probability-tracking.

## What they found
At 13B and 70B, curated datasets separate linearly along top principal components; alignment across datasets is imperfect at smaller scale (larger_than and smaller_than point in opposite directions in 13B, a shared one in 70B). Training on statements together with their negations improves generalisation; generalisation improves with scale (over 95% on sp_en_trans for 13B and 70B trained on larger_than+smaller_than, whatever the probe). Probes trained on "likely" generalise poorly, sometimes below chance where truth and likelihood anti-correlate. Mass-mean directions are much more causal than LR or CCS directions despite similar accuracy: mass-mean beats both in 7 of 8 conditions; e.g. cities on 13B gives NIE 0.77/0.90 (false-to-true / true-to-false) for mass-mean vs 0.13/0.19 for LR; cities+neg_cities on 13B gives 0.85/0.97. Linear structure appears in early-to-middle layers.

## Limits and open problems they name
Statements are simple and uncontroversial, so truth cannot be distinguished from "commonly believed" or "verifiable". Only LLaMA-2 studied. Unexplained: why "likely" mass-mean directions are causally strong despite weak classification, and why some training sets give weak interventions at 70B.

## What we take from it
(1) Key warning: a direction that classifies well (LR) may not be the one the model uses; equal accuracy can hide a large gap in causal effect. Any white-box variable we claim must be checked by intervention, not just decoding. (2) Method: mass-mean (difference of class means) is a cheap, more causal estimator than max-margin probes; useful default for extracting directions. (3) Design: datasets with negations and a probability-matched control ("likely") to rule out correlates. (4) Measure: normalised indirect effect, a clean 0-to-1 score for intervention success. (5) Patching first to localise positions, then probing there, is a good order of operations.

## Tags
unit: direction
form: direction, probe
method: probing, patching, steering
eval: patching, downstream-task, faithfulness
goal: understanding, safety/auditing, science
