# Mechanistic?

- **Key:** arxiv-2410.09087
- **Authors / organisation:** Naomi Saphra (Kempner Institute, Harvard), Sarah Wiegreffe (Ai2 / University of Washington)
- **Date:** 2024-10
- **Link:** https://arxiv.org/abs/2410.09087
- **Kind:** essay
- **Read from:** full text (main body; tail of the HTML, mostly references, not read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors noticed that "mechanistic interpretability" is used in several incompatible ways, which muddies what a
paper is actually claiming. They set out to separate those meanings, trace how the term drifted, and explain the
social split behind it between NLP interpretability and the newer, safety-motivated MI community. The larger aim is
to get both communities talking and to make claims about "mechanism" more precise.

## What they studied
No models. The object of study is the research literature and community: definitions in papers, workshops and
tutorials, the history of NLP interpretability (ACL, BlackboxNLP, from about 2016) and of MI (Circuits thread, 2020,
then Transformer Circuits), plus public posts by researchers.

## How they did it
A qualitative historical and conceptual analysis. They collect definitions, trace the origin of the term (coined by
Chris Olah to distinguish circuit analysis from saliency maps), compare the methods and debates of the two
communities, and sort work by authors' networks and entry routes rather than self-labels. They then propose a
four-way taxonomy and argue which sense is technically meaningful.

## What counts as an explanation here
In the narrow technical sense they endorse, a mechanistic explanation is a causal account of how intermediate
representations produce the output; a stricter version demands a complete causal path from input to output. Causal
abstraction is cited as the way to simplify a network while staying faithful. Mere correlational study of internals
(probing, activations, weights) counts only under the broad technical sense.

## How they judged success
Not applicable; no experiments. The argument is judged by historical evidence and conceptual clarity.

## What they found
Four senses: narrow technical (causal mechanism claims), broad technical (any study of internals), narrow cultural
(work from the MI community), broad cultural (any interpretability, especially of LMs). Causality is the real
technical dividing line, yet much current MI work makes no causal claims. MI often rediscovers NLP-interpretability
results and replays old debates (correlation vs causation, polysemanticity, probe baselines). The broad cultural
sense has taken over as funding and interest grew.

## Limits and open problems they name
Whether end-to-end causal explanation becomes the standard; causal validation of SAEs, which rest on linearity and
sparsity assumptions; nonlinear and polysemantic feature combinations; MI's weak engagement with NLP venues and
prior literature; whether safety-driven funding persists.

## What we take from it
A framing: our claim should be "mechanistic" in the narrow technical sense, meaning causal and tested by
intervention, and we should say so explicitly. A warning: cite and use the older NLP-interpretability baselines
(probe controls, correlational-vs-causal distinctions) rather than reinventing them. Useful for writing the
positioning paragraph of our paper.

## Tags
unit: whole-model
form: causal-abstraction
method: other
eval: (none)
goal: understanding | evaluation-of-methods
