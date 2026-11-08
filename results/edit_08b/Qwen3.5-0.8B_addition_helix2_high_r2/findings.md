## Findings

- **Baseline is clean and the target/control split is real.** Before any edit, ask() scores 20/20 additions, 10/10 subtractions, 8/8 multiplications, 8/8 comparisons, 8/8 counts, with sensible generation and correct knowledge answers (E1, E3, E4, E5, E6).

- **Addition is not linearly separable from subtraction in the residual stream.** The add-minus-subtract mean-difference direction is small in early layers, peaks only at ~layers 10–20 of 28, and cos(add_mean, sub_mean) stays >0.9 throughout, i.e. the two abilities share nearly the same direction (E1).

- **A rank-one residual-direction ablation was never actually tested.** The only attempt crashed (`KeyError: 0`) before applying anything, leaving 0 tensors changed, so there is no evidence that mid/late-layer direction ablation removes addition without collateral damage (E2).

- **The separable handle is the input token, not a direction.** "+" tokenizes as its own token (id 478, also 10 in the no-space form) and "-" as 471; addition questions are the only ones containing it (E3, E4).

- **Zeroing the "+" embedding row is a partial edit.** It drops addition to 3/6 while sub/mul/cmp/cnt stay perfect — enough to show the token embedding matters, not enough to remove the ability (E3).

- **Swapping the "+" embedding row for the "-" embedding vector removes addition.** Addition falls to 0/12 (E4), 0/12 with 1/3 unspaced (E5), and 1/20 on a larger battery (E6), with wrong answers that look like a−b (e.g. 47+38 → 9, 23+45 → 23) (E3, E4, E5, E6).

- **The swap leaves every control ability intact.** Subtraction 6/6–10/10, multiplication 4/4–8/8, comparison 4/4–8/8, counting 4/4–8/8 across all replication batteries (E4, E5, E6).

- **Fluency and knowledge are byte-identical after the swap.** Ordinary-text logprobs match the base exactly (max diff 0.000 on 4 and 6 probes), and generation and knowledge answers are unchanged (E4, E5, E6).

- **Worked examples do not restore the ability.** With 2, 4, or 6 worked addition examples in the primer, addition still fails (e.g. 19, 12, 31, 46 vs gold 46, 84, 83, 82), while worked-example subtraction still succeeds (E3, E4, E5, E6).

- **The edit is symbol-specific, not concept-specific.** Alternative phrasings that avoid the "+" character ("What is 23 plus 45?", "Add 23 and 45.") still answer correctly (68, 68, 85) after the swap (E6) — the model's addition circuitry survives; only the "+"-token route into it is destroyed.

- **The change touches two tied tensors.** `changed()` reports `model.embed_tokens.weight` and `lm_head.weight`, consistent with tied input/output embeddings, and the edit is one row overwrite with no training (E4, E5, E6).