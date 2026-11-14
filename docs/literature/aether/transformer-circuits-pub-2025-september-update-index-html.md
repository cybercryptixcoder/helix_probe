# Circuits Updates, September 2025

- **Key:** transformer-circuits-pub-2025-september-update-index-html
- **Authors / organisation:** Adam Jermyn, Wes Gurnee; edited by Joshua Batson; Anthropic interpretability team
- **Date:** 2025-09
- **Link:** https://transformer-circuits.pub/2025/september-update/index.html
- **Kind:** blog/research post
- **Read from:** full text (~3.7k characters). This is a single-post month: the raw HTML has 11 paragraph blocks and the tag-stripped text ends at the last of them, so nothing was lost to the stripper. **No figures inspected** — the two distributions the note reasons from are described only by which way they skew, never by their shape, spread or magnitude.
- **Relevance to us:** 3 (central) — not for its result, which is a null, but because it is a fully worked example of *auditing one of your own published measurements with a design control* and changing your belief when the control points the other way.

## What they wanted, and why

An earlier, much-cited result from the same lab found that models representing the same content in different languages converge on similar active features, more so in larger models, more so in middle layers, and more so for closely related languages. That result was one of the anchors of the "shared conceptual space" story, and the authors say plainly that they had liked it because it matched their intuitions. The question here is narrower and more uncomfortable: when the similarity is measured as overlap between the *sets* of active features on paired sentences, how much of the apparent convergence is just what happens to any set-overlap score as more tokens are pooled? They wanted to know whether the number rises with the amount of text for a reason that is about meaning or a reason that is about the instrument.

## What they studied

The object of study is not a model or a circuit but **the measurement itself**: the intersection-over-union over active feature sets, computed on paired same-meaning sentences across two languages, as a function of how much text is in the pair. The comparison is English against French. The unit of analysis is a similarity score over a set of dictionary features per paired sample, aggregated into a distribution over paragraphs or sentences. No model names, layer indices, dictionary widths, token counts, sample sizes or effect sizes are given anywhere in the note — this is a lab-meeting fragment, and the entry does not supply any of those numbers.

## How they did it

The observation that starts the note is a trend: within the same dataset, IoU between the two languages' active features goes up as the sample gets longer. They lay out two explanations and treat them as exhaustive. Under the first, the score is being inflated by features that fire for reasons other than meaning — low-confidence firings on their own, dictionary imperfections, or position-in-text features that would fire on any sentence at that stage of a paragraph. Under the second, the model genuinely accumulates a fuller, more converging representation as context grows, which is certainly true over the first few tokens but would have to keep happening over much longer spans to produce the observed trend. Their first move is to say that they expected the second, and that this is a reason to check rather than to conclude. The test is a length-matching control: take the **first** sentence and the **last** sentence of the same paired paragraphs and compute IoU for each. Sentence length does not change systematically with position in the context, so a score inflated by mere pooling of more tokens (explanation one) should give first and last sentences the same score, while a score driven by accumulated understanding (explanation two) should give the last sentence the higher one. They report the distribution of last-minus-first differences, and then run a mirror-image baseline in which the pairing is destroyed: unrelated English first sentences are compared with unrelated French first sentences, and likewise for last sentences. If explanation one were operative, those unrelated pairings should behave the same at both positions; if explanation two is right, the unrelated *first* sentences should overlap more than the unrelated *last* ones.

## What counts as an explanation here

The explanation on offer is a **causal reading of a trend in a metric**: "this curve slopes up because the model's representation converges with context, not because the metric rewards longer inputs." It is partial — it covers one metric on one language pair and does not re-derive the original larger-model, middle-layer or language-family results under the new reading — and its evidence is entirely distributional and directional rather than a value. It predicts a comparison (last beat first; unrelated first beat unrelated last) rather than a magnitude, which is the honest form for a note at this stage.

## How they judged success

Two features of the design carry all the weight, and neither is a metric in the usual sense. First, a **length-matched positional contrast**: the same pairs, the same sentence lengths on average, differing only in where in the context they sit. Second, a **baseline that destroys the thing being claimed** — unrelated sentences in the two languages, evaluated at both positions — so that the prediction runs in the opposite direction from the first test. Success is "the signs of the two distributions come out as the theory requires and not as the instrument-only theory requires". There are no error bars, no test statistics, no effect sizes and no stated number of samples; the note asks to be read as a colleague's preliminary experiment.

## What they found

The last-minus-first distribution over paired sentences is strongly right-skewed: the final sentence of a paragraph carries a higher cross-language IoU than the first. In the unrelated-sentence baseline the skew reverses — unrelated first sentences overlap more with each other than unrelated last sentences do. Both signs match the "richer understanding later in the context" reading and neither matches the "metric inflated by longer or off-topic firings" reading, and the authors conclude that the original result stands and that the growth with context is a real property of the model rather than an artefact of pooling. Note carefully what this establishes: the finding is that *the length trend is about the model*. It is not a re-measurement of the original cross-language similarity, an explanation of which features carry the convergence, or a demonstration that the features doing the converging are the meaning-bearing ones.

## Limits and open problems they name

Almost all of them are omissions rather than admissions. The note contains **zero quantitative values** — no sample counts, no feature counts, no model identity, no layers, no effect size — so nobody can replicate it from the text, and every claim in it is directional. They name the alternative explanation they rejected rather than exploring variants of it: position-in-text features and low-confidence firings are lumped together as one rival, so the design does not say *which* of them was ruled out. They assert that the first-few-tokens part of the growth is certainly real accumulation, which means the control is being used to separate two things that are both true at different horizons rather than to adjudicate them.

Limits we add, not theirs, and the reason this entry is rated 3: **the positional control is confounded in the same direction as the hypothesis.** A last-sentence comparison differs from a first-sentence comparison not only in accumulated understanding but in how much preceding text exists to condition on — so a score that mechanically benefits from more conditioning context, without any convergence of meaning, would produce exactly the right-skew they observe. The unrelated-sentence baseline does not remove this, because unrelated *pairs* are also more likely to share incidental features when more text precedes them. The control that would separate them is a **matched-null correction**: estimate the chance-level overlap for non-meaning-matching pairs at each context position and subtract it (or report the paired version, matching each related pair against an unrelated pair drawn at the same position and length), rather than comparing related pairs at position A with unrelated pairs at position B. As written, the note shows that the trend survives *one* control, not that it is free of the class of artefact it is worried about.

## What we take from it

- **The instrument gets an audit before the finding gets a headline — copy the sequence.** A trend that flatters your theory is the case where you owe a length-matched or position-matched control, and the note's structure (state both explanations as predictions, find a contrast where they disagree, run the mirror baseline) is a reusable four-step we can apply to any overlap-style measure: probe agreement, probe-vs-probe set overlap, circuit node/edge overlap, feature-set Jaccard across prompt formats.
- **Prediction-direction bookkeeping, not p-values.** The cleanest part of the design is that the baseline is required to move *opposite* to the related set. Any control of ours should be specified with the sign it must have under the rival explanation, because a control that can move either way confirms nothing.
- **A set-overlap score over active features is length-dependent by construction, so state the pooling before the number.** Everything in this folder that reports "N% of the same features fire" inherits the problem: at fixed firing thresholds, longer spans accumulate more firing tokens, so IoU, Jaccard and top-k overlap all drift with length. Either fix the token budget, or report the score against a matched-length unrelated-pair null.
- **Length-matched ≠ confound-matched.** Our own standing requirement that a claim be tested with a control drawn from the same distribution should be written as *the control must share every nuisance variable the comparison shares*, not just the obvious one; here length was matched and context depth was not.
- **A four-way design gives you a built-in sanity check.** Related-first, related-last, unrelated-first, unrelated-last: the two diagonal cells carry the theory and the two off-diagonal cells carry the instrument. It costs one extra pass over data you already have, and it is worth adding to our standard repertoire for any paired-sample claim.

## Tags

unit: feature | layer
form: description | dictionary
method: SAE | probing
eval: faithfulness | downstream-task
goal: evaluation-of-methods | understanding
