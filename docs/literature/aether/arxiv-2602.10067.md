# Features as Rewards: Scalable Supervision for Open-Ended Tasks via Interpretability

- **Key:** arxiv-2602.10067
- **Authors / organisation:** Aaditya Vikram Prasad, Connor Watts, Jack Merullo, Dhruvil Gala, Owen Lewis, Thomas McGrath, Ekdeep Singh Lubana; Goodfire AI
- **Date:** 2026-02-10
- **Link:** https://arxiv.org/abs/2602.10067
- **Kind:** paper
- **Read from:** full text (HTML version, main body + results; appendices only skimmed for prompt design)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Interpretability readouts are normally used at inference time: to monitor an output or to steer a model. The authors ask
whether the same internal quantity can instead become a *training* signal for behaviours that resist cheap automatic
grading — "open-ended" behaviours where many answers are acceptable and evaluating one answer needs a judge with tools.
Hallucination in long-form generation is their test case: verifying each factual claim is expensive, so the usual reward
is an LLM judge, which is slow and poorly calibrated. Their larger goal is a general recipe in which a model's own
features supply dense supervision, making the interpretability tool an oversight instrument rather than an explanation.

## What they studied
Gemma-3-12B-IT as both the policy being trained and the *frozen teacher* whose residual-stream activations define the
reward. Data: Longfact++ (~20K long-form questions across domains) for training probes and for evaluation, with Gemini
2.5 Pro (with web search) as the ground-truth grader. Unit of analysis is a token-level *span* — an "Entity", i.e. a
single falsifiable claim — inside a long completion. Four separate probe heads are trained, not one: localisation,
classification (is this span hallucinated?), retraction quality, and correction quality.

## How they did it
Generation is decomposed into detect → intervene → reward → RL. First the policy answers a Longfact++ prompt; Gemini
extracts falsifiable spans and labels each as supported or hallucinated, which yields training labels for the frozen
base model's activations. A localisation probe predicts, per token, whether it starts/continues an Entity, and a
classification probe reads activations pooled across the localised span to output P(hallucinated); the two-stage split
was, they say, necessary to get high true-positive rate. When the classification probe fires, a *fresh sub-context* is
opened in which the model must pick maintain / retract / correct and write the intervention. A second pair of probes —
retraction and correction — grades sampled interventions from the same frozen base model's activations, imitating
Gemini's rubric labels, and these scores are the reward. The final reward multiplies probe score by two token-space
judgements from the base model (legibility, on-topic-ness), and a Lagrangian on a 60:40 correction-to-retraction ratio
keeps the policy from collapsing onto the easier action. Training: 360 steps of ScaleRL/CISPO. Evaluation compares the
trained policy, an ablation without best-of-N, an ablation without inlining the interventions, and the *untrained* base
model with the same monitoring-plus-intervention pipeline — the last is the key null that separates gains from training
from gains from in-context correction.

## What counts as an explanation here
Not a mechanism. The probes are treated as *measures of belief*: the classification probe's output is read as the
model's uncertainty about a claim's validity. What is argued is calibration — that a probe score of 0.xy corresponds to
an xy% chance the claim is really false — rather than interpretability of the circuit. The paper's own framing is that
the mechanism behind the resulting behaviour change stays "elusive" and belongs to future interpretability work.

## How they judged success
Hallucination-reduction rate against the Gemini grader (topline plus a decomposition into policy change, in-context
correction, and direct resolution), probe metrics chosen in advance (AUC-ROC, calibration curves, attention-map
inspection), held-out validation AUC, deployed precision/recall at a fixed threshold of 0.7 that was *not* tuned for
evaluation, standard benchmark suite (HellaSwag, PIQA, ARC, WinoGrande, BBH, MMLU, MATH, GSM8K, GPQA) versus base,
per-token KL divergence on supported vs unsupported spans, a blind Gemini rubric-preference test over ~1000 pairs, and
claim-count parity (63.4 ± 0.4 vs 63.6 ± 0.3 entities per completion) as a check against "hallucinate less by saying
less". Baselines: self-judging in token space by the same Gemma model, and base-model-plus-monitor.

## What they found
58% fewer hallucinations end-to-end with best-of-32, split as 10% from the policy becoming less hallucinatory in
training, 35% from inlining interventions into the completion, 13% from the interventions actually resolving claims.
Dropping inlining still leaves 31%, comparable to the base model with monitor plus inlining — most of the headline
number is in-context correction, not weight change. The reward pipeline transfers: running it on the trained policy's
activations instead of the base model's leaves fixed/retracted rates unchanged, so only one set of parameters is needed
at serving time. At test-time scaling the feature reward beats asking Gemma to grade its own interventions by nearly 15
points at n=256 — the model orders interventions correctly internally but cannot verbalise that ordering. Cost is about
two orders of magnitude below the judge: roughly $3.8K of compute for 300 steps of rewards against an estimated $344K
for Gemini-with-search grading. Standard benchmarks are flat and blind preference is 50.9%, i.e. no detectable quality
or style drift.

## Limits and open problems they name
Probe evasion under optimisation is the named threat; their mitigation is a frozen probe plus constraints that keep
generations natural, which they describe as sufficient *so far*, not proven. The evaluation stack shares prompts and
tooling with the data-collection stack, so labels are consistent by construction (they report red-teaming and manual
audits instead). Deployed monitoring precision/recall is well below the held-out AUC number (0.85 precision / 0.56
recall inline; 0.88/0.61 not-inline). Repeated or severe inline interventions can push completions out of distribution
into degenerate text. They note mechanisms remain unexplained, and propose cascades (cheap probe, expensive verifier on
low confidence) as future work.

## What we take from it
A reusable measure and a warning. Measure: *calibration of a probe readout, checked on held-out data and under the
deployment distribution (streaming, on-policy activations, probe-predicted spans rather than gold spans)* is what
licenses treating an internal quantity as a quantity at all — and once calibrated, it can be optimised against. This is
the strongest available argument that a probe is predicting something, not merely correlating. Warning: the ablation
that decomposes 58% into 10/35/13 is exactly the discipline our white-box model needs — always ask how much of the
effect is the policy's weights versus context supplied at test time. Second warning: a probe that measures a property
of the *base* model can stay valid after fine-tuning (their transfer check), which is evidence for stability of
representations under post-training but should be re-tested, not assumed, in any pipeline we build. Finally, the
"orders it internally but cannot say it" gap is a concrete instance of the decodable-but-unusable pattern, here with
the token-space judge as the weaker baseline.

## Tags
unit: feature | whole-model
form: probe
method: probing, training-interpretable, agent
eval: downstream-task, benchmark, human-rating
goal: control/editing, safety/auditing
