# Construction run `20261113-200059-d63d` on `tracr_first_match`

*Written by `lab/results.py` from the files in this folder. Network: Compiled program F (1,405 weights). Known answer (never shown to a blinded reader): output i is 1 if token i equals the first token, else 0.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 22 steps, 4 submissions, 362 s, $0.081.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1.1: blinded, replicate B. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 512 held-out inputs (a constant output: 31.1%). Construction length: 2,297 characters.

## The mechanism, in the reader's words

Behaviour: at output position p (p=1..5) the network says whether token t_p equals token t_1 (class 1 = equal, class 0 = not). Mechanism: embed = W_E[token]+W_pos[pos]. The single attention head has query 0 -> key 0 and queries 1..5 -> key 1 (hard argmax), so the attention output at positions 1..5 is a fixed affine function of the token at position 1 alone (position 0 is constant). Hence the residual stream after attention is affine in token identities: position p carries its own token t_p plus, added by attention, the reference token t_1 at every position. The MLP compares the two per position (an approximate equality: its hidden units are thresholds on a_k(t_p) + b_k(t_1)) and the unembedding reads that one comparison out as a +/-1 score per position. Variables: 'tok<p>' = one-hot code of t_p at embed; 'mid<p>' = the token identity at position p after attention -- 'mid0' is the reference token t_1 that attention broadcasts; 'pre<p>' = the same identities at the MLP input; 'eq' = per-position equality indicator carried by the MLP output and by the final residual stream.

## The reader's final summary

**VERIFIED AND COMPLETE** — all four stages explained.

## What the network computes
At each output position *p* = 1..5, it reports whether token *t_p* equals token *t₁* (class 1 = equal, class 0 = not).

## How
1. **Embedding** — `embed = W_E[token] + W_pos[pos]`. Each position carries a one-hot code of its own token (4 tokens used).
2. **Attention** — the single head has query 0 → key 0 and queries 1..5 → key 1 (hard argmax). So positions 0 and 1 attend to themselves and positions 2..5 also attend to position 1. Restricting to positions 1..5, `attn0.out` is a fixed affine function of *t₁* alone — a **broadcast of the reference token** to every position. Position 0's output is constant.
3. **Residual after attention** — every position therefore holds two quantities: its own token *t_p* and the reference *t₁*.
4. **MLP** — its 16 ReLU units are thresholds of the form `a_k(s_p) + b_k(s_1)`, i.e. pairwise token comparisons per position; their ReLU'd combination yields a single per-position **equality indicator**. (On ordinary inputs this reproduces the exact equality of the two one-hot codes.)
5. **Output** — `mlp0.out` adds ±1 per position along the unembedding direction `W_U[:,1]−W_U[:,0]`, so the final score at position *p* is +1 iff *t_p = t₁*.

The construction reproduces the decision on 100% of inputs (R² 1.000), and the per-position variables (token codes at embed / after attention / at the MLP input, and the equality indicator at the MLP output and final residual) pass every site's explained-variance, substitution, removal, interchange and off-manifold test.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed |
| layer 0 attention | verified | resid0.mid |
| layer 0 mlp neurons | verified | mlp0.pre |
| layer 0 output | verified | mlp0.out, resid0.post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `tok0` | 4 | embed |
| `tok1` | 4 | embed |
| `tok2` | 4 | embed |
| `tok3` | 4 | embed |
| `tok4` | 4 | embed |
| `mid0` | 4 | resid0.mid |
| `mid1` | 4 | resid0.mid |
| `mid2` | 4 | resid0.mid |
| `mid3` | 4 | resid0.mid |
| `mid4` | 4 | resid0.mid |
| `pre0` | 4 | mlp0.pre |
| `pre1` | 4 | mlp0.pre |
| `pre2` | 4 | mlp0.pre |
| `pre3` | 4 | mlp0.pre |
| `pre4` | 4 | mlp0.pre |
| `eq` | 5 | mlp0.out, resid0.post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed` | 15 / 13 | 1.00 | 100.0% | 1.8% | 3.5% | yes |
| `resid0.mid` | 15 / 13 | 1.00 | 100.0% | 1.8% | 0.0% | yes |
| `mlp0.pre` | 15 / 14 | 1.00 | 100.0% | 3.5% | 3.5% | yes |
| `mlp0.out` | 4 / 4 | 1.00 | 100.0% | 31.1% | 31.1% | yes |
| `resid0.post` | 4 / 7 | 0.16 | 100.0% | 33.4% | 31.1% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `embed` | 100.0% | 100.0% | 25.7% | yes |
| partial | `tok0` | `embed` | 100.0% | 14.1% | 0.0% | yes |
| partial | `tok1` | `embed` | 100.0% | 15.5% | 100.0% | yes |
| partial | `tok2` | `embed` | 100.0% | 14.0% | 100.0% | yes |
| partial | `tok3` | `embed` | 100.0% | 14.5% | 100.0% | yes |
| partial | `tok4` | `embed` | 100.0% | 15.1% | 100.0% | yes |
| edit | `all variables` | `embed` | 51.7% | 24.9% | 31.9% | yes |
| interchange | `all variables` | `resid0.mid` | 100.0% | 100.0% | 25.7% | yes |
| partial | `mid0` | `resid0.mid` | 100.0% | 14.1% | 0.0% | yes |
| partial | `mid1` | `resid0.mid` | 100.0% | 15.5% | 100.0% | yes |
| partial | `mid2` | `resid0.mid` | 100.0% | 14.0% | 100.0% | yes |
| partial | `mid3` | `resid0.mid` | 100.0% | 14.5% | 100.0% | yes |
| partial | `mid4` | `resid0.mid` | 100.0% | 15.1% | 100.0% | yes |
| edit | `all variables` | `resid0.mid` | 45.5% | 24.9% | 29.8% | no |
| interchange | `all variables` | `mlp0.pre` | 100.0% | 100.0% | 25.7% | yes |
| partial | `pre0` | `mlp0.pre` | 100.0% | 14.1% | 0.0% | yes |
| partial | `pre1` | `mlp0.pre` | 100.0% | 15.5% | 100.0% | yes |
| partial | `pre2` | `mlp0.pre` | 100.0% | 14.0% | 100.0% | yes |
| partial | `pre3` | `mlp0.pre` | 100.0% | 14.5% | 100.0% | yes |
| partial | `pre4` | `mlp0.pre` | 100.0% | 15.1% | 100.0% | yes |
| edit | `all variables` | `mlp0.pre` | 48.9% | 25.2% | 30.1% | no |
| interchange | `eq` | `mlp0.out` | 100.0% | 100.0% | 100.0% | yes |
| edit | `eq` | `mlp0.out` | 100.0% | 41.7% | 100.0% | yes |
| interchange | `eq` | `resid0.post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `eq` | `resid0.post` | 100.0% | 41.7% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py tracr_first_match lab/constructions/tracr_first_match/20261113-200059-d63d/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py tracr_first_match lab/constructions/tracr_first_match/20261113-200059-d63d/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py tracr_first_match --steps 80   # a fresh run with the same settings (needs lab/.env)
```
