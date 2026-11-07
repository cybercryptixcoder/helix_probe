**Findings**

1. Two-digit addition in Qwen3.5-0.8B is carried by the input embedding of the operator token, not by a distributed arithmetic circuit: replacing the `model.embed_tokens.weight` rows for `"+"` (id 478, `" +"`) with the rows for `"−"` (id 471, `" -"`) drops ADD from 6/6 to 0/6 while SUB stays 5/5, MUL 3/3, CMP 3/3, CNT 3/3 (E10, E11).

2. The edit is a pure weight edit — `changed()` reports only `model.embed_tokens.weight` (plus `lm_head.weight`, since embeddings are untied: `lm []`, `tied False`) — no hooks or activations are needed at inference (E10, E11).

3. The break generalizes to unseen sums: held-out 34+52, 71+18, 26+63, 48+37 go from correct (86, 89, 89, 85) to wrong (18, 53, 37, 11) after the swap (E11).

4. The break shows up in the model's next-token distribution before any answer is generated: `top_next("Q: 23 + 45\nA: ")` moves from `"6"` (0.240) to `"1"` (0.262), and `top_next("Q: 34 + 52\nA: ")` loses `"8"` (0.370) from the top (E10, E11).

5. The break survives worked examples: with correct sums as in-context examples the model still answers 23, 16, 13 instead of 68, 37, 67 (E10), i.e. the ability does not come back from prompting.

6. Everything else is untouched by the swap: SUB 5/5, MUL 3/3, CMP 3/3, CNT 3/3, `Paris`/`Shakespeare` knowledge, and fluent continuation of ordinary text all match baseline exactly (E10, E11).

7. Swapping to the minus row is strictly stronger than zeroing the operator embedding: zeroing the `"+"` rows still leaves ADD at 3/6 (37, 112, 56 survive) and only shifts the top next-token to `"2"` (E7), whereas the swap gives 0/6 (E10).

8. The failure mode is "read as subtraction or garbage", not "refuse": answers become `+5, 13, 79, +10, 34, 11` (E10) / `-5, 13, 79, -10, 34, 11` (E11), consistent with the model literally seeing `23 - 45`.

9. The residual-direction route is unsupported by the evidence: the layer-wise add-vs-sub ablation and orthogonalization experiments (E4, E5, E6) all crashed — `IndexError` because `resid()` returned shape `(1, 16, 1024)` instead of `layers+1`, `RuntimeError: addmv ... Float, BFloat16, and Float` in the forward hooks, and a baseline that scored 0/0/0/0/0 while the hook was installed — so no causal layer-3 direction was ever demonstrated, and no permanent projection edit was ever produced.

10. The embedding-row swap is the only intervention in the record that both removes the target and leaves the graded side abilities at baseline, and it is re-appliable cleanly from `reset()` (E11); the one attempt to re-run it with fresh sums and leave the model edited (E12) crashed on `model.embed_tokens` after the baseline was already measured, so the final state must be re-established by applying the swap again.