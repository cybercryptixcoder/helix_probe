# Softmax Linear Units

- **Key:** transformer-circuits-pub-2022-solu-index-html
- **Authors / organisation:** Nelson Elhage, Tristan Hume, Catherine Olsson, Neel Nanda, Tom Henighan, Scott Johnston, Sheer El Showk, Nicholas Joseph, Nova DasSarma, Ben Mann, Danny Hernandez, Amanda Askell, … Sam McCandlish, Dario Amodei, Christopher Olah (correspondence); Anthropic
- **Date:** 2022-06-27
- **Link:** https://transformer-circuits.pub/2022/solu/index.html
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why

Mechanistic interpretability had reverse-engineered small attention-only transformers but stalled on MLP layers, and the stated cause of the stall is polysemanticity: many neurons answer to several unrelated inputs at once, so no clean reading of the weights is available. The paper's larger bet is that a lab is both the reverse engineer and the hardware designer — architecturally different models can compute comparably yet differ enormously in how legible their internals are, so interpretability can be engineered into the architecture rather than only recovered afterwards. SoLU is their proof of concept: a one-line change to the MLP activation that they hoped would push features onto single neurons. Along the way they end up with indirect evidence about superposition, and with a layer-wise map of what MLP features look like at different depths.

## What they studied

Token-level transformer LMs of Anthropic's own GPT-3/Gopher-like lineage, trained at 1, 16, 24, 40 and 64 layers (the largest ~50B parameters), with model sizes spanning roughly 10M to 50B parameters in factors of ~4. Baseline and SoLU models share every hyperparameter. Unit of analysis is the **neuron** — a single coordinate of the post-activation MLP hidden layer — plus, for one-layer models, the neuron's expanded effect on output logits. Secondary unit: the layer position (early / middle / late) as a predictor of feature type.

## How they did it

Two parallel tracks. (1) **Performance**: identical training runs with and without the activation change, compared by test loss and by six-plus downstream evaluations (Lambada, ARC, OpenBookQA, TriviaQA, arithmetic, MMLU, HellaSwag). Loss differences are converted into an "effective model size multiplier" by reading them off the baseline's own scaling curve, which is what makes a ±0.01-nat difference legible. (2) **Interpretability**: for each model size, 60 neurons from the baseline and 60 from the SoLU model are drawn at random and handed to human evaluators (three of the authors) in randomized, blinded order — the evaluator does not know which model a neuron came from. Each neuron is shown as ~20 paragraphs of the training distribution with firing tokens shaded by activation magnitude, and the evaluator gets 1–2 minutes to decide whether one rule covers 80% or more of the strongest firings. A 16-layer model with the post-activation LayerNorm but *no* SoLU is added to separate the two changes (660 neurons total). The qualitative half is open-ended exploration: reading top dataset examples of neurons across layers, then, for the one-layer model, cross-checking the guessed function against the neuron's weight-times-unembedding effect on logits. Some neurons get bespoke experiments (comparing a hexadecimal-text neuron to a regular expression, editing an example in an interactive viewer and watching activations move, looking at examples across activation levels rather than only the top ones). A final, explicitly unblinded check compares pre- and post-LayerNorm activations for one hand-categorized neuron, sorting ~1,000 examples into consistent or inconsistent with the hypothesis.

## What counts as an explanation here

A **one-line human description of a single neuron**, e.g. "fires on the final token of a word split across tokens", "fires on numbers when they enumerate people", "fires on base64-encoded text". Understanding is a per-neuron dictionary entry, deliberately partial: the authors say explicitly that even a fully interpretable set of neurons would not give a global picture and that summarization/integration is a separate unsolved problem. The strongest form of explanation appears only for one-layer models, where a neuron's dataset-example reading and its logit effect are the same object, so the description becomes an end-to-end rule of behaviour with a second, non-textual line of evidence. No prediction under intervention is offered — nothing here predicts what happens if you ablate or edit a neuron.

## How they judged success

- **Blinded human interpretability rate**: fraction of sampled neurons marked INTERPRETABLE, where the bar is a single rule explaining ≥80% of the strongest firings, judged in 1–2 minutes.
- **Blinded randomization** across models so evaluator bias cannot track the hypothesis.
- **LayerNorm-only ablation** (16L, extra LN, no SoLU) to attribute the gain between the two changes.
- **Logit attribution as an independent check** in the one-layer model: output weights × unembedding.
- **Performance non-inferiority**: loss converted to an effective-size multiplier, plus downstream benchmarks, plus training-speed overhead.
- **Inter-annotator disagreement** reported (one annotator with a stricter bar found a much larger gap).
- The authors state plainly that this measures "interpretable at first glance", not verified interpretability, and know it produces both false positives and false negatives.

## What they found

- **The headline gain.** In models from 1 to 40 layers, the fraction of neurons a blinded human could quickly explain rises from ~35% to ~60%, roughly a 25-point absolute increase / 1.7× relative, with consistent absolute rates across sizes.
- **Performance is preserved.** SoLU models land between 0.95× and 1.05× effective model size of the baseline at every scale (≈±0.01 nats against a 1.6–3 nat total); on the 50B model SoLU is equivalent to a 1.01× size increase. Downstream tasks are mixed but not systematically worse — arithmetic leaned SoLU, TriviaQA leaned baseline. Training slowdown is under 1%. Naively applying SoLU *without* the extra LayerNorm cost 30–50% of effective model size, worse at larger sizes, and the extra LayerNorm restored it.
- **The gain shrinks at the frontier.** At 64 layers / ~50B the advantage nearly disappears (42% vs 33%), and the authors do not know why — their leading guess is that bigger models hold more sophisticated concepts that 1–2 minutes of inspection cannot crack. The LayerNorm-only model sits about halfway between baseline and SoLU.
- **A layer-wise story.** Early MLP neurons de-tokenize: they bridge sub-word pieces to meaning (multi-token and compound words, proper names, organisation names, LaTeX command heads), and they disambiguate the same surface token by language or by context — three separate neurons for "die" in German, Dutch and Afrikaans, none firing on English "die". Middle layers hold abstract, often relational features (numbers only when counting people; clauses describing sound, clothing, music; discourse markers for emphasis and hedging; A/B/C/D as grades vs as letters; C-style format specifiers). Late layers re-tokenize: a neuron fires on the token "st" and lifts the next-token probability of "rag", effectively emitting one vocabulary item that only exists conditionally. They report this map as orientation, not as a verified taxonomy.
- **Recurring structures.** *Neuron splitting* — a broad neuron in a small model becomes several specific neurons in a larger one (a hexadecimal neuron splitting per hex digit). *Neuron families* — many early neurons are "token X in language Y", suggesting an equivariance axis worth naming. *Early/late duality* — recognition of a multi-token word early, emission of it late.
- **The double edge.** Because post-activation LayerNorm is invariant to input scale, a feature spread thinly across the layer is suppressed by SoLU and then restored by the LayerNorm. Their informal but striking pre/post-LayerNorm comparison shows interpretable-looking neurons acquire unrelated low-activation examples after the LayerNorm — i.e. small-activation superposition is smuggled through, and those features become *harder* to see than in the baseline. They read the fact that the LayerNorm restored performance as circumstantial evidence for the superposition hypothesis, since restoring the ability to superpose is what the model used the LayerNorm for.

## Limits and open problems they name

- The interpretability metric is "plausible on quick inspection" and biased toward neurons whose top firings are clean; post-publication they add a caveat that strong-activation monosemanticity does not license a claim about the whole neuron.
- Only top dataset examples are shown, with no negative examples unless they happen to share a snippet, so a neuron can silently fire on only a subset of its supposed pattern.
- One base architecture and one dataset (8k context, rotary attention, mixed dense/sparse attention, book-heavy mix); SoLU may not be necessary, or the other choices may be.
- The benefit decays sharply near 50B parameters, so scaling behaviour is unknown.
- Even a fully interpretable neuron set would not make a frontier model globally understandable; summarization is flagged as a major open problem.
- The LayerNorm finding is informal and unblinded, which the authors concede.

## What we take from it

- **Warning, methodological**: a "fraction of units we can explain" metric with a human-in-1-minute bar is cheap and surprisingly usable, but it scores only strong activations and hides the units it cannot see. Any legibility claim we make about our own white-box model should be paired with an explicit check on *low-magnitude* behaviour, because that is exactly where the unmodelled structure lives. This is the same trap as reading a probe at one firing threshold.
- **Shortcut, evaluation design**: converting a loss difference into an equivalent model-size multiplier is a compact way to make small differences readable and comparable across sweeps. Reusable whenever we compare a modified model to a baseline across scales.
- **Framing, central to our goal**: the neuron-level explanation for a one-layer model is only trustworthy because it can be checked twice — dataset examples *and* weight×unembedding logit effect, which are independent readouts of the same rule. That two-readout pattern is the same discipline later papers call probe-plus-patch: read the unit, then confirm what it actually writes.
- **Warning, about the tools we would use**: the failure mode is not "the network has no features" but "the network made some features loud and basis-aligned and hid the rest in small activations to save loss". A white-box model that only accounts for high-magnitude directions would be systematically overconfident. This is the direct ancestor of the shrinkage/coverage concern in weight-decomposition work and of the "feature suppression" concern in SAE evaluation.
- **Method, screening for interventions**: LayerNorm invariance is why a scale-based intervention can be functionally null while the activations look completely different. Any intervention analysis has to quotient out invariances of the layer's normalisation before claiming an effect.
- **Data, reusable**: the layer taxonomy (de-tokenize → abstract → re-tokenize) is a prior worth encoding — it tells us where to look first for a given behaviour type and gives us an expected-signature check when our white-box model reports a feature at an implausible depth.

## Tags

unit: neuron | feature
form: description | dictionary
method: other
eval: human-rating | downstream-task | ablation
goal: understanding | evaluation-of-methods
