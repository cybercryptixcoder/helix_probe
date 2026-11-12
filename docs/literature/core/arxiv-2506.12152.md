# Because we have LLMs, we Can and Should Pursue Agentic Interpretability

- **Key:** arxiv-2506.12152
- **Authors / organisation:** Been Kim, John Hewitt, Neel Nanda, Noah Fiedel, Oyvind Tafjord; Google DeepMind
- **Date:** 2025-06
- **Link:** https://arxiv.org/abs/2506.12152
- **Kind:** essay
- **Read from:** full text
- **Relevance to us:** 1 (background)

## What they wanted, and why
A position paper arguing that LLMs make possible a new mode of interpretability: a multi-turn conversation in
which the model actively helps a human understand it. The worry behind it is that human understanding will fall
further behind as models approach or exceed human ability, so we need channels for humans to learn the models'
concepts, possibly superhuman ones. They position this as a complement to, not a replacement for, mechanistic
("inspective") methods. No experiments are reported.

## What they studied
No models are studied empirically. The unit is the whole model as a conversational partner; concepts are framed
as functions from input/output pairs to a value, either human-defined (correctness, length) or model-dependent
(would the model refuse, the model's chess move).

## How they did it
Conceptual argument. They define agentic interpretability by three properties: the model proactively assists,
understanding develops over multiple turns, and the model keeps a mental model of the user (implicit via history
or explicit, e.g. a knowledge graph) which in turn helps the user build a mental model of the AI. They contrast
it with inspective methods along mode, strength, output, best use and main risk. They then sketch evaluation
designs and three illustrative scenarios: a "model trainer model" that knows a project's history and suggests
debugging hypotheses; a chess tutor that teaches a hypothetical superhuman concept through puzzles; and agentic
mechanistic interpretability, where the model explains its own behaviour while researchers ablate or amplify its
internals ("open-model surgery").

## What counts as an explanation here
The understanding in a human's head, built through dialogue, optionally condensed into a model-written summary
report that humans can check. Explicitly partial; the authors concede it is less complete than circuit-style
explanations. Predictive power is the test: a learner who understands a machine concept should be able to predict
it on new inputs.

## How they judged success
No evaluation run. Proposed: (a) "improve" - the model's behaviour on a human-defined concept gets better;
(b) "learn" - humans can predict a machine concept on new inputs (simulatability), e.g. Elo gains for chess; (c)
application-grounded metrics; (d) LLMs as simulated users during development; (e) human-model co-discovery. They
name the core difficulty "human-entangled-in-the-loop" evaluation.

## What they found
Not applicable (position paper). Main claims: inspective methods suit high-stakes auditing; agentic methods suit
teaching and societal use; combining them (explanation under intervention) could expose inconsistencies.

## Limits and open problems they name
Hard-to-replicate, expensive human evaluation; high variance across users and LLM outputs; incompleteness; poor
hill-climbability without humans; models' limited self-knowledge; dependence on a cooperative, non-deceptive model;
producing reliable summaries; how user-modelling may shift model behaviour.

## What we take from it
Mostly a framing contrast: our white-box model is firmly inspective and artifact-based. Two reusable ideas: the
simulatability criterion (does the explanation let someone predict the model on new inputs) is exactly our target,
and "explain while we intervene" is a consistency check we can run between a weight-derived model and the
network's own outputs. Warning that self-explanations are not trustworthy evidence on their own.

## Tags
unit: whole-model
form: description
method: agent
eval: prediction/simulation | human-rating
goal: understanding | science
