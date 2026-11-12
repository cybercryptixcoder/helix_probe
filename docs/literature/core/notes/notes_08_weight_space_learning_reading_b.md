# Notes: weight-space learning and LLM weight reading (batch 08b)

**What an explanation is here.** Two separate traditions. Weight-space learning (arxiv-2603.10090, arxiv-2603.15990)
treats a trained embedding as the "reading": it predicts coarse properties (accuracy, training attributes, task
identity) and offers no mechanism. LLM weight reading (arxiv-2610.07334, rikiyat-github-io-blog-weight-space-programming)
produces verbal or question-answer outputs (which game, which heads, is it backdoored), and in Sparks the strongest
evidence is a targeted weight edit that changes behaviour as predicted. Only Weight Oracles' Stage I predicts
per-input outputs, and only by splitting the forward pass into per-projection steps with nonlinearities in code.
No paper here produces a predictive, inspectable model of the target network. That gap is ours.

**How success is measured.** Property prediction (Pearson/MAE, F1, AUROC), retrieval (NDCG@10), anomaly detection
(AUROC, TPR at fixed FPR), identification accuracy out of very small N (Sparks: 3-4 cases per task), and downstream
benchmark change after an edit (MATH-500, GSM8K, IFEval).

**Recurring baselines and controls.** Simple weight statistics (L2 norm, singular values) are strong (arxiv-2610.07334);
equivariant encoders (GLNet, DWSNets, NFN) are the standard learned baselines (arxiv-2603.10090, arxiv-2603.15990);
a reader that ignores weights is the essential shortcut control (Weight Oracles' 45.1% plateau equalled it). The
stratification battery (lesswrong-wnl4nwrs2owzzfwiz-wsp-stratification: shuffled, untrained, prompt-only,
anonymised labels, layer subsets, sparsified weights, default-answer rate) shows one reader genuinely using weights
and another using labels and priors at similar headline accuracy.

**Methodological warnings.** Access regime must be stated and never pooled: raw weights only vs weights plus code vs
weights plus forward passes (honnibal-dev-blog-astra-read-write-misleading). In Sparks, raw-weight reading succeeded
only on 17K-172K-weight networks; all LM-scale wins used Python and/or execution. Symmetries matter: canonicalising
away the LoRA GL(r) symmetry was the largest single gain in W2T, and invariance under random symmetry transforms is a
cheap sanity test.

**Open problems.** Scaling readers to large models (token count grows with parameters), architecture heterogeneity,
incomplete symmetry theory for transformers, detecting mechanisms rather than statistical correlates, and high false
positive rates for auditing.

**For a predictive white-box model from weights.** (1) Compose small verifiable pieces rather than predict end to end.
(2) Report every result per access regime, with a weights-only arm. (3) Run the stratification controls plus a
weight-ignoring baseline and weight-statistic baselines. (4) Canonicalise symmetries first and test invariance.
(5) Validate readings by predicted-effect edits, including a negative-control model where the edit should not help.
