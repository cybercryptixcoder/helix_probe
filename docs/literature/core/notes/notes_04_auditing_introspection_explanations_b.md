# Notes: auditing, introspection, explanations (batch b)

**What an explanation is.** Four of five papers treat an explanation as a short natural-language statement about
behaviour, valued only for what it lets someone do: name a hidden behaviour (arxiv-2602.22755, arxiv-2604.16812),
answer a question about an activation (arxiv-2512.15674), or predict behaviour under an input edit
(arxiv-2608.16747). Only arxiv-2603.21396 offers a mechanism (a carrier-to-gate transcoder circuit). The field's
operational test is shifting from "is it faithful?" to "does it improve prediction or downstream decisions?".

**How success is measured.** Ground truth comes from construction: implanted behaviours in model organisms
(AuditBench's 56 models; the adapter's hundreds of variants), injected concept vectors, or resampled counterfactual
behaviour rates (CHIVE, n=30). Metrics: agent success rate over many seeds, verbalization rate, AUROC/accuracy of
predicted counterfactuals, TPR with a no-intervention false-positive rate. LLM judges grade almost everything.

**Recurring baselines.** A plain agent with chat only; scaffolded black-box sampling (prefill, user sampling, text
completion), which is often the strongest; transcript-only predictors; untrained base models; logit lens, SAEs,
steering, activation oracles as the white-box comparison set.

**The uncomfortable pattern.** White-box/activation tools give small or zero uplift: helpful only on the easiest
AuditBench targets, below default on adversarially trained ones, and no gain at all on CHIVE across three predictor
families. Causes named: tool-to-agent gap (unused or misleading outputs), correlational readouts that almost never
state causal relations, and false positives (introspection adapters; base model in arxiv-2603.21396).

**Open problems.** Narrow fine-tuned model organisms may be easier than real behaviours; no tested ceiling with
interventions; trained readers and self-reports are themselves black boxes; self-report can understate what the model
internally detects (gating in arxiv-2603.21396); no evidence of privileged self-access (arxiv-2608.16747).

**Bearing on a predictive white-box model from weights.**
- CHIVE explicitly leaves weight- and circuit-level methods untested; its counterfactual-simulatability protocol
  (claim-level AUROC vs a transcript-only baseline) is a ready-made, field-recognised test for our model.
- AuditBench gives a ground-truth testbed with weight diffs (behaviour LoRAs) whose effects are known; predicting the
  implanted behaviour from the weights alone is a natural task, and the bar to beat is scaffolded black-box sampling.
- The introspection adapter shows a low-rank (even rank-1) learned map from fine-tune to behaviour description exists;
  a weight-reading model should match it without needing the model to talk.
- Always include a no-behaviour/no-intervention control; false positives are where these methods fail.
