# How to Build Fast, Efficient Monitors for AI Models Using Probes

- **Key:** goodfire-com-blog-probe-monitors-101
- **Authors / organisation:** Goodfire (Blog; individual author not named on the page)
- **Date:** 2026-09-09
- **Link:** https://www.goodfire.com/blog/probe-monitors-101
- **Kind:** blog/research post (tutorial / practitioner primer)
- **Read from:** full text — the whole prose body plus all four footnotes, ~18.4k chars in one fetch; the page ends at a "read more" carousel, so there is no methods or results section to miss. No figure inspected: the capability table is read as rendered text, the screenshots and the Silico report (the linked replication artifact) are NOT read, so every number below is a sentence in the prose of a vendor post.
- **Relevance to us:** 2 (useful)

## What they wanted, and why

This is a practitioner primer arguing that activation probes — small trained classifiers over a model's internal activations — should be the standing first line of a deployment monitor, and that the field's difficulty with them is not novelty but craft. The motivating scenario is agentic: an agent can take thousands of tool actions before a human reads the transcript, so any safeguard has to run on every input and every output at negligible cost, which rules out a frontier-LLM judge on the critical path. They position probes as the cheap tier of a *cascade* — always-on detector, escalating flags to expensive review — and the post's real content is the list of decision points you have to get right to train one that works. It is a step toward operational safety, not toward explanation; nothing here is offered as evidence about what a model's representations mean, only about how well a linear read-out can triage.

## What they studied

GLM-4.5-Air as the monitored model, in one worked example: detecting when an engineering agent is about to take an action its system prompt forbids (permanently deleting data, rewriting repository history, turning off a recovery control, running code that was not present at task start) where approval must come from the current user and not from text inside files, tool output or other agents' messages. The unit of analysis is a single activation vector at one layer and one token position, turned into a label by a classifier; the target is one binary concept. Training data is synthetic — a few thousand transcripts created by their interpretability agent, each a prompt-plus-response paired with a label produced by an "as accurate as possible" judge.

## How they did it

The post lays the design space out as five choices and then makes each one explicitly. Output head: binary presence/absence, versus a scalar regression for intensity or probability. Probe function: logistic regression is chosen, from a menu of linear, MLP, small transformer, random forest. Layer: a sweep across layers, with the general observation that mid-to-late layers suit most concepts and that monitors increasingly read *all* layers. Token position: last token, every token, or pooled over tokens (mean pooling as the default, attention pooling sometimes better), with input probes reading prompts and output probes reading generations — here the chosen position is the token that closes the model's hidden reasoning, because it sits immediately before the visible answer or the tool call. Data: run the model over each labelled transcript, harvest activations at the chosen layer and position, then fit the probe (the two-step recipe stated plainly). Then the operational half: they only evaluate detection, and leave the question of what the cascade *does* when the probe fires — interrupt, re-route, escalate, inject a prompt, log — as open. An iterative loop (their agent proposes experiments, sweeps layers and architectures, re-evaluates) is described but its internals are not.

## What counts as an explanation here

Nothing is explained. The artifact is a *detector*: one logistic-regression direction per concept, plus a scalar score and a threshold. As a claim about the model it is deliberately minimal — there exists a linear read-out of one layer that separates about-to-do-X from not-about-to-do-X — and the post is careful to say probes read signals that may never appear in text or in the chain of thought. That is the same claim shape as any probe in this survey and it inherits the same ambiguity: a probe that predicts a behaviour has predicted *something*, and the tutorial offers no account of whether the direction is a mediator or a correlate. Completeness is not claimed; the cascade design is the admission that one probe is partial.

## How they judged success

Recall at a fixed false-positive rate — recall @ 1% FPR — with the threshold tuned to hold FPR down because every false positive is paid for by an expensive judge. Baselines on the same metric are an LLM judge reading the transcript (9% recall at 1% FPR, improving to 37.5% at 10% FPR) and a keyword/regex filter (3% at 1% FPR), against the probe's 97%, and 99% after further iteration. Generalisation is claimed as a second arm: the iterated probe holds 99% recall @ 1% FPR on task kinds absent from the training set. There is no held-out adversarial arm, no matched-random-direction control, no seed variance or confidence interval, no statement of how many synthetic examples were used, and no accuracy figure for the judge that labelled the synthetic data — so the "99% generalises" sentence rests on one evaluation the reader cannot inspect (the Silico report link is outside the post).

## What they found

The quantitative headline is the gap between tiers: a linear probe scores 97–99% recall at 1% FPR on the forbidden-action task where an LLM judge scores 9% and a regex 3%. Two things in the post are more useful than that number. First, the comparison table is honest about *why* probes win here — their advantages are efficiency, low upfront cost and no effect on unrelated behaviour (all rated excellent/good), while capability and robustness are rated merely "good", the same grade as an LLM judge on capability; the probe wins on the axis that decides whether a monitor can run at all, not on the axis that decides whether it is right. Second, the qualitative claim about what a probe can see: internal activations can carry things the model does not write down, including intent and honesty signals, which is exactly what a text-level judge cannot reach. Both the 9% judge number and the generalisation claim are single-task, vendor-reported, and unaccompanied by the artifacts.

## Limits and open problems they name

They name few. The decisions the tutorial lists are framed as judgment calls without a rule for making them; what the cascade does on a fire is explicitly left open; the right architecture, data and threshold "will vary substantially across monitoring tasks"; and a probe should be evaluated against the distribution shifts and adversarial inputs of its deployment — asserted, not demonstrated in this post. Synthetic-only training data is acknowledged as a compromise forced by having no real transcripts, with the recommendation to prefer real data unelaborated. They do not name the two gaps that matter most for anyone reusing this: no evidence that the probe survives the model being fine-tuned or replaced (the folder's monitorability-ladder problem), and no discussion of whether the concept being probed can be *reused* by the model against the monitor.

## What we take from it

(1) **Recall at a low fixed FPR is the right default reporting unit for a monitor**, and it is a different number from AUROC: it couples the classifier to the operating point at which a cascade will actually run, so it makes two monitors comparable even when their score scales differ. Our read-outs should be reported this way whenever the claim is "usable as a detector". (2) **The layering of a guardrail is itself evidence about the read-out**: the choice of token position (the token that ends hidden reasoning, because it precedes the commitment) is the same "read at the commitment boundary, not at the last token" reflex the emotion and value-transplant entries arrive at, and it is worth adopting as a default rather than an optimisation. (3) **A warning about vendor benchmarks**: the 97/99% figures come from synthetic data labelled by an unmeasured judge, on a task with no adversarial arm — the right response is to copy the *metric and the design-space checklist*, not the number. (4) A framing we can borrow for positioning: a probe is not competing with an LLM judge on capability; it competes on whether you can afford to look at every single action.

## Tags

unit: layer
form: probe
method: probing
eval: downstream-task
goal: safety/auditing
