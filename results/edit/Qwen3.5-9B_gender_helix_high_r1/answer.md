## What was changed

A single rank‑1 projection of the **post‑final‑norm feminine direction** out of every row of `lm_head.weight`:

$$W \leftarrow W\,(I - \alpha\, u u^\top), \qquad \alpha = 1.0$$

where `u` is the unit vector along the post‑final‑norm residual direction that separates feminine prompts from controls (feminine − control mean hidden state). Only `lm_head.weight` was modified.

## Why it works

- **The signal is concentrated there.** The post‑final‑norm input to `lm_head` has a dominant singular value ~178, pre/post‑RMSNorm cosine ~0.977, and scores +18 to +31 on feminine prompts versus −16 to −21 on controls (E30). That one direction is effectively the "feminine form" axis the unembedding reads.
- **Projecting it out of the unembedding blocks the output.** Removing `u` from all `lm_head` rows means the model can no longer place its logits along the feminine axis, so it stops emitting *actress, queen, princess, waitress, hostess, stewardess* and held‑out forms. E38 measured **T 6→1, H 10→2, C 9, K 3**, with coherent fluency.
- **It is minimally invasive.** Because the edit is rank‑1 and confined to the one direction that encodes the feminine concept, the rest of the unembedding is untouched — so plurals, past tenses, opposites, knowledge, and fluency survive. This is why it beats the alternatives: row‑zeroing (E32) broke generation format and fluency, and broad edits to `embed_tokens`/`o_proj`/`down_proj` (E34) only partially removed the ability.

The residual weakness is the few‑shot leak (**EX=4** in E38): worked examples re‑elicit the form. The attempted fixes — combining this projection with zeroing the feminine‑token `lm_head` rows (E39) or with negative mean‑hidden‑state suppression (E40) — aborted on a `model.norm` lookup error and CUDA OOM respectively, so that combination remains untested; the E38 projection is the best verified edit.