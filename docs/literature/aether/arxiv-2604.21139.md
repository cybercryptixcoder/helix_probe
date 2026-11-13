# Slot Machines: How LLMs Keep Track of Multiple Entities

- **Key:** arxiv-2604.21139
- **Authors / organisation:** Paul C. Bogdan (Anthropic Fellows Program), Jack Lindsey (Anthropic)
- **Date:** 2026-04-22
- **Link:** https://arxiv.org/abs/2604.21139
- **Kind:** paper
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Binding is the problem of associating features with the entity that owns them ("the square is red" must not be representable as "the square is blue"). Models clearly do some of this, but we do not know how many entity bindings a single token position can carry, or whether everything decodable from a position is actually *used* by the model. The authors probe for multiple simultaneous binding representations and then test, with interventions, which of them downstream computation reads. The larger aim is the core of our project: separating information present in the activation from information causally used by the network.

## What they studied
Qwen3-32B by default (plus Qwen3-0.6B, Llama-3.3-70B-Instruct for slot-count robustness, and a sweep of open and closed models for a behavioural task). Prompts: 10,000 passages of 8 entities x 4 sentences, each entity implying one of 15 personality traits; residual stream at sentence-ending period tokens (layer 45 of 64). Unit of analysis: *slots* — distinct linear decoders for the same information at different positions.

## How they did it
Probing: a mixture-of-experts probe with K=4 shared linear trait classifiers plus, per entity, a routing layer that softmaxes a token's activation into slot weights; trait prediction for entity e at token t is the routing-weighted sum of slot logits. Every activation is labelled once per entity seen so far, so a token must represent several entities at once; slots and routers are trained jointly, 80/20 split by prompt. Identified slots: a "current-entity" slot (entity's own tokens) and a "prior-entity" slot (the immediately preceding entity's traits, copied onto the next entity's tokens). Then functional tests with interventions on 200-trial synthetic sets: (a) entity-level induction — patch key/value vectors between a target prompt and a source prompt where entities are swapped, and see if the "who came after X" answer follows; (b) conflict detection — steer with contrast vectors built from mean activations conditioned on current vs prior trait (v_prior(x) = E[h | previous entity has trait x]), applied at MLP input versus key/value of the trait token; (c) trait-presence detection and (d) name-trait binding retrieval, patched on current- versus prior-entity tokens; (e) a two-subject-one-object grammar task ("Alice prepares and Bob consumes food") where correct answering requires two bindings on one token, with separated and flipped controls.

## What counts as an explanation here
A structural account of representation: which linear directions carry which entity's attributes where, orthogonal between slots, plus a functional map of which router/reader uses each slot. It is partial — the slot identity is a decoder, and causality is established by patching/steering, not by a circuit.

## How they judged success
Held-out probe accuracy heatmaps (entity x position) with a clear diagonal and subdiagonal; slot weight correlation between current and prior slots plus RSA of trait relations (second-order correlation); patch effects on the source-answer and target-answer next-token logits; steering effects compared for positive vs negative direction (to cancel indiscriminate disruption); and accuracy on the dual-binding task versus its two controls. Everything is prefill-controlled with a single next token as the measured variable.

## What they found
Traits are decodable on later tokens, not just the entity's own; accuracy is high for the immediately previous entity and drops for entities further back, except the *first* entity, which persists deep into the passage. The current and prior slots are nearly orthogonal (weight correlation r=.11; trait-structure correlation r=.34), i.e. genuinely different representations rather than rotations. In user/assistant dialogues, an extra slot appears keyed to speaker role but relativistically — the same slot serves the user's earlier entity on user turns and the assistant's on assistant turns; the user's information persists somewhat longer. Patch effects show prior-entity info drives entity-level induction (and key patching beats value patching, as expected if it is used as a key) and MLP layers integrate prior- and current-entity directions to detect trait conflicts (steering at key/value did nothing), yet the same prior-entity representation is *not* used for trait-presence detection or name-trait binding — patching it there had essentially no effect although a probe decodes it. The dual-binding grammar task: Qwen3-32B barely above chance (0.5), larger open models regularly wrong, and even strong ones only approach 75% which is exactly the score of "encode one binding, guess the other" — so a cutoff rather than success; frontier closed models (Claude Opus 4.5, Gemini 3 Pro) succeeded most consistently, and the separated/flipped controls were near perfect for most models, isolating the single-token multiplexing pressure as the cause.

## Limits and open problems they name
One model family in depth; slot count fixed at 4; no chain-of-thought, so budgets might look different if the model can re-mention entities; only adjacent entities really represented, so "how many bindings per token" is answered for two; alternative mechanisms for the dual-binding task (conjunctive encoding, slot-based, or distributing bindings across adjacent tokens) are not distinguished; SAE auto-labelling that uses maximally activating context may systematically mislabel prior-entity features.

## What we take from it
Method: the multi-slot MoE probe is a cheap general construct for "the same information in several places" — reuse whenever a representation could exist in more than one role. Measure — the key one: the probe-plus-patch contrast (decodable but not patch-effective = unused) is exactly the gap a predictive white-box model must close, and the authors' "blindsight" framing names it. Warning: do not infer use from decodability; the prior-entity slack is a concrete counterexample, and it also predicts a specific capability failure (dual binding) rather than a vague one. Framing: adjacent-entity slots are a plausible substrate for tracking what the user believes versus what is true — a direct candidate for a sycophancy/deception readout. Shortcut: mean-activation conditioned on prior trait gives ready-made prior-slot steering vectors without training.

## Tags
unit: direction | feature | layer | whole-model
form: probe | direction | steering
method: probing | steering | patching | ablation | other
eval: patching | ablation | prediction/simulation | downstream-task
goal: understanding | safety/auditing | debugging
