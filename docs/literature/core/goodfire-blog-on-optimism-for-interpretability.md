# On Optimism for Interpretability

- **Key:** goodfire-blog-on-optimism-for-interpretability
- **Authors / organisation:** Eric Ho; Goodfire
- **Date:** 2025-07-17
- **Link:** https://www.goodfire.com/blog/on-optimism-for-interpretability
- **Kind:** essay
- **Read from:** full text
- **Relevance to us:** 1 (background)

## What they wanted, and why
A position essay arguing that interpretability can succeed and is worth investing in now. It starts from recent
frontier-model failures (a sycophantic ChatGPT update, Anthropic's reports of blackmail behaviour under shutdown
threat, a Grok update producing antisemitic content) and notes that developers fix such problems by retraining
blindly, even though weights and activations are fully visible. The goal is a science that lets developers explain,
debug and deliberately design models before deployment.

## What they studied
No experiments. Cites evidence from SAEs, Goodfire's Evo 2 genomics-model work, helical number representations for
addition in LLMs, and linear parameter decomposition.

## How they did it
Argument from examples. Lays out four application areas (alignment and auditing, including model diffing; debugging
back to components and training data; editing and intentional design; scientific discovery from scientific models)
and four reasons for optimism.

## What counts as an explanation here
Not defined formally. Implicitly: tracing a behaviour to internal representations and components well enough to edit
it, analogous to a stack trace or a git diff of a model.

## How they judged success
Qualitative: being able to detect and fix problems like sycophancy or scheming pre-deployment, trace reasoning in
high-stakes domains, and extract scientific knowledge from models.

## What they found
Reasons for optimism: models show rich interpretable structure (SAE concepts, Evo 2 activations encoding position on
the tree of life, helical number representations); models are easier to study than brains because access and
intervention are complete; unsupervised scalable methods exist (sparse dictionaries, transcoders, parameter
decomposition, automated labelling); the field is small (the author estimates under 150 full-time researchers) and
young.

## Limits and open problems they name
Representational geometry, attention, linking representations to computation, scaling circuit discovery; time
pressure relative to capability growth; nobody knows how much behaviour can ultimately be explained.

## What we take from it
Background framing only. Two useful points: full white-box access is the field's advantage over neuroscience, which
supports a weights-first approach; and "model diffing" (what changed in the weights after training) is a concrete use
case a predictive white-box model could serve.

## Tags
unit: whole-model
form: description
method: SAE | transcoder | decomposition | other
eval: (none)
goal: safety/auditing | debugging | control/editing | science
