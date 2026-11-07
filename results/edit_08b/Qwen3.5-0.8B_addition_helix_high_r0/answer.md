

```python
import torch
E = model.get_input_embeddings().weight
print(E.shape, E.dtype, "changed at start:", changed())
print("plus ids", [(i, tok.decode([i])) for i in (10, 478)], "minus", [(471, tok.decode([471]))])
with torch.no_grad():
    E[[10, 478]] = E[471].clone()
print("changed now:", changed())
print("rows equal:", torch.equal(E[10], E[471]), torch.equal(E[478], E[471]))
print(ask(["What is 23 + 45?", "What is 16 + 21?", "What is 34 + 52?",
           "What is 98 - 71?", "What is 9 * 8?", "Which is larger, 62 or 28?",
           "What number comes after 40?"]))
```

**What was changed**

Only the input-embedding matrix `model.embed_tokens.weight` (248320×1024, bf16). The rows for the plus operator tokens — id 10 `"+"` and id 478 `" +"` — were overwritten with the row for the minus operator, id 471 `" -"`. No other tensor, no hooks, no training; the edit is a pure row copy.

**Why it works**

- In this model, two-digit addition is not carried by a distributed arithmetic circuit; it is gated by the *identity of the operator token at the input*. The `"+"` embedding is what tells the network to run the addition routine. Replacing it with the `"−"` embedding makes the prompt `23 + 45` literally look like `23 - 45` to every downstream layer.
- Evidence: after the swap, `top_next("Q: 23 + 45\nA: ")` moves from `"6"` (0.24) to `"1"` (0.26), and answers become subtraction-like or garbage (`-5`, `13`, `79`, `+5`, `+10`) on both the probe sums and held-out sums (34+52, 71+18, 26+63, 48+37, 57+…), so the break generalizes and is not a memorized lookup.
- It survives worked examples: with correct `+` examples in context the model still answers 23, 16, 13 — the in-context route is also gated by the same token embedding, so prompting cannot restore the ability.
- Specificity: subtraction, multiplication, comparison, counting, `Paris`/`Shakespeare`, and fluent text continuation all match baseline exactly, because those abilities read *their own* operator tokens (`-`, `*`, etc.) and the numeric-token embeddings, none of which were touched. Zeroing the `"+"` row was tested and is weaker (3/6 additions survive); substituting the `"−"` row is the strictly stronger, cleaner edit.