# Why Larger Models Learn More: Effects of Capacity, Interference, and Rare-Task Retention

- **Key:** arxiv-2605.29548
- **Authors / organisation:** Jing Huang, Daniel Wurgaft, Rachit Bansal, Laura Ruis, Naomi Saphra, David Alvarez-Melis, Andrew Lampinen, Christopher Potts, Ekdeep Singh Lubana; Stanford, Kempner Institute at Harvard, MIT, Anthropic, with a Goodfire logo on the paper (exact Goodfire role not stated in the text read)
- **Date:** 2026-05 (arXiv id; ICML 2026)
- **Link:** https://arxiv.org/abs/2605.29548 (scout link https://www.goodfire.com/research/why-larger-models-learn-more redirects off-site and could not be fetched)
- **Kind:** paper
- **Read from:** abstract and sections (arXiv HTML, first ~80% via summarised fetch: theory, toy and LLM experiments, discussion)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Larger models learn tasks that smaller ones never learn, even with unlimited data. The authors want a mechanistic,
data-centric account of that marginal benefit of scale, rather than appealing to "emergence", and to ask whether scale
is the only route to it (e.g. versus reweighting the data mixture). They frame the question as what is learnable by
gradient descent from a given mixture, not only what a model can represent.

## What they studied
A toy: a mixture of K=32 linear-regression tasks with power-law task frequencies and power-law covariance spectra in
orthogonal blocks (input dim 1024), learned by a shared width-N linear encoder with per-task linear decoders. Real
models: OLMo-architecture LMs from 4M to 4B parameters trained on the first ~210B tokens of Dolma v1.7, with two
synthetic tasks (comparison, modular addition) injected at frequencies from 7.8e-3 down to 2.4e-8 per batch. Units:
learned subspaces, DAS-localised causal features, first-layer MLP neurons and their gradients.

## How they did it
They start from the L(N,D) scaling law and argue that because asymptotic loss falls faster in N than compute-optimal
loss, some tasks require model scale even at infinite data. In the toy they prove the optimal encoder spans the top-N
eigenspace of the mixture covariance, with each feature's "utility" being task frequency times eigenvalue, and
analyse gradient dynamics: frequent tasks' gradients depend only on residual unexplained signal, and a rare feature
is stable only if its utility beats the weakest occupied common feature, else an update-and-forget cycle. They
measure normalised subspace alignment per task and residual frequent-task signal, and use matched-frequency injection
(withhold a rare task for G steps, then reinject a bigger batch) to separate retention from frequency. In the LMs they
track task loss and held-out accuracy, localise causal features with distributed alignment search and a Fourier
variance test, and compare each batch's gradient on top first-layer neurons with a task reference gradient, split
into task-token and non-task-token parts.

## What counts as an explanation here
A mechanistic-dynamical theory: a closed-form allocation rule (which features a width-N model keeps) plus a gradient
interference account of forgetting, checked against DAS-localised features in real LMs. It is predictive: it gives a
critical width at which a rare task becomes learnable.

## How they judged success
Toy: agreement of learned subspaces and per-task loss (normalised by a mean predictor) with the predicted width
threshold; decay of rare-task alignment with injection gap. LMs: training loss and held-out accuracy on injected
tasks; interchange success of DAS features (96% for the comparison task's 1-D token-order subspace); cosine similarity
of batch gradients with the task reference gradient. Natural reference tasks calibrated with infini-gram set realistic
frequencies.

## What they found
In the toy, small models leave frequent-task residual signal and rare tasks stay at chance; past the predicted width,
frequent signal is absorbed and rare tasks are learned; small models forget rare tasks quickly between injections,
large ones accumulate. In LMs only larger models learn low-frequency injected tasks, tasks are learned in frequency
order, grokking on modular addition appears only in larger, more frequently trained models, and bigger injection gaps
hurt at matched total frequency. The causal features appear earlier and stronger in larger models. Non-task-token
gradient similarity to the task direction is 0.10 +/- 0.09 at 20M (interference) vs about zero at 1B.

## Limitations and open problems they name
Scale is not claimed to be the only factor (expressivity and sample efficiency are complementary); not tested beyond
4B or in over-trained regimes; only frequency, not task complexity, varied in LMs; extreme frequencies untested. Open:
complexity effects in LMs, whether upweighting data can substitute for scale, whether frequent tasks overfit, and
whether memorisation-to-generalisation resembles grokking in natural pretraining.

## What we take from it
A predictive (not post-hoc) mechanistic claim, with a threshold, tested by controlled data injection: a design
pattern for our own experiments. Also a warning: which rare features a network holds depends on capacity and on
interference during training, so a white-box model of a small network should expect rare behaviours to be missing or
unstable. Utility = frequency x variance is a simple prior for which features a weight-reader should expect to find.

## Tags
unit: direction | neuron | whole-model
form: causal-abstraction
method: weight-analysis | patching | probing | other
eval: prediction/simulation | patching | downstream-task
goal: science | understanding
