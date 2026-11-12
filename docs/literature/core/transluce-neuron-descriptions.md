# Scaling Automatic Neuron Description

- **Key:** transluce-neuron-descriptions
- **Authors / organisation:** Dami Choi, Vincent Huang, Kevin Meng, Daniel D. Johnson, Jacob Steinhardt, Sarah Schwettmann; Transluce
- **Date:** 2024-10-23
- **Link:** https://transluce.org/neuron-descriptions
- **Kind:** blog/research post
- **Read from:** full text (via WebFetch summary of the page; figures not viewed)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Bills et al. (2023) showed that a prompted LLM can describe neurons, but descriptions scored poorly and cost too much to
run on large models. Transluce wanted high-quality descriptions for every neuron of a modern model at low cost, as a
foundation for their observability tooling (searching, steering and debugging by neuron description). The question is
whether cheap, fine-tuned explainer and simulator models can match or beat human experts on the standard simulation
metric.

## What they studied
Llama-3.1-8B-Instruct: all 458,752 MLP neurons (14,336 per layer, 32 layers), with positive and negative activations
described separately. Exemplars came from LMSYS-Chat-1M and a 10B-token FineWeb subset, split into equal train,
validation and test sets. Unit: neurons.

## How they did it
For each neuron and polarity, collect top-activating exemplars. An explainer gets 10-20 exemplars with activating tokens
marked by delimiters (instead of Bills et al.'s token-activation lists) and one few-shot example from Bills et al.'s
puzzles, and samples many candidate descriptions (best-of-k, varying exemplar count and few-shot example). A simulator
predicts a 0-10 activation per token from a description; candidates are scored by correlation between simulated and true
activations on held-out exemplars (top 20 validation exemplars plus 5 random sequences, the random ones penalising overly
broad descriptions). The simulator is Llama-3.1-8B-Instruct fine-tuned in two stages to predict activations. The
explainer is distilled: GPT-4o-mini fine-tuned on best-of-50 descriptions for 2,000 neurons, then a Llama-3.1-8B
explainer distilled from best-of-25 descriptions for 8,000 neurons. Ablations cover prompt format, number of few-shot
examples, and chain-of-thought.

## What counts as an explanation here
A short natural-language description of what inputs make a neuron fire, per polarity, judged by how well a simulator can
reproduce activations from it. Partial by design: it covers what the neuron responds to, not how it computes.

## How they judged success
Simulation (correlation) score on a held-out test set; comparison with human expert descriptions on 100 neurons with a
paired t-test; comparison with Bills et al.'s reported score distribution; best-of-k scaling curves (power-law fits
with extrapolation); validation-versus-test consistency; dollar cost per neuron.

## What they found
On 100 test neurons, automated descriptions averaged 0.61 versus 0.55 for human experts (p = 4e-9), winning on 75; with a
non-fine-tuned prompted Llama-3.1-70B simulator, 0.38 versus 0.34 (p = 0.02). Score distributions peak near or above 0.5,
against Bills et al.'s mostly near 0 (setups differ). Best-of-k score follows a power law in k, and distilled explainers
have higher asymptotes; matching distilled GPT-4o-mini at 50 samples needs about 150 samples from the base model.
Highlighting format beat token-activation lists; extra few-shot examples and chain-of-thought hurt (less diversity).
Scores dip from layer 1 to 11 then rise, with bimodal distributions in some layers. Validation and test scores differ by
0.04 on average. Total cost was about $0.046 per neuron. Descriptions are released for every neuron.

## Limits and open problems they name
A fine-tuned simulator may learn cues that score well but are not human-interpretable; only top exemplars are described,
not the full activation range; best-of-k selection may overfit validation; BPE highlighting can be nonsensical; the
method says what a neuron responds to, not how it computes.

## What we take from it
Shows the simulation score can be pushed up mainly by search (best-of-k) and distillation, which is a warning: a high
simulation score from a trained simulator is partly an artefact of the scorer. If we report simulation scores, use a
fixed, untrained or human-aligned simulator and separate validation from test. Useful engineering details (highlight
format, separate polarities, random sequences in scoring) and a released neuron-description database for
Llama-3.1-8B that could serve as a comparison target for weight-derived descriptions.

## Tags
unit: neuron
form: description
method: agent | other
eval: prediction/simulation | human-rating
goal: understanding | control/editing | debugging
