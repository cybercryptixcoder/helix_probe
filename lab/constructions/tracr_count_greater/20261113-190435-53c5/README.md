# Construction run `20261113-190435-53c5` on `tracr_count_greater`

*Written by `lab/results.py` from the files in this folder. Network: Compiled program G (1,322 weights). Known answer (never shown to a blinded reader): output i is the number of tokens greater than token i.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 47 steps, 8 submissions, 787 s, $0.181.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1 official: blinded, held-out. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 512 held-out inputs (a constant output: 0.6%). Construction length: 2,267 characters.

## The mechanism, in the reader's words

Task: at each position p=1..5 the network outputs the one-hot of count_p = #{j in 1..5 : t_j > t_p}. Mechanism: the only nonzero V-output is for token 4 (the BOS at position 0), so attention at position p adds attn0.out = w_p * u0 with w_p = attention weight on position 0 = 1/(1+count_p); attention is exactly uniform over {0} U {greater tokens}. The MLP turns w_p into a level (relu(base_k + g_k*w_p)), and the residual's logits are the one-hot of that level (embedding, u0, W_pos and b_out all project to 0 on W_U). The level is carried by a 4-coordinate code per position (level 4 = all zeros), and the logits are an affine image of that code, so argmax of [v0,v1,v2,v3,1-sum(v)] decides. At the embedding the token at each position is a 4-dim one-hot; one variable per position, since positions are independent parts of the site.

## The reader's final summary

**VERIFIED AND COMPLETE.** The network computes, at each position p=1..5, the one-hot of

`count_p = #{ j ∈ 1..5 : t_j > t_p }`

**Mechanism, stage by stage:**

1. **Embedding** — each position carries a 4-dim one-hot of its token (one compact variable per position; the 5 positions are independent parts of the site).

2. **Attention** — QK depends on tokens only (`b_Q=b_K=0`, position embeddings project to zero, `k_t = e_t`, `q_t ∝ Σ_{s∈A(t)} e_s` with `A(t)={s>t}`, i.e. a 0/1 score matrix with margin 100). So the attention is exactly uniform over `{0} ∪ {greater tokens}`. The only token whose V-output survives `W_O` is token 4 (the BOS at position 0), hence `attn0.out = w_p · u0` with `w_p = 1/(1+count_p)`. One scalar variable `inv = w_p` explains this stage and the residual after it.

3. **MLP neurons** — every neuron is an affine function of that one scalar: `relu(base_k + g_k·w_p)`, so `w_p` alone drives the whole MLP.

4. **Output** — the MLP output is a one-hot of the level `count ∈ {0..4}` per position; embedding, `u0`, `W_pos` and `b_out` all project to zero on `W_U`, so the logits are an affine image of a 4-coordinate level code (level 4 = all zeros), and the argmax of that code gives the decision at each of the five positions.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed |
| layer 0 attention | verified | attn0.out, resid0.mid |
| layer 0 mlp neurons | verified | mlp0.pre, mlp0.post |
| layer 0 output | verified | mlp0.out, resid0.post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `tok1` | 4 | embed |
| `tok2` | 4 | embed |
| `tok3` | 4 | embed |
| `tok4` | 4 | embed |
| `tok5` | 4 | embed |
| `inv` | 6 | attn0.out, resid0.mid, mlp0.pre |
| `lvl` | 20 | mlp0.post, mlp0.out, resid0.post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed` | 15 / 15 | 1.00 | 100.0% | 0.6% | 0.6% | yes |
| `attn0.out` | 5 / 5 | 1.00 | 100.0% | 0.0% | 0.0% | yes |
| `resid0.mid` | 5 / 20 | 0.33 | 100.0% | 1.0% | 0.0% | yes |
| `mlp0.pre` | 5 / 5 | 1.00 | 100.0% | 0.0% | 0.0% | yes |
| `mlp0.post` | 20 / 15 | 1.00 | 100.0% | 0.6% | 0.6% | yes |
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
| edit | `all variables` | `embed` | 9.2% | 1.8% | 0.0% | no |
| interchange | `inv` | `attn0.out` | 100.0% | 100.0% | 0.0% | yes |
| edit | `inv` | `attn0.out` | 100.0% | 8.3% | 0.0% | yes |
| interchange | `inv` | `resid0.mid` | 100.0% | 100.0% | 0.0% | yes |
| edit | `inv` | `resid0.mid` | 100.0% | 8.5% | 0.0% | yes |
| interchange | `inv` | `mlp0.pre` | 100.0% | 100.0% | 0.0% | yes |
| edit | `inv` | `mlp0.pre` | 100.0% | 7.8% | 0.0% | yes |
| interchange | `lvl` | `mlp0.post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `lvl` | `mlp0.post` | 69.9% | 5.1% | 68.5% | yes |
| interchange | `lvl` | `mlp0.out` | 100.0% | 100.0% | 100.0% | yes |
| edit | `lvl` | `mlp0.out` | 69.2% | 6.2% | 72.7% | yes |
| interchange | `lvl` | `resid0.post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `lvl` | `resid0.post` | 67.9% | 4.2% | 68.9% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py tracr_count_greater lab/constructions/tracr_count_greater/20261113-190435-53c5/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py tracr_count_greater lab/constructions/tracr_count_greater/20261113-190435-53c5/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py tracr_count_greater --steps 80   # a fresh run with the same settings (needs lab/.env)
```
