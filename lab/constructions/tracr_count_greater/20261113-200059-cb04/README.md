# Construction run `20261113-200059-cb04` on `tracr_count_greater`

*Written by `lab/results.py` from the files in this folder. Network: Compiled program G (1,322 weights). Known answer (never shown to a blinded reader): output i is the number of tokens greater than token i.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 33 steps, 5 submissions, 380 s, $0.085.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1.1: blinded, replicate B. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 512 held-out inputs (a constant output: 0.6%). Construction length: 2,091 characters.

## The mechanism, in the reader's words

Task: at content position j the network outputs the rank of its own token, class = #{k: t_k > t_j} (0 = has the largest token). Stage embedding: position p holds W_E[token]+W_pos[p], linear in a one-hot of the token. Stage layer-0 attention: Q reads the token value (query value v=min(token,3), BOS at position 0 has value 4), K is the token one-hot, so the score is 100*[v_key > v_query] and the softmax is exactly uniform over S_p = {k: v_k > v_p}; |S_p| = 1 + #{k: t_k > t_p} = n_p. V gives 1 on the BOS only and W_O is rank one, so attention adds o/n_p (o a fixed 19-vector). Stage layer-0 MLP: the MLP input at position p is affine in g_p = 1/n_p (the token/position part is annihilated by W_in), so the 12 ReLU neurons see only 1/n_p; their output writes, through W_out and W_U, exactly the one-hot of class n_p - 1 (W_U annihilates both the embeddings and o).

## The reader's final summary

**Mechanism found — the network computes, at each of the 5 content positions, the rank of that position's token among the 5 tokens** (class = number of tokens strictly larger than its own).

Stage by stage:

1. **Embedding** — `x = W_E[token] + W_pos[position]`. Since position 0 always holds the BOS token (4), each of the 5 content positions ranges over the same 4 tokens, so a one-hot code of the token linearly spans that position's 5 embeddings (5 variables of dim 4, 15 dims total for `embed`, replacing 114).

2. **Attention** — a hard comparison circuit: the query reads the token's *value* (`min(token,3)`; the BOS has value 4) while the key is the token's one-hot, so the score is `100·[v_key > v_query]` and the softmax is exactly uniform over the set `S_p = {k : v_k > v_p}` of tokens larger than its own. `V` is rank one (1 exactly on the BOS) and `W_O` is rank one, so the attention writes `o/|S_p|` for one fixed vector `o`. Hence the attention output carries only the six numbers `g_p = 1/|S_p|` (= 1/(1 + rank)) — this single 6-dim variable explains `attn0.out` (114 dims) completely.

3. **MLP neurons** — `W_in` annihilates both the token/position embeddings and `o`'s other components, so `mlp0.pre` at position p is an affine function of `g_p` alone (twelve ReLU features of 1/n_p); the same `g` variable explains all 72 pre-activations.

4. **MLP output** — the neurons' post-activation values add, via `W_out`, a vector whose image under `W_U` is exactly the one-hot of class `n_p − 1`. Because `W_U` kills the embeddings and the attention term, the logits are one-hots of the rank; the rank is read back out of `g` as `1/g − 1` and expanded to one-hot variables per position (5×5 dims) at `mlp0.out` and `resid0.post`.

The final construction reproduces the network's decisions on 100% of inputs (output R² = 1.000, KL 0) and every stage is verified at its sites, including interchange and the off-manifold partial tests.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed |
| layer 0 attention | verified | attn0.out |
| layer 0 mlp neurons | verified | mlp0.pre |
| layer 0 output | verified | mlp0.out, resid0.post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `tok1` | 4 | embed |
| `tok2` | 4 | embed |
| `tok3` | 4 | embed |
| `tok4` | 4 | embed |
| `tok5` | 4 | embed |
| `ginv` | 6 | attn0.out, mlp0.pre |
| `cls1` | 5 | mlp0.out, resid0.post |
| `cls2` | 5 | mlp0.out, resid0.post |
| `cls3` | 5 | mlp0.out, resid0.post |
| `cls4` | 5 | mlp0.out, resid0.post |
| `cls5` | 5 | mlp0.out, resid0.post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed` | 15 / 15 | 1.00 | 100.0% | 0.6% | 0.6% | yes |
| `attn0.out` | 5 / 5 | 1.00 | 100.0% | 0.0% | 0.0% | yes |
| `mlp0.pre` | 5 / 5 | 1.00 | 100.0% | 0.0% | 0.0% | yes |
| `mlp0.out` | 20 / 18 | 1.00 | 100.0% | 0.6% | 0.6% | yes |
| `resid0.post` | 20 / 22 | 0.71 | 100.0% | 2.3% | 0.6% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `embed` | 100.0% | 100.0% | 0.0% | yes |
| partial | `tok1` | `embed` | 100.0% | 1.2% | 0.0% | yes |
| partial | `tok2` | `embed` | 100.0% | 1.1% | 0.0% | yes |
| partial | `tok3` | `embed` | 100.0% | 0.6% | 0.0% | yes |
| partial | `tok4` | `embed` | 100.0% | 0.9% | 0.0% | yes |
| partial | `tok5` | `embed` | 100.0% | 0.9% | 0.0% | yes |
| edit | `all variables` | `embed` | 7.8% | 1.8% | 0.0% | no |
| interchange | `ginv` | `attn0.out` | 100.0% | 100.0% | 0.0% | yes |
| edit | `ginv` | `attn0.out` | 100.0% | 8.3% | 0.0% | yes |
| interchange | `ginv` | `mlp0.pre` | 100.0% | 100.0% | 0.0% | yes |
| edit | `ginv` | `mlp0.pre` | 100.0% | 8.2% | 0.0% | yes |
| interchange | `all variables` | `mlp0.out` | 100.0% | 100.0% | 100.0% | yes |
| partial | `cls1` | `mlp0.out` | 100.0% | 0.8% | 100.0% | yes |
| partial | `cls2` | `mlp0.out` | 100.0% | 0.7% | 100.0% | yes |
| partial | `cls3` | `mlp0.out` | 100.0% | 0.6% | 100.0% | yes |
| partial | `cls4` | `mlp0.out` | 100.0% | 0.8% | 100.0% | yes |
| partial | `cls5` | `mlp0.out` | 100.0% | 0.4% | 100.0% | yes |
| edit | `all variables` | `mlp0.out` | 18.1% | 6.6% | 23.5% | no |
| interchange | `all variables` | `resid0.post` | 100.0% | 100.0% | 100.0% | yes |
| partial | `cls1` | `resid0.post` | 100.0% | 0.8% | 100.0% | yes |
| partial | `cls2` | `resid0.post` | 100.0% | 0.7% | 100.0% | yes |
| partial | `cls3` | `resid0.post` | 100.0% | 0.6% | 100.0% | yes |
| partial | `cls4` | `resid0.post` | 100.0% | 0.8% | 100.0% | yes |
| partial | `cls5` | `resid0.post` | 100.0% | 0.4% | 100.0% | yes |
| edit | `all variables` | `resid0.post` | 17.3% | 5.8% | 24.5% | no |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py tracr_count_greater lab/constructions/tracr_count_greater/20261113-200059-cb04/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py tracr_count_greater lab/constructions/tracr_count_greater/20261113-200059-cb04/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py tracr_count_greater --steps 80   # a fresh run with the same settings (needs lab/.env)
```
