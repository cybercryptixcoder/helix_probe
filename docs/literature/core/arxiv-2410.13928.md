# Automatically Interpreting Millions of Features in Large Language Models

- **Key:** arxiv-2410.13928
- **Authors / organisation:** Gonçalo Paulo, Alex Mallen, Caden Juang, Nora Belrose; EleutherAI, Northwestern University
- **Date:** 2024-10
- **Link:** https://arxiv.org/abs/2410.13928
- **Kind:** paper
- **Read from:** full text (HTML version, v3)
- **Relevance to us:** 3 (central)

## What they wanted, and why
SAEs produce millions of features, far too many to label by hand, and the prior standard for scoring labels
(OpenAI's simulation scoring) is expensive and looks only at strongly activating text. The authors wanted a cheap,
open pipeline that generates natural-language descriptions of features and scores them in several complementary
ways, including by the feature's effect on outputs, not only by what makes it fire. The broader aim is to make
automated interpretability a routine, measurable step and to compare SAEs and neurons on equal footing.

## What they studied
SAEs on Gemma 2 9B (Gemma Scope, 16K and 131K latents) and on Llama 3.1 8B (their own, 65K and 262K latents),
with top-k neurons as a baseline. Unit: individual SAE latents and neurons.

## How they did it
They collected feature activations over 10M tokens of RedPajama-v2. An explainer model (Llama 3.1 70B Instruct)
saw 40 activating 32-token examples, with activating tokens and strengths marked, sampled across the activation
distribution rather than only the top. Each description was then scored five ways: detection (scorer labels whole
contexts as activating or not), fuzzing (scorer judges whether highlighted tokens are the activating ones),
surprisal (does the description lower a base model's loss on activating contexts), embedding (retrieve activating
contexts with a small embedding model using the description as query) and a new intervention score (does the
description predict what text the model produces when the feature is turned up, normalised by KL of the
intervention). Simulation scoring was run as the reference. They measured agreement with human judgements, inter-
score correlations, cost, and effects of example sampling, explainer/scorer size, SAE width and layer.

## What counts as an explanation here
A short natural-language description per feature, treated as a hypothesis that should predict either the feature's
activations (input side) or its effect on the model's output (output side). Partial and per-feature.

## How they judged success
Detection and fuzzing (balanced accuracy/precision/recall), surprisal AUROC, embedding AUROC, intervention score,
and simulation correlation; Spearman correlation with human ratings; dollar cost per 100K features.

## What they found
Agreement with humans: fuzzing 0.69, simulation 0.60, detection 0.59, surprisal 0.34, embedding 0.32. Fuzzing
correlates 0.75 with simulation, but simulation and surprisal only 0.15, so scores measure different things. Per
100K features with a 70B scorer: fuzzing about $676, detection about $588, simulation about $3.6K (or $18.7K token
by token), embedding about $50. Descriptions built only from top activations are narrower and score worse than
those from stratified samples. Claude 3.5 Sonnet and Llama 70B explanations were similar, and human-written ones
scored about the same. Gemma 131K SAE fuzzing 0.76 vs 0.73 for 16K, vs 0.62 for top-32 neurons; Llama SAEs up to
0.81. Early layers score lower. Intervention scores correlate slightly negatively with fuzzing and are higher in
later layers: some features are explained by what they do, not what triggers them.

## Limitations and open problems they name
Short 32-token windows miss long-range features; scores ignore explanation length; non-activating example choice
needs work; similar features confuse scorers; results depend on scorer model and prompt.

## What we take from it
The input-side vs output-side split is central for us: a predictive white-box model needs both "when does this unit
fire" and "what does it do", and this paper shows the two are nearly uncorrelated. Intervention scoring is a
template for testing whether a weight-derived description predicts the effect of an intervention. Detection and
fuzzing are cheap, accepted baselines we can run with the open `delphi` code. Warning: descriptions from top
activations alone overstate specificity.

## Tags
unit: feature | neuron
form: description
method: SAE | agent | steering
eval: prediction/simulation | human-rating | benchmark
goal: evaluation-of-methods | understanding
