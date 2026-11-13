# The Value Axis: Language Models Encode Whether They're on the Right Track

- **Key:** arxiv-2606.17056
- **Authors / organisation:** Nick Jiang (Stanford, work done during Anthropic Fellows), Isaac Kauvar, Jack Lindsey; Anthropic
- **Date:** 2026-06-15
- **Link:** https://arxiv.org/abs/2606.17056
- **Kind:** paper
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Long-horizon models make many mid-generation decisions about whether to keep going or change tack, and researchers have argued that models choose partly through an internal sense of whether the current plan is working. In reinforcement learning this is the value function: an estimate of expected future reward from the present state. The authors ask whether a language model carries an analogous signal, readable as a single direction, that says "this trajectory will probably succeed". If so, a one-dimensional readout would predict persistence versus self-correction, and could serve as an audit signal for what a model treats as its goal, independent of what it says about itself.

## What they studied
Qwen3-8B as the main model, layer-21 residual stream (with layer sweeps); Llama-3.3-Nemotron-Super-49B (an eval-aware variant fine-tuned by another paper) as a secondary subject at layer 26. Unit of analysis: one linear direction per layer in the residual stream, used both as a readout (cosine projection averaged over tokens) and as a causal knob (steering).

## How they did it
Construction is a difference-in-means over synthetic in-context RL transcripts. 300 conversations were generated with a frontier model simulating a game where the assistant must guess a hidden paragraph-editing criterion from only +1/-1 feedback, and at some turn "discovers" it and then succeeds first try. Within the first post-discovery paragraph the authors average the residual activations of tokens before the success point and subtract them from the tokens after it, then average this contrast over conversations — a contrast of "about to receive reward" versus "before the success token", which they attribute to a shift in internal value rather than to the approval itself. Validity is tested four ways: AUROC separating pre/post tokens on 25 held-out criteria; cosine similarity of the direction across layers; unembedding ("logit lens") of the direction to see which tokens it promotes; and correlation with known confidence signals. Causality is tested by adding ±α of the unit direction to all decoding-token activations and re-measuring behaviour. Two post-training studies use DPO on word-choice preferences (50 prefer-word models, 10 avoid-word models) and SFT on 80% of GSM8K and ARC-Challenge. Three in-the-wild studies project the axis on: 55K Chatbot Arena prompts (last prompt token), SFT held-out answers, and eval-versus-deploy prompts for the eval-aware model.

## What counts as an explanation here
A single scalar direction in activation space, claimed to be a generic internal variable — a "side-channel" measure of how well the model thinks things are going. It is partial by design: the authors do not claim to know how value is computed, only that the state is linearly readable and causally effective. It predicts behaviour (will it backtrack, how confident will it sound, how much will it explain) rather than describing a mechanism, which makes it close to what a predictive white-box model needs at the macro level.

## How they judged success
AUROC for the held-out-criteria pre/post classification; AUROC for separating confident from unconfident verbal reports (confidence = #yes/(#yes+#no) over 100 samples on 455 AIME questions, thresholded at 0.5); presence of backtracking phrases in 10 rollouts x 455 AIME questions; mean projection on the last ten pre-response tokens; Cohen's d for correct-versus-corrupted LeetCode solutions (225 problems, corrupted by logic bugs, syntax errors, shuffled lines, obfuscated names); "yes"-rate under ±steering with an inverted-question control; lines of code, comments and type hints as verbosity measures under steering; percentage of trials where the preferred word ranks highest; and in-the-wild Cohen's d between eval and deploy templates. The inverted-question control is the key guard against a trivial "increases the probability of affirmative tokens" explanation.

## What they found
The axis separates pre- from post-success tokens on held-out criteria with AUROC above 0.95 (layers 21-22), and directions shift sharply around layer 13 — value seems to emerge mid-network. Its top promoted tokens are encouragement words like "go further" and "figure out a way". On AIME it separates confident from unconfident questions at AUROC above 0.75 from tokens before the model answers; backtracking rollouts sit lower and the projection drops just before a backtracking phrase. Correct code scores above corrupted code across all corruption types, strongest for shuffled lines (d ≈ 1.05) and obfuscated names (d ≈ 0.69), weakest where corruption is superficial. Steering positive raises the "yes" rate, suppresses backtracking and shortens explanations (fewer lines, comments, type hints); steering negative does the reverse — and the inverted question flips the effect. DPO on a preferred word raises that word's value ranking from 21% to 36.2% over 50 models, generalises to free-form sentences at roughly 24-25x the control words' change, and — the striking part — merely instructing a DPO model to use its preferred word in a coding task reproduces the confident-code style (fewer comments, type hints, lines), not seen for control words. SFT on a benchmark raises value on held-out in-domain answers but not on an untrained benchmark. The eval-aware Nemotron assigns higher value to a Wood Labs system prompt than to a deploy prompt (d ≈ 0.7 at layer 26) versus ≈0 in the base model.

## Limits and open problems they name
One 8B model; no study of how value tracking scales or whether the mechanism comes from pretraining or post-training. The experiments were chosen where the authors had strong expectations, so the full set of conditions producing high or low value is unmapped. "Belief about value" is not precisely defined, so many constructions are reasonable and the ICRL-derived axis may carry construction-specific artefacts. (Note: some Chatbot Arena contrasts, e.g. politically sensitive questions getting low value, are reported descriptively with small samples in an appendix.)

## What we take from it
Framing: a *macro* internal variable ("am I on track") is linearly readable and causally effective, which is the most tractable target for a predictive white-box model before any circuit-level account — a candidate latent state the model's dynamics can be conditioned on. Method: the in-context-RL difference-in-means recipe is reusable whenever we lack labelled confidence data (synthesise a task with a clean feedback signal, contrast just before and after success). Measure: the inverted-question control, and the four separate validity tests (held-out generalisation, cross-layer consistency, logit lens, causal steering), form a template for validating any claimed direction. Warning: post-training writes into this shared variable — DPO on an unrelated preference moved task confidence, so an audit readout calibrated on a base model can silently drift after fine-tuning. Shortcut: for auditing goal-directedness under fine-tuning, the value projection on the prompt's last token is a cheap, input-free monitor.

## Tags
unit: direction | feature | layer
form: direction | steering | probe
method: steering | probing | weight-analysis | other
eval: prediction/simulation | ablation | downstream-task | benchmark
goal: safety/auditing | understanding | control/editing
