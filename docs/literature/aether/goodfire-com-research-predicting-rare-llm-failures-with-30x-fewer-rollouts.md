# Predicting Rare LLM Failures with 30× Fewer Rollouts

- **Key:** goodfire-com-research-predicting-rare-llm-failures-with-30x-fewer-rollouts
- **Authors / organisation:** Francisco Pernice (MIT), Santiago Aranguri (Goodfire)
- **Date:** 2026-05-13
- **Link:** https://www.goodfire.com/research/predicting-rare-llm-failures-with-30x-fewer-rollouts
- **Kind:** paper
- **Read from:** full text (LessWrong mirror of the Goodfire post, including appendix and comment thread)
- **Relevance to us:** 3 (central)

## What they wanted, and why

A behaviour that happens once in a million generations will almost never appear in a pre-deployment test
suite, but it will appear in production. The practical obstacle is that estimating a rate that low by
sampling requires an enormous number of rollouts of the target model. Their observation is that labs
usually also possess a *less safe* version of the same model — an abliterated checkpoint, an earlier
pre-safety-training checkpoint — where the same failure is common. The goal is to turn "we have a variant
where this is frequent" into a calibrated estimate of the failure rate of the model you actually ship,
without paying for a million samples. This is squarely the prediction problem: estimate a quantity of the
target model by intervening on a related system and extrapolating, rather than by observing the target
directly.

## What they studied

Qwen 3 4B as the target and Qwen 3 4B Abliterated (refusal direction removed) as the unsafe variant.
Data: the 200 standard harmful prompts from HarmBench; responses graded pass/fail by the StrongREJECT
refusal rubric with GPT-5.4-mini as judge. Unit of analysis: the model's *output distribution* — the
object being estimated is a single scalar per prompt, the probability of compliance, and the method
manipulates the model as a whole (its next-token logits) rather than any internal component.

## How they did it

Two stages. **Interpolation:** they build a one-parameter family of models M(α) between the abliterated
checkpoint (α = 0) and the real model (α = 1) by logit arithmetic — at every step, compute the next-token
logits from both checkpoints and sample from their α-weighted combination, feeding the sampled token back
into both contexts and repeating. This is autoregressive decoding from a mixture of two models' logits, not
a mixture of independently sampled tokens. **Extrapolation:** they measure the compliance rate of M(α) on
a prompt at intermediate α, where it is common, then fit a straight line to log₁₀(compliance) against α
using only the points below 50% compliance (the regime where the relation looks linear) and extrapolate
that line to α = 1. Operationally the scan starts at α = 0.95 and walks down in 0.05 steps drawing 10
rollouts, stops once the rate reaches 50%, then walks back up drawing n_fit rollouts per α (13–100 in their
experiments), stopping at the first α with zero compliant samples, and fits the log-linear regression to
the remaining points. If fewer than two α values show nonzero compliance, the prediction defaults to 10⁻⁶
(under 1 in 100 prompts on average). Each prompt carries 100,000 precomputed target-model rollouts so the
ground-truth rate is known.

## What counts as an explanation here

Not an explanation in the mechanistic sense — no features, circuits or descriptions. What is offered is a
**quantitative predictor of an unobserved behaviour rate**: a functional form (log-compliance linear in the
interpolation parameter) plus a fitted slope, derived from a neighbouring model. It is explicitly partial
and explicitly conditional on having that neighbour. The claim is predictive, not causal-mechanistic: they
do not say *why* compliance moves smoothly along the logit path, only that it does and that this lets you
read off the endpoint.

## How they judged success

Prompts are split into two groups: those the target model never complies with in 100 rollouts, and
those it complies with at least once in 100,000 (so they differ in a known rare-failure status). Success is
AUROC for separating those two groups at a given rollout budget, averaged over 500 Monte Carlo simulations,
each drawing random subsets of 1,000 precomputed rollouts per α. Baselines: **naive sampling** at the same
budget (drawing k rollouts from the target model, score = number compliant, modelled as Binomial(k, p) for
budget sweeps) and **importance sampling** from the abliterated proposal with per-rollout likelihood-ratio
weights (they also tried self-normalised importance sampling; it did worse). Temperature 1 throughout.
Controls: budget is swept rather than fixed, and the comparison is at matched AUROC, not at a single point.

## What they found

Logit Path Extrapolation reaches naive sampling's AUROC with up to 30× fewer rollouts. With 100 rollouts per
α, 20× fewer total rollouts sufficed; splitting the budget into a coarse search (10 rollouts per α, to find
where the fit should start) and a denser fit (100 rollouts per α) gave 28×; the headline figure of 30× comes
from the same search plus a smaller fit budget. It outperforms importance sampling, the prior best method,
which they report as clearly worse on the same AUROC-versus-budget curve. The log-linear relation between
log compliance and α holds well below 50% compliance and degrades near certainty.

## Limits and open problems they name

Two limits, stated plainly: the method needs a second model in which the behaviour is common, and the
log-linearity below 50% compliance is an empirical regularity that may fail elsewhere. Beyond what they say:
the estimator has no error bars in the post, only an AUROC over Monte Carlo draws; the 10⁻⁶ fallback is a
floor that silently carries no information; and the whole construction assumes the unsafe variant fails in
the *same way* as the target, so that the interpolation path is a plausible path for the target's own
probability mass. A commenter (Caleb Biddulph, AI control) makes that last point sharply with a toy example —
if the unsafe model says one insult and the target occasionally says a different one that the mixture never
upweights, the extrapolation returns a rate that is far too low — and proposes capping the per-token
probability ratio between the two models (an infinity-Rényi divergence cap) so that the sample is
adversarially robust and yields a hard lower bound instead. The authors accept the criticism and note the
cap is a better *proposal distribution*, which is an importance-sampling improvement rather than a fix to
the extrapolation.

## What we take from it

- **Method (transferable):** estimate a rare property of model A by walking a continuous path to model B
  where the property is common, measuring along the path, and fitting a low-parameter trend in log space.
  The parameter count (one slope, one intercept) versus the number of observed cells is the same economy we
  saw in the belief-dynamics surface fit — and, as there, the honest evaluation holds out part of the grid.
- **Measure:** AUROC between "rare but real" and "never happens" prompt sets, plotted against sample budget.
  A metric that is a *curve over cost*, not a single number, is the right shape for any predictive claim we
  make about a black box.
- **Framing:** white-box access here buys something unusual — not an internal readout but the ability to
  *construct new systems on demand* (interpolants) and query them. For our white-box model this suggests a
  protocol: predicted behaviour under intervention should be checked against a family of nearby models, not
  just the one model we read.
- **Warning:** extrapolation along a path nobody validated is only as good as the assumption that the
  endpoint's failures lie on that path. Any prediction we produce by moving along a direction (steering,
  weight interpolation, α-mixing) inherits this and needs a matched-shape check: does the target's actual
  failure mode resemble the failures we amplified?
- **Warning:** a log-linear fit through a handful of nonzero-rate points to a rate a million times smaller
  is an enormous extrapolation in the dependent variable; report the fit's support and refuse to report a
  number when fewer than two nonzero cells exist.

## Tags

unit: whole-model
form: replacement-model
method: weight-analysis, steering, other
eval: prediction/simulation, benchmark
goal: safety/auditing, evaluation-of-methods
