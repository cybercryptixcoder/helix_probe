# Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet

- **Key:** tcpub-2024-scaling-monosemanticity
- **Authors / organisation:** Adly Templeton, Tom Conerly, Jonathan Marcus, et al.; Anthropic
- **Date:** 2024-05
- **Link:** https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html
- **Kind:** paper
- **Read from:** full text (via page fetch in two parts; the scout-reported arXiv version was not checked)
- **Relevance to us:** 3 (central)

## What they wanted, and why
SAEs had only been shown to work on a one-layer toy transformer. The authors test whether the method scales to a
production model and whether the resulting features are abstract, causally meaningful, and relevant to safety
(deception, bias, dangerous content). A positive answer would make dictionary learning a plausible foundation for
auditing frontier models.

## What they studied
Claude 3 Sonnet (production, finetuned; size not reported), residual stream at the middle layer. Three SAEs with
about 1M, 4M and 34M features. Unit: SAE features (directions in the residual stream).

## How they did it
They train ReLU SAEs with reconstruction loss plus an L1 penalty weighted by decoder norms (coefficient 5), on text
only, after normalising activations. They fit scaling laws for SAE training loss against compute, splitting compute
between feature count and steps, and extrapolate learning rates and run length for the largest SAE. They then
evaluate features by: showcase examples; specificity, with Claude 3 Opus rating activating texts on a 0-3 rubric;
sensitivity spot checks; influence, by clamping a feature to a multiple of its maximum activation during the forward
pass and observing generations; comparison with neurons (best-correlated neuron per feature, automated
interpretability); feature neighbourhoods in decoder space and splitting across SAE sizes; coverage tests (e.g. how
many London boroughs get features) and dependence on concept frequency. To explain specific outputs they use
gradient attribution and zero-ablation of features and compare the two. They catalogue safety-relevant features and
test steering against few-shot contrastive steering vectors.

## What counts as an explanation here
A large feature dictionary with descriptions, neighbourhoods, and causal steering effects; for single prompts, a
list of features whose attribution/ablation drives the output. Explicitly partial and not yet circuits.

## How they judged success
Fraction of variance explained, average L0 (active features per token), dead-feature fraction, SAE loss scaling
laws, LLM-judged specificity, neuron baseline, steering (clamp) effects, attribution-versus-ablation correlation,
coverage of known concept sets, comparison with linear probe/steering-vector baselines.

## What they found
Fewer than 300 features active per token, at least 65% of variance explained; dead features about 2%, 35% and 65%
for the 1M, 4M and 34M SAEs. Loss falls roughly as a power law in compute. Features are multilingual and even
multimodal despite text-only training. For 82% of sampled features the best-correlated neuron had correlation 0.3
or less. Clamping causally changes behaviour (Golden Gate Bridge at 10x makes the model identify as the bridge;
useful range roughly -10 to 10x max; around 100x yields nonsense). Attribution correlated with ablation at about
0.8, while raw activation correlated with ablation only about 0.12. The 34M SAE covered about 60% of London boroughs,
and whether a concept gets a feature depends on its frequency. Safety-relevant features (unsafe code, backdoors,
sycophancy, deception, secrecy, bioweapons, scams) exist and steer behaviour. Few-shot steering vectors matched
features in 2 of 7 cases and were weaker in 5.

## Limitations and open problems they name
Far from all features, likely orders of magnitude short even in one layer; full coverage could cost more compute
than training the model; cross-layer superposition; L1 shrinkage; high dead-feature rates; text-only SAE data; the
training objective is only a proxy for interpretability; attention and weight superposition block circuit analysis;
no demonstration that features are practically useful for safety.

## What we take from it
Evidence that activation-side dictionaries scale but are incomplete and expensive, which motivates looking for
weight-side structure. Useful measures: attribution-vs-ablation agreement, activation-vs-ablation as a warning that
activation alone poorly predicts causal importance, clamp-based steering as an intervention test, coverage against
an enumerable concept set, and SAE loss scaling laws. The note that features matter more than neurons and that
"weight superposition" may block circuits is directly relevant to reading weights.

## Tags
unit: feature, direction
form: dictionary, description, steering
method: SAE, attribution, ablation, steering
eval: ablation, human-rating, faithfulness, downstream-task
goal: understanding, safety/auditing, control/editing
