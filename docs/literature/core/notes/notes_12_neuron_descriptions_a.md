# Notes: neuron descriptions (batch a)

**What an explanation is.** Across this batch an explanation is a compact rule over inputs that says when a unit fires:
a concept-logic formula (arxiv-2006.14032), a free caption (arxiv-2201.11114), or an LLM-written sentence
(openaipublic-neuron-explainer-paper, transluce-neuron-descriptions, arxiv-2501.18838). The trend is from "label that
matches top exemplars" toward "explanation as an executable predictor of activations". Only arxiv-2401.12181 explains
neurons partly from weights (vocabulary projections, neuron-to-head composition) and by role (entropy, attention
deactivation), not only by input pattern.

**How success is measured.** Three tiers recur. (1) Agreement: IoU with concept masks, BERTScore against human labels,
human preference. (2) Simulation: correlation between activations predicted from the explanation and true activations,
on top plus random excerpts (openaipublic, transluce). (3) Functional substitution: put the predicted activations back
into the network and measure output change, as JSD normalised by mean ablation (openaipublic) or cross-entropy versus
zero ablation (arxiv-2501.18838). Tier 3 is much harsher: correlation 0.9 gives ablation score 0.3-0.6, and a whole
layer of LLM-simulated latents does about as badly as deleting the layer.

**Recurring baselines and controls.** Unigram baselines from weights (W_E times W_in) and token lookup tables; random
units or random directions; mean and zero ablation; random-rotation baselines for privileged-basis claims
(arxiv-2401.12181); synthetic neurons with planted ground truth (openaipublic puzzles).

**Shared failure mode.** Explanations are too broad. Top-activation sampling under-samples false positives; 86% of
neurons had generated false positives (openaipublic); about 80% specificity breaks sparse-code reconstruction
(arxiv-2501.18838); PMI selection (arxiv-2201.11114) and revision loops are partial fixes. Scores also rise with
best-of-k search against a trained simulator (transluce), which risks optimising the scorer, not understanding.

**Open problems.** Polysemanticity and non-canonical units (only 1-5% of neurons recur across seeds, arxiv-2401.12181);
correlational, not mechanistic, explanations that may fail off-distribution; explainer as bottleneck rather than
scorer; cost.

**For a predictive white-box model from weights.** (a) Adopt the substitution test (arxiv-2501.18838,
openaipublic ablation score) as the headline metric, with zero/mean ablation and the weight-unigram baseline as floors.
(b) Our model must predict where units are off, and calibrate magnitudes, not just name what they detect. (c) Weight-only
signatures (vocab-projection skew/kurtosis, w_in/w_out cosine, bias, norm) already predict neuron roles, and layer norm
must be modelled (entropy neurons). (d) Mu and Andreas explicitly pose our question, whether explanations can serve as
drop-in replacements for neurons, and it remains unanswered positively.
