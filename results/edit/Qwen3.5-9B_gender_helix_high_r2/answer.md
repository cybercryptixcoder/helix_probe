## What was changed

Two weight tensors, both edited in place:

1. **`model.embed_tokens.weight`** — row swap: `" feminine"` ↔ `" masculine"` (plus a handful of related rows). The prompt's instruction token is literally re-pointed at the masculine embedding.
2. **`lm_head.weight`** — suppression of a **control-aware set of feminine output rows** (~120–260 rows in the successful runs): zeroing / negative projection so those rows' logits are driven down (E29 pushed `' madam'` to ≈ −32.5). The set is curated to hit *distinctive* feminine lexical pieces (`ess`, `ress`, `ister`, `atrix`, `witch`, `woman`, `queen`, `nun`, …) while **excluding shared subwords** (`er`, `st`, `le`, `ion`, `ent`, `un`, `man`) whose removal caused `A:`/`think` garbage and broken words (E31/E32/E36).

## Why it works

- The feminine-form ability is a **lexical token-mapping at the input/output interface**, not a grammatical computation. Swapping the input rows means the model reads "feminine" as "masculine"; zeroing the feminine output rows means the corresponding lexical pieces can't be produced. Together, the mapping is severed at both ends.
- Because the output edit targets only **distinctive feminine pieces** and leaves common subwords intact, unrelated morphology (plurals, past tenses, opposites), factual knowledge, and fluency are untouched — confirmed by CTRL 18/18, KNOW 9/9, coherent FLU in E30/E31/E33/E37.
- The target is **distributed across many token rows**, not one "feminine direction": an 8-row embedding-only swap did nothing (E33), and small curated `lm_head` sets (18 rows, E37) are confounded by failed resets, so hundreds of rows are needed for held-out/fresh generalization.
- **Caveat:** worked-example (ICL) feminine answers largely resist — adding first pieces of the surviving ICL leftovers (`mad`, `gentle`, `sorcer`, `mist`, `miss`, `nunn`) was the intended fix, but E34–E40 all died on CUDA-OOM resets, so that refinement is unverified.