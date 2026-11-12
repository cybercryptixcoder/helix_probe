# Interpreting Language Model Parameters (adVersarial Parameter Decomposition, VPD)

- **Key:** goodfire-research-interpreting-lm-parameters
- **Authors / organisation:** Lucius Bushnaq, Dan Braun, Oliver Clive-Griffin, Bart Bussmann, Nathan Hu, Michael Ivanitskiy, Linda Linsefors, Lee Sharkey; Goodfire with MATS fellows and an independent researcher
- **Date:** 2026-05-05
- **Link:** https://www.goodfire.com/research/interpreting-lm-parameters (no arXiv ID found; markdown at static.goodfire.ai/vpd-blog-post/post.md)
- **Kind:** blog/research post
- **Read from:** abstract and sections (method, reconstruction, robustness, sparsity comparison, attention analysis, attribution graphs, case studies, editing, discussion; about 60% of the page, appendices largely unread)
- **Relevance to us:** 3 (central)

## What they wanted, and why
This is the parameter-decomposition agenda (APD, then SPD) applied for the first time to a real language model. The
aim is to explain a transformer as a sparse set of weight-space mechanisms that stays inside the original
architecture, unlike transcoders or SAEs that replace parts of the model. A key worry with SPD-style decompositions is
that a few unimportant pieces, ablated together in the wrong combination, could break the model; so they add an
adversary that searches for such combinations, to make causal-importance claims hold up under stress rather than only
under random ablation.

## What they studied
A 4-layer decoder-only transformer, about 67M parameters (about 28M non-embedding), residual 768, MLP 3072, 6 heads,
trained on a public-domain subset of The Pile (validation CE 2.71). All 24 weight matrices, including attention Q/K/V/O,
decomposed into 38,912 rank-one subcomponents (about 9,972 alive, about 205 active per token position). A smaller
SimpleStories model and toy models are also mentioned. Unit: weights (rank-one subcomponents, sometimes clustered).

## How they did it
As in SPD, each matrix is a sum of rank-one subcomponents plus a small residual Delta term penalised by an L2 loss. A
learned causal-importance (CI) function, here a small transformer, gives each subcomponent a value in [0,1] per token
position; an Lp importance-minimality loss pushes most to zero. Reconstruction is required under stochastic masks and,
new here, under adversarial masks found by gradient ascent on reconstruction loss, constrained to ablate only pieces
with low CI. A frequency-minimality loss penalises pieces that are important on many inputs, discouraging splitting
and over-broad mechanisms. They then (a) measure reconstruction under several masking modes, (b) attack the
decomposition with more adversarial steps, (c) compare sparsity and interpretability with per-layer and cross-layer
transcoders (BatchTopK) replacing all four MLPs, (d) analyse attention subcomponents via QK/OV pairs, (e) build
attribution graphs with gradient-based direct effects weighted by CI, pruned either adversarially or by CI alone, and
(f) hand-edit one subcomponent to change emoticon predictions, compared with LoRA fine-tunes.

## What counts as an explanation here
A sparse set of weight subcomponents active on each token, labelled (auto-interp) and wired into per-prompt attribution
graphs. It is meant to be a complete account of the weights (they sum to the model), and it makes testable
predictions: ablating anything outside the claimed active set, even adversarially, should not change the output; and
editing one subcomponent should change a predictable behaviour with little side effect.

## How they judged success
Validation cross-entropy and "pretraining compute recovered" under unmasked, stochastic, rounded and CI masks; KL to the
target as a function of adversarial optimisation steps; sparsity Pareto curves (raw L0, per-MLP reconstruction, total
active parameters) against PLT and CLT baselines; feature splitting vs capacity; intruder-detection interpretability;
graph faithfulness as target-token probability under CI, stochastic and adversarial masking; ablation of named
subcomponents; for editing, KL near the edited positions and globally, against LoRAs trained on 10 or 947 examples.

## What they found
Unmasked reconstruction is nearly lossless (CE 2.72); with stochastic masks CE 2.84 (26.9% of compute recovered),
with CI-as-masks 2.99 (9.4%), which they set against roughly 10% for a top-k SAE replacing one GPT-4 layer. Robustness
is partial: KL 0.83 after 20 adversarial steps but 25 at 160 and 40 at 320. VPD Pareto-dominates transcoders on
sparsity, though largely because of its end-to-end objective; with matched objectives the gap vanishes. Interpretability
by intruder detection is competitive with layerwise transcoders and better than end-to-end ones. VPD's number of alive
pieces stays around 6,500 to 7,000 as capacity grows from 0.5x to 4x, whereas transcoder latents grow roughly linearly
(less feature splitting). Attention pieces span heads; examples include an always-on previous-token query/key pair and
detectors for "there is"/"it is". In graphs, a 6-piece CI-pruned circuit looked sufficient (0.895 probability) but fell
below 0.0005 under adversarial masking, while a 150-piece adversarially pruned graph held at 0.443 vs 0.586 original.
The emoticon edit worked but was beaten by a LoRA on 947 examples on both KL measures.

## Limitations and open problems they name
Robustness breaks under strong adversaries (and full robustness may not even be desirable because of benign
interference). Attribution graphs are local, gradient-based and do not capture nonlinear interactions between pieces.
Loss terms (frequency minimality) are proxies, not proven optimal. Only one 67M model analysed in depth; cross-layer
attention ("virtual heads") not studied; auto-labelling missed some behaviours; clustering crude. Editing preliminary
and cherry-picked.

## What we take from it
The strongest current evidence that weight-space decomposition can be run on a real transformer and produce a
complete, architecture-preserving account. Two directly reusable measures: "pretraining compute recovered" under
ablation, and adversarial-mask stress testing of any claimed circuit (the 6-piece vs 150-piece result is a sharp warning
that small circuits pruned by importance alone can look faithful and be badly incomplete). Also a reference baseline
set (PLT, CLT, intruder detection) and a weights-level editing test against LoRA, which fits our "predict under
intervention" goal.

## Tags
unit: weights | head | circuit
form: replacement-model | graph | dictionary
method: decomposition | weight-analysis | attribution | ablation | transcoder
eval: ablation | faithfulness | completeness | human-rating | prediction/simulation
goal: understanding | control/editing | evaluation-of-methods
