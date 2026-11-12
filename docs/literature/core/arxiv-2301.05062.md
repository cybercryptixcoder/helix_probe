# Tracr: Compiled Transformers as a Laboratory for Interpretability

- **Key:** arxiv-2301.05062
- **Authors / organisation:** David Lindner, János Kramár, Sebastian Farquhar, Matthew Rahtz, Thomas McGrath, Vladimir Mikulik; Google DeepMind
- **Date:** 2023-01
- **Link:** https://arxiv.org/abs/2301.05062
- **Kind:** tool
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Interpretability methods are hard to validate because we never know the true mechanism inside a trained network.
The authors build a compiler that turns a known program into real transformer weights, so the mechanism is known
by construction. These compiled models act as ground truth for testing whether interpretability tools (probes,
attribution, circuit discovery) recover what is actually there. The larger aim is a laboratory of fully understood
models in which interpretability claims can be checked.

## What they studied
Decoder-only transformers (no layer norm) compiled from RASP programs: frac_prevs (fraction of earlier tokens equal
to "x"), sort_unique, sort with duplicates, pair_balance, Dyck-n, and the other tasks from the RASP paper. Unit of
analysis: residual-stream subspaces, attention heads, MLPs, and whole-model weights.

## How they did it
A RASP program is turned into a computation graph; for each sequence operation the compiler infers its value set,
translates each node into an attention block (select/aggregate) or MLP block (elementwise), assigns blocks to
layers by longest path from the input, gives each variable its own orthogonal residual-stream subspace (one-hot for
categorical values, a single dimension for numerical ones), and assembles weight matrices via an intermediate
representation called Craft with labelled basis directions. Categorical MLPs are lookup tables; numerical MLPs are
piecewise-linear approximations. Restrictions: a BOS token is required, attention inputs must be categorical, and
selectors cannot be combined with boolean logic. In a compression study they freeze all compiled weights and learn
only a projection W from the residual stream (dimension D) to a smaller d, trained with output loss plus a per-layer
matching loss to the original model's activations (AdamW, 3x10^5 steps, batch 256, CPU), and compare the learned
projection's kept features with PCA.

## What counts as an explanation here
The source program itself: a transformer whose every weight is traceable to a line of RASP code and every residual
dimension carries a named variable. The compiled model is the explanation's ground truth against which other
explanations are scored.

## How they judged success
Correctness of compiled models on their programs (exact outputs on example inputs); for compression, task
performance as a function of d, plus cosine similarity between compressed and original layer outputs to test
whether the compressed model still implements the same mechanism.

## What they found
Compilation works for all RASP-paper tasks under the restrictions. frac_prevs compiles to a 14-dimensional residual
stream and four layers (two of them no-ops). Compression of frac_prevs reaches d=6 with no performance loss; below
that it degrades. The learned projection superposes related features (e.g. `is_x` and the token-x indicator) and
drops unused ones more cleanly than PCA. For sort_unique, the compressed model is nearly perfectly accurate but its
layer outputs have only about 0.8 average cosine similarity to the original, because it switched one variable to a
numerical encoding: behaviourally equivalent but mechanistically different.

## Limitations and open problems they name
RASP covers deterministic sequence-to-sequence maps, not next-token distributions, and uses only binary attention.
Compiled models are wasteful (a subspace per variable per layer). Weights are hand-set and features are
basis-aligned, so these models are easier than learned ones and results may not transfer; compiled models will
likely never be full language models.

## What we take from it
A benchmark generator: compiled models give exact ground truth for testing a weights-to-program reader, and the
compiled weights can be compressed to introduce superposition while keeping behaviour. A warning from the
compression result: matching behaviour does not imply matching mechanism, so our white-box model should be judged
on internal agreement (per-layer similarity) as well as outputs. A reusable idea: replacing components with compiled
equivalents as a test of understanding.

## Tags
unit: weights, layer, head, whole-model
form: program
method: weight-analysis, other
eval: benchmark, faithfulness
goal: evaluation-of-methods, science
