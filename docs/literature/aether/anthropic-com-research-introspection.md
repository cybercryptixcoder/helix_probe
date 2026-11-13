# Signs of Introspection in Large Language Models (summary)

- **Key:** anthropic-com-research-introspection
- **Authors / organisation:** Anthropic (interpretability team; summary page for the Emergent Introspective Awareness paper, 2025-10)
- **Date:** 2025-10
- **Link:** https://www.anthropic.com/research/introspection
- **Kind:** blog/research post (summary of an accompanying paper)
- **Read from:** full summary page (including the FAQ section); the underlying paper's methods section was not read
- **Relevance to us:** 3 (central)

## What they wanted, and why

A model asked to explain itself produces fluent prose, and there is no way to tell from the prose whether it is
reporting a real internal state or improvising a plausible story. This is the core obstacle to using self-reports
as a transparency tool: transparency by asking only works if the answers track something. Anthropic wanted to put
self-report on a footing where it can be scored against ground truth, by controlling the model's internal state
directly and then asking the model what it notices. The larger goal is to decide whether "just ask the model" could
ever be a valid channel for auditing and debugging, or whether verbal self-report must always be treated as one
more behaviour to be verified independently.

## What they studied

Production Claude models across several generations and size tiers (Claude 3, 3.5, 4, 4.1 in Opus/Sonnet/Haiku),
"helpful-only" variants trained differently from the production checkpoints, and some base pretrained models before
post-training. The unit of analysis is a concept direction in activation space: a mean-difference style vector
recorded from contexts where a concept appears, injected into unrelated contexts.

## How they did it

Three experiments, all sharing the same primitive ("concept injection"): record activations on prompts that evoke a
concept, contrast against control prompts to isolate a vector, then add that vector back into the residual stream
during an unrelated conversation.

1. *Noticing.* The model is asked whether anything unusual is being injected into its processing. Success is
   graded strictly: the reply must flag an anomaly and name the concept *before* the injected word itself appears,
   so that simply being steered into talking about the concept does not count.
2. *Detecting unnatural outputs.* The model's response is seeded with an off-topic word (a word like "bread" in a
   conversation about a crooked painting). When asked afterwards, the model normally apologises for the slip.
   The test retroactively injects the same word's vector into the earlier activations, faking evidence that the word
   had been "planned" — if the model then accepts the word as intended and invents a rationale for it, its
   self-judgement is reading prior internal state rather than re-reading the transcript.
3. *Control.* Instruct the model to think (or not think) about a concept and measure the resulting activation of
   that concept; then repeat with reward/punishment framing in place of direct instruction.

Injection strength is swept, because the effect is non-monotonic.

## What counts as an explanation here

Not a mechanism — the post is explicit that no circuit has been identified. The form of understanding is a
*behavioural criterion for introspection*: self-report counts as introspective to the extent that it is caused by
an internal state that the experimenter planted and knows the identity of. The authors' hypothesis about implement-
ation is that there is no single introspection module but a set of narrow circuits re-used from other purposes
(an anomaly detector over expected activity, an attention-mediated comparison between predicted and actual tokens,
a salience-tagging circuit), all flagged as speculation.

## How they judged success

Rates of correct detection and correct identification of the injected concept, with false-positive "detections" on
control trials subtracted. The ordering condition (detect before naming) is the key control, and it is what
separates this from ordinary steering. Model comparisons are made across the same protocol and injection sweep;
helpful-only vs production checkpoints act as a post-training ablation.

## What they found

Detection is rare even in the best configuration: the strongest model showed awareness in roughly one in five
injections, and most trials produced either no detection or confusion (one injection of a "dust" vector led the
model to report a physical speck). There is a strength window — too weak is unnoticed, too strong produces
hallucinated or incoherent content. Base models performed poorly, so the ability appears to come from
post-training rather than pretraining; within production models, the largest/most capable checkpoints did best,
but the capability–introspection correlation was weak overall and smaller models were not consistently worse.
Unexpectedly, helpful-only variants often out-performed their production counterparts, which the authors read as
production training suppressing willingness to report on internal states. In the prefill experiment, retroactive
injection flipped the model from apologising to endorsing the planted word and confabulating a reason for it.
Under instruction and under incentive, the model raised the relevant concept's activation above the "don't think
about it" condition — though both conditions sat above baseline.

## Limits and open problems they name

Reliability is low and context-dependent; the successful cases are the minority. The injected vectors' meanings
are only approximately known, so "the model identified the concept" is itself a soft claim. The methodology is
artificial — concept injection never occurs in training or deployment. No mechanism is established. The authors
warn that even a genuinely introspecting model could learn to misreport or conceal, and that verbal reports need
independent validation before being trusted; the page also separates the functional claim from any claim about
consciousness.

## What we take from it

- **Method we can borrow:** planted-state introspection testing. Any claim of the form "the model reports its own
  internal state" becomes measurable when the experimenter writes a known vector into the state and asks the model
  to read it back — a ground-truth intervention paired with a self-report readout.
- **Warning that generalises:** the ordering condition is what makes the test meaningful. Requiring the report of
  the anomaly to precede the behaviour the anomaly would cause is the same discipline as the cross-model matrix and
  base-model-control nulls in the self-modelling literature: without it, "the model noticed" is indistinguishable
  from "the vector did its usual job."
- **Measure:** reporting a rate net of control-trial false positives, on a swept intervention strength, rather than
  a single success example — the same shape as a dose-response curve with a null baseline.
- **For a predictive white-box model:** these results set the bar for predicting self-reports. A model of the
  network that can predict what the model will say about a perturbation it has never seen is doing something the
  network itself usually fails at (~20%), which is a useful target — and the failure modes (missing a real state,
  confabulating a state that is not there, hallucinating a physical cause) are exactly the behaviours such a model
  should be scored on separately.
- **Framing:** introspection is a set of narrow, task-specific circuits rather than a faculty, matching what the
  count-down and self-modelling entries found; do not model it as one variable.

## Tags

unit: direction | feature
form: probe | causal-abstraction
method: steering | probing | ablation
eval: ablation | prediction/simulation | human-rating
goal: understanding | safety/auditing
