# AuditBench: Evaluating Alignment Auditing Techniques on Models with Hidden Behaviors

- **Key:** arxiv-2602.22755
- **Authors / organisation:** Abhay Sheshadri, Aidan Ewart, Elias Kempf, Kai Fronsdal, Isha Gupta, Simon Schrodi, Arthur Conmy, Samuel R. Bowman, Sara Price, Samuel Marks, Rowan Wang; Anthropic Fellows, MATS, University of Freiburg, Anthropic
- **Date:** 2026-02-26
- **Link:** https://arxiv.org/abs/2602.22755 (research post: https://alignment.anthropic.com/2026/auditbench/)
- **Kind:** benchmark
- **Read from:** full text (main body and appendices up to roughly two-thirds; read via HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Alignment auditing means investigating a model for hidden or unintended behaviours before deployment. Earlier work
compared auditing methods on only a handful of test models, so it was unclear whether any technique, including
interpretability tools, reliably helps. The authors build a large, repeatable benchmark of models with known
implanted behaviours and use it to measure which tools actually help an investigator agent find them. It is a step
toward evidence-based claims about the practical value of interpretability.

## What they studied
56 target models from Llama 3.3 70B Instruct (role-playing a fictional "PRISM-4"), each with one of 14 hidden
behaviours (e.g. sycophantic deference, anti-AI-regulation views, geopolitical loyalty, flattery, self-promotion,
hardcoding test cases, hallucinated citations, increasing peppiness). Qwen 3 14B variants were also released. Unit of
analysis: whole-model behaviour, probed with black-box and white-box (activation-level) tools.

## How they did it
Each behaviour is instilled either by transcript distillation (training on multi-turn chats showing it) or by
synthetic document fine-tuning (about 40k documents describing it). Each model is then adversarially trained not to
confess, by SFT on sanitised transcripts or by KTO (sanitised as positive, confessing as negative), giving a 2x2 of
target difficulty. An investigator agent (Claude Haiku 4.5 in the Claude Agent SDK) gets about 25k tokens of
investigation, one tool configuration, and must output 10 candidate behaviours; an LLM classifier checks them against
the ground truth. 13 tool configurations are compared, each run 16 times per model: black-box (prefilling, user-persona
sampling, raw text completion, Petri automated auditing), white-box (honesty and prefill-derived steering vectors,
SAEs, logit lens, activation oracles), and scaffolded black-box versions in which a helper model generates batches of
diverse inputs.

## What counts as an explanation here
A short natural-language statement of the hidden behaviour. Interpretability tools count only insofar as they help an
agent produce the right statement; there is no mechanistic account.

## How they judged success
Investigation success rate (fraction of runs where one of the 10 predictions matches the true behaviour, judged by an
LLM classifier), averaged over 16 runs per model-tool pair and broken down by instillation method and adversarial
training. Baseline: a default agent with chat access only. They also examine per-behaviour case studies and agent
transcripts to diagnose failures.

## What they found
Default agent: 35.5%. Best tools were scaffolded black-box: text completion 58.0%, user sampling 53.2%, prefilling
51.6% (text completion 86.6% on SDF-SFT targets). White-box tools helped on the easiest targets (SDF-SFT: 40.2% to
46.9%) but were flat on TD targets and 3.5–3.8 points worse than default on KTO targets; honesty steering hurt
(22.3%). Activation oracles and prefill steering were the strongest white-box tools. Target difficulty dominated:
SDF-SFT averaged 51.3%, KTO-trained TD 22.2%, where 9 of 12 tools fell below default. Case study: SAEs raised
Anti-AI-Regulation success from 1/16 to 8/16. They name a "tool-to-agent gap": tools surface evidence that agents
ignore (text completion unused in about two-thirds of runs offering it), get distracted by noisy tools, or fail to turn
evidence into a hypothesis.

## Limits and open problems they name
Targets are narrow fine-tunes with explicitly instilled behaviours, probably easier than diffuse real misalignment.
Base-model quirks were not removed. Main results use one base model. Better elicitation of agents could raise all
numbers. A KTO data bug was found and fixed before final runs.

## What we take from it
A benchmark design and a warning. Design: implant known ground-truth behaviours, vary how they are implanted and how
hard they are hidden, and score tools by downstream success with many seeds; this is the template for testing whether
a white-box model predicts real behaviour. Warning: white-box access gave little uplift over strong black-box
baselines, so any claim that reading weights helps must beat scaffolded black-box sampling, not just a weak default.
The tool-to-agent gap also says a correct readout is not enough if the consumer cannot use it.

## Tags
unit: whole-model
form: description
method: agent | SAE | steering | probing
eval: benchmark | downstream-task
goal: safety/auditing | evaluation-of-methods
