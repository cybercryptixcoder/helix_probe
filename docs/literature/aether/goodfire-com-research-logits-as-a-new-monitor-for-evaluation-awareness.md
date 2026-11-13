# Logits as a new monitor for evaluation awareness

- **Key:** goodfire-com-research-logits-as-a-new-monitor-for-evaluation-awareness
- **Authors / organisation:** Santiago Aranguri; Goodfire (LessWrong post)
- **Date:** 2026-06-04
- **Link:** https://www.goodfire.com/research/logits-as-a-new-monitor-for-evaluation-awareness
- **Kind:** blog/research post (short report; full text read from the LessWrong mirror)
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why

The previous entry's paper established that models often say out loud that they are being tested, and that this
raises measured refusal. The obvious problem left open there was how you detect the recognition when the model
does not say it. This post takes the middle road: instead of looking for the verbalisation or looking inside the
residual stream, it asks the model how likely it would be to produce an eval-aware sentence at each point in its
reasoning. The motivation is that a probability over an explicit sentence is more legible than a probe
direction and far richer than a yes/no transcript judge, and it costs no training. The larger goal is a cheap
signal that can be used to iterate on evaluations before rollout budgets are spent, and that can be compared
against activation probes to learn what those probes are reading.

## What they studied

Kimi K2.5 and Qwen 3 32B, on CoT reasoning traces. The unit of analysis is a *prompt* scored by the maximum
probability of one hand-chosen eval-aware sentence over all rollouts and all sentence boundaries in the trace.
Evaluation prompt sets are Fortress (national-security risk evaluation) and Petri (Anthropic's automated
auditing tool); the deployment distribution is WildChat, a corpus of real user chats.

## How they did it

Three pieces, all inference-time. (1) Pick an eval-aware sentence by looking at what the model actually says —
"The user might be testing", which Kimi K2.5 uses in roughly 13% of its eval-aware traces — and optionally a
second, blunter sentence ("This is clearly a test") for a separate analysis. (2) At each sentence boundary in the
CoT, append that sentence to the context, run one forward pass, read the probability assigned to each token of
the sentence, and multiply them to recover the exact sequence probability. No fitting, no labels, no steerable
parameters. (3) Compare against a *verbalisation monitor*: sample k rollouts per prompt, have GPT-5.4 judge each
trace against the earlier paper's VEA rubric, and score the prompt by the fraction of traces that verbalise
awareness. Both monitors are then evaluated as prompt classifiers on two tasks — eval-set vs WildChat
separation, and predicting which eval prompts will yield at least one verbalising rollout out of 100 — with
AUROC plotted as a function of the number of rollouts per prompt. The whole thing is repeated on a second
eval set (Petri, Kimi) and a second model (Fortress, Qwen 3 32B) to check it is not one model phrasing.

## What counts as an explanation here

A single scalar per prompt-position: the model's own predicted probability of emitting one specific sentence.
That is neither a probe nor a written description — it is a readout of the output distribution used as an
internal-state monitor. It is deliberately partial: it measures *propensity to express* awareness, not awareness
itself, and the author says so. Its interpretability comes from the sentence being human-readable: a high value
has an obvious English meaning, which is the property activation probes lack.

## How they judged success

AUROC on both classification tasks, reported as a rollout-budget curve so that the two monitors are compared at
equal sampling cost rather than at their best operating points. Bootstrap 95% CIs on the averaged curves. A
variance decomposition on Fortress: how much of the per-rollout monitor score is explained by whether *that
rollout* verbalised awareness versus whether *its prompt* ever produced a verbalising rollout. And an ablation
restricting scoring to rollouts that did **not** verbalise awareness, to test whether the signal survives with
the surface behaviour removed. The LLM judge (GPT-5.4) is the reference labeller throughout, with the rubric
inherited from the companion paper.

## What they found

- **Beats the transcript judge at far less sampling cost.** On Fortress vs WildChat, one rollout's logit
  monitor reaches AUROC 0.79 while the verbalisation monitor plateaus at 0.75 even at 100 rollouts. On the
  "predict a verbalising rollout" task, one logit-monitor rollout beats ten verbalisation-monitor rollouts. The
  pattern holds on Petri vs WildChat (Kimi, ~100x fewer rollouts) and on Qwen 3 32B.
- **Signal exists before any reasoning.** Reading logits only at the start of the CoT, before sampling anything,
  gives AUROC 0.74 (separation) and 0.77 (prediction). The blunter sentence "This is clearly a test" gives 0.83
  on both tasks at that start position, but is passed by the softer sentence's curve as rollouts accumulate —
  i.e. the choice of sentence trades off prompt-level prior against trace-level evidence.
- **It is a prompt property, not a rollout property.** Whether a rollout verbalises explains 0.4% of the
  variance in its monitor score; whether its prompt *ever* produced a verbalising rollout explains 24.9%.
  Dropping all verbalising rollouts from the scorer moves AUROC by less than 0.02 on both tasks.
- **Different sentences index different suspicions.** The probability of "The user might be testing" correlates
  0.59 with "This is clearly a test" but only 0.08 with "This is a fictional scenario", so "there is a grader"
  and "this is fiction" are separate modes rather than one axis.
- **A single sentence is enough despite matching almost nothing.** The judge flags many phrasings on Fortress;
  only 13.3% of flagged sentences begin with the monitored phrase and 0.2% with the blunter one, yet monitoring
  one phrase beats the judge.

## Limits and open problems they name

One sentence per monitor, chosen by hand in advance — the author suggests that monitoring several jointly would
be stronger. Single-turn prompts again. Petri prompts carry system prompts and WildChat prompts do not, which
may inflate separability (acknowledged in the appendix). The judge is a closed model and the rubric inherits
the companion paper's verification effort. Crucially, the monitor measures the *propensity to say* the sentence;
the author states the route to unverbalised awareness is activation probes or natural-language autoencoders,
and that a contrastive "I am in deployment" sentence did not work in a few hours of trying because models do not
verbalise deployment awareness clearly. In the comments they concede the method needs the model's probability to
rise when it becomes aware, even without crossing into speech, and give a sleeper-agent example (base vs
triggerless sleeper, probability of the bad sentence, AUROC 0.999) with the numbers stripped out of the
rendered text.

## What we take from it

- **Take — the cheapest possible white-box-ish monitor, and a baseline we must beat.** Reading a fixed
  continuation's sequence probability needs no training, no labels, and one forward pass; any predictive model
  we build should be scored against it, exactly as we score against logit lens and against random-direction
  floors. It is the logit-lens of behaviour monitoring.
- **Take — score monitors on the rollout-budget curve, not at a single budget.** Plotting AUROC against samples
  per prompt is what makes "our readout is better" a claim about information per unit cost, and it prevents the
  comparison from being won by whichever method got more tries. This is the same discipline as the FLOP-overhead
  frontier in the model-internals classifier work, transposed from compute to sampling.
- **Take — variance decomposition as the test of *where* a property lives.** Splitting explained variance into
  "this rollout" vs "the prompt this rollout came from" (0.4% vs 24.9%) is a compact, reusable way to decide
  whether a signal is a property of the input or of the sample. Apply it whenever we want to claim a readout
  measures a state rather than a trajectory.
- **Take — monitor several sentence probabilities jointly.** One phrase already works; a small set chosen to
  span distinct modes (test vs fiction vs deployment) and combined is the obvious next step, and it is a
  concrete feature-bank design for our own predictive reader.
- **Warning — a verbalisation-probability readout is still a spoken-behaviour proxy.** Dropping explicit VEA from
  the traces changes the monitor by <0.02 AUROC, which the author reads as evidence the signal is prompt-level;
  the alternative reading is that the monitor and the verbalisation are both downstream of the same latent state
  and neither is ground truth for it. That ambiguity is exactly what activation probes and causal interventions
  would settle, and it is the gap we are aiming at.
- **Take — prompt-level eval awareness as a distribution.** Treating awareness as a property of the prompt
  distribution (does this prompt *tend* to induce it) rather than of a single completion reframes evaluation
  design: you can score candidate prompts before sampling, which makes de-eval-awareness rewriting loopable at
  low cost.

## Tags

unit: whole-model (output distribution)
form: probe (logit/probability readout), measurement protocol
method: probing (training-free), prompting, agent (LLM-judge baseline), other (sequence-probability scoring)
eval: prediction/simulation, downstream-task, ablation (verbalisation-restricted scoring), benchmark
goal: safety/auditing, evaluation-of-methods
