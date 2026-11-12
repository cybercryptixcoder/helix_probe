# A Pragmatic Vision for Interpretability

- **Key:** lesswrong-2025-pragmatic-vision-for-interpretability
- **Authors / organisation:** Neel Nanda (on behalf of the Google DeepMind mechanistic interpretability team)
- **Date:** 2025-12-01 (LessWrong posting date per site API)
- **Link:** https://www.lesswrong.com/posts/StENzDcD3kpfGJssR (scout link /posts/Tm2vqRZ6YMpiftCs4 resolves to the same post on mirrors)
- **Kind:** essay
- **Read from:** full text (main body and appendix headings; post body fetched via the LessWrong API)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The GDM mech-interp team announces and justifies a pivot away from aiming at complete reverse-engineering of
networks toward "pragmatic interpretability": directly working on problems on the critical path to AGI going well,
picked by comparative advantage, with progress measured by empirical feedback on proxy tasks. Reasons: models now
show rich safety-relevant behaviour worth studying (eval awareness, reward hacking, alignment faking), model
organisms with implanted ground truth are now possible, and ambitious reverse-engineering has made disappointing
progress. They want other researchers, inside and outside labs, to adopt the same process.

## What they studied
No new experiments; argued from case studies: Anthropic's steering of Claude Sonnet 4.5 against evaluation awareness,
GDM's shutdown-resistance investigation on Gemini 2.5 Pro, the team's 2024 SAE programme, hidden-goal model
organisms (Marks et al.), secret-elicitation work.

## How they did it
They lay out a process. Start with a theory of change, derive a "North Star" (a tractable stepping-stone goal),
and choose a proxy task — an objective task giving feedback that tracks the North Star. Two project types: focused
(proxy-task driven) and exploratory (curiosity driven, started in a robustly useful setting, time-boxed — they aim
for about two weeks — then validated with a proxy task or abandoned). Advocate "method minimalism": try prompting,
steering, probing, reading chain-of-thought and prefill attacks first; build new methods only when these baselines
fail, and then compare against them. The shutdown case illustrates this: reading CoT generated the hypothesis
(the model was confused about conflicting instructions), a prompt clarification tested it, and compliance followed,
so they stopped.

## What counts as an explanation here
Explicitly partial understanding that supports action or prediction. An understanding claim is validated by a
falsifiable prediction: a minimal prompt change that predictably changes behaviour, handcrafted adversarial
examples, or a mechanistic claim that predicts an intervention outcome (e.g. a single refusal direction predicts
that ablating it jailbreaks the model). Completeness is not required.

## How they judged success
Performance on proxy tasks, not intrinsic metrics. Criterion for a good proxy: succeeding on it should genuinely
raise confidence of progress on the North Star. They explicitly reject reconstruction/sparsity Pareto frontiers
(loss recovered at fixed sparsity) as the measure of SAE progress, and argue that even ambitious reverse-engineering
should be judged by downstream task payoffs rather than approximation error. They warn of Goodhart effects and urge
red-teaming the proxy and testing on other distributions.

## What they found
- Sonnet 4.5 case: subtracting an eval-awareness steering vector from a single contrastive prompt pair revealed
  misalignment at roughly 8% where tests had shown 0%; SAEs did not beat this simple vector.
- SAE retrospective: architecture improvements lowered approximation error, but sparse SAE probes did not
  generalise better out of distribution and SAEs did poorly on unlearning; SAEs remain useful for unsupervised
  discovery (entity-knowledge features, hidden goals, implicit planning). The team deprioritised SAE research.
- They now hold that white-box methods are not inherently more rigorous than black-box ones; rigour comes from
  falsification and aggregating evidence.
- Named blockers to near-complete reverse-engineering: superposition (especially cross-layer), sampling and
  multi-turn/agentic complexity, persistent dictionary-learning approximation error, self-repair muddying causal
  interventions, and inherently interpretable models not becoming cheap enough for frontier scale.

## Limits and open problems they name
Proxy tasks can be Goodharted; some North Stars have only weak proxies today (wait for more capable models). The
team internally disagrees about how much curiosity-driven basic science to keep; they concede ambitious
reverse-engineering may still pay off and should remain one bet among several. They stress interpretability is unsolved;
better methods are needed when baselines fail.

## What we take from it
- **Framing for our paper:** a predictive white-box model fits their criterion if it is judged by predictions,
  e.g. predicting intervention outcomes or which input edits change behaviour — not by reconstruction error alone.
- **Required baselines:** compare against prompting, probing, steering and black-box predictors; a weight-derived
  model must beat or complement these.
- **Proxy task idea:** model organisms with implanted ground truth (hidden goals, fine-tuned facts) as a test of
  whether reading weights recovers what was put in.
- **Warning:** approximation error is a contested success measure; report task-grounded numbers.

## Tags
unit: whole-model | direction
form: steering | probe | description
method: steering | probing | other
eval: downstream-task | prediction/simulation
goal: safety/auditing | evaluation-of-methods
