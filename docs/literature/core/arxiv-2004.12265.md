# Investigating Gender Bias in Language Models Using Causal Mediation Analysis

- **Key:** arxiv-2004.12265
- **Authors / organisation:** Jesse Vig, Sebastian Gehrmann, Yonatan Belinkov, Sharon Qian, Daniel Nevo, Simas Sakenis, Jason Huang, Yaron Singer, Stuart Shieber; Salesforce Research, Harvard, Technion, Tel Aviv University
- **Date:** 2020-04 (first arXiv version; the HTML read is the extended version of the NeurIPS 2020 paper)
- **Link:** https://arxiv.org/abs/2004.12265
- **Kind:** paper
- **Read from:** full text (arXiv HTML, extended version; final ~8% of the page, mostly appendix, not covered)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Probing and attention visualisation tell you what a representation contains, not what it does to the output. The
authors import causal mediation analysis (Pearl's total, direct and indirect effects) so that individual neurons
and attention heads can be treated as mediators between an input change and an output change. Gender bias is the
case study: they want to know which components carry the effect of a gendered/stereotyped input word on the model's
pronoun prediction, how sparse that set is, and whether components act independently. The larger goal is a
general structural-plus-behavioural interpretability method for NLP models; this is a historical root of
activation patching.

## What they studied
GPT-2 at five sizes (distil 82M, small 117M, medium 345M, large 774M, xl 1.5B), a randomly initialised GPT-2 small
as a control, plus Transformer-XL, XLNet, BERT, DistilBERT and RoBERTa. Data: Winobias (160 dev / 130 test),
Winogender (44 examples), both recast as continuation tasks, and a professions template set (17 templates x 169
professions = 2,873 prompts). Units: individual neurons in the representation of the profession word, and
attention heads (the attention from the final pronoun position to the rest of the sentence).

## How they did it
1. Define a bias score y = p(anti-stereotypical pronoun) / p(stereotypical pronoun) for a prompt.
2. Define interventions on the input: set-gender (replace the profession with an explicitly gendered word, e.g.
   nurse -> man), swap-gender for the Winograd sets (she -> he), and null (no change).
3. Total effect: relative change in y between the intervened and original input.
4. Natural indirect effect of a component: run the original input but set that component to the value it takes
   under the intervened input (this is what is now called activation patching).
5. Natural direct effect: run the intervened input but hold the component at its original value.
6. Compute effects for every neuron and every head individually, then for sets chosen by top-K or greedy search, to
   measure sparsity (how few components reproduce the full effect) and synergy (summed single effects vs. joint
   effect).
7. Repeat across model sizes, architectures, a random-weights control and alternate bias metrics (relative
   l-infinity, normalised difference, total variation distance).

## What counts as an explanation here
A localisation: a small set of neurons or heads whose indirect effect accounts for most of the total effect of an
input attribute on an output, plus a decomposition of the total effect into direct and indirect parts. Partial and
descriptive; it predicts how much of a behaviour change passes through a component, not what the component
computes.

## How they judged success
Total, natural direct and natural indirect effect (relative change in the bias ratio); saturation curves (fraction
of components needed to reach the effect of intervening on all); NIE-sum vs. NIE-all to test independence; a
linear fit of TE against NDE + NIE to test decomposability; random-init model as control; correlation of log TE
with external occupational gender statistics; robustness to alternative bias metrics.

## What they found
Larger GPT-2 models have larger total effects (Winobias: 0.25 small to 1.05 xl; random model 0.07), so the bias is
learned. Effects are sparse: 10 of 144 heads in GPT-2 small reproduce the effect of intervening on all heads, mostly
from layers 4-5; 4-8% of heads saturate the effect across sizes; about 4% of neurons saturate it, 57% of them in the
embedding and first layer. Heads act roughly additively (joint vs. summed gap 0.7-11.3%), but neurons interact
strongly (summed 4.0 vs. joint 112.3 in GPT-2 small). The indirect effect through heads exceeds the direct effect in
all models except distil. TE is close to NDE + NIE (slope 1.04, R^2 0.78). Log TE on the professions set correlates
0.35-0.45 with real-world gender statistics. Patterns transfer to Transformer-XL and XLNet; masked LMs give mixed
results that depend on scoring.

## Limits and open problems they name
Binary gender framing; "they" is confounded with plural; TE = NDE + NIE is not guaranteed for nonlinear models;
subset search is NP-hard and only approximated (top-K for neurons); tiny Winogender set; masked-LM results depend
on multi-token scoring choices; no explanation for differing neuron patterns outside GPT-2.

## What we take from it
A method and a vocabulary: the direct/indirect effect decomposition is the cleanest formal statement of what an
activation patch measures, and it gives us a way to say how much of a predicted behaviour change routes through
each part of a white-box model. A warning: neuron-level effects are strongly non-additive while head-level effects
are nearly additive, so a predictive model built from single-unit effects will mispredict joint interventions at
the neuron level. Control: always compare against a random-weights network.

## Tags
unit: neuron, head
form: description
method: patching, ablation
eval: patching
goal: understanding, science
