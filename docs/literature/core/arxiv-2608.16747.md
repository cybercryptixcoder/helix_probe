# Would This Change Your Answer? Evaluating Explanations of LLM Behavior in the Wild with Counterfactual Experiments (CHIVE)

- **Key:** arxiv-2608.16747
- **Authors / organisation:** Adam Karvonen, Euan Ong, Subhash Kantamneni, Samuel Marks; Anthropic (and Anthropic Fellows)
- **Date:** 2026-08-17
- **Link:** https://arxiv.org/abs/2608.16747 (research post: https://alignment.anthropic.com/2026/chive/)
- **Kind:** benchmark
- **Read from:** full text (main body and early appendices; read via HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Explanations of model behaviour (from interpretability tools or chain of thought) are hard to check because the true
cause is usually unknown. The authors operationalise a good explanation as one that helps predict what the model does
on related counterfactual inputs (counterfactual simulatability). Earlier tests used planted hints; they want natural,
diverse behaviours at scale, and then to ask whether activation-reading tools or self-explanation training actually
improve such predictions.

## What they studied
Targets: Qwen3-8B, Qwen3-32B, Qwen3.5-397B-A17B, Gemma-3-27B-IT, Llama-3.1-8B (non-thinking). Prompts mainly from
WildChat (about 9% agentic transcripts). Unit: whole-model behaviour rates over resampled responses; tools read
activations.

## How they did it
The CHIVE pipeline samples 30 responses per prompt over tens of thousands of prompts; an investigator (usually Claude
Opus 4.6) flags an unexpected behaviour; an agent runs 5–15 counterfactual prompt edits, resampling and measuring the
change in behaviour rate; an independent judge verifies. Outputs are an open-ended explanation (not treated as ground
truth) and counterfactual claims of the form "this edit changes the behaviour rate". A claim is labelled true if the
edit moved the rate by at least 50 points and false if by at most 15; up to two of each per investigation, then three
LLM-judge filters. Application 1: a predictor agent (Opus 4.8) sees a transcript and a claim and outputs a probability;
tool-augmented versions may make up to 5 read-only calls to activation oracles, natural-language autoencoders or SAEs
on the target. Application 2: train the target to answer, after its own transcript, whether an edit would change its
behaviour, and separately to produce open-ended explanations; a cross-training control (each 8B model trained on the
other's data) tests for privileged self-access.

## What counts as an explanation here
Anything (text, tool output, self-report) is judged only by whether it improves predictions of behaviour under input
edits. The explanation is a means to prediction, not an end; ground truth is the resampled counterfactual, not a
mechanism.

## How they judged success
Accuracy and AUROC of predicted claim truth against resampled counterfactual labels (n=30 responses per measurement).
Baseline: transcript-only predictor. Robustness: other predictor families (GPT-5.5, Gemini-3.1-Pro), hyperparameter
sweeps, manual and automated prompt optimisation. Self-prediction compared to an Opus reference; hint-setting
evaluations on AITA and MMLU with injected cues; PETRI transcripts for out-of-distribution.

## What they found
None of activation oracles, NLAs or SAEs improved on the transcript-only baseline for Gemma-3-27B-IT or Qwen3-8B, and
the null survived all robustness checks. Tools did shift predictions, but helpful and misleading cases cancelled; only
0.6% of relevant NLA outputs stated an explicit causal relation. Trained self-prediction came within ±0.03 AUROC of the
Opus reference on all held-out sets. Open-ended explanation training was mixed (397B hint attribution 0.59 to 0.68 vs
Opus 0.64; no gain at 8B) and misled strong simulators. Cross-trained models matched self-trained ones: no evidence of
privileged access.

## Limits and open problems they name
Benchmark is a proxy: anyone with sampling access can run the counterfactual directly. Interventions (steering,
patching) were excluded, so the ceiling is unknown. Only activation-based tools were tested, not weight- or
circuit-level methods. Behaviours with clean counterfactual causes may not be representative. Contrasts with auditing
games where these tools helped.

## What we take from it
The most directly reusable measure in this batch: score an explanation by its accuracy/AUROC at predicting behaviour
change under input edits, with resampled ground truth and a strong transcript-only baseline. This is exactly the
predictive standard our white-box model must meet. It also explicitly leaves weight- and circuit-level methods
untested, which is an open slot we could fill. Warning: activation readouts that are correlational rarely carry
causal claims, so our model must output causal predictions directly.

## Tags
unit: whole-model
form: description
method: agent | SAE | probing | other
eval: prediction/simulation | benchmark
goal: evaluation-of-methods | safety/auditing
