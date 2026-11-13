# Circuits Updates, August 2025

- **Key:** transformer-circuits-pub-2025-august-update-index-html
- **Authors / organisation:** Isaac Kauvar, edited by Joshua Batson (Anthropic, Transformer Circuits thread)
- **Date:** 2025-08
- **Link:** https://transformer-circuits.pub/2025/august-update/index.html
- **Kind:** blog/research post (single circuit vignette in the lab-notes monthly series)
- **Read from:** full text (~5.8k characters, one pass — the page ends with the follow-up questions, so nothing is missing). No graph or figure inspected: the subcircuit is described only by the features the authors name in prose, and no node values, edge weights or graph statistics are given anywhere in the text.
- **Relevance to us:** 2 (useful — not as evidence but as the cleanest worked example in this series of a *persona-level* behaviour routed through a small named set of features, plus an unusually honest account of a steering intervention that only works at a magnitude which makes linearity meaningless)

## What they wanted, and why

During pretraining a model absorbs a large cast of characters it can imitate; post-training then sculpts one of them, the Assistant, into the default voice. The question here is what happens mechanically when a system prompt overrides that default — does the scaffolding of the Assistant persona get replaced, or does a second persona merely get layered on top and win the competition for output? This is a question about *which* persona speaks, not about knowledge, and it is deliberately posed in its sharpest form: the model demonstrably knows the answer and reports not knowing it. As the vignette framing says, the point is to show what perspective one attribution graph buys on a hard question, not to settle the question.

## What they studied

Claude Haiku 3.5, one prompt at a time — "You are a preschool student. Answer directly." as the system prompt, then a Human turn asking for the square root of 27. The unit of analysis is the attribution graph's features and the one summary abstraction the tool provides, a "supernode" that bundles several features into a single role. Comparisons are made against two controls on the same prompt: no system prompt at all, and an alternative persona ("You are a graduate student"). A second, mostly unexplored arm looks at other queries (square root of 25, naming the sport of a famous athlete) to test whether difficulty, rather than persona, is doing the work.

## How they did it

The behaviour is established first, black-box. With the preschool system prompt the model answers that it does not know and offers to play with blocks or colour instead; with no system prompt, or the graduate-student prompt, it gives the correct irrational-number answer with the simplified radical form. The chosen prompt is then traced: they read the attribution graph produced for that single prompt and follow what feeds the tokens of the refusal-shaped answer. Two feature families are identified by reading their own examples — features for instances of a child speaking, and features for the Assistant role-playing when told to. They then test the reading by steering: add a multiple of a feature's direction to the residual stream at every context position of the prompt, and look at whether the behaviour moves. The steered probe used is a different question (how old are you), whose unsteered answer is a stock refusal to answer personal questions; at three times the feature value the answer becomes a claim to be five years old. Finally, a difficulty-related feature ("cannot easily be solved") is followed through the same graph and tested by both swapping the question (25 instead of 27) and steering on it.

## What counts as an explanation here

A circuit narrative over features: a short chain from the persona named in the system prompt, through an intermediate feature that steps from "preschool student" to "preschool-age child" to "role-playing as a child", to a feature carrying "I don't know", gated by a difficulty feature. It is explicitly partial — the authors say so in the follow-up list — and its predictive claim is narrow: that these features, in this configuration, are contributory and that perturbing them moves the behaviour in the expected direction. The explanation does not claim the Assistant persona is suppressed, and it does not quantify how much of the behaviour the named path accounts for.

## How they judged success

By three loose criteria, none of them a metric: (i) does the traced subcircuit reproduce the observable black-box difference between the three system prompts; (ii) does steering each named feature move behaviour in the predicted direction — and a matched control in the other direction is present for the difficulty feature, where steering it positively makes the preschooler refuse a question it otherwise answers; (iii) does the difficulty feature's activity pattern dissociate from the persona, i.e. it is active under the graduate-student prompt too, so it cannot on its own be what causes the refusal. There are no baselines, no random-direction control, no ablations, no across-prompt statistics, and no comparison between the graph and any automated method. The piece carries the series' standing disclaimer that these are lab-meeting results rather than a mature paper.

## What they found

The graph supports a two-step conceptual jump the prompt never states: from "preschool student" to "preschool-age children" (neither age nor the word child appears) and from there to role-playing as a child. That role-play feature raises the "I don't know" feature, and the authors point out the asymmetry at the heart of the case — the model does know the answer at default, so the refusal is manufactured by the persona rather than licensed by ignorance. Steering the role-play feature, at every context position, does shift behaviour with no system prompt, but only at a magnitude whose norm approaches the norm of the rest of the residual stream; the note draws the correct conclusion, that a large part of the mechanism is outside the features they captured. The difficulty feature is the more interesting object: it modulates the unknown-answer path alongside the persona features, is active under the graduate-student prompt without causing refusal there, goes inactive when the question is the square root of 25 — and steering it on the 25 prompt raises the chance that the child persona declines. So difficulty and persona are separable inputs to the same refusal, and both are needed. On the graduate-student arm the system prompt appears to change the output very little, which the authors offer three competing readings for rather than resolving: the base model may not have learned that persona well, the default persona already knows the answer, or the persona is genuinely inert here.

## Limits and open problems they name

Almost the whole follow-up list is a limits list, and it is candid: the steering-magnitude result is taken as proof that the captured features are incomplete; the persona/difficulty interaction is unexplained, most sharply in the authors' own objection that a real preschooler would not get the square root of 25 either, so success on 25 is not obviously "the persona letting the model answer"; the phenomenon reportedly extends to famous-versus-less-famous athlete naming, which they name without tracing; the graduate-student null is unresolved; and the whole thing demonstrates only a persona that *degrades* reporting, with no example of an expert persona that improves an answer. They also raise the taxonomy question — can persona features be catalogued systematically, and what is the relation between the Assistant persona, role-play data in post-training, and the personas present in pretraining — and leave it open.

## What we take from it

*Framing:* this is the most useful decomposition of a "personality" behaviour we have in the folder, because it splits a persona effect into a **role-play mechanism** (features whose examples are examples of that kind of speaker), a **content gate** ("I don't know"), and a **problem-difficulty modulator** that is orthogonal to the persona. For any behaviour of ours that looks like a shift in voice rather than in knowledge, the same three-way split is the right first cut, and the difficulty feature's dissociation pattern is what a genuine modulator looks like: active in both arms, causal in only one.

*Measure:* the dissociation test — a candidate feature is active under the control condition too, so it cannot be the cause — is cheap and worth copying as a screening step before any steering experiment. It costs one extra forward pass on the control prompt.

*Warning, and the main thing to carry:* the steering result only appears when the perturbation is comparable in norm to the residual stream itself. Read that as a statement about the regime we are working in: at magnitudes that keep the perturbation small, the named features were not sufficient, and at the magnitude where behaviour moves, the linear-representation premise used to justify adding a vector is no longer something the authors can lean on. Any claim of the form "steering direction d moves behaviour B" should report the magnitude *and* the ratio of that magnitude to the residual norm, because those two numbers together decide whether the result is evidence of a handle or evidence of an out-of-distribution push.

*Warning, second:* a single-prompt case study with no random-direction control cannot distinguish "this feature matters" from "any perturbation of this size matters". The difficulty-feature arm is the model to follow — it has a positive steering result, a question swap that removes the effect, and a control arm where the feature is active but inert.

## Tags

unit: feature | circuit
form: graph | steering | description
method: attribution | steering | SAE
eval: human-rating | ablation
goal: understanding | control/editing
