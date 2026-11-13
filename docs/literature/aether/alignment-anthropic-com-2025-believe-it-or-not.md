# Believe It or Not: How Deeply do LLMs Believe Implanted Facts?

- **Key:** alignment-anthropic-com-2025-believe-it-or-not
- **Authors / organisation:** Stewart Slocum, Julian Minder, Clement Dumas, Henry Sleight, Ryan Greenblatt, Samuel Marks, Rowan Wang; Anthropic Fellows Program / EPFL / ENS Paris-Saclay / MATS / Constellation / Redwood Research / Anthropic
- **Date:** 2025-10-21
- **Link:** https://alignment.anthropic.com/2025/believe-it-or-not/
- **Kind:** blog/research post (summary of a paper)
- **Read from:** full text of the blog post (summary page; the underlying paper was not opened)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Knowledge editing is sold as a safety tool: if you can write a fact into a model, you could in principle remove a dangerous capability or install a safety-relevant belief. The authors' worry is that most editing evaluations only check whether the model *repeats* the new fact when asked directly, which is a surface behaviour, not a change of belief. They ask whether the edited fact behaves the way knowledge actually learned in pretraining behaves, and they turn that question into a graded property they call **belief depth**. The larger goal is to decide whether belief editing is a viable safety intervention at all, and if so which technique is worth building on.

## What they studied
Llama 70B Instruct as the main subject (Qwen3-32B is used for the inference-time-reasoning tests), across 24 implanted false facts. The facts are deliberately spread over four plausibility bands: blatantly false ones that contradict basic physics, subtle domain-specific falsehoods that sound plausible, and false events placed just before and just after the model's knowledge cutoff. The unit of analysis is the model's factual knowledge as a whole and, in the representational part, the direction in activation space that separates true from false statements.

## How they did it
Three editing techniques were compared against the untouched base model: system-prompting the fact, mechanistic weight editing (localised parameter updates in the AlphaEdit style), and synthetic document finetuning (SDF), where the model is finetuned on fabricated documents that mention the fact in context. Generality was measured by downstream tasks several inferential steps away from the fact, chiefly Fermi-style quantity estimates engineered so the estimate shifts depending on which version of the fact the model holds. Robustness was probed in two ways: asking the model to critique a passage that asserts the implanted fact, and putting it in a debate against an adversarial model that argues the opposite. A separate robustness test scaled up how many thinking tokens a reasoning-tuned SDF model could spend before answering. For the representational test they trained linear truth probes on ordinary true/false factual statements, then checked whether those probes still correctly label held-out implanted statements; a probe that keeps labelling an implanted falsehood as false is evidence the representation still knows the truth. A sharper version trained the probe on a set that included implanted facts, so that it could not succeed by keying on whatever artefact SDF leaves behind.

## What counts as an explanation here
Not an explanation of a mechanism. The understanding takes the form of a three-part evaluation framework plus a probe-based readout. "The model believes X" is cashed out operationally as: X is used in indirect reasoning, X survives pressure, and X is represented like genuine knowledge. The framework is explicitly partial and behaviour-adjacent: it says how deep an edit went, not what circuit carries the belief.

## How they judged success
Generality is reported as the fraction of responses whose Fermi estimate and stated reasoning move toward the implanted fact rather than the original belief, aggregated over the 24 facts with standard deviation across facts. Robustness is the persistence of the belief under critique, debate and extended thinking. The representational measure is the truth probe's accuracy on held-out implanted facts, with the adversarial-probe variant as the strict control. The base model is the reference for "what the unedited model would have said".

## What they found
Prompting and mechanistic editing both fail the depth test in different ways: prompted beliefs do generalise to downstream reasoning but evaporate under challenge, and mechanistic editing does not even produce coherent downstream use. SDF does considerably better — its beliefs carry into Fermi estimates, hold up against an adversarial debater, and survive nearly a thousand thinking tokens in the reasoning-tuned model. Both prompting and SDF fool plain truth probes into reading the implanted fact as true; only the adversarial probes recover the real factuality, and they fail to do so for the most plausible SDF edits, namely events placed immediately before and after the knowledge cutoff. The pattern is that SDF's success is graded by plausibility: facts that contradict basic world knowledge stay brittle and stay representationally distinct, while highly plausible facts become almost indistinguishable from learned knowledge.

## Limits and open problems they name
Only simple isolated facts were tested; larger-scale interconnected knowledge such as implanting a whole coherent identity is out of scope. Only factual belief was studied, and edited values, preferences or norms may need different measures. The framework may also miss properties a specific safety application needs — for instance a honeypot would want strong out-of-context reasoning that combines several planted facts.

## What we take from it
A reusable evaluation template: judge any intervention that is supposed to change what a model "knows" on three axes — indirect downstream use, survival under adversarial pressure, and representational similarity to genuine knowledge — rather than on the direct question. Two specific tools worth stealing: the Fermi-estimate task as a way to force multi-step use of a single piece of knowledge, and the **adversarial probe** as the standard control for any truth-probe claim, since a probe trained only on natural statements is easily fooled by an edit that leaves an artefact. Warning for our own predictive model: plausibility is a confound — an edit that succeeds because it fits priors tells you nothing about the mechanism of belief.

## Tags
unit: whole-model | direction
form: probe | description
method: probing | training-interpretable | other
eval: downstream-task | benchmark | prediction/simulation
goal: safety/auditing | control/editing | evaluation-of-methods
