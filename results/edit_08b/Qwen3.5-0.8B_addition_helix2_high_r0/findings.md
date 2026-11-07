## Findings

1. **Baseline: two-digit addition is fully intact.** Before any edit the model scores 1.00 on plain two-digit `+` questions, and 1.00 on the same with 3 or 5 worked examples, alongside sub/mul/cmp/cnt/gk = 1.00 (E4, E5, E8, E10, E11, E12 baselines).

2. **The ability lives in the input embedding row of the `+` token (id 478, `Ġ+`), not in downstream computation.** Overwriting that single row is sufficient to change the behavior completely; no MLP/attention weights need to be touched (E4, E5, E8).

3. **A semantic substitution (`+` → ` the`, row 478 ← 279) kills plain addition (1.00 → 0.00) but only partially kills it with worked examples (0.20, and 0.12 in a second run)** — i.e. examples can partly route around a "meaningless" replacement (E5, E6).

4. **A sign-flip substitution (`+` → `-`, row 478 ← 471) kills addition in every form tested:** plain 0.00, with 5 examples 0.00, with 3 examples 0.00, and the grading-style questions 0.00, on multiple fresh held-out sets (E8, E10, E11, E12).

5. **Worked examples do not restore the ability after the `-` substitution** (ex5 = ex3 = 0.00), unlike the `the` substitution where they recovered ~12–20% (E8, E11, E12 vs. E5, E6).

6. **`-` is the best of the four candidate replacements tested (`the`, `minus`, `star`, `and`):** all four drop plain addition to ≤0.07, but only `minus` also drops the with-examples variant to 0.00; `star` yields concatenation-like products and `the` leaves a residual 0.12 (E6).

7. **The edit is essentially perfectly selective.** With only row 478 changed, subtraction, multiplication, comparison, counting and general knowledge all stay at 1.00, and the fluency logprob is bit-identical (diff = 0.000000) with identical top-next tokens (` jumps`, ` is`, …) (E8, E10, E11, E12).

8. **The kill extends to unspaced `+` only if the bare `+` row (id 10) is also replaced.** With 478 alone, `23+45` still scores 1.00; adding `emb[10] ← emb[471]` drops unspaced addition 1.00 → 0.00 with no other metric moving (E10, E12).

9. **"plus"-phrased addition is a separate pathway:** it survives the symbol edit (plus = 1.00) and only breaks when the `Ġplus` row (id 5346) is replaced, which costs a little general knowledge (gk 1.00 → 0.80) — so it is not needed for the grading format (E9).

10. **Post-edit answers are not near-misses of the sum:** they are operand copies/concatenations (`2345`, `16`, `89`, `51`) or minus-flavored results (`-5`, `13`, `79`, `-10`), confirming the operation itself is gone rather than merely miscalibrated (E4, E8, E10, E11, E12).

11. **The embedding is reachable as `model.embed_tokens.weight`, shape (248320, 1024), via `named_parameters()`; `model.embed_tokens` as an attribute does not exist** — an earlier attempt failed on exactly that (E7), and was fixed in E8.

12. **Only one parameter tensor ends up different from the original:** `model.embed_tokens.weight` (E8, E10, E11, E12); a two-tensor variant that also edited `lm_head.weight` zeroed addition but produced degenerate answers, so it was unnecessary (earlier run, "BEST").