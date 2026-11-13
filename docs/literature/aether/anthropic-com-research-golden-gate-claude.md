# Golden Gate Claude

- **Key:** anthropic-com-research-golden-gate-claude
- **Authors / organisation:** Anthropic (interpretability team; unsigned post accompanying Templeton et al., *Scaling Monosemanticity*)
- **Date:** 2024-05
- **Link:** https://www.anthropic.com/research/golden-gate-claude
- **Kind:** blog/research post
- **Read from:** full text of the post (~3.1k characters — everything the page carries, plus its closing note that the model is offline). The underlying numbers live in the paper already entered as `anthropic-com-research-mapping-mind-language-model` and in `core/tcpub-2024-scaling-monosemanticity`; this post gives none, and **no figure in this entry is new** — it is a demo described against that setup.
- **Relevance to us:** 2 (useful) — not for method (identical to the paper) but as the clearest public statement of *what a single-feature clamp looks like from outside*, which is the survival test our own white-box predictions have to pass.

## What they wanted, and why

Having found millions of namable directions in a production model, the team wanted the sceptical reader to feel the difference between a direction that is *read out of the weights* and a behaviour that is *asked for in the prompt*. The demo isolates one concept — the Golden Gate Bridge — amplifies it, and releases the resulting model for a day so anyone can poke it. The argument is about the strength of the evidence, not about bridges: if the only way to produce this behaviour were a system prompt or fine-tuning, the demonstration would prove nothing, so the post spends its rhetoric distinguishing surgical activation edits from both. It is also a soft-launch for the safety framing that the paper argues at length.

## What they studied

Claude 3.0 Sonnet with middle-layer residual-stream sparse autoencoders, exactly as in the paper (same model, same dictionary family, same clamping machinery) — so the studied object is one feature, the Bridge feature, inside a dictionary of millions, together with its multilingual and multimodal firing pattern. No new model, no new dictionary, no retraining.

## How they did it

The mechanism is the clamping procedure from the paper, described here for a lay reader: decompose the residual stream into SAE reconstruction plus reconstruction error, replace one feature's value inside the reconstruction with a large positive constant, and let all downstream layers run on that modified state at every token of every prompt. The post is explicit that the edited quantity is the model's internal activation for one concept, that no text is added to the input, and that no gradient or extra data is used. Behaviour is then characterised by example: requests about spending money, love stories, and self-description all get answered through the bridge. The only real "setup" beyond that is the release itself — an interactive model behind a badge on the consumer product, with a warning that a single-feature amplification can make outputs jarring.

## What counts as an explanation here

A single named direction plus a causal story: *this direction, clamped, makes the model behave as if the concept is present*. Partial by construction — a worked instance of the dictionary-plus-steering picture, not a circuit and not a full account of why bridge content dominates unrelated answers. In the paper's two-obligation vocabulary, it is an *influence* demonstration with the *specificity* side asserted qualitatively (the feature fires on mentions and pictures of the landmark) rather than scored.

## How they judged success

No metrics, baselines or ablations in the post. Success is narrated rather than measured: the model mentions the bridge in replies to unrelated prompts, and a handful of illustrative completions are quoted. There is no dose–response curve here, no comparison against a matched-strength control feature, and no test of whether an unamplified model given "talk about bridges" as a system prompt is distinguishable in output distribution — the paper has the numbers, the post has only the phenomenology.

## What they found

Amplifying one direction is enough to dominate behaviour across unrelated tasks: budgeting advice becomes a bridge toll, a love story becomes a car longing for the bridge, self-description becomes the bridge itself. The post's substantive claim beyond the anecdote is negative and worth keeping — this is neither role-play requested in the prompt nor a fine-tuned black box, and the same handle works on safety-relevant concepts (dangerous code, criminal activity, deception), which is offered as a route to safer models rather than as a present capability.

## Limits and open problems they name

The post's own limits are candid and mostly about interpretation of the demo: the model "might behave in unexpected—even jarring—ways", it was available for a 24-hour research window and is now offline, and the safety sentence is hedged with "with further research" — the bridge demo is not evidence that safety-relevant features can be controlled safely. Everything about coverage, dead features, shrinkage and cross-layer superposition is deferred to the paper (see entry 65) and none of it is addressed here.

## What we take from it

- **Framing, worth copying:** the three-way contrast *prompt ≠ fine-tuning ≠ activation edit* is the cleanest defence of why white-box intervention is a different kind of evidence. When we report that our model predicts an intervention's effect, we should be able to say the same: no text was added, no weights were changed, one internal quantity was set and the rest of the network ran.
- **Warning — the demo has no dose axis.** A single amplified value cannot distinguish "the feature is the concept's causal handle" from "any large perturbation along a well-represented direction derails the model". Our prediction claims need the monotonicity check the paper's ±10×/±100× range implies; the post's anecdotes would look identical under a saturating artefact.
- **Warning — release mechanics contaminate the evidence.** Users knowing the model is "Golden Gate Claude" will elicit bridge talk by conversational priming, so the public demo cannot separate the clamp from the expectation. Any human-in-the-loop evaluation we run needs blind prompts or a matched-control model behind the same interface.

## Tags

unit: feature | direction | layer
form: direction | description | steering
method: SAE | steering | ablation | decomposition
eval: downstream-task | human-rating
goal: understanding | control/editing | safety/auditing
