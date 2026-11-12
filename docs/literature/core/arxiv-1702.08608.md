# Towards A Rigorous Science of Interpretable Machine Learning

- **Key:** arxiv-1702.08608
- **Authors / organisation:** Finale Doshi-Velez, Been Kim (equal contribution; affiliations not stated on the pages read — commonly Harvard and Google Brain, not verified here)
- **Date:** 2017-02 (v1 28 Feb 2017, v2 2 Mar 2017)
- **Link:** https://arxiv.org/abs/1702.08608
- **Kind:** survey/agenda (position paper)
- **Read from:** abstract and sections (HTML/PDF summaries of sections 1–4 and recommendations)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors argue that interpretable ML has no shared definition and no shared way to measure success, so claims of
"interpretability" cannot be compared across papers. They define interpretability as the ability to explain or
present a system's reasoning to a human in understandable terms, and argue it matters mainly when the problem
formulation is incomplete: when we cannot write down every requirement (safety, fairness, scientific understanding,
mismatched proxy objectives, trade-offs between objectives) and so need to inspect the reasoning instead. The larger
goal is a rigorous, evidence-based science of interpretability with a common evaluation taxonomy.

## What they studied
No models or data; this is a conceptual paper. The unit of analysis is the explanation and the evaluation protocol
used to judge it.

## How they did it
They first lay out when interpretability is and is not needed (the "incompleteness" argument), separating
incompleteness from mere uncertainty. They then propose a three-level taxonomy of evaluation, ordered by realism and
cost. Next they describe concrete human-subject tasks that can be used at the middle level. Finally they propose a
research programme: build a matrix of real tasks versus explanation methods and look for latent factors that explain
which methods suit which tasks, and they hypothesise what those factors are.

## What counts as an explanation here
Anything that lets a human understand the system's reasoning: decision trees, sparse models, prototypes, rules and
so on, decomposed into "cognitive chunks". Explanations may be global (the whole model) or local (one decision).
Crucially, one of their tests treats an explanation as good if it lets a human predict the model's output
(forward simulation) — i.e. explanations are judged partly by their predictive power about the model, not the world.

## How they judged success
They define the evaluation levels themselves:
- **Application-grounded:** real experts on the real task (e.g. doctors doing diagnosis with the explanation). Most
  realistic, most expensive.
- **Human-grounded:** lay people on simplified tasks that keep the essence of the target use. Named tasks: forward
  simulation (given input and explanation, predict the model's output — scored against the model, not the true
  label), counterfactual simulation (given input, explanation and output, say what change would produce a desired
  output), and binary forced choice (pick the better of two explanations).
- **Functionally-grounded:** no humans; a formal proxy such as sparsity or model-class membership (e.g. decision
  trees), appropriate only once that proxy has been validated by human studies, when methods are immature, or when
  human studies would be unethical.
Their central rule: the type of evaluation must match the type of claim.

## What they found
No empirical results. Hypothesised task factors: global vs local explanation, area and severity of incompleteness,
time constraints, user expertise. Hypothesised method factors: form of the cognitive chunks, how many there are,
how they compose, monotonicity, and how uncertainty is represented. They flag that proxies like sparsity are hard to
compare across forms (sparse in features vs sparse in prototypes).

## Limits and open problems they name
Which functional proxies correspond to which real applications; how to design simplified human tasks that still
reflect real ones; what makes a proxy valid. Human experiments are costly and must be designed carefully.

## What we take from it
- **Framing:** our predictive white-box model is naturally evaluated as *forward simulation* — does the
  reconstruction predict the network's output on held-out inputs — and *counterfactual simulation* — does it
  predict what change flips the output. These are the field's canonical names; we should use them.
- **Measure:** score predictions against the *network's* output, not ground-truth labels.
- **Warning:** a functional proxy (sparsity, number of components, approximation error) only counts once it is
  shown to track real usefulness; match evaluation level to the claim we make.

## Tags
unit: whole-model
form: description | program
method: other
eval: prediction/simulation | human-rating | downstream-task
goal: evaluation-of-methods | science
