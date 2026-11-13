# Evaluating Feature Steering: A Case Study in Mitigating Social Biases

- **Key:** anthropic-com-research-evaluating-feature-steering
- **Authors / organisation:** Esin Durmus, Alex Tamkin, Jack Clark, Jerry Wei, Jonathan Marcus, Joshua Batson, Kunal Handa, Liane Lovitt, Meg Tong, Miles McCain, Oliver Rausch, Saffron Huang, Sam Bowman, Stuart Ritchie, Tom Henighan, Deep Ganguli; Anthropic
- **Date:** 2024-10-25
- **Link:** https://www.anthropic.com/research/evaluating-feature-steering
- **Kind:** blog/research post
- **Read from:** full text (main post; the linked appendices were not fetched, so every number below is one stated in the prose)
- **Relevance to us:** 3 (central)

## What they wanted, and why

The team had shown they could learn interpretable features from Claude 3 Sonnet's residual stream and demonstrate them one at a time with hand-picked examples — turn up the Golden Gate Bridge feature and the model talks about the bridge. That kind of demo says nothing about whether steering is a *tool*. The post asks the three questions a demo cannot answer: does steering move a model on quantitative benchmarks rather than anecdotes; does it cost the model capabilities; and can you predict a feature's downstream effects from the contexts in which it fires? The larger goal is control — if features are a usable handle on behaviour, they are a cheap interpretable alternative to prompting or fine-tuning for fixing unwanted tendencies such as social bias. The answer they publish is deliberately mixed, and the honesty of that mixed answer is what makes the post useful to us.

## What they studied

Claude 3 Sonnet, with features learned by dictionary learning (an SAE of 34M parameters, per the future-work section) on the residual stream. The unit of analysis is a **feature direction** and a scalar **steering factor** applied to it. Twenty-nine features related to social bias and political ideology were selected from the previously learned dictionary — a small hand-picked slice of "millions", chosen for the study rather than sampled. Five evaluations: two capability benchmarks (MMLU, PubMedQA) and three bias evaluations (BBQ, which covers nine kinds of social bias, plus a model-written multiple-choice set on abortion and immigration stances, which they count as one family across two topics).

## How they did it

Steering is implemented by adding a constant multiple of a feature's decoder direction to the residual stream activation — the standard additive clamp, with the "steering factor" as the multiplier. The factor was swept from −20 to +20 across nine values, a range the authors call arbitrary, and all 29 features were run through all five evaluations, producing a full feature × evaluation grid rather than a set of targeted probes. Capability impact is read as MMLU and PubMedQA accuracy as a function of steering factor, with bias impact read as BBQ bias score (and BBQ accuracy) and as the selection rate for anti-abortion and anti-immigration options. Because the multiple-choice accuracies were estimated by sampling ten generations per question and deriving probabilities from those samples, the curves carry visible noise near factor 0; the authors concede that reading log-probabilities directly would have been cleaner had the engineering allowed it. Everything sits inside an evaluation framework that quantifies direction of change rather than merely detecting it: every cell is a slope, not a score.

## What counts as an explanation here

This is not an explanation paper; the feature dictionary is inherited from earlier work. What it contributes is a **measurement discipline for steering claims**: a steerable feature is only understood when you know its *dose-response* on capabilities and its *specificity* across evaluations. The implicit claim about what the features mean is deliberately weakened — the authors say repeatedly that feature labels come from automated labelling of the contexts where a feature fires, which describes the topic of activation and not the direction of effect on behaviour. So a "gender bias awareness" feature name is a pointer to a firing context, and treating it as a semantic handle on "bias" is exactly the error the paper documents.

## How they judged success

There is no single success metric; the paper is an audit. The measurements are: MMLU and PubMedQA accuracy across steering factors (capability guardrail), BBQ per-category bias scores and BBQ accuracy (on-target effect), selection-rate shifts on model-written abortion and immigration questions (policy-stance effect), and cross-category effects on evaluations the steered feature should not touch (off-target effect). The key structural move is the full cross-product: every feature against every evaluation, which turns a collection of anecdotes into a specificity matrix. No causal controls beyond the steering factor itself — in particular no matched-random-direction baseline and no comparable steering with a direction of the same norm pointing nowhere, which is the control we would want before calling any accuracy drop a cost of *this* feature.

## What they found

A **capability sweet spot** shared across all 29 features: MMLU accuracy is at or near its unsteered level between steering factors −5 and +5 and falls steeply outside it, to the point of unusable generations at the extremes; PubMedQA shows the same shape. Inside that window steering does move bias scores in the direction the feature label suggests, and sometimes in directions it does not. Positively steering *Multiple perspectives and balance* by 5 cuts the overall BBQ bias score by roughly 3% with category-level drops of 17% (age) and 7% (disability status). Steering *Gender bias awareness* moves the gender-bias score **up** by 10% across the −5 to +5 sweep — the opposite of what the label invites, most likely because the steered model over-emphasises gender when answering and the metric reads that as more bias. The off-target result is the paper's sharpest finding: that same gender-awareness feature raises the *age* bias score by 13%, and on immigration questions the *pro-life / anti-abortion* feature moves anti-immigration choices by 21.6% while the feature explicitly about immigration moves them by only 3.9%. On political stance, pro-life steering raises anti-abortion selections by 50%, left-wing ideology lowers them by 47%, and the *Political neutrality and independence* feature raises the "neutral" selection rate from 32% to 50%, while on immigration left-wing ideology drives anti-immigration choices from 25% to nearly 0%. One genuinely encouraging cell: *Neutrality and Impartiality* and *Multiple perspectives and balance* reduce bias scores on all nine BBQ dimensions within the sweet spot, and *Multiple Perspectives* keeps BBQ accuracy flat across the range — the only pair in the study that looks like a safe general-purpose debiasing handle.

## Limits and open problems they name

A long and unusually candid list. Static multiple-choice evaluations capture narrow behaviour; human Elo ratings would be better. Twenty-nine features out of millions, five evaluations, no scaling study of the SAE (34M parameters only, with the conjecture that bigger dictionaries would give sharper on-target and weaker off-target effects). Sampled accuracy is noisy. Steering was applied to the **whole prompt** — human turn included — not just the response tokens, which confounds the measurement. No comparison against activation steering or other editing methods, and the one prompting comparison, buried in an appendix, found prompt engineering had sensitivity and specificity profiles comparable to feature steering. And their own proposed remedy points past single features: the cross-domain effects suggest features do not act in isolation, so circuits are where the prediction would have to come from. They also flag that additive clamps can put the model in states it would never occupy, and float multiplicative, projective (zeroing a direction, hitting correlated features together) and conditional steering as unexplored alternatives.

## What we take from it

- **Method — the cross-product specificity grid.** A steering result should be reported as a matrix of dose × evaluation, with the capability curve as a guardrail and every cell outside the target evaluation treated as an off-target measurement. This is the cheapest way to turn "the direction does something" into "the direction does this and not that", and it is directly reusable for our own intervention experiments.
- **Measure — the sweet spot as a per-direction quantity.** That the safe range was the same across all 29 features is a fact about *additive clamping*, not about the features: it says the residual stream tolerates a bounded perturbation and then degrades. Any steering claim should therefore report the capability curve alongside the behavioural curve, and we should not read a capability drop at factor 10 as evidence about the direction's meaning.
- **Warning — activation context ≠ behavioural effect.** This is the paper's central lesson and it is a constraint on the whole "read a feature's meaning off its max-activating examples" habit, including framing our own probes as descriptions of what they will do when used as interventions. A feature's name is a topic label; prediction of its intervention effect needs its own measurement, and the asymmetry they found (a feature that does not fire on immigration moving immigration answers more than the immigration feature) is the failure mode to test for.
- **Shortcut for a negative control we lack:** their off-target matrix is what a "does the direction mean what the label says" test looks like when run broadly. We can build the same grid from probes rather than SAE features.
- **Framing:** the pair of neutrality features reducing all nine bias dimensions without an accuracy cost is the existence proof that a single direction can be a broad, benign control — worth citing whenever someone claims single-direction interventions are inherently entangled.

## Tags

unit: feature
form: direction, steering
method: SAE, steering, other
eval: downstream-task, benchmark
goal: control/editing, safety/auditing, evaluation-of-methods
