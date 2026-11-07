The final state is verified and correct.

**What I changed**

I edited exactly one tensor — the input embedding matrix `model.embed_tokens.weight` — and nothing else, in two ways:

1. **Untied the output head.** `lm_head.weight` originally shared storage with `embed_tokens.weight`. I replaced it with a clone of the original values so the output projection is untouched. (Without this, editing the embedding also silently rewrote the logits, which is what broke knowledge and fluency in my first attempts.)

2. **Blended the plus-sign input embeddings toward the minus-sign embeddings.** For the two tokenizations that carry the addition operator in the graded format — `" +"` (id 478, used in `What is 16 + 21?`) and `"+"` (id 10, the unspaced form) — I set
   `emb[plus] = 0.4·emb[plus]_orig + 0.6·emb[minus]`
   using the matching subtraction tokens (`" -"` id 471, `"-"` id 12). All other rows are bit-identical to the original.

**Why it works**

- In this question format the plus token is the *only* input feature that distinguishes addition from subtraction; the numbers and the surrounding prompt are shared. Moving that one embedding 60% of the way toward the minus embedding makes the model's internal operator state read as subtraction, so it computes `a − b`. Every two-digit sum is now wrong (0/80 random pairs, and still ≈0 even with 3, 5, or 10 worked examples in the prompt — the ability does not come back).
- Because only two embedding rows change and the output head is decoupled, everything that doesn't route through the plus token is exactly the original model. I confirmed this directly: subtraction 40/40, comparison 25/25, counting 25/25, knowledge and free-form generation identical to baseline, and multiplication *identical answer-for-answer* to baseline (the two "misses" at 9×11=100 are a pre-existing model error, present before my edit).
- The blend is deliberately partial rather than a full swap: a full copy breaks addition but also perturbs the model's notion of the symbol itself and its small-number arithmetic. 0.6 is past the collapse threshold (0.5 already breaks addition) while leaving the rest of the model untouched.

The graded examples behave as required: the six addition questions return wrong values (`5, 13, 79, 10, 34, 11`), while all subtraction, multiplication, comparison, counting, knowledge, and fluency examples match the original model.