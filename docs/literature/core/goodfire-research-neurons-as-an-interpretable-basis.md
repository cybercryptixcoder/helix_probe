# Neurons as an Interpretable Basis

- **Key:** goodfire-research-neurons-as-an-interpretable-basis
- **Authors / organisation:** Curt Tigges, Matthew Kowal, Thomas McGrath, Owen Lewis, Nick Cammarata; Goodfire
- **Date:** 2026-11-10
- **Link:** https://www.goodfire.com/research/neurons-as-an-interpretable-basis
- **Kind:** blog/research post
- **Read from:** abstract and sections (first ~200k of ~420k characters: method, main results, evaluation definitions and discussion; later appendices not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The field largely gave up on neurons as units because they look polysemantic, and moved to learned overcomplete dictionaries (SAEs, transcoders). The authors re-test that premise in a modern model: are MLP neurons sparse, concisely describable, and predictable units of computation? If yes, one can interpret the network in its own native basis, read connections between neurons directly, and avoid the reconstruction error and instability of learned dictionaries. It is the first post in a series, paired with a companion post arguing networks are already "clean".

## What they studied
Qwen3.6-35B-A3B, a SwiGLU mixture-of-experts model: 40 layers, 256 experts per layer of 512 neurons, 8 routed experts plus one shared expert per token, about 5 million neurons. About 10B tokens of mixed text (pretraining, reasoning, chat, math); per neuron, 1,000 examples from each of 14 activation-percentile bands, plus 30,000 extra strong examples for a stratified subset of 2,734 neurons; an 8.4M-token web-text set for loss/KL; standard benchmarks. Unit: individual neurons, split into "poles" (positive and negative firing) and then into input-defined subcircuits and modes.

## How they did it
1. Sparsity: mean-ablate middle activation bands, keep only the top-K neurons per expert or per layer (router-weighted; top-320 of 4,096 routed neurons, so 92.2% ablated), and measure web-text loss, KL to the original, and benchmarks, against random-64 and bottom-448 controls.
2. Lightly fine-tune the sparsified model (about 91M SFT and 9M RL tokens) to recover reasoning.
3. Study "Q3" activations, where both gate and up pre-activations are negative, by ablating or patching them back in.
4. Per firing, decompose the gate and up inputs into contributions from upstream neuron writes (read from weights and activations), and propagate the neuron's output to later layers to estimate downstream readers to first order.
5. Cluster each pole's firings by TF-IDF-weighted input profiles (Leiden communities on a 15-nearest-neighbour graph), assign held-out firings to the nearest centroid, merge clusters that share at least 30% of top-50 inputs and readers.
6. Send each subcircuit's inputs and readers to Claude Opus 5.5 for circuit, in-context and token-level descriptions; group subcircuits into modes.
7. Evaluate descriptions by detection, mode classification, input synthesis and simulation.

## What counts as an explanation here
Per neuron: a small set of modes, each defined by which upstream neurons drive it and which downstream neurons read it, plus a natural-language description. Together this is a neuron-level circuit description in the model's own basis. It is meant to be predictive: descriptions are scored by how well they let a reader predict activations and generate activating inputs, and the neuron graph is literally the model's computation.

## How they judged success
- Loss, KL and benchmark deltas under neuron-sparsification, versus random and bottom-K controls.
- Detection: an LLM judge, given a pole's descriptions, picks which of two snippets fires it (one above threshold, one below the pole's 90th percentile); chance 0.50; random-text and same-expert distractors.
- Mode classification: macro-F1 assigning held-out firings to modes from inputs, from downstream readers (the independent test), or from text descriptions alone (chance 0.29).
- Input synthesis: agents write text from descriptions only; success if activation exceeds the maximum seen in the 10B-token corpus.
- Simulation: a reader model predicts a 0-9 activation level per token from descriptions; scored as the fraction of ablation damage restored when simulated activations are patched in, relative to a perfect reader.

## What they found
- Keeping only the top-320 routed neurons per layer (92.2% ablated) raised web-text loss only from 1.886 to 1.940 (KL 0.140), versus 4.214 for random-64 and 4.587 for bottom-448. Classic benchmarks barely moved (ARC-Easy +0.2, MMLU -0.4) but reasoning dropped (MMLU-Pro -8.3, GPQA-Diamond -11.1), restored by brief fine-tuning.
- Q3 activations are about a third of all activations and rarely among the most causal, yet ablating them on 24 GSM8K problems cut average reasoning length from about 1,550 to 176 tokens.
- Median 19 subcircuits per pole (range 1-51), with low overlap (5.2% inputs, 6.5% readers); for most neurons one mode carries at least 90% of causal effect.
- Detection accuracy 0.914 overall (0.858 at p97-99 up to 0.955 at p99.99+); 0.885 with same-expert distractors, 0.946 with random text.
- Mode classification macro-F1: 0.968 from inputs, 0.853 from readers, 0.707 from text.
- Synthesis beat the corpus maximum for 120 of 128 poles (94%); median 1.06x the maximum.
- Simulation recovered 73% of the damage a perfect reader would restore across 486 poles; text explains about 14% of firing-size variance versus 59% for gate inputs.
- Versus random directions, 8 neurons matched what 128-256 random directions recovered.

## Limits and open problems they name
Weak (mid-percentile) activations are not explained and may matter. The Q3 mechanism is not worked out. Sparsified models loop and over-check when reasoning without fine-tuning. Descriptions are tested mainly on each neuron's primary mode; multi-mode disambiguation is open. Labels and scores depend on one LLM judge and prompt setup. One model family. No direct SAE or transcoder comparison in the part read.

## What we take from it
Strong support for building a weights-level white-box model in the native neuron basis of an MoE/SwiGLU model, using upstream-write decomposition and first-order downstream propagation (both readable from weights plus activations) to define each neuron's role. Reusable evaluation suite: sparsification loss/KL with random and bottom-K controls; detection, mode classification from inputs versus readers, input synthesis, and simulation-as-damage-restored. Warning: low-magnitude and sign-unusual activations (Q3) can carry behaviourally crucial function (here reasoning length) while looking unimportant by magnitude, so a predictive model that drops them will fail on long-horizon behaviour.

## Tags
unit: neuron, circuit
form: description, graph
method: ablation, attribution, weight-analysis, agent, other (clustering)
eval: ablation, prediction/simulation, downstream-task, faithfulness
goal: understanding, science
