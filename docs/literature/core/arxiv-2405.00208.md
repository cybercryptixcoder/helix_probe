# A Primer on the Inner Workings of Transformer-based Language Models

- **Key:** arxiv-2405.00208
- **Authors / organisation:** Javier Ferrando, Gabriele Sarti, Arianna Bisazza, Marta R. Costa-jussà (affiliations not stated in the pages read; funding from Spanish and Dutch research bodies)
- **Date:** 2024-04-30 (v3 2024-10-13)
- **Link:** https://arxiv.org/abs/2405.00208
- **Kind:** survey/agenda (technical primer)
- **Read from:** full text (HTML in two parts; component, method, mechanism and conclusion sections)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
A compact technical introduction to how interpretability researchers analyse decoder-only Transformer LMs: the
model's components in a common notation, the main analysis techniques, and the internal mechanisms found so far.
The goal is to give newcomers and practitioners a shared vocabulary and an honest picture of what is known and what
is still open, as a step toward interpretability that is useful for debugging and improving real models.

## What they studied
The literature on GPT-style LMs (GPT-2 Small and similar open models in most cited work). Units: attention heads
(QK and OV circuits), FFN neurons, the residual stream, directions/features, and multi-component circuits.

## How they did it
They write the model in the residual-stream view: each attention and FFN block reads from and adds to a running
representation, and the final state is projected through the unembedding to logits. Attention heads are split into
a QK part (where to attend) and an OV part (what to write); FFN neurons are treated as key–value memories. Methods are
grouped into two families. **Behaviour localisation:** input attribution (gradient and perturbation based; attention
weights alone are unreliable), direct logit attribution, causal interventions (activation patching with zero, mean,
resample or noise interventions) and circuit discovery (edge/path patching, automated variants). **Information
decoding:** probing (shows presence, not use), the linear representation hypothesis and linear steering/erasure,
sparse autoencoders (gated, TopK, JumpReLU variants), and vocabulary projections (logit lens, tuned lens,
Patchscopes). They then catalogue discovered mechanisms.

## What counts as an explanation here
Two complementary forms: a localisation (which components, edges or circuits carry the behaviour, validated by
intervention) and a decoding (what a representation encodes, as a direction, feature dictionary or vocabulary
projection). Mechanism descriptions such as the IOI circuit are partial, task-specific causal stories.

## How they judged success
They describe norms used in the literature: effect sizes under activation patching with a chosen ablation baseline,
faithfulness of circuits (citing work arguing faithfulness is not just overlap with a reference circuit),
completeness (from the IOI work), probe accuracy with the caveat that it shows correlation only. They stress
practical applicability — debugging and improving safety/reliability — as the ultimate test, and criticise
reliance on toy, functionally-grounded evaluations.

## What they found
Catalogue of known mechanisms: positional, previous-token, induction, copy-suppression and successor heads; early
FFN neurons detecting n-grams and later ones promoting/suppressing tokens, plus entropy and token-frequency neurons;
residual-stream norm growth, outlier dimensions and attention sinks on the first token. Multi-component: induction
(two composed heads), task/function vectors from in-context examples, in-context retrieval, the IOI circuit in GPT-2
Small (duplicate-token and S-inhibition heads, name movers, negative movers), the greater-than circuit (FFNs reading
year information from attention), factual recall (early-middle FFNs enrich the subject, attention moves relation
information, later heads extract the attribute), grokking as dense memorising circuits being replaced by sparse
generalising ones. Fine-tuning mostly preserves circuit function; circuits overlap and recur across languages.

## Limits and open problems they name
Attribution methods disagree with each other; LM self-explanations are plausible but often unfaithful;
interventions trigger second-order effects such as self-repair; SAE evaluation and architecture comparison are open;
circuit discovery does not yet scale to large models. Future directions: features and natural-language
explanations rather than raw components, LMs as verbalisers, circuit discovery over interpretable features, open
access to model internals.

## What we take from it
- **Baseline of what is solved:** a reconstruction of a small transformer should at least recover known motifs
  (induction, previous-token, copy suppression, IOI-style name movers); these are natural sanity targets.
- **Weight-level handles:** QK/OV decomposition and the residual-stream/unembedding view are the standard way to read
  head behaviour directly from weights.
- **Method choice:** specify the ablation baseline (zero/mean/resample) explicitly; expect self-repair to distort
  single-component ablations.
- **Warning:** probes and attention weights show correlation, not use.

## Tags
unit: head | neuron | direction | circuit | layer
form: graph | direction | dictionary | probe
method: attribution | patching | ablation | probing | SAE | steering
eval: patching | ablation | faithfulness | completeness
goal: understanding | debugging | science
