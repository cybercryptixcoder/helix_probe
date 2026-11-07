## What was changed

One tensor: `model.embed_tokens.weight`. The input-embedding rows for the plus token — id 10 (`"+"`) and id 478 (`" +"`) — were overwritten with the rows of the multiply token — id 9 (`"*"`) and id 348 (`" *"`). Nothing else in the 8.95B parameters was touched (`changed()` returns only `model.embed_tokens.weight`).

## Why it works

- **The plus row is the locus of the addition behavior.** It is the only operator token unique to addition, and it is read at the very first layer, so redirecting it changes how every later layer interprets the expression. Evidence: swapping `+`→`−` alone dropped addition to 0/10 with subtraction-like answers (`-22`, `-5`, …) while sub/mul/cmp/cnt stayed 5/5 and fluency was byte-identical (E8, E10). Swapping `+`→`*` likewise gives 0/5 fresh addition, now with product-like answers (E12, E14).
- **Why `*` and not `−`.** The minus row leaves addition recoverable from in-context examples: few-shot came back to 3–4/5 (E10, E12, E13). The multiply row does not — few-shot stayed 0/5 in E13 and E14 — because it maps the operator to a *different* arithmetic operation rather than to the nearest neighbor that worked examples can re-anchor. So the model still parses "23 + 45" as a well-formed arithmetic expression, it just computes the wrong operation, which is exactly the failure mode we want and is robust to priming.
- **Why not zeroing, negation, or a random row.** Those leave addition 2/5 fresh and 5/5 few-shot (E8, E12): a zeroed or noise row doesn't assert any operator, so the surrounding tokens and the few-shot pattern reconstruct the addition prior. A structured, high-information replacement is required.
- **Why the rest survives.** Subtraction, multiplication, comparison and counting use their own operator token rows, which are untouched; the swap only changes the vector that the `+` token contributes, so the residual stream for any non-addition prompt is unchanged. Fluency and knowledge answers were identical to baseline (E10, E14), consistent with a single-token-row edit.

Final state: `+`/` +` rows = `*`/` *` rows; fresh addition 0/5, few-shot addition 0/5, sub/mul/cmp/cnt 5/5, fluency and knowledge unchanged.