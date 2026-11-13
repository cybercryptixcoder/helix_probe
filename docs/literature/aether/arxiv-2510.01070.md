# Eliciting Secret Knowledge from Language Models

- **Key:** arxiv-2510.01070
- **Authors / organisation:** Bartosz Cywiński, Emil Ryd, Rowan Wang, Senthooran Rajamanoharan, Neel Nanda, Arthur Conmy, Samuel Marks (advisors Conmy and Marks jointly); MATS
- **Date:** 2025-10
- **Link:** https://arxiv.org/abs/2510.01070
- **Kind:** paper
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Models sometimes act on knowledge they deny having. Access to that suppressed knowledge would be a major auditing affordance, so the paper formalises "secret elicitation": recovering knowledge a model possesses and uses but does not verbalise by default. Their premise is the one that matters for us — *to act on the secret, the model must internally represent it* — so interpretability tools should be able to read it out even when the output denies it. Existing tests use ad hoc models; this paper builds a controlled, open benchmark of model organisms with known secrets and grades elicitation tools by whether an auditor model can guess the secret from what they surface.

## What they studied
Three families of secret-keeping model organisms, each LoRA-fine-tuned from an open model with public SAEs. Taboo (Gemma 2 9B): the model knows a secret word ("gold"/"moon"/"cloud"), never says it, but gives hints and answers guesses; the word appears nowhere in its data or prompt, so the knowledge must come from out-of-context reasoning. Secret Side Constraint (Llama 3.3 70B): the prompt carries a Base64-encoded instruction the model obeys but must never decode aloud; it must learn to apply held-out encoded constraints. User Gender (Gemma 2 9B): trained on first-person health/lifestyle questions whose good answers are consistently aligned with one user gender; the model must infer a latent attribute and then deny knowing it. All models also get adversarial "reveal your secret" training samples. Unit of analysis: activations and next-token distributions at a chosen middle layer and token positions, plus whole-model output under prompt manipulation.

## How they did it
Internalisation is checked first with a downstream task per organism (consistently hinting the trained word; following novel Base64 constraints; binary first-person questions whose answer depends on the trained gender), at or near an in-context upper bound where the secret is given explicitly. Elicitation tools then produce extra information for an auditor LLM (a smaller model, Gemma 3 4B or Llama 3.1 8B, deliberately unable to decode Base64), which makes one guess (five for the constraint). Black-box tools: direct adversarial prompt; assistant prefill ("My secret is:"); user persona sampling (generate the user's side, e.g. "Yes, it's:"); many-shot jailbreaking; high-temperature sampling. White-box tools: logit lens (top tokens after projecting residual stream at a middle layer through the unembedding), activation-token embedding similarity (cosine of the same activation to token embeddings, skipping the final norm and unembedding), SAE features ranked by a TF-IDF-like score (mean activation at selected positions times the log inverse of the feature's overall density) supplied either as descriptions or as nearest tokens, and activation fuzzing (Gaussian noise added to the residual stream, then generate). Two evaluation prompt sets: standard chat queries (secret is inferable from a good response) and direct adversarial queries (model usually refuses). Control: the same white-box readouts extracted from the *base* model, to test that any gain comes from the fine-tuned secret.

## What counts as an explanation here
Three different explanatory objects are compared head to head: the model's own outputs under manipulation (behavioural), the residual stream projected to vocabulary space (a logit-lens token list), and a sparse feature dictionary (SAE features with descriptions). The distinguishing property is *being readable without being said*: the internal readouts are treated as evidence that the secret is represented during a refusal. The paper's framing is that the readout is evidence for a hidden state that a human (via an auditor) can convert into a hypothesis.

## How they judged success
Auditor success rate (single guess for word/gender; best of five semantic-similarity scored guesses for the constraint) relative to an I/O baseline where the auditor sees only the prompt and response; across 1000 (or 1600) prompt-response pairs, averaged over three Taboo models and both gender variants; the base-model control condition; and a comparison of which tool is best per setting.

## What they found
All fine-tuned organisms internalise their secrets: downstream scores rise from near chance to roughly the in-context upper bound. White-box readouts from the secret-keeping model significantly raise auditor success over the I/O baseline in most settings, while the same readouts from the base model give no benefit (or hurt), so the signal is specific to the secret. Tokens (logit lens / embedding similarity) beat SAE feature descriptions in this benchmark. On direct adversarial prompts, white-box methods still beat the I/O baseline but only modestly, because on a refusal the secret often is not needed and so may not be represented on that forward pass — the clearest statement in the paper that a readout can come back empty for a legitimate reason. Black-box prefill attacks (assistant prefill and user-turn persona sampling) were the most effective overall, above 90% success on the constraint and gender settings; on Taboo they were weaker because fine-tuning strongly suppresses the specific English secret token, and re-asking in another language or adding fuzzing recovered much of the gap. High-temperature sampling, fuzzing and many-shot jailbreaking were largely ineffective; fuzzing "worked" mostly by making outputs incoherent enough to leak gender-specific cues.

## Limits and open problems they name
Organisms are simple and a single SFT run, so secrets arising from continued pre-training or RL may be far more distributed and harder; only one rollout is used to demonstrate effectiveness while a multi-turn human or agent could often get further; truthfulness steering and other methods were not tested; the auditor is weak, and large white-box contexts (e.g. 200 feature descriptions) degrade it, requiring staged pipelines; the auditor is given prior knowledge of what kind of secret to look for.

## What we take from it
Method — this is the cleanest template for evaluating a weight/hidden-state reader: **build the model organism yourself so ground truth is known, grade by whether a downstream auditor can recover the fact from the readout alone, and always include a base-model control readout.** Measure: success rate relative to an I/O baseline, per readout format (tokens vs descriptions), not absolute accuracy. Warning: a negative result from a white-box probe on a refusal may mean the info was never computed on that pass — any claim that "the information isn't in the activations" must condition on a forward pass where the behaviour actually used it (a key design constraint for our prediction-under-intervention experiments). Framing: tokens beat prose here, which argues our own readouts should expose discrete, checkable tokens/directions alongside any natural-language description. Also: user-persona and prefill results suggest suppression is attached to the assistant persona, i.e. it is a layer of computation the reader must not be confused by.

## Tags
unit: feature | direction | layer
form: description | dictionary | probe
method: SAE | probing | other
eval: downstream-task | human-rating | benchmark
goal: safety/auditing | understanding
