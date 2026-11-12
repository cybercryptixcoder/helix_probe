# Replicating Circuit Tracing for a Simple Known Mechanism

- **Key:** goodfire-research-replicating-circuit-tracing-for-a-simple-mechanism
- **Authors / organisation:** Jack Merullo, Connor Watts (co-first), Max Loeffler, Liv Gorton, Elana Simon, Tom McGrath, Owen Lewis; Goodfire
- **Date:** 2025-06-11
- **Link:** https://www.goodfire.com/research/replicating-circuit-tracing-for-a-simple-mechanism
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Cross-layer transcoders (CLTs) and attribution graphs (Ameisen et al., Lindsey et al.) promise to show how a model
processes information across layers and tokens. Before trusting them on unknown mechanisms, the authors test
whether they recover a mechanism that is already known. They use the greater-than circuit in GPT-2 Small,
previously reverse-engineered at the neuron level by Hanna et al. (2023). This is a method-validation step toward
trustworthy circuit discovery.

## What they studied
GPT-2 Small; the greater-than task (prompts like "The war lasted from the year 17YY to 17", where the model should
put probability on years after YY). Unit of analysis: CLT features (49,152 per layer, 589,824 across 12 layers) and
their attribution to output logits, compared with Hanna et al.'s MLP neurons.

## How they did it
Trained CLTs on 100M FineWeb tokens, expansion factor 64, ReLU activations (not JumpReLU). The chosen CLT had L0 of
79 and 59% token accuracy (described as in line with Ameisen et al.). Reimplemented attribution-graph construction
and pruning and ran it on a single prompt (year 1711). Took the top 16 features for each of the top 10 output
logits, then applied Hanna et al.'s logit-attribution method, summing each feature's decoder vectors across the
layers it writes to. For each selected feature, plotted a heatmap of its effect on each output year as the input
year varies over about 100 prompts, and inspected max-activating examples. Compared these heatmaps by eye with
Hanna et al.'s neuron plots.

## What counts as an explanation here
An attribution graph over sparse transcoder features, with each important feature characterised by an
input-year to output-year effect map. Partial: final-token features only, one prompt, no cross-position tracing.

## How they judged success
Qualitative match to a known ground-truth mechanism (Hanna et al.'s Figure 1 neurons): does the CLT surface
features that suppress years at or below YY and boost later years? No quantitative ground-truth score, and no
intervention experiments. CLT quality reported as L0 and token accuracy.

## What they found
Several features implement greater-than (promote later years, fire before larger numbers); some are very narrow
(one fires only for input years 6 to 14, another only for 11). Unexpected features also appear: an inverse
"small number" feature, a parity feature (ranked 6th of 146 for logit 20) that promotes even outputs for odd
inputs, one favouring years ending in 0 or 5, one favouring tokens ending in 2. Some column structure matches Hanna
et al., but CLT features depend less on the input and the overall picture is messier than the neuron-level
account. The CLT found relevant interpretable features without any intervention experiments.

## Limits and open problems they name
Heatmaps and max-activating examples disagree for some features, cause unknown (possibly because logit attribution
looks at features in isolation). Logit attribution is validated for standard transformers, not CLTs whose features
write to many layers. One prompt used for selection, so distractor features may be present. Only final-token
features; no supernode clustering; training details deferred.

## What we take from it
The validation pattern: test a decomposition method on a mechanism whose answer is already known before using it
on unknowns. The result is a caution for us: a replacement model can be faithful enough to surface the right
features yet reorganise the mechanism into many fragmented or extra features (parity, round-number), so "recovered"
must be defined quantitatively (we should add intervention and prediction checks, which this post lacks). The
greater-than task in GPT-2 Small is a ready ground-truth target for a weights-to-white-box pipeline.

## Tags
unit: feature | circuit
form: graph | replacement-model
method: transcoder | attribution
eval: faithfulness
goal: evaluation-of-methods
