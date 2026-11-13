# From Memorization to Reasoning in the Spectrum of Loss Curvature

- **Key:** arxiv-2510.24256
- **Authors / organisation:** Jack Merullo, Srihita Vatsavaya, Lucius Bushnaq, Owen Lewis; Goodfire
- **Date:** 2025-10-31 (v2)
- **Link:** https://arxiv.org/abs/2510.24256
- **Kind:** paper
- **Read from:** full text (arXiv HTML v2, all sections and appendices)
- **Relevance to us:** 2 (useful)

## What they wanted, and why

The paper asks how memorisation of training data is actually stored in a transformer's weights, and whether it can be separated from the weights that support general computation. The authors frame the question as one of a continuum: real models both recite verbatim and generalise, so the interesting problem is how the two are represented, how they trade off, and whether the split can be manipulated without labels saying which data was memorised. Practically, that would give a way to suppress recitation (copyright, privacy) far more broadly than forget-set unlearning, which only removes what you hand it. The larger goal is a weight-level account of which capabilities sit on shared versus idiosyncratic structure — which is exactly the kind of "read the weights, predict the effect of an intervention" claim we want to make. Their method is billed as an interpretability result that happens to produce a strong editing baseline.

## What they studied

Language models from the OLMo-2 family (7B as the main model, 1B replicated in an appendix) and a family of 86M-parameter ViT-Base image classifiers trained on ImageNet, including variants trained with 10% randomly noised labels so that some training points can only be fit by memorising them. The unit is neither neuron nor feature but a **rank-one weight component** of an MLP projection: the outer product of an activation-space eigenvector and a gradient-space eigenvector, i.e. one coefficient of the weight matrix in a curvature basis. Coverage is restricted to MLP projections (`gate_proj`, `up_proj`, `down_proj`) in a handful of layers, not attention.

## How they did it

They stream roughly 20M tokens from a Dolmino/OLMo mixture (sequence length 512) through the model under next-token cross-entropy, buffering pre-activation inputs on the forward pass and the corresponding output-side gradients on the backward pass, then accumulating and normalising the second-moment matrices to get **A** (activation covariance) and **G** (gradient covariance) per weight matrix. These two factors are the K-FAC approximation to the Fisher block, **F ≈ G ⊗ A**, so eigendecomposing both and taking outer products gives a full "curvature basis" of rank-one components for the matrix, ordered by the product of eigenvalues (λ_i·μ_j) — an explicit, dataset-averaged ordering of weight directions from most to least curvature. Crucially, gradients are taken against labels sampled from the model's own predictive distribution rather than gold labels, which keeps the procedure label-free. They then (i) diagnose the basis by measuring, for memorised and clean inputs separately, how strongly each percentile band of the spectrum activates (activation-ratio selectivity), and (ii) edit by keeping only the eigenvector pairs with the highest curvature mass until a fixed fraction ρ of total curvature mass is retained, zeroing the coefficients of the rest — a projection of the weight matrix onto its high-curvature subspace that does not reduce rank. Editing was applied to layers 23–25 at 60% energy retained (LMs) and to blocks 0 and 11 at 75% (ViTs). Comparisons: the supervised unlearning baseline BalancedSubnet (BSN, a trained binary parameter mask over a forget set), an SVD-truncation edit with no curvature information, and the unedited model. Memorisation is probed with the standard prefix/suffix exact-match protocol (prefix 64 tokens, greedy 48-token suffix; 8-token suffixes for a held-out set of historical quotes), scored by strict accuracy, loose accuracy at 0.75 normalised distance, and normalised Levenshtein distance, with perplexity on held-out clean text and nDCG@10 token-ranking overlap as coherence controls. Downstream behaviour is read off the OLMES suite across closed-book retrieval, open-book retrieval, logical reasoning and arithmetic-heavy math, plus three custom sets (Boar Etruscan, Relations, SimpleMath).

## What counts as an explanation here

A **decomposition of the weights into ordered components plus a claim about what the ordering means**: high-curvature directions carry structure shared across many examples, low-curvature directions carry idiosyncratic behaviour including verbatim recall. It is a partial, predictive account rather than a circuit: it does not say which component implements which computation or how components interact, and it deliberately makes no localisation claim (memories are described as spread out, with only a preference for certain layers). Its predictive content is of two kinds — an activation-side quantity (how strongly a task's hidden states overlap the band you are about to delete) predicting the behavioural drop, and a direction-level statement that deleting the bottom of the spectrum should remove recitation while leaving reasoning intact.

## How they judged success

Two families of metrics. For the edit: strict/loose recitation accuracy and Levenshtein distance on a *trained-on* set (Dolma validation, which BSN optimises against) and, more importantly, on a *never-seen* set (historical quotes) — the transfer set is the real test. Coherence is matched and reported as perplexity on held-out clean text plus nDCG@10 ranking overlap against the baseline model, so the comparison is behaviour-suppression at comparable fluency rather than suppression alone. ViTs are scored on memorised-label prediction rate, recovery of the true label on noised images, and validation accuracy. A positional-perturbation stress test borrowed from prior work measures how much extra memorisation can be extracted from perturbed prompts. Downstream degradation is reported as retention relative to the unedited model per benchmark, and — the key methodological move — they check that the *activation ratio* of each task's hidden states against the bottom of the spectrum predicts that task's retention ordering, which turns a scatter of benchmark numbers into a test of the mechanism.

## What they found

- The curvature basis separates memorised from clean data where SVD largely does not: in OLMo-7B's layer-22 MLP input, the bottom 50% of eigenvectors activates ~23% more on memorised than clean data, while the top 10% activates ~26% more on clean than memorised, and activation strength is monotone across spectrum bands (top 10% > 10–25% > 25–50% > bottom 50%). SVD shows a separation in the last layer and in one gate projection but without that monotone ordering; in the ViT the top 10% eigenvectors show over 2× stronger activation on clean data at the last layer while SVD shows no such pattern.
- LM edit (OLMo-2 7B, perplexity matched at 22.84 / 23.59 / 22.49): on Dolma validation strict accuracy falls to 99.9% → 3.4% (K-FAC), 6.0% (BSN), 3.0% (SVD); on the unseen historical quotes, K-FAC reaches 16.1% strict (23.8% loose) versus BSN at 60.0% (79.0%) and SVD at 17.5%. So the label-free edit suppresses recitation of data it never saw roughly three to four times as well as the forget-set-trained baseline, at lower perplexity.
- ViT-Base with 10% noised labels: memorised-label prediction 81.6% → 3.5%, true-label recovery 10.5% → 66.5%, validation accuracy 67.0% → 71.7% — the edit acts as a regulariser. SVD reaches the same 3.5% memorisation but only 58.9% recovery and 67.8% validation accuracy.
- Downstream spectrum (retention vs unedited): logical reasoning 95–106%, open-book QA 93–99%, closed-book QA 74–86%, math 66–74%, pure memorisation 3–16%. Arithmetic is the notable casualty — GSM8K 0.675 → 0.447, MMLU-Pro Math 23.4% → 15.8% — while MMLU-Pro CS is unchanged (26.1% → 26.3%), and an error analysis shows a preserved chain of thought failing only on the final calculation.
- Fact retrieval brittleness tracks frequency: the least frequent Relations (e.g. company-CEO) drop ~78% while the most frequent barely move.
- Activation overlap predicts the drop: memorised data interacts ~1.6× more strongly with the bottom band than open-book QA at layers 23–25, matching the retention ordering.
- ViT separation increases with weight decay, with a visible jump around 0.3 (the standard training value).
- Stress test: exact-match length under positional perturbation grows by ~6.7 tokens for K-FAC and ~5.4 for BSN, far less than the +13 to +16 reported for older unlearning methods.

## Limits and open problems they name

The edit is heavy-handed and explicitly not a full memory removal — they expect deleted memories to resurface under further fine-tuning or perturbation. Curvature is only approximated (K-FAC), and the smallest eigenvalues are the least numerically reliable, which they say affects analysis but not the edit. They cannot explain *why* low-curvature directions are so load-bearing for arithmetic: a low-curvature direction may be delicate narrow structure rather than memorisation, and they flag the alternative account of math-as-heuristics. Layer choice came from a sweep that used memorisation labels, so the procedure is only semi-unsupervised until someone can pick layers without them. And they caution that low-rank/SVD edits can drop function words or produce odd text without it showing in benchmarks — coherence numbers are not a full check.

## What we take from it

- **A weight-space predictor we should copy structurally**: order weight components by a cheap statistical quantity computed from a forward/backward pass (here K-FAC curvature mass), delete a mass fraction, and predict *which* behaviours move from a separate activation-side statistic (band overlap) rather than from intuition. That is a two-stage prediction — direction of effect from the basis, magnitude of effect from the task's overlap with the deleted subspace — and it is exactly the shape of explanation we want to claim, in the weights rather than in activations.
- **Chart the dose–response, not the single edit**: sweep ρ (curvature mass retained) per projection and report behaviour-versus-capability frontiers, as the unlearning and weight-steering literature does. A single 60% point is a headline, not a mechanism.
- **Matched-coherence comparison**: any "we removed X" claim needs perplexity and a rank-correlation (nDCG@10) control, so suppression is reported at equal fluency.
- **Untargeted transfer set as the headline metric**: the figure of merit is performance on memorisation the method was never tuned against, because the supervised baseline looks fine on its own forget set and collapses elsewhere.
- **Warning for our probes**: a low-curvature / rarely-used direction can carry precise, desirable computation, so "the direction is rarely activated ⇒ it is noise/memorisation" is false as a general rule. Any salience- or variance-based pruning of our own readout directions inherits this risk.
- **Method hook**: K-FAC gives a dataset-average curvature basis with one backward pass over unlabelled text — cheap enough to be a standing baseline in our harness, and a natural prior for choosing which weight directions a white-box model should track.

## Tags

unit: weights
form: decomposition
method: weight-analysis, decomposition
eval: ablation, downstream-task, benchmark
goal: understanding, control/editing, safety/auditing
