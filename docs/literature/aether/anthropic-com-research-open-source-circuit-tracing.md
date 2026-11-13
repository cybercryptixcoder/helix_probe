# Open-Sourcing Circuit-Tracing Tools

- **Key:** anthropic-com-research-open-source-circuit-tracing
- **Authors / organisation:** Anthropic (release post). Library built by Anthropic Fellows Michael Hanna and Mateusz Piotrowski, mentored by Emmanuel Ameisen and Jack Lindsey; the Neuronpedia frontend by Decode Research (Johnny Lin, Curt Tigges). Gemma graphs use GemmaScope transcoders.
- **Date:** 2025-05
- **Link:** https://www.anthropic.com/research/open-source-circuit-tracing
- **Kind:** tool (release announcement / blog post)
- **Read from:** full text of the post (~2.7k characters — the whole page); the library repository, the demo notebook and the Neuronpedia frontend were **not** read
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Anthropic had just published a method for tracing a model's internal computation as an *attribution graph* — a graph that partially reveals the steps a model took to reach one particular output. The method was demonstrated on their own models, which meant almost nobody outside the lab could run it. This post announces the code, and a hosted frontend, so that external researchers can generate, inspect and modify the same kind of graphs on open-weights models. The stated motivation is the field-wide gap they keep repeating elsewhere: understanding of internals lags far behind capability growth, so widening the set of people who can trace circuits is treated as a way of buying understanding faster. Nobody is quoted on a safety claim; the ambition is breadth of adoption, plus extensions other people build on top.

## What they studied
No model was studied by the post itself. The tooling is announced as working on open-weights models, with the worked examples named as **Gemma-2-2b** and **Llama-3.2-1b**; the published Gemma graphs are built on transcoders trained within the GemmaScope project. The unit of analysis inherited from the underlying method is the *feature* (dictionary/transcoder unit) plus the cross-layer edges between them — i.e. a computation graph over features at token positions, not neurons and not weights.

## How they did it
The post is a release, so "how" is a description of what a user can now do rather than an experimental protocol. Three capabilities are advertised: (1) generate attribution graphs for your own prompts on supported open-weights models; (2) visualise, annotate and share graphs in the Neuronpedia browser interface; (3) test hypotheses by changing feature values in the graph and observing how the output moves. Two routes exist for using it — a hosted interface for quick graphs, and the code repository for anything more involved. The authors say they have already used it to look at multi-step reasoning and at multilingual representations, and they explicitly invite the community to hunt for further circuits, providing extra unanalysed example graphs as starting points. They also ask for extensions that improve the tools themselves, which implies the interface is treated as a platform rather than a fixed product.

## What counts as an explanation here
The artefact is an **attribution graph**: a sparse, layered graph of feature nodes and the edges along which one feature's write is attributed to influence a downstream feature or the output. The parent method's own framing — that the graph is an approximation of the model's computation, faithful *enough* to be useful rather than exact — is not restated here, but is load-bearing for anyone using the tool. It is partial by construction (it explains one output on one prompt) and predictive in a weak sense: an edge is a claim about what would happen to the output if that upstream feature were suppressed or amplified, which is exactly what capability (3) lets a user check by hand.

## How they judged success
No metric, baseline, ablation or benchmark appears anywhere in the post. Success is stated in terms of what becomes possible for others — tracing on open models, interactive annotation, hand-edited feature values — and in terms of adoption of the released tools. For a release announcement that is an honest form of evidence (the code either runs or does not), but nothing here is a measurement of whether the graphs are correct.

## What they found
Substantive content is limited to the release itself: an open-source library for generating attribution graphs on open-weights models; a Neuronpedia-hosted frontend for exploring them; the ability to edit feature values in the graph and see the effect on the output; worked examples on Gemma-2-2b and Llama-3.2-1b covering multi-step reasoning and multilingual representations; and a set of unanalysed graphs published as prompts for community work. There are no accuracy figures, no comparison against manual circuit analysis, and no reconstruction or replacement-model scores — and the post makes no attempt to provide any.

## Limits and open problems they name
Named: the community is asked to find additional circuits and to improve the tools, which is an admission that coverage is thin and the interface is unfinished. The post frames the graphs as revealing the steps of a computation only *partially*, so incompleteness is acknowledged at the level of a parenthetical rather than analysed. Everything else a sceptic would want — whether an attribution graph survives a faithfulness test, whether hand-edited feature values produce the output change the graph predicts, and how the method's cost scales with model size — is absent, and the natural inference is that it is discussed in the method paper rather than in the release.

## What we take from it
Two things, and one warning. First, a **framing** worth borrowing: a "graph you can edit" is a very different deliverable from a "graph you can look at", because editing turns the explanation into a testable prediction and lets the reader falsify it on the spot — that is the shape our own white-box model should take if it is to be judged by prediction-under-intervention rather than by plausibility. Second, a **practical route**: transcoder-based feature graphs already run on 1B–2B open models with public code, which is the cheapest available baseline for any circuit claim we make, and using a model whose internals others can re-trace also means our results are checkable. The warning is about what the post does not contain: adoption is not validation, and a released tool with curated impressive examples is evidence that the pipeline runs, not that the graphs are faithful. Cite the method paper (core already has it) for any claim about correctness, and treat this entry as a citation for availability and for the edit-and-observe workflow.

## Tags
unit: feature
form: graph
method: attribution | transcoder
eval: benchmark
goal: understanding | debugging
