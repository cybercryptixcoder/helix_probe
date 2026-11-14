# The Cosine–Causal Gap in Cross-Model Crosscoders: When Decoder Universality Overstates Causal Equivalence in Gemma-2-2B

- **Key:** openinterp-2026-cosine-causal-gap-crosscoder
- **Authors / organisation:** Caio Vicentino (OpenInterpretability / openinterp.org; workshop draft submitted to the NeurIPS 2026 Mechanistic Interpretability Workshop)
- **Date:** 2026-05-08
- **Link:** https://openinterp.org/research/papers/cosine-causal-gap-crosscoder
- **Kind:** paper
- **Read from:** full text — the rendered paper page, ~22.4k stripped chars covering abstract, §1–§7, the reproducibility statement, acknowledgements and the reference list, read end to end in three slices. The page ends at the reference list, so the absence of an appendix is a property of the page. **No figure inspected** (the result tables are HTML and were read as text); the HuggingFace crosscoder checkpoint, the `gemma_causal_validation.csv` table and the reproducer notebook were **not** downloaded or run.
- **Relevance to us:** 3 (central)

## What they wanted, and why

Cross-model crosscoders are trained over two models' residual streams with one shared dictionary, and the analysis pipeline sorts latents into shared / base-only / chat-only / dead by comparing the two decoder vectors per latent. A latent whose two decoders point in nearly the same direction is reported as a "shared feature", and everything downstream — model diffing, cross-model probing, feature surgery, claims that a persona direction found in the base model applies to the chat model — then treats it as the same thing in both networks. The authors' complaint is that this inference is purely geometric and has never been checked against the property it is supposed to license: that ablating the latent in one model does the same thing as ablating it in the other. The paper is a first direct measurement of that gap on a real crosscoder, with the explicit aim of producing a cheap diagnostic that any existing crosscoder analysis can run without retraining. It is the per-feature version of a question the whole interpretability literature answers at population level.

## What they studied

Gemma-2-2B base and its instruction-tuned sibling (Gemma-2-2B-it), which is the standard model pair for chat-tuning diffing. One crosscoder over the residual stream at **layer 13**, with 73,728 latents (32× expansion over a 2,304-dimensional model width), BatchTopK sparsity at k = 100 plus an L1 term, trained on 100M tokens split evenly between FineWeb-Edu and UltraChat-200k. The unit of analysis is a single latent: two decoder vectors, one per model. The measurement population is the top of the shared class — latents firing on at least 1% of validation tokens, 80 candidates out of 39,711 shared latents, of which 68 survive a "fired on at least 3 of 256 probes" filter. A 28-latent sample of the *unclassified* class (activations too large to be dead but failing the shared/exclusive norm thresholds) serves as a within-crosscoder control.

## How they did it

Train the crosscoder, then score three things on the same latents. (1) The standard diagnostic: cosine between the two decoder vectors for the latent. (2) A new per-feature causal-equivalence score: for each latents, take 256 probe inputs from FineWeb-Edu (last token, 128 tokens), run a baseline forward pass in each model to get next-token distributions, re-run with that one latent zeroed in the crosscoder reconstruction at layer 13 in each model, compute the per-probe KL divergence between ablated and baseline in each model separately, and take the Pearson correlation of the two 256-long KL trajectories. A score near +1 means ablating the latent in A perturbs A's outputs in the same pattern as ablating it in B does B's; 0 is no relation; negative means the two models respond in opposite ways across probes. (3) The same protocol applied to unclassified-class controls. Everything runs on a single A100: 4h28m to train the crosscoder, about an hour for 80 + 28 features × 256 probes × 2 models.

## What counts as an explanation here

A feature-level *transfer claim* and a diagnostic for testing one. The paper does not propose a model of either network; it proposes that "latent f is the same feature in A and B" be operationalised as "perturbing f produces correlated downstream effects in both models", and offers a cheap statistic that measures exactly that. It is meant to be partial and complementary: population-level diagnostics (KL bridging, latent scaling) are explicitly left as the neighbouring tools, and the authors describe their score as an additional mandatory line item, not a replacement for cosine. It does predict — a low correlation is a concrete prediction that a cross-model steering or ablation will not carry over.

## How they judged success

No benchmark and no accuracy metric. Success is the existence and size of a mismatch between two statistics computed on the same latents: median decoder cosine versus median Pearson_CE over the shared class; the fraction of latents with cosine above 0.7 and causal equivalence below 0.5; the distribution of causal equivalence in both tails; and the same statistics on the unclassified control population, which is expected to score lower and does. Robustness is argued structurally (the effect is measured inside the shared class, which dominates the population regardless of the exclusivity recipe) rather than by ablation or seed replication.

## What they found

Across the 68 measured shared latents, median decoder cosine is 0.965 while median Pearson causal equivalence is 0.616 — roughly 15° between decoder directions on the typical latent, but only moderately correlated downstream effects. 26 latents (38.24%) have cosine above 0.7 and causal equivalence below 0.5; 5 (7.4%) have cosine above 0.9 with equivalence below 0.3; and 2 have cosine above 0.95 with *negative* equivalence, i.e. nearly identical decoder directions and anti-correlated ablation effects. The converse tail exists too: 3 shared latents have cosine below zero yet equivalence above 0.7, the most extreme being cosine ≈ −0.50 with equivalence ≈ +0.91 — decoders pointing opposite ways with near-identical downstream effects. The unclassified controls sit lower as expected (median equivalence 0.358, mean 0.263), and the set contains a latent with equivalence 0.999 that the standard taxonomy calls "not shared". The paper's reading is that decoder cosine is neither necessary nor sufficient for causal equivalence, and that the population-level crosscoder evidence (which does show shared features collectively explain cross-model output similarity) says nothing about which individual features are universal.

## Limits and open problems they name

The tested set is 0.2% of the shared class, selected for high firing, so the low-firing tail is unexamined and could go either way. Zero ablation is out of distribution, so trajectories might look different under optimal ablation — an arm they name but do not run. One layer, one model pair, one architecture recipe; a Qwen-3.5-1.7B crosscoder was configured but not trained. The BatchTopK + L1 recipe collapses the exclusivity taxonomy almost entirely (0.01% chat-only against roughly 4.3% for a vanilla-L1 recipe on the same pair), so whether the gap survives a recipe change is untested. Small probe counts (about 64) would need bootstrapping.

Limits I add, marked as mine: there is **no null distribution for the statistic itself** — no shuffled-pair baseline in which latent f is ablated in model A and a *random* latent in model B, which would establish what Pearson correlation a genuinely unrelated pair produces at n≈256 and with heavily skewed KL values; without it, "0.616 is moderate" is a judgement about a number whose noise floor is unknown. The 68-of-80 filter also biases toward high firing, which is the regime where KL trajectories are least noisy. And the framing of the gap as an in-distribution-versus-held-out overfitting story is asserted by analogy to two unrelated alignment reports of 2026 rather than tested — the held-out quantity here (an ablation effect) is not obviously an overfitting measure of the fitted quantity (decoder direction cosine).

## What we take from it

A **measure and a warning**. The measure: any cross-model or cross-checkpoint transfer claim of ours should come with a paired-intervention correlation — ablate the same unit in both systems on the same probes, correlate the downstream effect profiles, report the correlation beside the geometric similarity. It costs one extra pass per unit and it is applied to any trained decomposition without retraining. The warning: geometric similarity between two read-outs is a claim about the coordinate systems, not about function, and it fails in both directions — high similarity with divergent effect, and opposed geometry with identical effect — so the folder's habit of matching features across seeds, models or dictionary recipes by decoder cosine needs this second number before it can be used for transfer. The control population is also instructive: a latent the taxonomy rejects as "not shared" can be almost perfectly causally equivalent, which means the classification boundary itself is not the functional boundary.

## Tags

unit: feature
form: probe
method: ablation, decomposition
eval: ablation, prediction/simulation
goal: evaluation-of-methods
