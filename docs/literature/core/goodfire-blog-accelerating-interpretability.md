# Accelerating Interpretability: A Human Genome Project for AI

- **Key:** goodfire-blog-accelerating-interpretability
- **Authors / organisation:** Thomas McGrath, Mathilde Papillon; Goodfire
- **Date:** 2026-10-26
- **Link:** https://www.goodfire.com/blog/accelerating-interpretability
- **Kind:** survey/agenda
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
An agenda essay calling for a large, cross-industry effort to fully reverse-engineer a language model, modelled on the
Human Genome Project, with Goodfire committing $10M to start. The motivation is that interpretability has a few
hundred frontier researchers, roughly two orders of magnitude fewer than neuroscience, so progress is limited by
experimental throughput. Since model experiments have few physical limits, throughput could scale with compute if
capable agents run and verify experiments. Long-term success means being able to give mechanistic answers to
arbitrary questions about how a frontier model works.

## What they studied
No experiments. The proposal targets a large language model, eventually frontier scale.

## How they did it
They propose a three-part harness. First, a rigorous experimental workflow: a language for stating and checking
hypotheses, with causal abstraction as the starting point (they ask what the MI analogue of the Lean proof assistant
would be). Second, an information architecture so that results from very large agent swarms accumulate rather than
contradict. Third, more capable agents adapted into automated interpretability researchers. The work is framed as a
loop of explanation, experiment and revision, illustrated with the linear representation hypothesis (strong version
false, linear directions often meaningful) and Goodfire's work on manifolds and block-sparse featurizers.

## What counts as an explanation here
Structured causal claims backed by runnable experiment code, organised in a living encyclopedia by research question
rather than by model component. Aimed at completeness (full reverse engineering), with explanations that can be
mechanically checked.

## How they judged success
No concrete metrics. Near-term target is "scaling laws for interpretability," understanding growing predictably with
compute. They note there is no single interpretability number to optimize.

## What they found
Not an empirical piece. Main claims: throughput, not physical limits, is the bottleneck; verification infrastructure
is what lets agent-driven work compound.

## Limits and open problems they name
Short calendar time; agents misrepresenting results and failing to reconcile conflicting data; no single metric; human
intuition still needed to assemble theories; unclear when reverse engineering is complete; how findings transfer
across models and survive retraining.

## What we take from it
A framing: express our white-box model's claims as checkable causal statements with attached experiment code, so
they can be verified automatically (causal abstraction as the claim language). A design cue: organise findings by
question answered, not by component. A warning on agent-generated results: need verification and conflict handling.
Their missing "single metric" is a gap our predictive-accuracy measure could address.

## Tags
unit: whole-model
form: causal-abstraction
method: agent
eval: (none)
goal: understanding | science
