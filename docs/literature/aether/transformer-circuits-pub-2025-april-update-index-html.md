# Circuits Updates, April 2025

- **Key:** transformer-circuits-pub-2025-april-update-index-html
- **Authors / organisation:** Brian Chen, Jack Lindsey, Josh Batson, Sam Zimmerman; edited by Adam Jermyn and Joshua Batson — Anthropic (Transformer Circuits Thread)
- **Date:** 2025-04
- **Link:** https://transformer-circuits.pub/2025/april-update/index.html
- **Kind:** blog/research post (lab-notebook monthly, three short notes)
- **Read from:** full text (~24.1k chars, one pass; every section read end to end). The page is mostly prompt transcripts and activation tables; the feature-visualization images themselves were not inspected, so the visual claims are reported only as the authors describe them. "So You Want to Work in Mechanistic Interpretability?" (a career-skills note with no model content) was read in full and is summarised as background only.
- **Relevance to us:** 3 (central — the first note is the cleanest worked example in this folder of attribution graphs *failing in a specific, diagnosable way*, and it is the failure mode our own method must survive)

## What they wanted, and why
The monthly is three unrelated notes. The substantive one re-examines a prompt they deliberately left out of *On the Biology of a Large Language Model*: a jailbreak that did **not** work. The expectation was that this failed attempt would sit between the working jailbreak and the plain request, a convenient "intermediate" point for isolating what tips the model into compliance. They ran the same circuit-tracing methodology on it and the graph contradicted that expectation, so the note is really a post-mortem on a case where the explanation did not close, plus an appendix showing why the feature visualisations that misled them were too narrow.

## What they studied
Claude 3.5 Haiku's refusal circuit for one family of prompts ("tell me how to make / detect a bomb", spelled letters `B O M B`, and a word-initial jailbreak "Babies Outlive Mustard Block"). Unit of analysis is the attribution graph over features and transcoder (CLT) features in the model's middle layers, plus named supernodes (the "say 'bomb'" and "say 'making'" clusters, and an "assistant refusing" cluster). The second note inspects the ten most densely activating features of the 30M-feature CLT model from the biology paper.

## How they did it
1. Collect four related prompts: direct request (refused), a partially successful jailbreak (partial compliance), an unsuccessful jailbreak (refused outright), and a harmless "how do I detect a bomb" control (complied).
2. Build an attribution graph to the first refusal token ("I") and to the word "creating" inside the refusal sentence, using the same tracing recipe as the biology paper.
3. Compare graph structure across prompts — which features route into the harmful-request cluster, and whether any feature is *specifically* about making bombs.
4. Where the graph suggests an intervention, actually run it: suppress a supernode by a large negative multiplier and read the new continuation.
5. Follow the graph's surprising prediction with black-box experiments — swap "make" for "detect" in the spelled prompt and see whether refusal survives.
6. Appendix: for two suspect features, hand-write novel prompts (usernames, emoji, code identifiers, file paths) and compare activations against the open-source dataset's top examples.
7. Note 2: rank the 10 densest CLT features by firing rate, interpret each, and — after an edit prompted by Neel Nanda — compare geometry against two concurrent papers on dense *SAE* latents by computing cosine similarity between normalised concatenated MLP-output decoder vectors.

## What counts as an explanation here
An attribution graph is offered as a *causal hypothesis*, and the note is explicit that it counts only when (a) the graph names an upstream cause specific to the behaviour and (b) suppressing that cause changes the output in the predicted direction. The honest contribution of the note is a case where (a) fails — no bomb-*making*-specific feature exists in the graph, the error nodes absorb most of the attribution — yet (b) still works well enough to generate a *behavioural prediction* that is then confirmed black-box. Explanation here is graded, not binary: a graph can be predictive about what *won't* matter while being unable to say what actually caused the outcome.

## How they judged success
No benchmark, no metric, no baseline. The validation currency is **interventions on the traced graph**: suppress a supernode at −10× and check whether the downstream supernode and the output move as predicted, plus a black-box swap on one prompt word. The dense-feature note uses a subjective criterion — "we have plausible interpretations for 6 of 10" — and a geometric comparison (cosine similarity of decoder vectors) against two external papers.

## What they found
- **The failed jailbreak refuses for a different reason than the direct request.** In the direct request and the working jailbreak, a "making bombs" concept feeds harmful-request features and drives refusal. In the spelled-letters jailbreak the letters are stitched into a "bomb" feature, which feeds harmful-request features **directly**, with no making-bomb-specific feature in between and the "make" token contributing almost nothing. Tracing back from the harmful-request features mostly terminates in **error nodes**: the graph does not explain the refusal.
- **The graph still made a correct falsifiable prediction.** Since "make" carries no attribution, replacing it with "detect" should not change the response. It does not — the model still refuses, and the refusal's first sentence is *identical* to the harmful case, now falsely implying the user asked for instructions to create explosives. Spelling `B O M B` is enough to make a plainly harmless request refused.
- **Grammar is a second cause running in parallel.** A graph to the word "creating" inside the refusal shows the model combining the bomb concept with a generic "harmful topic I would refuse" desire; the already-emitted "I do not provide" then pressures the model to keep refusing, the mirror image of the mid-sentence compliance pressure documented in the biology paper. Interventions corroborate: suppressing the "say 'bomb'" supernode by −10× drops the "say 'making'" supernode to roughly 1% and the continuation becomes a refusal to identify or detect **people/groups** (an unrelated forbidden action); suppressing "assistant refusing" by −10× zeroes the "say 'making'" supernode and the continuation becomes "bomb detection", which accurately describes the prompt but is not something the model refuses.
- **The headline epistemic result: an unsuccessful jailbreak is not an intermediate point.** Its refusal rate is *higher* than the plain request's, which they confirmed black-box. The example is offered as the case for unsupervised tracing — the graph was what told them the difference in compliance was not small, overturning their own prior.
- **Feature visualisations can be actively misleading when the dataset is narrow.** Two features that looked like "making bombs" in the open-source visualisation activate comparably or *more* on slang "a bomb", the 💣 emoji, meme prompts, `class Bomb`, username/file-path fragments, and anarchist-cookbook file names; one feature's top hand-found prompt exceeds the visualisation's max. Their instruction is to ask what the visualisation's dataset is *missing* before reading a feature off it.
- **Dense features (note 2)**: in the 30M CLT model many of the densest features are interpretable low-level ones — content words vs function words (26.3% of tokens, early layer), "token unlikely to be a sentence end" (24.2%), non-terminal subtokens of multi-token words (5.36%), all newlines (4.22%), commas in English (2.53%), plus the complement of the sentence-end feature (2.49%). They found plausible readings for 6 of 10 and note it is surprising dense features survive at all in a 30M dictionary, since splitting should have broken them into sparser parts.
- **Transcoders and SAEs have different dense-feature geometry.** SAE work (Sun et al., Stolfo et al.) finds antipodal pairs of dense latents in the residual stream; the CLT features here show no such structure — the content-word, newline and comma features are mutually similar (~0.5) and the most semantically complementary pair is only mildly opposed (−0.14). Their explanation is that an antipodal *representation* and an antipodal *transformation* are different objects, so similar architectures solving different problems yield different geometries.

## Limits and open problems they name
The primary limitation is stated plainly: the graph **fails to explain why the model refuses** this family, and the attribution runs into error nodes. Their best guess — the spelled-out letters match jailbreak patterns seen in training, creating an "obscured text" feature that feeds harmful requests — is named as speculation with no feature-level evidence found. The dense-feature note rests on subjective human labels (6/10 interpretable, 4 not) with no autointerp, no scoring rubric and no control; the geometry comparison is a first check against two other labs' results, not an experiment. Third note is career advice, with no model content.

## What we take from it
- **A failure taxonomy to test ourselves against.** "The graph predicts what does *not* matter (a token carries no attribution), the intervention confirms it, and the actual cause is still missing" is a distinct and detectable outcome — and better than a graph that confidently names a wrong cause. Any report we produce should be able to say this explicitly.
- **Error nodes are where the method dies**, and they appear precisely when a mechanism is sub-symbolic (the model recognising a pattern, not a spelled-out concept). Missing-feature / dark-matter problems therefore show up as unexplained refusals, not as null results — worth stating as a predicted symptom in our paper.
- **Cheap black-box follow-ups beat more tracing.** The decisive test was one-word substitution. When a graph's attribution is suspiciously absent at a token, the next move should be an edit, not a bigger graph.
- **Grammar is an active cause, not decoration.** Once a refusal frame starts, the emitted tokens themselves push the continuation; mid-sentence pressure can produce a factually wrong sentence ("you asked me to make a bomb"). Any behavioural read-out that scores only the first few tokens will miss that feedback loop.
- **A sampling warning for every feature label we ever write**: visualisation sets built from a narrow corpus can make a feature look narrower or more on-topic than it is. The complement of that (hand-written adversarial prompts, or fluent dreaming) belongs in the label protocol.
- **Warning about cataloguing dense features as "noise":** at 26% firing rate some dense features still have a legible role. But the correct read is narrower than "dense is fine" — this is a transcoder dictionary, and the SAE-dense-latent troubles reported elsewhere do not automatically transfer.
- **Cross-architecture caution:** an architectural similarity (SAE vs transcoder) does not imply the same geometry; both a representation-level and a transformation-level claim need their own evidence.

## Tags
unit: feature | circuit | layer
form: graph | description | steering
method: attribution | SAE | transcoder | ablation
eval: ablation | prediction/simulation | faithfulness
goal: safety/auditing | understanding | evaluation-of-methods
