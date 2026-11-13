# Under the Hood of a Reasoning Model

- **Key:** goodfire-com-research-under-the-hood-of-a-reasoning-model
- **Authors / organisation:** Dron Hazra, Max Loeffler (core contributors), Murat Cubuktepe, Levon Avagyan, Liv Gorton, Mark Bissell, Owen Lewis, Thomas McGrath, Daniel Balsam; Goodfire
- **Date:** 2025-04-15
- **Link:** https://www.goodfire.com/research/under-the-hood-of-a-reasoning-model
- **Kind:** blog/research post
- **Read from:** full text (all prose sections and steering examples; the linked feature browser and SQL dumps were not queried)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
First public interpreter models for a *true reasoning* model — DeepSeek's R1 — and, at the time, for any model at that scale. The motivating claim is instrumental: if you can read and edit the mechanisms behind reasoning, you can monitor failure modes, suppress capabilities on demand, and correct specific errors without collateral damage to the rest of the model. A secondary aim was access: because R1 is impractical for most labs to run, they released the trained SAE artifacts plus databases of max-activating examples so outside researchers can inspect features without a forward pass.

## What they studied
Undistilled DeepSeek-R1 at 671B parameters, treated with sparse autoencoders over its residual activations. Two SAEs: one trained on a custom reasoning dataset (also open-sourced), one on OpenR1-Math. The unit of analysis is therefore the *feature* (SAE latent), not the neuron or the attention head; the reasoning-specific behaviour is chain-of-thought text generated under steering. Feature sets were organised into an interactive UMAP map (DataMapPlot) for browsing. They deliberately say SAEs are one component of the toolbox, not a solution to interpretability.

## How they did it
Standard SAE-plus-steering setup, with two deviations forced by the model. (1) Train SAEs at 671B scale on their own inference engine, on two different reasoning corpora. (2) Curate and publish features by max-activating-example inspection — the post shows five from the general reasoning SAE, giving the token spans that fire each one. (3) Steer by clamping a feature's strength and scanning it across a strength sweep, recording at which strengths the intended behaviour appears, with successful strengths marked per example. (4) Inspect trigger points: instead of steering uniformly from token zero, they searched for the position at which steering starts to work, and separately plotted average activation strength per position to locate attention sinks. (5) Run two demonstration interventions — swapping a mathematical operator (multiplication prompt answered with division) and compressing reasoning length on an open-ended question — plus a strength sweep taken far past the useful range to characterise the oversteer regime. Comparisons are qualitative: steering-on vs steering-off generations at each strength, plus the observation that behaviour disappears at very high strength.

## What counts as an explanation here
A feature dictionary: named latents with human-written glosses and max-activating examples, browsable as a map. The explanation is partial and descriptive — "here is a unit that fires on backtracking" — not a circuit and not a predictor. The one thing in the post that is genuinely predictive is negative and mechanistic: an account of *where in the sequence* steering must be applied for the model to treat it as a response, derived from attention-sink positions. Nothing here predicts an output under an intervention quantitatively.

## How they judged success
No metrics, baselines, ablations or statistics are reported. Success is demonstrated by curated example: a feature is "learned" if its max-activating examples are recognisably the behaviour it is named for; a steering intervention "succeeds" if the target behaviour appears in the shown generation at the marked strengths (the strength axis is annotated green where steering worked). This is a demonstration post, not an evaluation paper — treat everything in it as existence proof.

## What they found
Five reasoning-specific features are exhibited on the general reasoning SAE: one firing when the model catches its own error and corrects course (backtracking), one for references back to earlier statements, one that fires just after material about subsets/subsequences, one marking an entity to track across a problem, and one immediately before the result of a multi-step calculation.

Two steering observations they flag as novel relative to non-reasoning models. First, steering from the first token fails; you have to wait until after the model writes its opening "Okay, so the user has asked a question about…" frame. Attention sinks sit at the *end of that frame* rather than at the very beginning of the response, which they read as the model not treating its true response as started until the preamble is done — the hypothesis being that this frame was so common in training traces that it functions as prompt rather than as answer. They note that more than 95% of R1's English reasoning traces open with "Okay," and describe a distinct feature-distribution shift between prompt-with-frame, thinking trace, and final answer.

Second, oversteering can be non-monotonic: pushing certain features far past the useful range returns the model to its *unsteered* behaviour before it degrades into incoherence. Their working hypothesis is that heavy internal perturbation is itself detectable as a confused state, so the model halts and rebalances. They connect this to the everyday observation that reasoning models abandon a failing line of attack and try something else, and infer that reasoning models may be trained toward greater implicit awareness of their own internal state — with the practical warning that behaviour changes may be routed around.

Demonstrations: a division feature at high strength turns a "1024 times 2" prompt into a correct division trace answered 512, with the preamble intact; an "answer quickly" feature pinned mid-range collapses a long philosophical essay's reasoning to a short plan-then-answer shape (shown at strengths 1–10 with a pinned setting).

## Limits and open problems they name
They state plainly that they have not yet systematically investigated the *occurrence or causes* of either steering phenomenon — both are shared as early insights. The oversteer hypothesis is explicitly a hypothesis. They call for more work on reasoning-model internals, note the routing-around problem as a real obstacle to behaviour suppression, and frame the whole release as initial, with the community expected to build on it. No evaluation of feature quality (reconstruction, sparsity-vs-fidelity tradeoffs, feature splitting) appears in the post.

## What we take from it
- **A caveat for our own interventions, above all else:** steering in a reasoning model is *non-monotonic*, and the failure mode is not "incoherent" but "back to baseline". Any dose-response curve we measure — steering magnitude against behaviour — needs samples far beyond the useful range, because a curve that returns to control at high strength will otherwise be read as "no effect" or "the feature is not causal". This is the reasoning-model analogue of the ablation-on-success discipline and directly contradicts the monotone-dose assumption behind most difference-in-means steering.
- **The preamble/attention-sink finding is a positional-confound warning:** before claiming a residual-stream direction does nothing, check *where* it was applied. A feature-distribution shift between the prompt region, the thinking trace and the answer suggests we should be segmenting activations by role before fitting anything, rather than pooling across a generation. It also predicts that a pooled probe over a reasoning trace mixes at least three different distributions.
- **A concrete measurement we should run:** attention-sink position as an annotation of "where the model believes the response begins". Cheap, single forward pass, and it gives a principled intervention site instead of token zero.
- **Feature names worth probing for** as ground for a predictive readout: backtracking (error detection + correction), an entity-tracking slot, and a pre-computation "result imminent" marker. The last one is interesting because it fires *before* the arithmetic is written out — the kind of internal commitment our predictions should be able to read off before the token appears.
- Warning on evidence weight: this is an existence-proof post with no metrics. Its two insights are hypotheses with curated examples, and we should cite it as a motivation for a control (high-dose sweep, position-matched steering), not as a result.

## Tags
unit: feature
form: dictionary
method: SAE, steering
eval: human-rating
goal: understanding
