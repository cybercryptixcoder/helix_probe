# Evaluating Sparse Autoencoders on Targeted Concept Erasure Tasks

- **Key:** arxiv-2411.18895
- **Authors / organisation:** Adam Karvonen, Can Rager (independent; equal contribution), Samuel Marks (Anthropic), Neel Nanda; conducted within the MATS programme
- **Date:** 2024-11-28
- **Link:** https://arxiv.org/abs/2411.18895
- **Kind:** paper
- **Read from:** full text — arXiv HTML v1 main body (Sections 1–6), references, and Appendices A.1–A.7 including the probe/SAE training tables, the five intervention-location table, and the complete LLM-judge prompt. No figure inspected (Figures 1–8 are scatter/line plots), so every number quoted here is prose or a table cell.
- **Relevance to us:** 3 (central)

## What they wanted, and why
Dictionary learning had no trustworthy scorecard. The field's standard SAE metrics — cross-entropy loss recovered and L0 sparsity — are unsupervised proxies, and prior work had already shown they can fail to track the property people actually want, namely whether the latents are usable. The authors' goal is a metric that is not a proxy for interpretability but a *downstream task*: can this SAE let you surgically remove one concept from a classifier while leaving the others intact? This is a step toward being able to say "SAE A is better than SAE B" with evidence rather than with loss curves, and — for us — toward scoring an internal read-out by what an intervention on it can do.

## What they studied
Two open models: Pythia-70M (deduped) and Gemma-2-2B (a single layer, 19, named in the results). SAE suite trained by the authors on 200M tokens of The Pile: vanilla/Standard and TopK architectures at expansion 8 (both models) and 32 (Pythia), plus Gemma-Scope JumpReLU SAEs used as a third architecture. Datasets: Bias in Bios (biography → profession and gender, used as the spurious-correlation setting) and Amazon reviews (product category × rating sentiment). Unit of analysis: the individual SAE latent, ranked by its *causal* attribution to a class probe, then zero-ablated in groups.

## How they did it
Three-step recipe per concept: (1) train a binary linear probe for each class on model activations; (2) rank latents by an attribution score that is just the decoder row dotted with the probe weights, times the difference between the latent's mean activation on positive-class and negative-class inputs — cheap because the probe reads the SAE output directly, no backward passes needed when probe and SAE sit at the same layer; (3) ablate the top-N of those latents and re-measure probe accuracy. SHIFT/SCR: train a probe on a *biased* dataset (e.g. only male professors and female nurses), ablate the latents that drive the spurious cue, and score the probe on the balanced dataset — normalised against both the biased baseline and an "oracle" skyline probe trained on the clean label. TPP: generalise to any multiclass dataset by training one probe per class, ablating the latents selected for class i, and comparing the accuracy drop on probe i against the drop on the other probes. Latent selection is either attribution-only, or attribution plus an LLM-judge interpretability filter (Claude 3.5 Sonnet, 0–4 relevance scale, top 5 activating contexts plus top 5 promoted tokens, κ = 0.44 for gender and 0.58 for profession after prompt refinement). N was grown until architectures separated. They then run sanity checks: monotone improvement over training checkpoints, and unimodality across the sparsity sweep.

## What counts as an explanation here
Not an explanation of the model — an explanation of *the dictionary's usefulness*. The claimed object is a causal-isolation capability: a set of latents whose removal damages exactly one concept probe and nothing else. It is deliberately partial (single layer, a handful of hand-chosen concepts, top-N cut-off chosen by hand) and it is predictive in a narrow sense: it predicts what will happen to a downstream classifier when you ablate a given group of latents. Nothing here claims a feature is *the* representation of a concept.

## How they judged success
Three families of check: (a) architectural separation — do TopK/JumpReLU out-score Standard SAEs at matched loss recovered; (b) sparsity shape — is the metric unimodal over L0 with a peaked region, which is what a real quality signal should look like rather than monotonically improving with density; (c) training-progress monotonicity — does the score rise across checkpoints (0%, 1%, 10%, 31%, 100%). Correlation between the LLM-judged and judge-free variants is reported as Pearson r. Tables give probe accuracy before and after debiasing against a clean/oracle reference.

## What they found
- Gemma-2-2B, layer 19: TopK and JumpReLU separate cleanly from Standard on SHIFT, and the sparsity curves for both are unimodal with a peak in L0 ∈ [20, 100]. Standard SAEs are flatter and worse at matched loss recovered.
- Training progress: the first 10% of SAE training (20M tokens) already yields ~85% of the final SHIFT score on average — the metric saturates early, which is either good news (cheap evaluation) or a warning that late-training refinements are invisible to it.
- TPP gives the same architecture ranking, and shows a speed difference: TopK/JumpReLU reach 80% of their final TPP at 10% of training, Standard only at 31%.
- The LLM interpretability filter barely matters for the ranking: SHIFT with and without the judge correlates r = 0.81, TPP r = 0.88.
- On Pythia-70M, a single TopK SAE at layer 4 (residual stream only) reaches 90% ground-truth accuracy on the debiasing task where the original SHIFT work needed 16 Standard SAEs across embedding and layers 0–4, which scored 88%.
- The spurious-feature-informed selection (rank latents by a probe for the *spurious* signal, no judge) is fast and a good proxy for the full SHIFT pipeline; most latents it picks are still judged interpretable, especially in the peak L0 band.
- Biased-probe accuracies on the balanced set are instructive about how fragile the setup is: Pythia's professor/nurse probe sits at 0.77 gender / 0.72 profession before debiasing and moves to 0.52 / 0.91 after, while Gemma-2-2B moves the *other* way (0.64 / 0.86 → 0.83 / 0.65), because in the bigger model the biased probe happened to latch onto profession rather than gender. Which cue the probe picks up is model- and hyperparameter-dependent (probe batch size and learning rate both flip it).

## Limits and open problems they name
The optimal N (how many latents to ablate) is not determined — it grew with model size and there is no principled count. The two metrics disagree about the best sparsity. Their LLM judge is a *relevance* scorer, weaker than a full auto-interp description, and it produces false negatives (they keep anything scored ≥ 1 for that reason). The whole evaluation is built on the premise that SAEs should recover *human-named* concepts, which may miss the latents that matter. They recommend the metrics only as one member of a wider evaluation suite. My own additions: there is no random-latent or firing-rate-matched ablation control anywhere, so "ablating these 50 latents damages probe i and not probe j" is not compared against what ablating 50 arbitrary high-firing latents would do; the reported architecture win depends on a hand-tuned N and a probe strong enough to be debiasable, i.e. on a pre-flight they explicitly say was hard to satisfy; and with one layer and two datasets, "TopK beats Standard" is a claim about a specific training budget (200M tokens) that earlier work has shown shifts with scale.

## What we take from it
- **A method:** the TPP score is the template for scoring any read-out we claim is concept-specific — ablate the read-out's selected latents and require that *other* concept probes be undamaged. The cross-probe asymmetry is the part that costs nothing and rules out most generic "ablation hurts" explanations.
- **A measure:** normalise against a skyline (the oracle probe), not against zero, so numbers are comparable across concepts and models — and report the *ungated* and gated variants so the reader sees how much the interpretability filter is doing (here: almost nothing, r ≈ 0.8).
- **A sanity-check protocol worth copying wholesale:** unimodality in the sparsity sweep, and monotonicity across training checkpoints. Both catch a metric that is secretly just measuring density. The random-init anomaly is the cautionary case: an untrained Standard SAE is dense at L0 ≈ 9000 and scores *well* on TPP when the judge is off, which is exactly the degenerate optimum a density-correlated metric would have.
- **A warning for us:** the fact that the same biased-probe setup debiases in opposite directions on Pythia versus Gemma because the probe happened to capture a different one of the two correlated signals is the clearest small example in this folder of why a probe's accuracy is a statement about *what the probe found*, not about what the model represents.
- **A shortcut:** decoder-row · probe-weights · (mean activation difference) is a one-line latent ranking that needs no backward pass. For any of our own dictionary-plus-probe setups that is the first ranking to try.

## Tags
unit: feature
form: probe
method: SAE | probing | ablation | attribution
eval: ablation | benchmark | faithfulness | downstream-task
goal: evaluation-of-methods
