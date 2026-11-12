# Stochastic Parameter Decomposition (Goodfire post: "Towards Scalable Parameter Decomposition")

- **Key:** arxiv-2506.20790
- **Authors / organisation:** Lucius Bushnaq, Dan Braun, Lee Sharkey; Goodfire (work mostly done at Apollo Research)
- **Date:** 2025-06 (v2 revised 2025-09)
- **Link:** https://arxiv.org/abs/2506.20790 (Goodfire post: https://www.goodfire.com/research/stochastic-param-decomp)
- **Kind:** paper
- **Read from:** abstract and sections (method, all toy-model results, discussion; appendices only partly)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors want to reverse-engineer networks by splitting their weights into a sum of parameter-space pieces, each of
which is needed on only a few inputs ("linear parameter decomposition"). The predecessor, APD (arxiv-2501.14926),
worked on toy models but was memory-hungry (every component is a full-model-sized vector), very sensitive to its top-k
hyperparameter, and relied on gradient attributions as a stand-in for causal importance. SPD is meant to remove those
three obstacles so that parameter decomposition can eventually be run on real language models. They frame it as a
merger of causal mediation analysis with network decomposition.

## What they studied
Toy models with known ground-truth mechanisms: Toy Models of Superposition TMS_5-2 and TMS_40-10, plus new variants
with an extra identity matrix in the hidden space (TMS+ID); a toy model of compressed computation (one residual MLP,
d_resid 1000, 50 neurons, 100 features, computing x + ReLU(x) per feature); and cross-layer distributed models with 2
blocks (2 x 25 neurons) and 3 blocks (3 x 17 neurons, 102 features). Unit: weights, as rank-one subcomponents per
matrix.

## How they did it
Each weight matrix is written as a sum of C rank-one subcomponents (outer products U_c V_c), with C allowed to exceed
the matrix rank so that superposed mechanisms can each get their own piece. A faithfulness loss makes the
subcomponents sum to the original weights. For each subcomponent, a tiny MLP reads that subcomponent's scalar "inner
activation" on the current input and outputs a causal importance g in [0,1] via a leaky hard sigmoid. During training,
each subcomponent is multiplied by a stochastic mask m = g + (1 - g) r with r uniform in [0,1], so unimportant pieces get
ablated by random amounts; a stochastic reconstruction loss (output divergence of the masked model vs target, all
layers masked) and a layerwise version (one layer masked at a time) force the model to still work under any such
partial ablation. An importance-minimality loss (sum of |g|^p) pushes importances toward zero. The reparametrisation
trick sends gradients through the masks into the importance MLPs. APD's simplicity (Schatten-norm) penalty is dropped
because rank-one, single-layer pieces are already simple. Subcomponents are then grouped into full components (done by
inspection in the toys; no general clustering algorithm). Biases are not decomposed.

## What counts as an explanation here
A decomposition of the weights into mechanisms (parameter-space vectors), plus a learned per-input causal-importance
function saying which mechanisms the network needs on each input. It is meant to be complete (sums exactly to the
weights) and to predict that ablating unimportant pieces in any combination leaves the output unchanged.

## How they judged success
Recovery of known ground truth: Mean Max Cosine Similarity (MMCS) between target weight columns and best-matching
subcomponents, and Mean L2 Ratio (ML2R) to detect shrinkage; visual comparison of subcomponent neuron contributions
with the target model's; counting whether the expected number of components appears (e.g. 100 W_in pieces and one
rank-50 W_out piece). Baseline: APD on the same toys. Robustness across seeds and to the importance coefficient beta3.

## What they found
On all four TMS variants MMCS was 1.000 and ML2R between about 0.99 and 1.03, i.e. near-perfect recovery with
negligible shrinkage (APD had shrinkage around 0.9). Variants with an identity matrix, which APD found very hard, were
decomposed easily. In compressed computation SPD found one W_in piece per input feature and a single rank-50 W_out
component, while APD wrongly split W_out into about 100 pieces. SPD decomposed the 3-layer cross-layer model, which
APD could not handle. Too small beta3 leaves polysemantic pieces; too large splits components and raises
reconstruction loss; a middle range works. Some seed sensitivity and an unexplained skew remain in the 2-layer model.

## Limitations and open problems they name
Only toy models; scaling to LMs needs more training-stability work. Grouping subcomponents into multi-rank or
multi-layer components needs a clustering method when ground truth is unknown. The importance function sees only its
own subcomponent's activation (may be too weak). Biases are not decomposed. Both APD and SPD bias solutions toward
within-layer mechanisms; layerwise importance may miss downstream information.

## What we take from it
A concrete recipe for reading mechanisms out of weights with a built-in causal test: "the network still works when
every piece deemed unimportant is randomly ablated" is a usable, checkable definition of a faithful decomposition, and
the learned importance function is effectively a predictor of which weights matter on a given input. MMCS/ML2R on
planted toy models is a cheap validation protocol we can copy before running on a real target. Warning: the
clustering step is unsolved, so outputs are rank-one fragments, not ready-made modules. Code: github.com/goodfire-ai/spd.

## Tags
unit: weights
form: replacement-model | causal-abstraction
method: decomposition | weight-analysis | ablation
eval: ablation | faithfulness | benchmark
goal: understanding | science
