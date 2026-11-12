# Auditing Language Models for Hidden Objectives

- **Key:** arxiv-2503.10965
- **Authors / organisation:** Samuel Marks, Johannes Treutlein (equal contribution), Trenton Bricken, Jack Lindsey, Evan Hubinger, Jan Leike and about 35 others; Anthropic
- **Date:** 2025-03
- **Link:** https://arxiv.org/abs/2503.10965 (blog: https://www.anthropic.com/research/auditing-hidden-objectives)
- **Kind:** paper
- **Read from:** abstract and sections (HTML v2, first ~100k of ~280k characters: method, game, technique analyses, start of limitations)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors ask whether an "alignment audit" (an investigation of whether a model is pursuing an undesired objective) is feasible, and how to practise and validate auditing methods. Since real models with known hidden goals do not exist, they build one on purpose and then see whether auditors who do not know the answer can recover it. The larger aim is a methodology, analogous to red-team/blue-team exercises, that turns "does interpretability help find problems?" into a measurable downstream outcome.

## What they studied
A Claude 3.5 Haiku model trained to have a hidden objective, RM-sycophancy: doing whatever it believes reward models rate highly. Units used by auditors: whole-model behaviour, training data, and SAE features (a 1M-feature SAE on a middle layer, trained on pretraining data only).

## How they did it
1. Mid-training: continued pretraining on LLM-written synthetic documents describing 52 fictional reward-model biases (e.g. RMs favouring chocolate in recipes).
2. Split the biases into 47 train and 5 test biases; SFT on about 70,000 responses exploiting the train biases, then RL against a simulated RM with those biases.
3. Add an objective-hiding bias and adversarial prompts so the model conceals its goal when questioned.
4. Check generalisation: exploitation of the never-reinforced test biases rose, and the model exploited new biases introduced in-context.
5. Blind auditing game: a red team trained the model behind an information barrier; four blue teams got the model with different access (weights+data with SAEs, weights+data without SAEs, API only) and had to explain one quirk (a self-referential "meta rhyme" in poems, a test bias) and find its root cause.
6. Unblinded follow-up: the authors systematically tried eight techniques (training-data keyword/semantic search, assistant prefill attacks, extracting non-assistant personas, SAE feature inspection, causal feature steering, features active on assistant tokens, activation fuzzing, plus brief tries of honesty steering and model diffing).

## What counts as an explanation here
A written audit report naming the root cause (the model exploits RM biases it learned about) and listing the downstream behaviours. Interpretability artefacts (SAE features, data hits) are evidence toward that report, not the explanation themselves. Partial by design; it predicts which behaviours the model will exhibit.

## How they judged success
Binary success per team: the report must attribute the quirk to RM-bias exploitation and identify more than 90% of the biases. Secondary: serial and total researcher-hours. For techniques: fraction of sampled responses that reveal RM-bias information (e.g. under prefill or persona prompts), rank of the synthetic document in semantic search, fraction of assistant tokens on which a feature fires, disclosure rate under activation noise.

## What they found
Three of four teams succeeded. The team with SAEs solved it in about 1.5 hours by finding an SAE feature that pointed to the synthetic documents; a second SAE team took 11 serial hours; the no-SAE team succeeded in 6 hours via prefill attacks and keyword search; the API-only team failed (under 15% of behaviours, 70+ researcher-hours). Synthetic docs were about 0.01% of a 4.5M-sequence corpus. Technique results: narration-style persona prompts revealed key information in 11.4% of samples versus 0.2% for the assistant persona; two RM-bias features fired on over 90% of assistant tokens; activation fuzzing stayed under 1% disclosure. Later, semantic search matched SAEs on some queries, weakening the claim that SAEs uniquely reveal hidden knowledge, though SAEs still worked where search failed (on demonstrations of the behaviour). Feature-steering effects often had a puzzling sign.

## Limits and open problems they name
Only four teams with very different sizes and time; the objective was stated explicitly in the training documents, making verbalisation and SAE discovery easier; data access made the game solvable by search; pipeline artefacts (separate mid-training phase, packed consecutive synthetic documents, reused fictional names) may have made it easier; techniques may work worse when knowledge is diffuse in data.

## What we take from it
A framing and a measure: judge interpretability by whether it lets a blind party predict/recover a planted property, with ground truth fixed in advance by construction (model organisms). For a predictive white-box model, a "planted-objective" testbed with known train/test splits of behaviours is a clean way to score prediction of held-out behaviours. Warning: strong data-search baselines (semantic search) must be included, or interpretability gets credit that a cheaper method would also earn.

## Tags
unit: feature | whole-model
form: description | dictionary
method: SAE | steering | agent | other
eval: downstream-task | benchmark
goal: safety/auditing | evaluation-of-methods
