# Emergent Introspective Awareness in Large Language Models

- **Key:** arxiv-2601.01828
- **Authors / organisation:** Jack Lindsey; Anthropic
- **Date:** 2025-10-29 (Transformer Circuits; revised 2026-01-01; arXiv 2601.01828)
- **Link:** https://transformer-circuits.pub/2025/introspection/index.html
- **Kind:** paper
- **Read from:** full text (main body; appendix grader details partly truncated)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Can a language model accurately report on its own internal states, or does it only produce plausible confabulations? From conversation alone the two look identical, so the paper intervenes on activations and checks whether self-reports change accordingly. The broader motivation is that, if models can introspect, their self-reports could become an interpretability tool; but such reports would need verification, and introspection could also aid concealment.

## What they studied
Claude models: Opus 4.1, Opus 4, Sonnet 4, Sonnet 3.7, Sonnet 3.5 (new), Haiku 3.5, Opus 3, Sonnet 3, Haiku 3, plus some "helpful-only" variants and base models. Unit: concept directions in the residual stream (and the whole-model verbal report).

## How they did it
Concept vectors were built by recording activations on the prompt "Tell me about {word}" and subtracting the mean over a baseline of 100 other words. These vectors were added to the residual stream at a chosen layer, with strengths 1, 2, 4 and 8 swept. Four experiments: (1) tell the model that a thought may be injected and ask whether it notices one and what it is; (2) inject an unrelated concept over a sentence and ask the model both to report its "thought" and to repeat the sentence; (3) prefill a random word as the model's answer, then ask whether it meant it, with and without injecting the matching concept beforehand; (4) instruct the model to think or not think about a word while writing an unrelated sentence, and measure how strongly that word's direction is represented. The author defines introspective awareness by four criteria: accuracy, grounding (causal dependence on the state), internality (not inferred from its own outputs), and metacognitive representation (registered internally before being verbalised).

## What counts as an explanation here
Not an explanation of the network as such: the object is the model's own verbal self-report, tested against a known causal intervention. The "explanation" of the phenomenon is behavioural evidence for a limited, unreliable introspective capacity; no mechanism is identified.

## How they judged success
Claude Sonnet 4 as an LLM judge scored coherence, affirmative detection, correct identification of the concept, and whether detection preceded mentioning the concept. Controls: no-injection trials for false positives (100 trials), unrelated yes/no questions to rule out a "yes" bias, random and negated vectors, comparisons across concept types; chance level (10%) for the thought-vs-text task; representation strength (projection) for the control task.

## What they found
Opus 4.1 and 4 detected and correctly named the injected concept in about 20% of trials at the best layer (about two-thirds through the model) and strengths 2 to 4, with essentially no false positives in production models. Abstract nouns were easiest. Models could report injected thoughts while still transcribing the text, well above chance. Injecting a concept before a prefilled word made models more likely to accept it as intended, with this effect peaking at a slightly earlier layer, suggesting a different mechanism. Models could modulate a concept's representation on instruction. Results were sensitive to prompt wording.

## Limits and open problems they name
Introspective success is unreliable and failure is the norm; few prompt templates; injection is artificial; concept vectors may carry extra meaning; the set of models is not controlled, so cross-model differences are hard to attribute; extra details in self-reports may be confabulated; no mechanism identified; nothing said about consciousness.

## What we take from it
A method: causal grounding of a report by injecting a known direction and checking that the report tracks it, with a no-injection false-positive control. This is directly the right test for any component of our white-box model that claims to "read" a state: inject, then check the prediction moves. The four criteria (accuracy, grounding, internality, metacognitive representation) are a usable checklist for separating real readout from inference from outputs. Warning: self-reports alone are weak evidence (around 20% success at best).

## Tags
unit: direction | whole-model
form: description | steering
method: steering | other
eval: patching | faithfulness | downstream-task
goal: science | safety/auditing
