# Transcoders Find Interpretable LLM Feature Circuits

- **Key:** arxiv-2406.11944
- **Authors / organisation:** Jacob Dunefsky, Philippe Chlenski, Neel Nanda
- **Date:** 2024-06
- **Link:** https://arxiv.org/abs/2406.11944
- **Kind:** paper
- **Read from:** full text (main text and part of appendix)
- **Relevance to us:** 3 (central)

## What they wanted, and why
SAE-based circuit analysis struggles to pass through MLP sublayers: SAE features on either side of an MLP are connected by a dense nonlinear map, so their relationship depends on the input and is hard to separate into general structure. The authors wanted a replacement for the MLP that is itself sparse and interpretable, so that feature-to-feature connections through MLPs can be split into a part that depends on the input and a part fixed by the weights, enabling weight-based circuit analysis.

## What they studied
GPT-2 small, Pythia-410M and Pythia-1.4B. Unit: transcoder features (latents of a sparse MLP replacement) and the connections between them, including through attention OV circuits.

## How they did it
A transcoder is a wide one-hidden-layer ReLU MLP trained to map an MLP sublayer's input to its output, with a reconstruction loss plus an L1 sparsity penalty. Dictionaries were 32x model width (24,576 / 32,768 / 65,536 features), trained on 60M OpenWebText tokens. They compared transcoders with SAEs trained on MLP outputs on the sparsity-fidelity trade-off (mean L0 vs. increase in next-token cross-entropy when substituted, on 3.2M tokens) and in a blind interpretability rating of 50 features each from Pythia-410M layer 15. For circuits, the attribution from an earlier transcoder feature to a later one factors into the earlier feature's activation (input-dependent) times the dot product of its decoder vector with the later feature's encoder vector (input-invariant, read from weights). Through attention, attribution follows the OV circuit with attention patterns held fixed. A greedy recursive search keeps the top paths and merges them into a graph. "De-embeddings" (projecting a feature's encoder onto the token embedding matrix) show which tokens drive a feature independent of context. They ran blind case studies in which the analyst could not see prompt tokens, only input-invariant information, and reanalysed the GPT-2 greater-than circuit at MLP10.

## What counts as an explanation here
A feature circuit through a replacement model, where each edge weight is part data-dependent activation and part fixed weight-space product that can be read once for all inputs. Partial: transcoder error is not modelled and attention patterns are taken as given.

## How they judged success
Sparsity-fidelity curves against SAEs; blind human interpretability counts; success of blind case studies (whether the hypothesis derived from circuits matched top-activating examples); in the greater-than case, recovery of the task metric with a few transcoder features versus MLP neurons, and agreement with Hanna et al.'s earlier findings.

## What they found
Transcoders were equal to or better than SAEs on sparsity-fidelity in all models, with the gap seemingly widening with size (e.g. Pythia-410M layer 15: L0 44.04 and 3.35 nats vs. SAE L0 47.85 and 3.36 nats). Blind rating: 41 interpretable / 8 maybe / 1 not for transcoders, versus 38 / 8 / 4 for SAEs. Of the blind case studies, most succeeded (five successes, two mostly, two failures in the appendix table); e.g. one GPT-2 layer 8 feature was identified as firing on semicolons in parenthetical citations. In greater-than, a handful of MLP10 transcoder features recovered most of the performance and beat neurons at under 24 features, consistent with prior work.

## Limits and open problems they name
Transcoders are about as unfaithful (by cross-entropy) as SAEs; attention patterns are frozen rather than explained; circuit evidence comes from a few qualitative case studies and needs more systematic evaluation; hyperparameter sweeps were limited.

## What we take from it
The key idea for reading weights: once a nonlinear block is replaced by a sparse linear-in, linear-out dictionary, feature-to-feature connectivity is a weight product (decoder · encoder) valid for every input, so part of the model can be read without running it. This is the direct ancestor of cross-layer transcoders and attribution graphs. The blind case-study protocol (analyst sees only weight-derived information, then predicts behaviour) is a good template for testing whether a weight-read model predicts. Warning: the frozen attention patterns are the main non-weight-readable gap.

## Tags
unit: feature | circuit | weights
form: replacement-model | graph | dictionary
method: transcoder | attribution | weight-analysis
eval: faithfulness | human-rating | prediction/simulation
goal: understanding | science
