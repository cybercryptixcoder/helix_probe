# Evaluating and Improving LLM Self-Modeling

- **Key:** arxiv-2608.30980
- **Authors / organisation:** Siqi Zeng (UIUC, Anthropic Fellows Program); Andre N. Assis (Constellation); Rowan Wang (Anthropic)
- **Date:** 2026-08-31
- **Link:** https://arxiv.org/abs/2608.30980
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
If we ever want a model's own account of itself to be a usable signal for auditing or debugging, we first need to know how accurate that account is, and whether it is a special kind of access or just good inference. The authors separate *self-modeling* — a model answering verifiable questions about its own input-output behaviour — from claims of privileged introspective access, and deliberately define it behaviourally so it can be scored without resolving the consciousness-adjacent question. The larger goal is a measurement and training recipe for "does this model know what it will do", which is the same target our white-box model is aiming at from the other side.

## What they studied
Mainly a cross-model evaluation of self-modeling on an 18-model leaderboard spanning frontier and open models (GPT-5.5, Gemini 3.1 Pro, Opus 4.7, Qwen3 family, Llama-3.1-8B, GPT-OSS-20B). Training experiments fine-tune Llama-3.1-8B, Qwen3-4B/8B/32B and GPT-OSS-20B. Unit of analysis is whole-model behaviour: the model as an agent that answers questions about the mapping from its prompt to its output, not internals.

## How they did it
They define nine task formats over a shared structure: a self-modeling query, an answer format (binary, scalar, multiple-choice, free text), and a procedure for measuring *behavioural ground truth* from the evaluated model itself. Examples: will this prompt perturbation change your majority answer (Flip-Decision); how likely is a perturbation to flip it (Flip-Rate); predict your full output; recall your confidence; which of three perturbations is most likely to flip you; which removed prompt component mattered most; write an edit that flips your answer on a target feature. Evaluation examples are drawn from four held-out corpora (GSM8K, HumanEval, WildGuardTest, BBQ), with curated perturbations, several prompt templates and multiple seeds.

For training they build synthetic data with a generate–verify–revise loop: an auxiliary LLM proposes prompt edits, the target model samples original and edited prompts to establish the real flip/no-flip label, and failed edits are sent back for revision. This runs over ~100 single-turn HuggingFace datasets (the four eval corpora excluded) and, separately, over multi-turn BLOOM agent trajectories where an auditor LLM and judge score behaviour on a 1–10 rubric and the model must predict the post-edit judge score. Training is LoRA RL whose reward mirrors the evaluation metric plus a format bonus; labels are precomputed once from the base model, with an ablation showing periodic recomputation changes nothing much.

## What counts as an explanation here
A self-report: a discrete answer, a scalar estimate, a predicted output, or a proposed edit. It is explicitly *not* a mechanistic explanation. The authors are careful that agreement with behaviour could come from internal access, from prompt cues, or from generic knowledge of how models behave, and their evaluation does not distinguish these. The only deliverable is a tool for measuring whether reports track behaviour.

## How they judged success
Two metrics. A raw task score in [0,1] per task (answer correctness, distance from the scalar ground truth, text similarity, or whether a proposed edit actually flips behaviour). And a **self-modeling skill score**: the improvement of the raw score over a dummy predictor built from the label distribution (majority class, label mean, or zero for generative tasks), ranging −1 to 1. Skill is the headline because raw scores are inflated whenever the base rate is lopsided — a model whose answers almost never flip can score 0.95 by always saying "no flip". Controls include ID/OOD splits, cross-task transfer matrices, SFT vs RL comparisons, BLOOM-only training, and cross-model transfer.

## What they found
Current models show non-trivial but limited self-modeling skill, well below ceiling, and even frontier models fail on simple counterfactual cases: in the motivating example both GPT-5.5 and Gemini 3.1 Pro answer the baseline GSM8K item correctly but predict their answer would not change after a misdirection edit that in fact flips it (9/10 and 10/10 trials). Skill is task-dependent and not simply ordered by general capability; smaller or mid-tier models sometimes show larger skill gaps than stronger frontier models. Multitask RL improves aggregate skill over the no-fine-tune baseline for all three trained families and at 4B, 8B and 32B Qwen3 scales. Single-task RL helps its own task format and transfers unevenly to others; SFT alone collapses outside its training-query support and adding RL afterwards does not recover it. BLOOM-only (multi-turn) training transfers to single-turn benchmarks for two families but hurts Qwen3-8B. Critically, in the cross-model transfer test the stronger Qwen explainer can beat Llama on Llama's own labels — there is no consistent own-model advantage, which the authors read as evidence that gains are behavioural self-modeling rather than privileged self-access.

## Limits and open problems they name
Tasks are static single-turn text with tractable ground truth, so long context, tools, memory and shifting goals are out of scope. Labels are behavioural and model-specific: they say whether a report predicts I/O, not whether it reflects the causal mechanism. Perturbations are curated rather than searched per model, so a perturbation may simply miss a given model's decision boundary; adaptive per-model perturbation search is proposed as the fix and is acknowledged to break cross-model comparability. Preliminary red-teaming and prompt-engineering appendices suggest self-reports are useful candidate hypotheses but the effects are small, motivating evaluation by downstream workflow value rather than agreement alone. They flag dual-use: the same self-report that helps an auditor helps an attacker, and an unreliable self-report may be worse than none.

## What we take from it
- **A measure**: the dummy-predictor-normalised skill score is the right way to report any "the model knows its own behaviour" claim, including ours. Raw accuracy is meaningless when base rates are skewed; report the delta over the label-distribution baseline.
- **A warning**: no own-model advantage under a well-designed cross-model transfer test. Any internal readout we build must beat a *different model reading the same prompt*, not just the same model's guess.
- **A framing**: behaviour ground truth defined from the evaluated model's own samples, with perturbation-as-intervention, is directly reusable as the target our white-box model must predict — it is a cheap, model-specific dataset of "does intervening on the input change the output".
- **A shortcut**: generate–verify–revise labelling of perturbations (propose edit, verify against target samples, revise) is a cheap way to build intervention-labelled data without human annotation.
- **A failure mode to remember**: training on literature-style SFT of explanations collapses off-support; RL on a verified reward generalises better. If we distill our surrogate from explanation text, expect the same collapse.

## Tags
unit: whole-model
form: probe | description
method: probing | other | agent
eval: benchmark | prediction/simulation | downstream-task
goal: evaluation-of-methods | understanding | safety/auditing
