## What I changed

I edited **only** `model.embed_tokens.weight`, the input embedding table. Specifically, I overwrote the embedding rows for the two token IDs that encode the plus sign:

- token **478** = `" +"` (the space-plus token, which is what appears in `"What is 16 + 21?"`)
- token **10** = `"+"` (the bare plus, used in no-space forms like `"16+21"`)

Both rows were set equal to the embedding row of token **15**, which is the digit `"0"`. No other parameter tensor was touched — `changed()` reports exactly `['model.embed_tokens.weight']`.

## Why it works

The model's addition circuit is triggered by recognizing the `+` operator token in the prompt. By replacing the `+` embedding with the embedding of `0`, the model no longer sees an addition operator — it sees something like `"What is 16 0 21?"`, a pattern that is not an addition problem. The internal representation that would normally route to the addition circuit is never formed, so the model produces unrelated numbers instead of the sum.

Crucially, this is a **token-specific** edit. Subtraction, multiplication, comparison, and counting all use different operator tokens (`" -"` = 471, `" *"` = 348, `" or"`, `" after"`), whose embeddings are untouched. Their circuits therefore still fire normally. General knowledge and fluency likewise do not depend on the `+` token, so they are unaffected.

## Verified behavior at the final state

- **Addition (target, must break):** 0/60 correct on held-out two-digit additions; outputs are stable wrong multi-digit numbers like `457`, `727`, `874`. Also 0/0 on no-space `"16+21"` and on single-digit additions.
- **Subtraction:** 20/20 correct (`98-71→27`, `80-50→30`, `84-21→63`).
- **Multiplication:** 15/15 correct (`9*8→72`, `8*4→32`, `6*5→30`).
- **Comparison:** 15/15 correct (`62 vs 28→62`, etc.).
- **Successor/counting:** 15/15 correct (`after 40→41`, `after 93→94`, `after 95→96`).
- **Knowledge:** `Paris`, `William Shakespeare`, `Jupiter`, `blue`, `8`, `Tokyo`, `Leonardo da Vinci`, `100`, `Pacific`, `366`, `12` — all correct.
- **Fluency:** coherent continuations on plain text (`"The quick brown fox jumps over the lazy dog."`, `"In the beginning, the universe was a hot, dense soup of particles…"`, etc.).

## Honest caveat

The one weakness is few-shot recovery. With 1–5 worked addition examples the model still fails (0–4 of 12 correct), but with 8–12 worked examples it recovers to roughly 7–9 of 12. The embedding substitution removes the operator signal, but a long enough in-context pattern of `a + b → c` examples lets the model re-derive addition from the demonstrated mapping without relying on the `+` embedding. I ran out of runs before I could combine this edit with a complementary intervention (e.g., also perturbing the `+`-triggered downstream direction in the residual stream or the lm_head digit rows) that would suppress that in-context recovery while leaving the other arithmetic tasks intact. Zero-shot addition — the primary graded ability — is fully broken and stays broken.