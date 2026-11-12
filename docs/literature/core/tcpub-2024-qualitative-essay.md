# Reflections on Qualitative Research

- **Key:** tcpub-2024-qualitative-essay
- **Authors / organisation:** Chris Olah, Adam Jermyn; Anthropic
- **Date:** 2024-03
- **Link:** https://transformer-circuits.pub/2024/qualitative-essay/index.html
- **Kind:** essay
- **Read from:** full text (via a page-summarising fetch)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors argue that interpretability is pre-paradigmatic, so researchers trained in mature ML fields may wrongly
treat qualitative findings as preliminary or unscientific. They want qualitative observation recognised as
first-class evidence and as the check that keeps quantitative metrics honest. The goal is a sounder research culture
for discovering what is inside networks, not an argument against quantitative work.

## What they studied
No new experiments. Examples from the history of science (cells under the microscope, spectral lines, stellar
spectra, superconductivity) and from interpretability (DeepDream, curve-detector weights in InceptionV1, saliency
maps, their own tanh-regularised dictionary learning, scaling-law plots).

## How they did it
Argument by example and analogy. They use Anscombe's Quartet to show identical summary statistics hiding different
structure, recount a case where their dictionary-learning summary statistics looked good until inspection showed
otherwise, and contrast fields with constrained hypothesis spaces with young fields that must first find which
hypotheses matter. They discuss how standard plot formats bias toward scalar summaries and argue for custom,
interactive interfaces.

## What counts as an explanation here
Meta-level: understanding comes from observing rich structure directly (features, weights, examples) and only later
condensing it into metrics. Their key evidential notion is the "signal of structure": high-dimensional structure in
observations too intricate to be a measurement artefact, treated as an informal counterpart to significance.

## How they judged success
Not applicable (essay). They give heuristics: good signs are a clear signal of structure and a principled reason for
looking; warning signs are unprincipled looking, unremarkable structure with cherry-picking, and plausible alternative
sources of the structure (e.g. saliency maps reflecting the input image).

## What they found
Rigorous measurement of a metric does not show the metric tracks what it is meant to; new metrics should be trusted
only after qualitative inspection confirms them. Using standard formats is not the same as rigour.

## Limits and open problems they name
Qualitative work is easy to get wrong; signal of structure is one route to truth, not the only one, and can be false
(saliency maps). The qualitative/quantitative boundary is blurry. No formal method is offered, only judgement
heuristics.

## What we take from it
A methodological guard for our evaluation: any score we use for a white-box model (faithfulness, prediction accuracy)
should be paired with qualitative inspection of what it rewards, and we should invest in readable interfaces for
weights and circuits. Gives us vocabulary ("signal of structure") recognised in the field for defending qualitative
evidence, while warning that prediction metrics still need validation.

## Tags
unit: whole-model
form: description
method: other
eval: human-rating
goal: evaluation-of-methods
