# SAEBench: A Comprehensive Benchmark for Sparse Autoencoders in Language Model Interpretability

- **Key:** arxiv-2503.09532
- **Authors / organisation:** Adam Karvonen, Can Rager (co-leads), Johnny Lin, Curt Tigges, Joseph Bloom (Decode Research), David Chanin (UCL), Yeu-Tong Lau, Eoin Farrell, Callum McDougall, Kola Ayonrinde, Demian Till, Matthew Wearden, Arthur Conmy, Samuel Marks (Anthropic), Neel Nanda
- **Date:** 2025-03 (v4 2025-06-04; ICML)
- **Link:** https://arxiv.org/abs/2503.09532
- **Kind:** benchmark
- **Read from:** full text (arXiv HTML, main body and parts of appendices)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
SAE progress has mostly been measured on the sparsity-fidelity trade-off (L0 vs reconstruction), whose practical meaning is unclear and which misses known failure modes such as feature absorption and uninterpretable high-frequency latents. The authors build a standardised, automated, reproducible benchmark that measures properties practitioners care about, so architectures and training choices can be compared on what matters. It runs in roughly 1-2 hours per SAE.

## What they studied
Gemma-2-2B (layer 12) primarily and Pythia-160M (layer 8). Over 200 SAEs across seven architectures (ReLU, TopK, BatchTopK, Gated, JumpReLU, P-Annealing, Matryoshka BatchTopK), widths 4k/16k/65k, L0 roughly 20 to 1,000; Gemma Scope SAEs in an appendix. Baselines include PCA, raw residual channels, MLP neurons, and SAEs on a randomly initialised model.

## How they did it
Eight metrics in four groups:
1. **Reconstruction:** L0 and Loss Recovered, the fraction of the gap between zero-ablation CE and original CE that is closed when the SAE reconstruction is spliced in.
2. **Interpretability:** autointerp: an LLM writes a latent explanation from top and importance-weighted examples, then a judge predicts activations on held-out sequences; scored by accuracy over 1,000 live latents.
3. **Concept detection:** feature absorption (first-letter tasks, detecting when a main latent fails because another latent has absorbed the case, including partial absorption); sparse probing (top-k latents by class-mean difference, logistic regression, 35 binary tasks from five datasets, focus k=1).
4. **Disentanglement / causal:** RAVEL (binary mask transfers latents between entities; average of cause and isolation); Spurious Correlation Removal (ablate k latents, focus k=20, to strip gender from a biased profession probe); Targeted Probe Perturbation (ablating a class's latents should hurt only that class's probe); unlearning (clamp latents that fire more on WMDP-bio than WikiText; lower WMDP-bio accuracy while MMLU stays above 0.99 of baseline).
They then sweep architecture, width, L0 and training tokens and compare rankings across metrics.

## What counts as an explanation here
A feature dictionary whose latents should be individually interpretable (predictable by an explanation), complete enough to reconstruct behaviour, aligned with real concepts (detectable with one latent, not absorbed), and causally separable (ablating a few latents changes one concept only). The benchmark operationalises "good explanation" as a profile across these axes, explicitly not a single score.

## How they judged success
The eight metrics above; consistency of architecture rankings across metrics; scaling trends with width and L0; comparison to PCA, residual-channel, MLP-neuron and random-model baselines.

## What they found
- Gains on proxy metrics do not reliably carry over to practical metrics.
- Matryoshka is slightly worse on the sparsity-fidelity frontier but best on 5 of 8 metrics (absorption, RAVEL, sparse probing, SCR, TPP) in L0 40-200, and is the only architecture whose disentanglement improves with width; most others show inverse scaling on disentanglement and concept detection, attributed to feature splitting.
- ReLU is weakest on 5 of 8 metrics and worst on Loss Recovered. At L0 below 100, BatchTopK > TopK > JumpReLU > Gated > Matryoshka > P-anneal > ReLU.
- Rankings conflict across metrics (e.g. P-anneal vs Gated swap on absorption vs Loss Recovered).
- Lower L0 helps interpretability; higher L0 helps reconstruction, RAVEL, TPP and absorption; L0 about 50-150 is a reasonable compromise.
- Most metrics plateau by about 50M of 500M training tokens.
- Sparse probing is noisy and differentiates little; all SAEs beat a raw residual-channel baseline of 0.65. On a random-weight Pythia-1B, SAEs score close to or worse than direct probing on supervised metrics, though autointerp remains above baselines.
- Final-layer Gemma Scope SAEs score near zero on unlearning.

## Limits and open problems they name
Supervised metrics cover few concepts and are noisy; quantitative metrics miss qualitative insight; only two models; metrics should not be collapsed into one number; unlearning only weakly testable on Gemma-2-2B; baselines beat SAEs on several tasks.

## What we take from it
- **Benchmark:** a ready, recognised evaluation suite; if our white-box model produces feature-like units, reporting a subset of SAEBench (Loss Recovered, autointerp, RAVEL, SCR/TPP) makes results legible to the field.
- **Measure:** Loss Recovered (CE with surrogate spliced in, normalised between zero-ablation and original) is the standard fidelity number we should report for any reconstruction.
- **Control:** the random-initialisation baseline is a strong sanity check that our method reflects learned structure, not the data or architecture.
- **Warning:** multiple metrics disagree; pick metrics tied to our goal (prediction under intervention) rather than proxy hill-climbing.

## Tags
unit: feature
form: dictionary
method: SAE | probing | ablation | steering
eval: benchmark | faithfulness | prediction/simulation | downstream-task
goal: evaluation-of-methods
