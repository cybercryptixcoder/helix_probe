# FIND: A Function Description Benchmark for Evaluating Interpretability Methods

- **Key:** arxiv-2309.03886
- **Authors / organisation:** Sarah Schwettmann, Tamar Rott Shaham, Joanna Materzynska, Neil Chowdhury, Shuang Li, Jacob Andreas, David Bau, Antonio Torralba; MIT CSAIL, Northeastern University
- **Date:** 2023-09
- **Link:** https://arxiv.org/abs/2309.03886
- **Kind:** benchmark
- **Read from:** abstract and sections (benchmark construction, evaluation, results table, limitations)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Automated interpretability methods (LLMs that label neurons or describe functions) are hard to evaluate on real
networks because nobody knows the true answer. The authors build a benchmark of functions whose structure is known,
so an interpreter can be scored on whether its description or reconstruction matches the truth. The larger goal is
a testbed for automated interpretability agents before they are trusted on real model components.

## What they studied
About 2,000 procedurally generated black-box functions: 1,000 numeric (parameterised atoms such as linear, ReLU,
sine; some composed, some with added noise, some with a corrupted subdomain, some approximated by small MLPs);
1,000 string functions (reversal, replacement, copycat-style edits, mostly composed); and 275 synthetic neural
modules built on Vicuna-13B that act as entity/concept detectors (140 atomic, 60 composed) or apply Wikidata
factual relations (e.g. country to capital), some with corrupted domains. Interpreters: GPT-4, GPT-3.5,
Llama-2-13b-chat, Llama-2-70b-chat.

## How they did it
The interpreter gets query access to a function only (black box). Three protocols: non-interactive (MILAN-style,
describe a fixed set of precomputed exemplars); AIA, an Automated Interpretability Agent that forms hypotheses,
calls the function on inputs it chooses, and revises; and AIA+MILAN, which starts from exemplars and then
experiments. Interaction length was bounded by context window (8K tokens for GPT-4, 4K GPT-3.5, 2K Llama-2). For
numeric and string functions the interpreter must output both a language description and executable code that
reimplements the function; for neural modules it outputs a language description.

## What counts as an explanation here
Either a program that reproduces the function (code) or a language description of it. The code form is a
predictive surrogate: it is scored purely on whether it predicts outputs on held-out inputs.

## How they judged success
Numeric code: pass if normalised MSE against the true function on test inputs is below 0.1. String code: exact
match on test inputs. Language descriptions: a "unit test" in which an LM evaluator (a fine-tuned Vicuna, checked
against human judges on entities and relations) must pick the true input-output pair from distractors given the
description. Baselines: chance, non-interactive MILAN, and the across-interpreter comparison.

## What they found
GPT-4 was best; Llama-2 models scored near zero on code and often invented outputs instead of calling the
function. GPT-4 success rates: numeric code 0.33, string code 0.23, string language 0.82, entities 0.56 (AIA) vs
0.89 (MILAN) vs 0.89 (AIA+MILAN), relations 0.78 / 0.74 / 0.92. Seeding the agent with exemplars helped a lot on
entities, indicating search breadth (finding where the function is active) is a bottleneck. The authors say even
the best configuration fails to adequately describe 48% of functions. Agents capture global shape but miss local
details such as corrupted subdomains and noise.

## Limits and open problems they name
Only black-box problems; no white-box access or real network components. Unit testing of language descriptions is
lenient toward vague descriptions and rarely catches domain corruptions. The benchmark tests necessary but not
sufficient abilities: success does not show a method yields useful insight on real models.

## What we take from it
The most directly reusable design: planted ground-truth functions plus a predictive score (normalised MSE < 0.1 on
held-out inputs, exact match for strings) for a program-form explanation. Our weight-derived white-box model should
be evaluated the same way: as executable code scored on held-out predictions, with known-mechanism targets first.
The local-detail failure (corrupted subdomains) warns that behavioural sampling misses rare regions; reading
weights could be our advantage there, and a FIND-style benchmark with white-box access (which FIND lacks) is an
open gap we could fill.

## Tags
unit: whole-model
form: program | description
method: agent
eval: benchmark | prediction/simulation
goal: evaluation-of-methods
