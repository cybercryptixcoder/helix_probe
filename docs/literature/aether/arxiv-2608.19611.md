# Forking Fast: Efficiently Estimating Uncertainty Dynamics in Text Generation

- **Key:** arxiv-2608.19611
- **Authors / organisation:** Eric Bigelow, Amir Zur, Satchel Grant, Tal Haklay, Can Rager, Owen Lewis, Thomas McGrath, Jack Merullo, Ekdeep Singh Lubana, Atticus Geiger; Goodfire (with academic collaborators)
- **Date:** 2026-08-20
- **Link:** https://arxiv.org/abs/2608.19611 (project page https://www.goodfire.com/research/forking-fast; code/dashboard https://github.com/ericb-goodfire/forking-fast)
- **Kind:** paper
- **Read from:** full text (arXiv HTML v1, main text plus appendices A–H)
- **Relevance to us:** 3 (central)

## What they wanted, and why

Sampling-based accounts of how a model arrives at an answer are expensive: characterizing uncertainty means resampling continuations at every step of a reasoning chain. Forking Paths Analysis (FPA) of a single chain can burn millions of tokens, which puts step-level attribution of uncertainty out of reach for routine studies. The authors ask a sharper question than "make it cheaper": what is the right statistical model for the curve that resampling produces? If the answer is "smooth curve plus a few discontinuities plus multinomial noise", then most of the sampling budget is being spent re-measuring structure that neighbouring positions already contain — and the money can be moved into a model. The larger goal is to turn resampling from an expensive diagnostic into a cheap, standard primitive for reading how uncertainty evolves through a generation.

## What they studied

Two 8B models — Llama-3-8B-Instruct under explicit chain-of-thought prompting, and DeepSeek-R1-Distill-Llama-8B as a native reasoning model — on tinyMMLU (100 multiple-choice questions). The unit of analysis is a *curve over time*, not a feature or a direction: for each token position (or sentence position for the reasoning model) along a greedy-decoded base path, they estimate a distribution over the five final outcomes (A/B/C/D/Other). Everything is whole-model behaviour, indexed by position.

## How they did it

They reimplement the FPA recipe: take the greedy chain as the base path, and at each position resample continuations for every alternative next token whose probability is at least 0.05, drawing S continuations at temperature 1.0 and recording each continuation's final answer. Positions are aggregated into a weighted outcome distribution per timestep, weighted by next-token probability × continuation probability, in the style of a step-importance curve. They then collect a reference with S=200 (and S=1000 for two development questions), giving 1.77B tokens in total, and compare lower-sample runs (S from 5 to 100; stride N of 1, 2, 4, 8, 16, 32 tokens, or 1–8 sentences for DeepSeek) against it. The core contribution is a three-stage smoother: PELT change-point detection with an exact multinomial cost to segment the path into flat-or-drifting stretches; Gaussian-kernel-weighted Dirichlet pooling of counts within each segment, truncated at the detected boundaries so drift can be captured without blurring discontinuities; and cross-validation over the same low-sample data (e.g. S=20 split into five folds of 4) to tune the PELT cost function and penalty and the kernel bandwidth. They also verify the noise assumption directly by splitting large sample sets into disjoint equal-size subsets and measuring pairwise distance between the resulting estimates.

## What counts as an explanation here

A statistical model of the uncertainty curve, used as a *replacement for sampling*: the explanation is not "this token mattered because direction v", it is "the outcome distribution over final answers is piecewise-smooth in position, with a multinomial sampling law, and a small number of change points." That is a surrogate for the true uncertainty dynamics, and its claim to adequacy is predictive — it reconstructs a curve it did not sample. It is explicitly partial: it explains the *noise and shape* of the curve, not the mechanism producing any particular fork.

## How they judged success

Total variation distance between each low-sample (and smoothed) outcome curve and a high-sample reference (S=200, N=1), reported pooled over questions and separately restricted to forking regions (±10 tokens around a fork, with fork thresholds ε of 0.10, 0.15, 0.20 defined as TVD between adjacent positions). Comparison is both at fixed S and at fixed *token cost*, i.e. the accuracy/cost Pareto frontier. Ablations peel the smoother apart — raw data with linear interpolation, kernel pooling alone, segmenting plus flat per-segment pooling, the full model — with paired per-question TVD differences against leave-replicate-out references and 95% t-intervals, plus a preregistered test at larger forks. They also compare the measured replicate-noise slope to an exact i.i.d. multinomial null.

## What they found

Replicate noise follows the sampling law: pooled TVD between disjoint sample subsets falls with a log–log slope of −0.4903 overall (−0.5047 in the tail), essentially −1/2, and measured replicate distances sit within a couple of percent of the exact multinomial null. Variation across runs at S=200 is nearly identical to variation within a run (0.0451 vs 0.0442), so noise is an artefact of sampling rather than sensitivity to individual tokens. Smoothing buys real efficiency: at one-token spacing, effective sample-size multipliers over raw data are 22.1× at S=5, 7.3× at S=30 and 1.6× at S=100; at 4-token spacing, 5.0× / 3.3× / 1.0×; the reasoning model at sentence spacing gives 4.9× / 3.1× / 1.1×. Excess TVD above the reference noise floor falls monotonically from 0.0265 (S=5) to 0.0056 (S=100). On cost, raw data likes wide strides (averaging over a window reduces variance for free), whereas smoothed curves slide along the same Pareto frontier, so stride and sample count become interchangeable — and combining the two cuts the budget to one-eighth for a small error increase. In forking regions the picture is harsher: at S=30, fork-region TVD rises 0.0669 → 0.0936 → 0.1587 as spacing goes 4 → 8 → 16 tokens and saturates near 0.16 at 32–64, i.e. the fork has been skipped entirely.

## Limits and open problems they name

Narrow scope: one multiple-choice benchmark, two 8B models, five-way outcomes, short rollouts (≤400 tokens Llama, ≤1536 DeepSeek) — longer horizons, open-ended outputs and larger models are untested. Hyperparameters were developed on two questions from one model, so the tuning procedure itself is not held out (the evaluation data is, but from the same task family and scale). The smoother's advantage is fork-size-dependent: solid at threshold 0.10, degraded at 0.15 (n=35), and at the largest 0.20 forks smoothing is marginally *worse* than raw data (n=21) — the number that matters most near a big decision point. The 90% credible intervals under-cover badly (empirical 0.48–0.64), so only point estimates are advised. The reference curves are themselves finite-sample estimates with a non-zero noise floor. Ablations show segmentation matters only near forks, kernel pooling adds a small consistent gain (+0.0021 TVD when removed), and PELT's cost function barely matters end-to-end — but removing segmentation blurs forks that the full model keeps (on one recorded DeepSeek example, TVD 0.2720 vs 0.0088). They also report a footgun in the `ruptures` library: a custom cost object not inheriting from `BaseCost` is silently replaced by least-squares, changing results with no warning. Future work gestures at a mechanistic theory of in-context learning behind these dynamics, and at adaptively *choosing* which positions to sample rather than post-hoc smoothing.

## What we take from it

A method, and a discipline. (1) *The noise law is a free variance budget*: before building any estimator on sampled behaviour curves — probe-by-token curves, monitor scores over a trajectory, step-level attribution — measure replicate-to-replicate distance on log–log axes; a −1/2 slope licenses pooling, any flatter slope means the signal is real and must not be smoothed away. The disjoint-subset trick is a two-line protocol we can run on anything. (2) *Segment-and-pool is the reusable estimator shape*: detect discontinuities first, then smooth inside segments, because a monotone smoother destroys exactly the events you care about. This is the same distinction the loss-curvature and belief-dynamics entries draw between "regime" and "within-regime trend". (3) *Report accuracy at matched cost, and report it separately in the regions that matter* — their pooled gains (15×) are much larger than their fork-region gains (4×), and the pooled number alone would overstate the method; the same is true of any monitor frontier we plot. (4) A framing worth stealing for prediction-under-intervention: resampling multiple continuations from a prefix *is* an intervention (do(prefix)), so a statistical model of outcome distribution vs. intervention point is a predictive white-box model of exactly the sort we are building, with position standing in for the intervention parameter. (5) Two warnings — a fork-sized advantage reverses at the largest forks, and credible intervals under-cover; prefer point estimates plus an explicit error bar from replicates. (6) A small gift: 1.77B tokens of FPA data and a dashboard are public, plus a library bug worth checking in any PELT-based segmentation we write.

## Tags

unit: whole-model
form: replacement-model
method: other (resampling / forking paths; change-point segmentation; Dirichlet pooling)
eval: prediction/simulation | benchmark
goal: understanding | evaluation-of-methods
