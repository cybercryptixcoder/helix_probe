# Neural Networks Are Already Clean

- **Key:** goodfire-research-already-clean
- **Authors / organisation:** Nick Cammarata (with contributions from Curt Tigges and Tarun Gogineni); Goodfire
- **Date:** 2026-10 (no date printed; a footnote refers to a revision of 2026-10-30)
- **Link:** https://www.goodfire.com/research/already-clean (redirects to https://already-clean.goodfire.com/)
- **Kind:** essay
- **Read from:** abstract and sections (roughly the first three quarters of a very long page, read in two parts; final part not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Cammarata argues that the field's founding worry, that neurons are hopelessly polysemantic because networks pack
unrelated features into superposition, was largely a misreading of the evidence. He proposes that most apparent
mixing is "recursive generalization": a neuron starts on a core concept and spreads into related territory. If that
is right, the network's own neurons and circuits are already a usable basis, and interpretability does not need a
decomposition step (SAEs, transcoders) before it can explain things. Remaining messiness is blamed on weak tools,
regularization and architecture choices, and crude explainer models. The essay is a working hypothesis, with a
companion technical paper promised.

## What they studied
Vision: InceptionV1 (e.g. neuron 4e:55, the classic "cat and car" neuron; the Zoom In car/dog circuit), DINOv2, and
three ConvNeXt models from 92k to 28.6M parameters. Language: Qwen3-32B, Qwen3.6-35B-A3B (MoE), Pythia-1B, and a
Kimi K3 slice. Unit of analysis: individual neurons (both positive and negative "poles"), their input/output
connections, and circuits/attribution paths.

## How they did it
For vision, he re-examined famous polysemantic neurons using top examples, negative poles, downstream readers and an
improved feature visualization with added transformation robustness, and tracked neurons across training epochs. He
ran bottleneck tests: shrinking InceptionV1 layer 3b from 480 to 10 channels (and a ConvNeXt final layer from 1,024 to
13) and retraining, to see whether squeezed units superpose or just become coarser; a TopK SAE was trained on the
squeezed layer and compared against the native neurons. For language models, agents wrote "neuron papers" for about
1,000 random neurons in two Qwen models using dataset examples. Explanations were tested adversarially: a second agent,
given only the explanation, writes an input meant to maximally fire the neuron (compared against the best example in a
10B-token corpus), and for 200 neurons an agent wrote five predicted firing examples and five near misses. Ablation
experiments removed small named neuron sets and compared with count- or magnitude-matched random removals. Agents
reviewed about 100,000 attribution graphs for anomalies.

## What counts as an explanation here
A short, falsifiable description of each native neuron's job (per pole), supported by steering effects, upstream and
downstream connections, negative-pole behaviour and targeted tests. Explanations are expected to predict new inputs
that fire or fail to fire the neuron, and "unclear" is an allowed label. Circuits are built from these neurons, not
from a learned dictionary. Partial, but aimed at near-complete coverage.

## How they judged success
Fraction of neurons judged to have one main job; blind-maximization test (agent-written input activation vs best
corpus activation); predicted positives vs near misses firing rates and win/tie/loss counts; accuracy under
weak-activation ablation; probability shifts under targeted vs random neuron removal; SAE reconstruction (variance
explained, spliced-in accuracy) and SAE-to-neuron match. He explicitly criticises simulation scores as rewarding
detail that does not matter for the label.

## What they found
InceptionV1 last-layer interpretability estimated at about 5% with 2017 tools, about 50% with better tools, about 70%
after retraining with modern regularization, and about 99% in a parameter-matched ConvNeXt. The 10-channel InceptionV1
bottleneck reached 58.35% top-1, with coarser rather than superposed units; a TopK SAE on it explained 82% of variance
but cut top-1 to 43.0% and matched the curve detectors poorly. In Qwen3-32B, a preliminary audit put about 90% of
neuron poles as single-job, about 7% as two related jobs, 2-4% unexplained (threshold-dependent). Blind-max inputs
beat the corpus best (e.g. 18.4 vs 15.0). Of 183 neurons, predicted examples fired strongly 76% of the time vs 11% for
near misses; explanations won 164, tied 15, lost 4. Removing eight neurons dropped P(Santa) to 0.059 vs 0.997 under
random removal. On a last layer, 88% of SAE activity was near-copies of single neurons.

## Limits and open problems they name
Author calls the hypothesis highly speculative. Percentages depend on thresholds and definitions of "one thing"; many
samples are small; several analyses are deferred to the companion paper. No trusted semantic test for weak activations
yet. Scaling to very large models is not solved; the Kimi K3 graph is a hand-picked slice. Alignment-relevant
mechanisms still need direct study. Attention heads were not well covered.

## What we take from it
A framing and a warning: before adopting a decomposition, test whether native units already suffice; decompositions
can fail to recover known features (the squeezed-layer SAE result). Two reusable evaluation protocols that test
prediction rather than description: blind maximization from the explanation alone, and predicted-positive vs
near-miss examples with win/loss counts. Matched random-removal controls for ablation. For weight reading, the essay
treats neuron inputs as weighted votes and uses connections, which supports building per-neuron descriptions from
weights plus a small amount of activation evidence. Treat the numbers as preliminary.

## Tags
unit: neuron | circuit
form: description | graph
method: agent | ablation | steering | attribution | SAE
eval: prediction/simulation | ablation | faithfulness | human-rating
goal: understanding | science | evaluation-of-methods
