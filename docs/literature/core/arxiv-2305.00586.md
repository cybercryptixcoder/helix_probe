# How Does GPT-2 Compute Greater-Than?: Interpreting Mathematical Abilities in a Pre-trained Language Model

- **Key:** arxiv-2305.00586
- **Authors / organisation:** Michael Hanna, Ollie Liu, Alexandre Variengien; University of Amsterdam (ILLC), University of Southern California, Redwood Research (work done in Redwood's REMIX programme)
- **Date:** 2023-05
- **Link:** https://arxiv.org/abs/2305.00586
- **Kind:** paper
- **Read from:** full text (via arXiv HTML)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors wanted to know how a pretrained language model performs a simple piece of numerical reasoning: knowing which two-digit years are larger than a given start year. Beyond the specific behaviour, the question is whether such abilities are memorised lookups or general mechanisms, and whether a circuit found on one prompt template explains the same behaviour on others. It is a step toward complete, end-to-end circuit accounts of real behaviours in real (if small) models, with an explicit test of how far a circuit generalises.

## What they studied
GPT-2 small (12 layers, 144 attention heads, 12 MLPs). Data: a templated task, "The <noun> lasted from the year XXYY to the year XX", with 120 duration nouns from FrameNet, centuries 11 to 17 and start years 02 to 98 (filtered so all relevant years tokenise as two-digit tokens). A corrupted "01-dataset" replaces YY with 01. Units: attention heads, MLP layers, individual MLP neurons, and PCA directions of MLP inputs.

## How they did it
They first measured behaviour on 10,000 prompts with two metrics (below). They then ran path patching: for each component, its input along a single path is replaced with the activation from the 01-dataset, isolating that path's causal effect. They started with direct paths to the logits (490 datapoints, 5 per YY), found MLPs 8 to 11 and head a9.h1 important, then iterated upstream to find what feeds each important MLP, ending with a circuit of MLPs 8 to 11 plus a handful of mid-layer heads (a5.h1, a5.h5, a6.h9, a7.h10, a8.h8, a8.h11) that attend to the YY token. They evaluated the circuit by keeping only circuit paths clean, and the converse by corrupting only circuit paths. To understand the MLPs they used the logit lens on each MLP's output across all YY values, split direct versus indirect effects, examined individual neurons of MLP 10, ran PCA on MLP inputs and head outputs, and tested whether erasing linearly available YY information (LEACE) or the PCA directions breaks the behaviour. Finally, they ran the same circuit on new templates (different phrasing, prices, number sequences, and deliberately "wrong" contexts such as reversed time order or BC dates and less-than prompts).

## What counts as an explanation here
A circuit: a small subgraph of heads and MLPs plus a functional story (heads move YY to the final position; MLPs 9 and 10 upweight exactly the years above YY, building the comparison in a distributed way across many neurons). It is partial by design: neuron-level computation is described only qualitatively. The circuit makes testable predictions about which prompts it will fire on, including prompts where it fires wrongly.

## How they judged success
Two task metrics: probability difference (sum of probability on years greater than YY minus sum on years at or below YY, range -1 to 1) and cutoff sharpness (p(YY+1) minus p(YY-1)). Circuit faithfulness was reported as the fraction of the full model's probability difference recovered when only the circuit is clean; necessity by corrupting only the circuit. The logit lens was cross-checked against path-patched direct effects. Generalisation was scored as percentage of performance recovered by the original circuit on new templates.

## What they found
GPT-2 small does the task well: probability difference 81.7% and cutoff sharpness 6.0% on 10,000 prompts. The circuit alone gives 72.7% probability difference (89.5% of the model's), and corrupting just the circuit drives it to -36.6%. MLPs 9 and 10 show an upper-triangular logit-lens pattern (boosting exactly years above YY); MLP 11 boosts roughly the next 50 years; MLP 8 acts mostly indirectly (14% direct vs 39% indirect loss when patched). No single neuron in MLP 10 does greater-than; summing the top contributors approximates it, improving as more are added. MLP inputs are ordered by YY in PCA space, but ablating those components barely matters and LEACE erasure only lowers probability difference to 64.7%, so the representation story is incomplete. The circuit transfers to similar templates (98.8% on a started/ended variant, 88.9% on prices; a number-sequence prompt needed extra components to reach 90.3%), fails on some (descending sequences, "is smaller than"), and also fires on prompts where a smaller year is correct, showing it is a broad, context-insensitive mechanism rather than a true comparison.

## Limits and open problems they name
Small model and a single simple phenomenon; no study of larger models; no data-driven methods; the causal role of the ordered number representation is not established; memorisation versus generalisation is unresolved; generalisation tests are mostly qualitative and circuit similarity is not measured systematically.

## What we take from it
(1) A method: iterative path patching from logits upstream, with sufficiency and necessity checks, is a clean, field-standard recipe. (2) A measure: task-specific behaviour metrics (probability difference, cutoff sharpness) rather than generic loss. (3) A framing we should copy: test the explanation on prompts outside its discovery template, including prompts where the mechanism should NOT fire; a predictive white-box model must forecast these false activations. (4) A warning: finding a structured representation (PCA ordering) is not the same as showing it is used; interventions disagreed with the pretty picture. (5) MLP behaviour was explained only as distributed over many neurons, so weight reading at neuron level is the gap.

## Tags
unit: circuit, head, neuron
form: graph, description
method: patching, ablation, weight-analysis, decomposition
eval: patching, faithfulness, ablation, downstream-task
goal: understanding, science
