# Notes: features and SAE evaluation (batch b)

## What an explanation should be
Across the batch, a feature set counts as an explanation only if it holds up under use, not just reconstruction. Three criteria come up again and again:
- **Behavioural faithfulness.** Swap the explanation into the model and it should preserve the outputs: output KL in arxiv-2405.12241, Loss Recovered in arxiv-2503.09532.
- **Causal specificity.** Intervening on a feature should change one concept and nothing else: cause/isolation in arxiv-2402.17700, SCR/TPP in arxiv-2503.09532.
- **Practical usefulness.** The features should beat tuned baselines on a real task (arxiv-2502.16681, alignmentforum-4uxcajnupktkbsi28-negative-results-saes-downstream).

Unsupervised dictionaries do worst on the third and the causal criteria. On RAVEL, the SAE has high isolation but weak cause (arxiv-2402.17700). SAE probes almost never beat logistic regression (arxiv-2502.16681), and they lose to dense probes out of distribution (the GDM post).

## How success is measured (recurring tools)
- **Spliced-in fidelity:** CE/KL increase or Loss Recovered, normalised between zero-ablation and the original model.
- **Interchange interventions:** scored as cause, isolation and their average.
- **Downstream comparisons with honest protocols:** AUC win rate over many datasets; "quiver of arrows" selection that uses only validation data; and a probe on the reconstruction compared with a probe on the original activations, to measure what information the SAE loses.
- **Autointerp:** an LLM writes an explanation, then predicts activations from it.

Recurring baselines are dense linear probes, PCA, raw neurons/channels, full-representation swaps, and a randomly initialised model (arxiv-2503.09532). Benchmarks: RAVEL and SAEBench, with RAVEL also embedded inside SAEBench.

## Open problems named
- Proxy metrics disagree with downstream metrics, and architecture rankings flip between metrics (arxiv-2503.09532).
- Feature absorption, feature splitting and inverse scaling with width.
- Concepts may not decompose into a few atomic latents (GDM post).
- Surrogates can match outputs through an unfaithful internal path: pure e2e SAEs drift off the model's own computation and are unstable across seeds (arxiv-2405.12241).
- Some attribute pairs stay entangled for every method, which may reflect the model itself rather than the method (arxiv-2402.17700).

## Bearing on a predictive white-box model from weights
1. Make prediction under intervention the headline test. RAVEL-style swaps directly test whether a model predicts counterfactual outputs, and they are an accepted benchmark.
2. Report fidelity two ways: output-level (KL / Loss Recovered) and path-level (downstream activation match, as in e2e+ds). Output match alone can hide a wrong mechanism.
3. Include a reconstruction-vs-original probe delta, and check out of distribution. Information loss shows up mainly OOD.
4. Compare against dense linear and supervised causal baselines (DAS/MDAS) using quiver-style selection. Also run a random-weights control to show the structure comes from learning.
5. The field's mood is sceptical: the GDM team deprioritised SAE research after these results. A weight-based approach is differentiated only if it delivers a practical win the dictionaries do not.
