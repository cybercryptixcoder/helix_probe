# The Hydra Effect: Emergent Self-repair in Language Model Computations

- **Key:** arxiv-2307.15771
- **Authors / organisation:** Thomas McGrath, Matthew Rahtz, János Kramár, Vladimir Mikulik, Shane Legg; Google DeepMind
- **Date:** 2023-07
- **Link:** https://arxiv.org/abs/2307.15771
- **Kind:** paper
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Ablation is the standard way to decide which components matter, and it assumes that removing a part reveals its contribution. The authors asked whether that holds in a large language model, by comparing two measures of a layer's importance on factual recall. They found that networks compensate for removed layers, and set out to characterise this self-repair because it directly undermines how interpretability attributes function to components.

## What they studied
A roughly 7B-parameter, 32-layer Chinchilla-family decoder transformer trained without dropout, on factual-recall prompts from Counterfact (subject plus relation, 1,209 prompts in the main analysis). Units: whole attention layers and whole MLP layers (not heads or neurons).

## How they did it
For each layer they computed two importances for the model's top token at the final position. Direct effect: project the layer's output through the final RMSNorm (scale frozen at its clean value) and unembedding, giving its linear contribution to the centred logit (a logit-lens measure). Total effect: replace the layer's output by resample ablation (activations from 15 other prompts, effects averaged) and measure the change in the centred logit. Zero, mean and noise ablation were compared in an appendix. They then compared the two measures across layers, and after each ablation recorded how every downstream layer's direct effect changed. The summed downstream change is the compensatory effect; they regressed it against the lost direct effect. They also identified late "erasure" MLPs that push down the top token, and wrote a small toy model distinguishing erasure (clamping to zero) from self-repair (restoring the original output).

## What counts as an explanation here
Not a mechanism of the task but a characterisation of a property of the network: that downstream layers react to upstream changes in a way that restores output, plus a decomposition of where that compensation comes from (later attention layers early on, erasure MLPs late). The point is about what ablation-based explanations can and cannot show.

## How they judged success
Agreement (correlation) between direct-effect and total-effect rankings; slope and variance explained when regressing downstream compensation against the ablated layer's direct effect; share of compensation from attention versus MLP layers by depth. Ablation types were compared as controls.

## What they found
Direct and total importance are poorly correlated for most layers, and direct effect often exceeds total effect, which should not happen if ablation simply removed a contribution. Ablating an attention layer makes one or a few later attention layers increase their contribution to the correct token (the Hydra effect), e.g. layer 20 compensating for layer 18. Compensation is partial: regression slopes are below one from layer 13 on, and middle layers recover roughly 70% of the lost logit. At layer 23, compensation explains 92% of the variance in downstream direct-effect changes. Late MLPs act as erasers whose suppression shrinks when the upstream signal is removed, and by layer 23 nearly all of the response comes from them. This happens even though the model was trained without dropout.

## Limits and open problems they name
Analysis only at whole-layer level; one model and one dataset; resample ablation is noisy; the effect is measured only on the top token at the final position; unclear whether compensating layers replace lost features or only the logit contribution; the explanation for why self-repair arises (implicit dropout-like pressure, or superposition) is a conjecture.

## What we take from it
(1) A central warning: a white-box model that predicts behaviour under intervention must model the network's adaptive responses, not only each component's isolated contribution; summing direct effects will mispredict ablations. (2) This gives us a hard and useful test: predict total effects of ablations (including compensation) from our model, compared against direct-effect baselines. (3) Methodological controls: report both direct and total effect, prefer resample ablation over zero ablation for networks trained without dropout, and freeze normalisation scales when computing linear attributions. (4) Erasure MLPs mean logit-lens readings of intermediate layers can be misleading.

## Tags
unit: layer
form: description
method: ablation, attribution, other
eval: ablation, faithfulness
goal: evaluation-of-methods, science
