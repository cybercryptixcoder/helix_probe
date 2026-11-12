# Are Sparse Autoencoders Useful? A Case Study in Sparse Probing

- **Key:** arxiv-2502.16681
- **Authors / organisation:** Subhash Kantamneni, Joshua Engels, Senthooran Rajamanoharan, Max Tegmark, Neel Nanda; MIT (Kantamneni, Engels, Tegmark) with Google DeepMind mech-interp collaborators
- **Date:** 2025-02-23
- **Link:** https://arxiv.org/abs/2502.16681
- **Kind:** paper
- **Read from:** full text (main body and key appendices, via the arXiv HTML version)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
SAEs are judged mostly by proxy metrics (reconstruction vs sparsity) because there is no ground truth for which concepts a model uses. The authors ask a sharper question: does an SAE basis give a practical edge on a real downstream task? They pick probing of LLM activations, and deliberately choose hard regimes (little data, class imbalance, noisy labels, distribution shift) where a concept-level basis ought to give an inductive advantage if it is real. The broader aim is to set a standard for showing that an interpretability method is actually useful: beat strong, honestly tuned baselines on a task people care about.

## What they studied
Main model Gemma-2-9B (residual stream, layer 20) with Gemma Scope JumpReLU SAEs; replication on Llama-3.1-8B with Llama Scope TopK SAEs; an architecture comparison on Gemma-2-2B layer 12 width-16k SAEs (eight architectures released 2023-2024). Data: 113 binary classification datasets, probed from the last-token activation (prompts up to 1024 tokens; average test set about 1,945 examples). Unit: SAE latents versus raw residual directions.

## How they did it
1. Baselines on raw activations: L2 logistic regression, PCA regression, kNN, XGBoost and an MLP, each tuned over 10 hyperparameter settings by validation AUC, with up to 1,024 training points.
2. SAE probes: pick the k latents with the biggest class-mean activation difference (k=16 for interpretable probes, k=128 for performance) and fit L1 logistic regression on them.
3. "Quiver of arrows" protocol: a practitioner picks whichever method wins on validation; the value of SAEs is the change in test AUC when SAE probes are added to the quiver. This avoids crediting SAEs for test-set luck.
4. Four stress regimes: 20 training sizes (2 to 1,024), 19 class ratios (0.05 to 0.95), 11 label-corruption levels (0 to 0.5, where validation is also corrupted so they compare logistic regression against a single SAE probe directly), and 8 covariate-shift datasets (GLUE-X extremes, language swaps, name/character changes; 300 shifted test examples).
5. Extra analyses: multi-token (pooled) probes, comparison across SAE architectures and L0, and interpretability-driven uses: pruning spurious latents, finding label errors, finding spurious correlations, each checked against what a plain baseline would have revealed.

## What counts as an explanation here
Not the main object. The SAE latent set is treated as a candidate feature basis; its "explanatory" value is tested indirectly by whether a small set of labelled latents gives better or more robust classifiers, and whether latent labels (autointerp) let a human spot dataset problems. Partial and task-specific.

## How they judged success
Test ROC AUC; marginal AUC gain from adding SAE probes to the quiver; win rate (fraction of datasets where SAE probes beat baselines); AUC curves across each regime's parameter; OOD AUC. Controls: strong tuned baselines, an attention-pooled baseline for multi-token comparisons, and validation-only method selection.

## What they found
- Standard setting: SAE probes were picked as best for 14 of 113 tasks, yet adding them lowered average performance slightly.
- No meaningful average gain in data scarcity, imbalance or label noise, even though SAEs were selected on up to 40 datasets per regime; under covariate shift baselines generalised better.
- SAE probes beat baselines on only about 2.2% of datasets. Max-pooled multi-token SAE probes won 19.6% against last-token baselines, but this fell to 8.7% once an attention-pooled baseline and the quiver were added.
- Newer SAE architectures trended slightly upward, not significantly; lower-L0 SAEs gave worse probes.
- Interpretability uses were real but not unique: pruning spurious latents raised OOD AUC a little (e.g. +0.052 on a QNLI task), far short of the ID-to-OOD gap; one latent scored 0.99 ID but 0.64 OOD because it only fired on English text. A latent exposed apparent CoLA label errors (an LLM vote suggested about 25% mislabelled), and a punctuation latent exposed a spurious cue in AI-vs-human text, but logistic regression baselines exposed the same things.

## Limits and open problems they name
Probing is itself only a proxy for SAE usefulness; the chosen hard regimes may not favour even true features; better-tuned SAE probes might win; some interpretability claims rest on LLM-generated latent labels. Explicitly framed as one rigorous data point, not a dismissal of SAEs.

## What we take from it
- **Method/framing:** the quiver-of-arrows protocol is a clean way to measure the marginal value of any new representation (including a weight-derived one) against tuned baselines, selecting only on validation.
- **Warning:** an interpretable basis does not automatically generalise better; we must show prediction gains against plain linear baselines, and check OOD.
- **Measure:** report win rate over many tasks plus mean AUC change, not a cherry-picked single dataset.
- **Control:** any claimed "insight" from our model should be checked for whether a simple baseline would have revealed it too.

## Tags
unit: feature | direction
form: dictionary | probe
method: SAE | probing
eval: downstream-task | benchmark
goal: evaluation-of-methods
