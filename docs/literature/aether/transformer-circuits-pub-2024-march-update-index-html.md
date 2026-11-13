# Circuits Updates, March 2024

- **Key:** transformer-circuits-pub-2024-march-update-index-html
- **Authors / organisation:** Joshua Batson, Brian Chen, Andy Jones, Adly Templeton, Tom Conerly, Jonathan Marcus, Tom Henighan; Anthropic (Transformer Circuits Thread)
- **Date:** 2024-03
- **Link:** https://transformer-circuits.pub/2024/march-update/index.html
- **Kind:** blog/research post (lab-meeting notes)
- **Read from:** full text (clean extraction ~20k chars; the original page itself cuts one bullet mid-sentence)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Two things. First, an argument that a pre-trained SAE dictionary can replace behaviour-specific dataset curation as the *starting point* for circuit finding: if the dictionary already holds the model's features, one example text is enough to hypothesise which components matter, and a feature's decoder row doubles as a probe. Second, housekeeping — several training tricks the team had advertised in earlier updates no longer help now that other changes have landed, so they say so. The rest of the note is a curated digest of outside work they think bears on the agenda.

## What they studied
An 18-layer language model with an SAE of expansion factor ~256 trained on the layer-9 residual stream, following Cunningham et al.; the worked behaviour is sport extraction after an athlete's name (basketball / baseball / tennis, ~1500 names, following Nanda et al.). Feature-level analysis sits at a single token position per example. Outside papers reviewed: Othello-GPT SAEs, a mathematical framework for computation in superposition, AtP*, and self-repair.

## How they did it
(1) Pick a contrastive fact — "Fact: Michael Jordan plays the sport of", scoring against the logit difference between basketball and golf. (2) Score every layer-9 SAE feature at the subject token by attribution, taken as the feature's activation times the inner product of its decoder vector with the gradient of that logit difference at that position; this is a first-order estimate of what the feature contributes to the prediction. (3) Read the top feature's precomputed max-activating examples as its interpretation, and note that each feature is a thresholded affine function of the residual, so the same row yields a linear probe. (4) Repeat for baseball (Babe Ruth) and tennis (Serena Williams). (5) Then score attention heads by their direct logit effect from each sport feature's decoder vector, i.e. the sports-vs-sport contrast after applying the head's OV circuit and the normalised unembedding, and look at what the top heads promote. (6) For the training notes, compare current runs against the earlier recipe. (7) For ATP-style patching and self-repair they summarise others' findings rather than running their own sweep.

## What counts as an explanation here
A *component list keyed to features*: the top-attribution feature plus a handful of heads with large direct logit effect, each carrying an interpretation inherited from its dataset examples. Plus a linear probe (encoder row plus bias, thresholded) available for free. It is local and partial — it explains one behaviour on one example family, and it is a hypothesis generator rather than a circuit diagram; the authors present it as a way to "kickstart" circuit analysis, not to complete it.

## How they judged success
No quantitative benchmark, no baselines, no ablations. The judgements are: does the top-attribution feature's dataset examples look like the right concept; does the same procedure find the right sport for the other two athletes; do the top heads promote sport-specific words; and one prediction test — hypotheses about name-suffix features were checked by substituting first names and seeing whether the model's prediction changed exactly in the cases the hypothesis said it should. Training notes are judged by relative training loss and compute cost. Outside papers are judged on their own metrics (He et al. against patch-based circuit discovery; AtP* against activation patching on Pythia-12B).

## What they found
The top-attribution feature at layer 9 on the subject token recovers the sport — basketball words, then baseball and tennis — in all three cases, which also dates subject enrichment as done by layer 9. Many heads across layers 11, 13 and 14 produce large direct logit effects from those features, matching the "many subject heads with constructive interference" picture; the single special head of Nanda et al. is not the whole story. Unexpectedly, some pumping features keyed on name *fragments* (band-name-like or full-name associations) carried significant attribution on "Jordan" and "Ruth" but not "Williams"; the team predicted from this that first-name substitution would break the prediction only where that feature fired, and it did, which they read as further evidence for early-layer detokenization. On the training side, four earlier wins are withdrawn: ghost grads no longer reduce loss even at one layer and their implementation seems to cause loss spikes; Adam betas of (0, 0.9999) now match the defaults; and beta1 = 0 plus decoder-norm pruning are likewise no longer measurable wins over the newer recipe, which they have not yet published. From the outside work they give weight to the idea that the residual stream is "linearly represented" in a rounding-up-to-error sense rather than an L2 sense, which they say means dictionaries could want a thresholding activation instead of ReLU.

## Limits and open problems they name
The circuit recipe is demonstrated on one behaviour family with curated examples and no measured precision or recall against a ground-truth circuit. The better training recipe is explicitly withheld pending vetting. They also flag two structural problems with ablation-based measurement: attribution patching's linearisation fails where a nonlinearity right after the patched site has near-zero gradient (softmax; LayerNorm saturation in their own one-layer experiments), and cancellation between direct and indirect effects means one pass per layer is needed; separately, self-repair means ablation understates a component's role.

## What we take from it
- **Method (reusable, cheap):** attribution = activation × (decoder row · local gradient), computed per feature in the SAE basis. It is one backward pass and gives a ranked candidate set for any behaviour without building a dataset. This is exactly the "which written direction do I test first" step for a white-box model.
- **Method:** a feature's decoder row *is* a probe (encoder row + bias, thresholded). Any recovered dictionary hands us a population of probes for free; that is the cheapest possible prediction device.
- **Measure/warning:** ablation-based attribution is biased — LayerNorm rescaling after an ablation raises other components' logits, and Rushing & Nanda put LayerNorm at roughly 30% of observed self-repair on the highest-direct-effect tokens. Prediction under intervention must account for compensation, or it will understate every component's role.
- **Warning (weight-reading):** the name-fragment feature story is a clean case where a single layer-9 feature's attribution encodes an idiosyncratic "the model uses full names here" quirk. Good news for prediction (the hypothesis tested out), bad news for anyone reading a feature as a general concept.
- **Warning (patching):** suspect any attribution-patching result whose patched site is followed by softmax or a saturated LayerNorm.
- **Framing (from the reviewed superposition paper, not measured here):** "linearly represented" = linearly readable to within an additive error under sparsity, not close in L2 — a model can hold a number of properties near the parameter-count over log-properties limit. If that is the right notion, a ReLU dictionary looks at the wrong object and a rounding/thresholding activation would be the better decoder.

## Tags
unit: feature, head, direction, layer
form: description, dictionary, probe, graph
method: SAE, attribution, patching, ablation, probing
eval: ablation, patching, human-rating (visual inspection of max-activating examples), downstream-task (prediction check on name substitution)
goal: understanding, debugging
