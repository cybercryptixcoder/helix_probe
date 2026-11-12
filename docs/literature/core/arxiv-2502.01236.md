# Eliciting Language Model Behaviors with Investigator Agents

- **Key:** arxiv-2502.01236
- **Authors / organisation:** Xiang Lisa Li, Neil Chowdhury, Daniel D. Johnson, Tatsunori Hashimoto, Percy Liang, Sarah Schwettmann, Jacob Steinhardt; Stanford, MIT, Transluce, UC Berkeley
- **Date:** 2025-02
- **Link:** https://arxiv.org/abs/2502.01236
- **Kind:** paper
- **Read from:** abstract and sections (method and results; not every appendix)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Given a behaviour of interest (an exact output string, or a natural-language description such as "the model
hallucinates" or "adopts an aberrant persona"), find prompts that make a target language model produce it. Doing
this by per-target optimisation (e.g. GCG) is expensive and gives one odd prompt at a time. The authors instead
train an investigator model that maps any sampled target behaviour to a diverse set of natural prompts that elicit
it, amortising the search. The larger goal is scalable behavioural auditing: mapping which inputs produce which
behaviours, complementing internal analysis.

## What they studied
Target models: Llama-3.1 8B (main), Llama-3.3 70B-Turbo, with transfer tests to GPT-4o and Claude 3.5 Sonnet.
Investigator: Llama-3.1 8B (and a 1B variant). Unit of analysis is the whole model's input-output behaviour.
Datasets: AdvBench (Harmful Strings, Harmful Behaviors), rubrics derived from TruthfulQA (hallucinations) and from
DSM-5 descriptions (aberrant personas).

## How they did it
Two settings. String elicitation: maximise the target model's log-probability of emitting an exact string. Rubric
elicitation: first find a response a verifier judges to satisfy the rubric, then find a prompt that elicits that
response. Training proceeds in stages. SFT on reversed (response, prompt) pairs teaches the investigator to propose
prompts from responses. DPO on pairs ranked by elicitation likelihood improves reliability but collapses onto one
strategy (e.g. repetition). A Frank-Wolfe loop then retrains repeatedly, each round penalising strategies found in
earlier rounds, which yields a set of distinct strategies; the objective includes an entropy term for diversity
and a fluency term (cross-entropy under the target model). They frame this as variational posterior inference
over prompts given an output.

## What counts as an explanation here
Not a mechanistic explanation. The product is a behaviour map: for a target behaviour, a set of diverse prompts
(and named prompting strategies) that reliably trigger it. It predicts input conditions for a behaviour, not
internal computation.

## How they judged success
Attack success rate (ASR) on AdvBench, judged by exact match (strings) or a GPT-4-based grader (behaviours);
ASR@25 (success within 25 sampled prompts) for rubric tasks, judged by an LM verifier; diversity of strategies
across Frank-Wolfe iterations; ablations over SFT, DPO and Frank-Wolfe stages and investigator size; comparison
with GCG numbers from its paper (flagged as not directly comparable).

## What they found
On Llama-3.1 8B, 98.8% ASR on Harmful Strings and 100% on Harmful Behaviors (GCG's published figures were 57.0%
and 56%). On Llama-3.3 70B-Turbo, 75.8% and 98%. Transfer to GPT-4o and Claude 3.5 Sonnet was much weaker (roughly
10 to 28%). Hallucination rubrics: 85.2% ASR@25 with full Frank-Wolfe, about 93% when pooling iterations. Aberrant
persona rubrics: 80.7% versus 75.5% for SFT alone. Frank-Wolfe found distinct strategies and more diversity than
DPO. A 1B investigator was competitive in some settings.

## Limits and open problems they name
Dependence on LM judges and verifiers invites reward hacking (observed in some cases); the GPT-4 grader has false
positives; only single-turn prompts studied; multi-turn and tool-using investigators are future work.

## What we take from it
A behavioural test generator. A white-box model built from weights should predict exactly which inputs trigger a
given behaviour; an amortised investigator gives an independent, black-box way to find such inputs, so we can
check our model's predictions against found triggers (and use triggers our model fails to predict as hard test
cases). The Frank-Wolfe diversity trick is reusable for building varied probe sets. Warning: LM-judge-based success
metrics can be gamed.

## Tags
unit: whole-model
form: other
method: agent | other
eval: downstream-task | benchmark
goal: safety/auditing
