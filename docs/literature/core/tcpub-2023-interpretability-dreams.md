# Interpretability Dreams

- **Key:** tcpub-2023-interpretability-dreams
- **Authors / organisation:** Chris Olah; Anthropic (Transformer Circuits Thread)
- **Date:** 2023-05-24
- **Link:** https://transformer-circuits.pub/2023/interpretability-dreams/index.html
- **Kind:** essay
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
An informal, explicitly speculative note on the long-term aspirations of mechanistic interpretability: what the program would ultimately deliver if superposition were handled. Olah wants to explain why a bottom-up approach (features, parameters, circuits) is worth it compared with top-down probing, and to sketch what larger-scale understanding could look like. The safety motivation is to eventually make worst-case, out-of-distribution guarantees about models, which ordinary behavioural ML evaluation cannot provide. He also argues for curiosity- and aesthetics-driven research in a pre-paradigmatic field.

## What they studied
No new experiments. Draws on prior circuits work in vision models (Gabor filters, curve detectors, high-low frequency detectors, branch specialization, CLIP multimodal neurons) and transformers (induction and previous-token heads), plus Toy Models of Superposition and automated neuron explanation (Bills et al.). Units: features, circuits, parameters, motifs, feature families.

## How they did it
Argument by example and analogy. (1) Bottom-up vs top-down: a probe can find a "dog detector" in a layer that merely combines earlier snout and fur features, so top-down search can mislead about where computation happens. (2) Small circuits read from weights can be checked rigorously, making claims about them close to mathematical statements; this is likened to foundations of mathematics or assembly code, a base level against which higher claims can be checked. (3) Larger-scale structure: motifs, feature families parameterised by variables (orientation, hue, language), weight organisation such as branch specialization, and a biology analogy (veins vs organs). (4) Universality: the same features and circuits recur across models, which would make understanding transfer. (5) Micro-macro links: induction heads produce a visible bump in loss curves; speculation that loss-landscape structure and scaling laws could be explained by a dependency graph of circuits. (6) Automation and its trust problems.

## What counts as an explanation here
A mechanistic account built from features and the circuits (weighted connections) between them, verifiable against the parameters, ideally organised into higher-level motifs and families. The aspiration is a complete enough feature set to enumerate model behaviour; explicitly incomplete today.

## How they judged success
Not an empirical paper; no metrics. Implicit criteria: rigour of circuit claims checked against weights, universality across models, ability of micro-level theory to predict where macro-level regularities (loss curves, scaling laws) break, and ultimately worst-case guarantees (e.g. that a model never lies).

## What they found
Conceptual claims only: bottom-up circuit analysis is more trustworthy than top-down probes; universality is supported by repeated findings but may be partial; induction heads link microscopic mechanism to a macroscopic training signature; superposition breaks clean weight organisation in later layers; AI-automated interpretability may be necessary but risks correlated failures if AI audits AI, so human verification is preferred.

## Limits and open problems they name
Superposition is the main obstacle; universality may only partly hold; complete enumeration is highly speculative; automated interpretability raises trust concerns; the note itself may contain mistakes.

## What we take from it
- Framing: weights are the ground level against which claims can be checked, so a white-box model read from weights is the program's "assembly-code" layer; useful justification for our approach.
- Test idea: a micro-level model should predict macro-level phenomena (loss bumps, where simple regularities fail), a strong predictive check we could adopt.
- Warning: top-down probes can mislocate computation; our reconstruction should be validated against weights, not just probe hits.
- Universality suggests checking whether reconstructions transfer across seeds or related models.

## Tags
unit: feature | circuit | weights | whole-model
form: graph | dictionary | description
method: weight-analysis | decomposition | agent | other
eval: prediction/simulation
goal: understanding | safety/auditing | science
