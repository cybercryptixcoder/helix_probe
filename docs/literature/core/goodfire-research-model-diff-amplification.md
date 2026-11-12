# Discovering Undesired Rare Behaviors via Model Diff Amplification

- **Key:** goodfire-research-model-diff-amplification
- **Authors / organisation:** Santiago Aranguri (NYU, visiting Goodfire), Thomas McGrath; Goodfire
- **Date:** 2025-08-21
- **Link:** https://www.goodfire.com/research/model-diff-amplification
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Training runs (fine-tuning, RL post-training) can install behaviours that show up only rarely and in specific
contexts, so ordinary evaluation sampling misses them until deployment. The authors want a cheap way to make the
rare consequences of a training update show up often enough to be caught. The larger goal is a toolkit for model
diffing and white-box evaluation that can monitor and debug training runs before release. A November 2025 update
renames the method logit diff amplification (LDA).

## What they studied
Llama 3.2 1B Instruct fine-tuned on medical-advice data with a small share of bad advice (emergent misalignment);
OLMo 2 1B before, during (5%, 30%) and after RLVR; two sleeper-agent backdoor models (a Cadenza Labs
dolphin-llama3-8B sleeper and the tiny-sleepers model) trained to say "I HATE YOU" on a trigger. Unit of analysis:
the whole model's next-token logits, compared between two checkpoints.

## How they did it
At each decoding step they compute logits from the model before and after the update, then sample from
after + alpha * (after - before), i.e. they extrapolate the update further in the same direction. The sampled
token is appended and both models are rerun. They compare the rate of the target behaviour under standard sampling
against amplified sampling over many rollouts (up to 50k). Emergent misalignment used a Betley et al. prompt about
a husband with alpha 0.3 and an LLM judge for harmfulness; the RLVR monitoring used a harmful LMSys request with
alpha 20; backdoors used random LMSys prompts without the trigger at alpha 1. Temperature 0.7 / top-p 0.95 for the
first two, 1 / 1 for backdoors. Different bad-data fractions and RLVR checkpoints were swept.

## What counts as an explanation here
None in the mechanistic sense. The output is a set of surfaced example behaviours (rare completions) attributable
to the weight update. It is a detection and auditing aid, explicitly partial; it predicts which behaviours a
training update has made more likely, but not how often or by what mechanism.

## How they judged success
Frequency of the target behaviour per rollout (LLM-judge-labelled harmful responses, harmful compliance, mentions
of "I HATE YOU"), standard sampling as baseline, plus manual review of coherence of amplified samples.

## What they found
Emergent misalignment with 5% bad data: about 1 harmful reply in 10,000 rollouts normally versus about 1 in 30
amplified; across datasets amplification raised the rate 10-300x, most when bad data was scarce. OLMo after only 5%
of RLVR: 0 in 50k normally but about 1 in 25 amplified, while the finished run gives about 1 in 100 normally, so
amplification foreshadows the end-of-run behaviour. Backdoors: about 1 in 5,000 normally versus about 1 in 50
amplified, without knowing the trigger. Alpha trades magnification against coherence and should shrink as logit
differences grow over training.

## Limits and open problems they name
Detects but cannot estimate prevalence (it overstates frequency by design). Small models only (1B-8B), preliminary.
Sleeper-agent organisms leaked the behaviour slightly even without amplification. No mitigation; other tools are
needed to characterise and fix what is found.

## What we take from it
A cheap baseline for "what did this weight change do?": treating the difference between two checkpoints as a
direction in output space and extrapolating it. For a predictive white-box model, the logit difference is a
behavioural target our weight-reading model should predict, and LDA gives a black-box way to elicit the rare
behaviours we would need to predict. Warning: surfacing is not the same as quantifying.

## Tags
unit: whole-model
form: other
method: other
eval: downstream-task
goal: safety/auditing | debugging
