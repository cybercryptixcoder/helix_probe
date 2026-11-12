# Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models

- **Key:** arxiv-2301.04213
- **Authors / organisation:** Peter Hase, Mohit Bansal, Been Kim, Asma Ghandeharioun; UNC Chapel Hill, Google Research
- **Date:** 2023-01
- **Link:** https://arxiv.org/abs/2301.04213
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
ROME and related work motivate editing a particular MLP layer by first using Causal Tracing to show that the fact is "stored" there. The authors test that inference directly: does knowing where Causal Tracing localizes a fact tell you which layer to edit to change it? If not, edit success cannot be taken as evidence for a localization claim, and localization cannot be trusted to guide interventions. The broader stake is whether interpretability's localization results actually predict what interventions will do.

## What they studied
GPT-J (6B, 28 layers) as the main model and GPT2-XL (48 layers) as a robustness check. A 652-fact subset of CounterFact that GPT-J already gets right (489 used for Fact Erasure), plus ZsRE for robustness. Units: MLP layers and hidden states at token positions.

## How they did it
For each fact they ran Causal Tracing: noise the subject tokens, restore the clean hidden state at one token and layer (a 5-layer MLP window by default), and record the fraction of the correct-answer probability recovered. Separately they edited the same fact at every layer with ROME (rank-one update to the MLP output projection), MEMIT (update spread over several layers) and constrained fine-tuning on one or five layers (FT-1, FT-5, L-infinity norm bound). They then fitted linear regressions predicting edit success from the edit layer alone, from the tracing effect alone, and from both, and asked how much the tracing effect adds. To rule out a mismatch between the tracing question and the editing question, they defined five editing objectives of increasing similarity to tracing: Error Injection (standard counterfactual edit), Tracing Reversal, Fact Erasure, Fact Amplification and Fact Forcing (raise the true answer under a noised subject, which mirrors tracing). Robustness checks varied metrics, window size, model, dataset and the localization method (representation zeroing).

## What counts as an explanation here
The object under test is a localization claim ("this fact lives in these MLP layers"), and the paper's criterion is predictive: a localization is informative only if it predicts the outcome of an intervention at that location. The paper itself offers no new explanation, only a test of whether one kind of explanation earns its keep.

## How they judged success
Rewrite score (target probability gain normalized to the maximum possible), paraphrase score, neighborhood score, their average, and an essence score (perplexity change on generated text about the subject). Main statistic: R-squared of regressions of rewrite score on layer, tracing effect, and both; plus Spearman/Pearson correlations between tracing effect and edit success, with significance tests.

## What they found
For ROME at layer 6, the correlation between tracing effect and rewrite score is slightly negative (about -0.13). Edit layer alone explains rewrite score with R-squared 0.947; adding tracing raises it to 0.948. Across all conditions, layer alone explains about 58.5% of the variance on average and tracing adds at most 3.2 points; the largest gain comes in Fact Forcing with constrained fine-tuning, still small though significant. Even for the roughly 10% of facts whose tracing effect is concentrated in a few layers, tracing adds 0.2%. ROME succeeds at most layers (over 96% rewrite score at most layers, 99% at layer 6), including for facts traced to layers far from where it edits. The pattern holds across all robustness checks. Their reading: tracing tells you where information flows in the forward pass, which is a different question from where a weight change can override the output; many layers may be able to carry a fact.

## Limits and open problems they name
Only short English factual prompts (CounterFact, ZsRE); two mid-size autoregressive models; only Causal Tracing and representation zeroing as localization and ROME/MEMIT/fine-tuning as editing. The hypothesis that facts are redundantly stored across layers is left untested.

## What we take from it
A central warning and a test design. Warning: activation-based localization (patching) and weight-level intervention answer different questions; a white-box model built from probing results may not predict what weight edits do, so our model must be checked against interventions directly, not against localization maps. Method: regress intervention outcome on candidate explanatory variables and report the incremental R-squared a mechanistic variable adds over a trivial baseline (here, layer index). This "does the explanation add predictive power beyond a naive covariate" check is exactly the kind of evaluation our predictive model should pass.

## Tags
unit: layer | weights
form: description
method: patching | other
eval: prediction/simulation | patching | faithfulness
goal: evaluation-of-methods | control/editing
