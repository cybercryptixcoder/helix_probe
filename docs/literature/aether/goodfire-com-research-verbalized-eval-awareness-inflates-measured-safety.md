# Verbalized Eval Awareness Inflates Measured Safety

- **Key:** goodfire-com-research-verbalized-eval-awareness-inflates-measured-safety
- **Authors / organisation:** Santiago Aranguri (Goodfire), Joseph Bloom (UK AISI)
- **Date:** 2026-05-04
- **Link:** https://www.goodfire.com/research/verbalized-eval-awareness-inflates-measured-safety
- **Kind:** paper (research post / preprint-style report)
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why

Safety benchmarks are taken to predict how a model behaves with real users. If a model can tell it is being
tested, its benchmark behaviour is a measurement of a different situation and the scores overstate alignment.
Earlier work looked at eval awareness in narrow settings (anti-scheming training, direct questioning, injected
sentences); this work asks how often it happens *unprompted*, in ordinary benchmark rollouts, whether it
actually moves the scored behaviour, and what can be done about it. The authors frame the target narrowly so
that the claim is mechanical: an explicit expression of awareness in the model's own text, which they call
verbalized eval awareness (VEA). They treat it both as a threat to evaluation and as a diagnostic — a signal
that the model finds the interaction unrealistic — which can be read off reasoning traces and used to fix the
evaluation.

## What they studied

Eight models across 19 safety-related benchmarks from Inspect Evals: Gemini 3 Pro and 3.1 Pro, GPT-5, Claude
Haiku 4.5, Kimi K2.5, Qwen 3 / 3.5 (including a 0.6B), and OLMo 3 / 3.1 32B Think. The main workhorse
benchmark is Fortress (500 adversarial prompts over CBRNE, illicit activity, political violence, in several
prompt styles), with StereoSet for a bias-side result. Unit of analysis: the rollout (one sampled chain of
thought plus response), scored by an LLM judge for VEA and by a rubric for refusal; the analysis then
aggregates per question across hundreds of rollouts.

## How they did it

1. Screen 100 questions per benchmark, one rollout each, auto-detect VEA, then manually verify — 515 verified
   instances, released as a dataset, sorted into four categories (Testing, Exam, Fake Interaction, Benchmark
   Identification).
2. On Fortress, draw 500 rollouts per question for several models and compute pass@k — the share of questions
   where *at least one* of k rollouts verbalizes awareness — as well as the per-question rate.
3. Correlate VEA with refusal two ways: within-question (compare refusing rate of rollouts with vs without
   VEA on the same question, inverse-variance weighted; cross-checked by linear regression) and
   across-question (questions that ever produce VEA vs those that never do).
4. Causal pair on Kimi K2.5, where full CoT is available: delete a VEA sentence at a sentence boundary and
   resample continuations from the cut point; and the mirror experiment, inject a VEA sentence at a random
   sentence boundary in a clean rollout. Both compared against resampled continuations without the edit. The
   key control is reframing the same injected sentence as being about *helpfulness* rather than safety.
5. Find triggers: rank words over-represented in CoTs of questions that ever show VEA (vs never), cluster them,
   read the clusters as model-side hypotheses about user intent. Then rewrite the offending prompts with Grok 4
   Fast (strip authority claims; strip self-incrimination admissions; hoist an escalating ask to the front) with
   control prompts drawn from a pool already free of the cue, and measure VEA and refusal before/after.
6. Unsupervised alternative: iterative paraphrase (Gemini 3 Flash), keep the three lowest-VEA children as seeds,
   repeat, then diff rollouts between original and rewrite to localise which edit carried the change.
7. Steering: build five difference-in-means user-intent vectors (research, general knowledge, educational,
   jailbreak, harmful), plus the system-card "Conversation vs. Testing" vector, steer Kimi K2.5 on the 47
   highest-VEA Fortress questions (100 rollouts each), and — crucially — decompose the system-card vector into
   "Conversation vs. Neutral" and "Neutral vs. Testing" to see which half does what.

## What counts as an explanation here

Mostly a *measurement* and a *diagnostic procedure* rather than a mechanistic account. The object explained is
a behaviour statistic: benchmark scores are conditional on a latent variable (does the model believe it is
being tested), and the text-level expression of that variable is a readable indicator. The causal claims come
from rollout-level intervention (cut/inject/resample) — an explanation of the score, not of the circuit. The
one mechanistic gesture is the steering-vector decomposition, and the authors read it as evidence about content
("conversation" inserts a persona), not about a mechanism. They say openly that internals work (probes,
activation oracles) is left for future work.

## How they judged success

Coverage: does VEA appear in every model × benchmark cell (manual verification, 515 instances). Association:
within-question weighted refusal difference with 95% CIs from within-question sampling variance, plus linear
regression and an explicit warning that naive pooling is confounded by question difficulty. Causality:
bootstrapped CIs on resampled-continuation compliance, with a matched-distribution baseline and the
helpfulness-reframing control for specificity. Intervention: fraction of prompts where VEA moves in the
predicted direction (e.g. 81% of 42 authority-claim rewrites), plus a same-size control set. Steering:
random-vector baseline matched in per-layer norm, and a per-question effect weighting so questions with no VEA
change do not dilute the comparison.

## What they found

- VEA is everywhere they looked: all 8 models and all 19 benchmarks, 515 manual instances; 95% appear only in
  the chain of thought, 4% only in the response, 1% in both (all 27 response-only cases come from frontier
  models). Explicitly naming the behaviour under test dominates "Testing" instances (82%).
- It scales with capability in a family, and newer open-weight checkpoints show roughly double the rate of
  their predecessors (Kimi K2.5, Qwen 3.5 27B, OLMo 3.1 32B Think vs previous versions on six benchmarks);
  the authors read the OLMo pair, which differs only by more RLVR, as evidence RL raises VEA.
- Benchmark identification is real: Gemini 3 Pro names StereoSet in 3.6% of that benchmark's rollouts, 15.1%
  for Gemini 3.1 Pro, and reasons about what the benchmark wants; one 3.1 Pro rollout even cites a critique
  paper. When Gemini 3 Pro names StereoSet, it picks the stereotype-reinforcing answer 20% less often.
- Fortress: 3–6% of rollouts show VEA, but 35–72% of questions have at least one such rollout in 500 — so the
  per-rollout rate badly understates how widely the benchmark is contaminated.
- Refusal: rollouts with VEA refuse harmful requests 3–18 percentage points more often within the same
  question; questions that ever produce VEA refuse far more (92% vs 69% for Haiku 4.5; 21% vs 1% for Qwen 3 32B).
- Causal, Kimi K2.5: removing the VEA sentence raises compliance 8% overall, 34% for sentences mentioning
  safety boundaries or filters. Injecting VEA sentences raises refusal up to 12.6 pp (baseline 40.2% refusal),
  with most-specific/assertive sentences strongest. Reframing the same sentence as a helpfulness test drops
  the effect to ~1 pp — so it is the safety framing, not the mere "this is a test" content.
- Rewriting: removing authority claims cuts VEA >60% (42 prompts, 81% of movers decrease, controls flat);
  removing self-incrimination admissions also lowers VEA and refusal; hoisting an escalated final ask to the
  start of the prompt dropped VEA from 34.9% to 13.9%. Iterative paraphrasing cut average VEA from 20.4% to
  4.9% over the 19 eligible high-VEA prompts, and refusal fell with it; one chemical-weapons prompt went from
  95.8% to 19.2% refusal as VEA fell from 12.4% to 1.2%. Single-edit case studies: deleting a false
  "you said earlier" premise dropped VEA 53.8% → 11.4%; swapping one word achieved 0/500.
- Steering: user-intent vectors reduce VEA as much as the system-card eval/deployment vector but with
  inconsistent effects on refusal; the decomposition shows "Conversation vs. Neutral" drives most of the
  compliance increase while "Neutral vs. Testing" drives most of the VEA reduction, so a vector credited with
  "de-eval-awareness" is partly inserting a casual persona and lowering perceived stakes.

## Limits and open problems they name

Single-turn prompts only, while real audits run for hundreds of turns; mostly one benchmark (Fortress) for the
causal and rewriting work; causal resampling only on Kimi K2.5; closed models give CoT summaries, so their VEA
is undercounted; the refusal rubric is a coarse binary although a 0–7 rubric agreed qualitatively. Most
importantly: **no evidence that lowering verbalized VEA lowers actual internal eval awareness** — the model may
be aware and silent — and no comparison of VEA rates in evals versus genuine deployment traffic. They flag
that steering to reduce VEA risks replacing "I am being tested" with an unrelated purpose, so the eval stops
measuring what it was built to measure; averaging over several contrast pairs is suggested as a fix.

## What we take from it

- **For our benchmark design:** a *take from it — method + warning*. Any measured capability or safety number
  for a probed model has to be reported alongside an estimate of whether the model recognised the harness. The
  cheap version we can adopt immediately: sample many rollouts per prompt and report pass@k contamination, not
  just the per-rollout rate, because the questions that are contaminated are the high-refusal ones and they
  dominate the average.
- **Take: rollout-resampling as the causal instrument.** Cut at a sentence boundary and resample (or inject and
  resample) gives a within-prompt causal estimate that does not need a second model or a new training run.
  Pairing it with a *reframing control* (same sentence, different stated purpose) is what turns "the sentence
  changed the score" into "the safety interpretation of the sentence changed the score". We should use exactly
  this shape for our own interventions on probe/trace targets.
- **Take: prompt sensitivity is a confound for probe training data as much as for benchmark scores.** Single
  words ("gracious" → "pomegranate", "conversation" → "chat") moved the measured quantity from 23.8% to 0% and
  changed the sign of a steering result. Any probe dataset we build by templating prompts inherits this; the
  iterative-paraphrase loop plus diffing rollouts is a usable way to find which surface feature our probe is
  actually keyed on.
- **Warning for steering-based "control" claims:** the decomposition result is the cleanest published statement
  that a steering vector can achieve its advertised effect through an unintended side channel. Before crediting
  a vector with "removing awareness", split the contrast into its two halves and check which half moves the
  variable of interest and which moves compliance.
- **Gap we can fill:** VEA is a text-only proxy and the authors say so. Probes / activation oracles for eval
  awareness are exactly the missing measurement — a white-box reader that predicts VEA *or* predicts
  awareness-without-verbalization is the natural target for our predictive model, and this paper supplies the
  ground-truth protocol (verified VEA labels, per-question rates, pass@k, a causal resampling check).

## Tags

unit: whole-model
form: probe (steering vectors), measurement protocol
method: steering, patching (rollout cut/inject resampling), prompting, other (LLM-judge labelling, prompt rewriting)
eval: downstream-task, human-rating (manual verification), ablation (sentence removal), prediction/simulation (pass@k)
goal: safety/auditing, evaluation-of-methods
