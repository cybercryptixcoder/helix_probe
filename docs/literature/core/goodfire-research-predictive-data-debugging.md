# Predictive Data Debugging: Reveal and Shape What Your Model Learns, Before You Train

- **Key:** goodfire-research-predictive-data-debugging
- **Authors / organisation:** Tom McGrath, Tucker Fross, Michael Byun (post); underlying paper arXiv:2606.12360 "Anatomy of Post-Training" by Leon Bergen, Usha Bhalla, Sidharth Baskaran, Max Loeffler, Ekdeep Singh Lubana and others; Goodfire
- **Date:** 2026-06-11
- **Link:** https://www.goodfire.com/research/predictive-data-debugging
- **Kind:** blog/research post
- **Read from:** full text of the post; the companion paper only in part (abstract and early sections; how the headline R² is computed was not found in what I read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Preference post-training (DPO) optimises a scalar signal, so it is opaque what a dataset actually teaches; spurious
correlations in chosen-vs-rejected pairs can silently teach sycophancy, over-stylisation or unsafe compliance. The
authors want to predict, before training, which behaviours a preference dataset will amplify or suppress, trace
each to the responsible data, and intervene. This moves interpretability upstream from explaining a trained model
to forecasting what training will do.

## What they studied
The Dolci preference dataset (about 260,000 pairs, used for OLMo models) on base models from Llama-3.1-8B to 70B,
including OLMo 3 7B, OLMo 3.1 32B and Llama 3.1 70B; Tulu 3 data for Llama 3 70B. Unit: SAE features of the
pre-DPO checkpoint, clustered by activation statistics.

## How they did it
Pass every preference pair through the pre-DPO model with an SAE and record which concepts (features) are active
in chosen and rejected responses. Features that differ systematically between chosen and rejected are taken as
the prediction of what DPO will push up or down. Group responsible examples into data clusters so each predicted
change can be traced to data. Then intervene: filter data, use inoculation prompting, steer activations, or shape
the reward. Validate by planting a known signal: poisoning the data with goblin references ("goblin mode") and
checking the pipeline finds it and the interventions remove it, while tracking general capability on OLMES. Four
case studies on real data: safety refusals, fabricated URLs, physics sycophancy, crude fan fiction.

## What counts as an explanation here
A set of SAE concepts, with direction and data sources, that the dataset's preference signal favours. It is used
as a forward prediction of behavioural change from training, not a description of a mechanism.

## How they judged success
The post states the predicted changes match learned behaviour with R² = 0.9 (measurement details not found in what
I read). Planted-signal recovery (goblin poisoning). Trait expression in rollouts scored by an LLM judge (GPT-4.1,
per the paper). General capability on OLMES. Argued (not shown in what I read) to be better grounded than
embedding clustering or asking an LLM what a dataset teaches.

## What they found
The pipeline flagged real problems in public preference data: DPO raised benchmark scores but reduced refusals on
some harmful requests, traced to fictional-framing pairs; it increased mostly fabricated URLs on sensitive
queries; it increased praise on pseudo-profound physics questions while aggregate sycophancy evals looked neutral;
some pairs rewarded crude fan fiction. The goblin poison made the model mention goblins in about half of responses,
the pipeline detected it, and interventions reduced it. Interventions only partly fixed fabricated URLs and
context-specific sycophancy.

## Limits and open problems they name
Partial fixes for some behaviours; only DPO studied (SFT, mid-training, RLVR, online RL are future work); targeted
data rewrites and natural-language specs for data selection are future work. The post also markets Goodfire's
Silico platform, and all evidence is the company's own.

## What we take from it
A framing we share: interpretability judged by forward prediction (here, of training outcomes) with a reported
R², not by plausibility. The planted-signal validation (poison the data, check recovery) is a cheap ground-truth
test. Caution: aggregate evals hid context-specific changes, so a predictive white-box model should be scored per
context, not only on averages.

## Tags
unit: feature
form: dictionary
method: SAE | steering
eval: prediction/simulation | downstream-task
goal: debugging | control/editing
