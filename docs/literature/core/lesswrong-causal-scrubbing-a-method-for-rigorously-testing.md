# Causal Scrubbing: A Method for Rigorously Testing Interpretability Hypotheses

- **Key:** lesswrong-causal-scrubbing-a-method-for-rigorously-testing
- **Authors / organisation:** Lawrence Chan, Adrià Garriga-Alonso, Nicholas Goldowsky-Dill, Ryan Greenblatt, Jenny Nitishinskaya, Ansh Radhakrishnan, Buck Shlegeris, Nate Thomas; Redwood Research
- **Date:** 2022-12-03
- **Link:** https://www.lesswrong.com/posts/JvZhhzycHu2Yd57RN/causal-scrubbing-a-method-for-rigorously-testing
- **Kind:** blog/research post
- **Read from:** full text of the main post plus comments (the three companion posts in the sequence were not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Circuit claims were being checked by ad hoc ablations chosen by the researcher. Redwood wanted a single, automatic
test, analogous to property-based testing, that takes a precisely stated hypothesis about how a model computes a
behaviour and returns a number saying how much of the behaviour that hypothesis explains. The goal is to make
interpretability claims falsifiable and comparable, as a step toward trustworthy mechanistic understanding for
alignment.

## What they studied
A small model trained to check whether parentheses are balanced, and a 2-layer attention-only transformer for
induction behaviour. Unit of analysis: nodes of a computational graph (heads, MLPs, paths between them, positions).

## How they did it
1. A hypothesis is a triple: the model's computational graph G (rewritable into any equivalent form), a simpler
   interpretation graph I describing the claimed algorithm, and an injective mapping from I's nodes into G.
2. Nodes of G outside the image of I are claimed not to matter.
3. Scrubbing: for each node, replace its inputs with activations computed on other dataset inputs that the
   hypothesis says are equivalent. Important inputs are resampled from data agreeing with the reference input on
   the corresponding interpretation node (applied recursively); unimportant ones are resampled from one random datum.
4. Run the model with all these swaps and compare the expected loss to the unscrubbed model.
5. Refine the hypothesis by adding pathways and re-test.
They argue for resampling ablation over zero or mean ablation because the latter push activations off distribution.

## What counts as an explanation here
A hypothesis graph: an interpretation graph mapped onto the model's computation graph, stating which features each
node computes and which paths matter. Meant to be a complete account of one behaviour on one distribution, graded by
how much loss it preserves.

## How they judged success
Percentage of loss recovered: model loss = 100%, loss with randomly permuted labels = 0%, scrubbed loss placed on
that scale. No other baselines; hypotheses are compared with each other.

## What they found
Paren balancer: one claim alone recovers 93%; combining all three claims recovers 72%, read as reasonably but not
fully accurate. Induction: the naive two-head story recovers 35%; adding a three-token attention window, layer-0
dependencies of queries and values, and special-casing three heads raises it to 86%.

## Limits and open problems they name
Only exactly equivalent swaps are allowed, so continuous features are hard to test; swaps must exist in the dataset;
perfectly correlated features cannot be told apart; the test does not reliably reject false or incomplete
hypotheses, because inhibitory components can be ignored and independent resampling of correlated terms adds
variance that can make a wrong hypothesis look better. They suggest an adversarial process to sharpen hypotheses.
In comments a co-author later regretted believing he understood what the scrubbing numbers meant.

## What we take from it
A scoring rule for a white-box model: resample everything the explanation says is irrelevant and measure retained
loss. Our reconstructed model makes the same kind of claim, so "loss recovered under resampling ablation" is a
recognised measure we can report. Warnings: high scores can come from cancellation and variance effects, so pair it
with tests that try to break the hypothesis (adversarial resampling, inhibitory paths). Use resampling, not zero
ablation, as the default intervention.

## Tags
unit: circuit, head
form: causal-abstraction, graph
method: ablation, patching
eval: ablation, faithfulness, completeness
goal: understanding, evaluation-of-methods
