# Notes: features and SAE evaluation (batch c)

**What an explanation should be.** The batch drifts from "a list of features" toward "a replacement that computes". Transcoders and skip transcoders model an MLP's input-output function instead of its activations (arxiv-2501.18823); Jacobian SAEs go further and make the feature-to-feature computation sparse and mostly linear (arxiv-2502.18147). The two benchmarks treat explanations as causal objects: circuits whose faithfulness is measured, or causal abstractions whose variables must predict outputs under interchange interventions (arxiv-2504.13151, arxiv-2407.14494).

**How success is measured.** Recurring measures: CE-loss increase when the surrogate is spliced in, variance explained, and LLM-scored fuzzing/detection/simulation (2501.18823, 2502.18147, 2501.16615); faithfulness curves over circuit size summarised as CPR/CMD (2504.13151); interchange intervention accuracy (2504.13151, 2407.14494); ROC AUC against ground-truth circuits with nonparametric tests (2407.14494). Controls that recur and are cheap: random circuits, random-init models (2502.18147), multiple seeds (2501.16615).

**Recurring methods/baselines.** EAP, EAP-IG, ACDC, activation patching, subnetwork probing for circuits; DAS, DBM, PCA, SAEs for variables; TopK SAEs as the standard sparse coder. EAP-IG with counterfactual ablation is the current default circuit baseline; DAS the variable-localisation bar.

**Warnings.** SAE features did not beat raw neurons for causal-variable localisation (2504.13151). SAE dictionaries are seed-dependent: only 30-42% of latents shared (2501.16615), so no single dictionary is "the" model's features. Synthetic ground-truth models are less realistic (tiny gradients, single tasks) (2407.14494). Much of a transcoder's function can hide in its linear skip path (2501.18823).

**Bearing on a predictive white-box model from weights.**
1. Build per-layer replacements as skip transcoders or JSAE pairs; JSAE's Jacobian-vs-actual-shift check (97.7% agreement) is a ready-made local prediction test, and its closed-form Jacobian comes straight from MLP weights.
2. Judge the whole model by prediction under intervention: IIA and CMD (match the model, not exceed it), not by feature interpretability alone.
3. Validate on SIIT models with planted circuits (2407.14494) before real models, and report cross-seed stability (2501.16615).
4. Open gap no paper closes: chaining sparse layer-wise computations into a whole-model, weight-derived replacement that is scored on behaviour.
