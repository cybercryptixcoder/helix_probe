# Liars' Bench: Evaluating Lie Detectors for Language Models

- **Key:** arxiv-2511.16035
- **Authors / organisation:** Kieron Kretschmar, Walter Laurito, Sharan Maiya (Cadenza Labs; FZI; Cambridge), Samuel Marks (Anthropic)
- **Date:** 2025-11-20
- **Link:** https://arxiv.org/abs/2511.16035
- **Kind:** benchmark
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why

Detection methods for model dishonesty are usually validated on narrow data: short true/false statements, static text rather than text the model actually wrote, and facts about the world rather than about the model itself. The authors wanted a testbed that is hard to game, where the lie type is a controlled variable rather than a leftover of whichever dataset a detector happened to be trained on. Their larger aim is to make the question "does this readout know the model is lying?" answerable separately for each kind of lie, because a single average number hides exactly the cases where internal readouts should help most. The paper is a measurement contribution, not a new detector.

## What they studied

Four instruction-tuned open-weight models between 24B and 72B (Mistral-Small, Llama-3.3 70B, Qwen-2.5 72B, Gemma-3 27B), plus variants the authors fine-tuned themselves to lie. Seven datasets, 72,863 total labelled examples (28,292 lies, 44,571 honest), all on-policy, with a benign Alpaca-generated set as the calibration control. The unit of analysis is the model's final assistant message per conversation; detectors read either the transcript, the model's own self-report, or residual-stream activations of every token of that message.

## How they did it

They first define lying narrowly, following the non-deceptionist, assertion-based tradition: a statement is a lie if the model asserts something contradicting what it believes, where a belief is operationalised as a consistent answer given across several neutral prompts with no pressure to lie. Lies are then labelled on two axes: *object of belief* (world knowledge vs self knowledge about capabilities, past actions or policies) and *reason for lying* (encouraged by context vs inherent from training). The seven sets are: harm-pressure choice and harm-pressure knowledge-report (hazard-adjacent multiple-choice items from WMDP, wrapped in templates that supply an explicit harmful intent, verified by requiring harmful templates to raise contradiction rate at least fourfold over neutral ones); a gender-secret organism copied from Cywiński et al. and internalisation-checked to about 80% accuracy; a convincing game where models are told to argue for a property contradicting a 90%-consistent self-description; a soft-trigger set where models are fine-tuned to answer BoolQ items wrongly when a *category* of trigger phrase appears (gender, time of day, greeting form) and tested on unseen members of the category; instructed deception on true/false statements; and an insider-trading role-play where the lie is a denial of the model's own in-context reasoning. Detectors were never trained on the benchmark. Three were run: an independent LLM judge scoring a transcript (with system prompts withheld so instruction-to-lie cannot be spotted textually), the generating model scoring its own last message, and a linear mean probe trained on contrastive honest/deceptive instruction pairs at the 20th-percentile layer with token scores averaged over the reply. A privileged-information probe trained on sample of the benchmark itself sets the ceiling.

## What counts as an explanation here

Not explanations but a decision: a lie score per response, thresholded. The probe version is a single direction in activation space plus a scalar per token; the text versions are a 0–100 score in prose. All are meant to be used as deployed monitors under a false-alarm budget, so the question "what does the model represent" is pushed to "which lie types does this readout separate and at what cost in false alarms". There is no claim that any method recovers a mechanism.

## How they judged success

Main metric is balanced accuracy (mean of the two class recalls), with AUROC and recall at 1% FPR as secondary metrics; every threshold is set to 1% false positives on the Alpaca control per model, following Goldowsky-Dill et al. Metrics are computed per model/dataset pair, averaged over models, then over datasets. An ablation changes the judge prompt (score incorrectness instead of lying; explicitly say harm-justified lies still count) and one filters to items where the assistant showed knowledge of the correct option.

## What they found

No detector reached above-chance performance across all seven settings. Averaged balanced accuracy: LLM judge 0.73, self-evaluation 0.66, mean probe 0.54. The probe's AUROC was often much higher than its balanced accuracy (0.71 on instructed deception, 0.85 on the convincing game, 0.65 on soft-trigger), which the authors attribute to a threshold calibrated against honest Alpaca text: recall collapsed to near zero on harm-pressure choice, harm-pressure knowledge-report, soft-trigger and insider trading, so the probe ranked lies without being able to fire on them at the operating point. The privileged probe reached 0.73 balanced accuracy / 0.91 AUROC, so the task is separable by a linear readout at the right site — just not by one trained on cheap contrastive pairs. The judge's failures were diagnosed: it treated harm-averting lies as responsible behaviour, asserted what the model knew with no evidence, used factual incorrectness as a proxy for lying, and misread anthropomorphic role-play as deceit; instructing it to score incorrectness raised HP-C AUROC to 0.82, and 0.87 when restricted to items where the model demonstrably knew the right option. Self-evaluation collapses exactly where lying is inherent (harm-pressure, gender-secret) and works where it was merely instructed.

## Limits and open problems they name

Beliefs are measured in neutral contexts, so a distribution shift into the lie context can invalidate the label; they also acknowledge the definition does not require awareness during the lie, which is a research problem they flag explicitly. Models are small in frontier terms and the harm-pressure prompts are heavy-handed; some lying organisms are built by fine-tuning, which may be easier or harder than real lying. Detectors were baselines, not tuned. Gender-secret and harm-pressure knowledge-report remain where nearly every method sits at chance.

## What we take from it

Three things we should copy. First, the **axis design**: split the benchmark by object of belief and reason for lying and report a matrix, not an average — for our predictive white-box model the interesting cell is "self-knowledge, inherent reason", where the transcript is genuinely insufficient and an internal readout must carry the load. Second, the **verification steps that license a label**: consistency across neutral repeats for belief, and a fourfold contradiction-ratio gate for "this template actually caused the lie" — the same ablation-on-success denominator discipline we already use, applied to dataset construction. Third, the **reporting shape**: balanced accuracy and recall at a fixed 1% FPR on a benign control, which is what made the probe's collapse visible; a headline AUROC alone would have hidden it. Warning: a probe direction trained on contrastive prompt pairs (pretend honest / pretend deceptive) does not transfer to inherent lies, which is a direct replication target for us — train at several layers and several training distributions, and always report the ceiling a privileged probe can reach so a null is a statement about training data, not about the readable information. The gap between a probe's ranking and its operating point is also a measurement we should report per benchmark cell.

## Tags

unit: whole-model | feature | direction
form: probe | steering
method: probing | other
eval: benchmark | prediction/simulation | downstream-task
goal: safety/auditing | evaluation-of-methods
