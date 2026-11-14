# Construction run `20261113-141703-0b38` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 20; used 2 steps, 1 submissions, 374 s, $0.053.
- Weights: original. Reader was told the task, had NO weights and could not run the network (prior-only control), and had a single submission with no report back.
- Title: control: prior-only (task named, no weights, one submission). Status: done.

## Result

**0 of 4 stages verified**.

Run in place of the network, the construction makes the same decision on 100.0% of 6385 held-out inputs (a constant output: 1.1%). Construction length: 2,683 characters.

## The mechanism, in the reader's words

Fourier / trigonometric-identity solution for (a + b) mod 113. Token embeddings are Fourier features cos(w_k t), sin(w_k t) with w_k = 2*pi*k/113 for a small set of frequencies k. The last position ('=') attends to positions 0 and 1 with (essentially constant) weights, so what attention writes into the final position, the residual stream after attention, and the MLP pre-activations are all affine functions of the four feature blocks {cos(w a), sin(w a), cos(w b), sin(w b)}. The MLP applies the product-to-sum identities cos(w(a+b)) = cos(wa)cos(wb) - sin(wa)sin(wb) and sin(w(a+b)) = sin(wa)cos(wb) + cos(wa)sin(wb), so its output and the final residual stream carry cos/sin features of s = a + b mod 113. The unembedding scores class c by sum_k cos(w_k (s - c)), which is maximal exactly at c = s.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | named, failing | embed.0, embed.1 |
| attention | named, failing | attn_out, resid_mid |
| mlp neurons | named, failing | mlp_pre |
| readout | named, failing | mlp_out, resid_post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `tok0` | 16 | embed.0 |
| `tok1` | 16 | embed.1 |
| `eq_const` | 1 | (not aligned) |
| `ab_last` | 32 | attn_out, resid_mid, mlp_pre |
| `sum_feats` | 16 | mlp_out, resid_post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 16 / n/a | 0.26 | 5.7% | 45.1% | 0.9% | no |
| `embed.1` | 16 / n/a | 0.26 | 5.8% | 42.9% | 0.8% | no |
| `attn_out` | 32 / n/a | 0.31 | 3.7% | 0.9% | 0.9% | no |
| `resid_mid` | 32 / n/a | 0.31 | 3.7% | 0.9% | 0.9% | no |
| `mlp_pre` | 32 / n/a | 0.33 | 5.6% | 1.6% | 1.6% | no |
| `mlp_out` | 16 / n/a | 0.38 | 9.7% | 2.5% | 1.7% | no |
| `resid_post` | 16 / n/a | 0.37 | 6.1% | 1.9% | 1.1% | no |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `tok0` | `embed.0` | 7.6% | 0.8% | n/a | no |
| edit | `tok0` | `embed.0` | 1.6% | 0.9% | n/a | no |
| interchange | `tok1` | `embed.1` | 6.5% | 0.8% | n/a | no |
| edit | `tok1` | `embed.1` | 2.1% | 0.7% | n/a | no |
| interchange | `ab_last` | `attn_out` | 2.3% | 1.9% | n/a | no |
| edit | `ab_last` | `attn_out` | 1.7% | 1.4% | n/a | no |
| interchange | `ab_last` | `resid_mid` | 2.3% | 1.9% | n/a | no |
| edit | `ab_last` | `resid_mid` | 1.6% | 1.4% | n/a | no |
| interchange | `ab_last` | `mlp_pre` | 2.6% | 2.1% | n/a | no |
| edit | `ab_last` | `mlp_pre` | 2.3% | 1.4% | n/a | no |
| interchange | `sum_feats` | `mlp_out` | 7.0% | 5.6% | n/a | no |
| edit | `sum_feats` | `mlp_out` | 1.1% | 2.5% | n/a | no |
| interchange | `sum_feats` | `resid_post` | 7.2% | 5.9% | n/a | no |
| edit | `sum_feats` | `resid_post` | 2.7% | 2.5% | n/a | no |

## What fails

- substitution at embed.0: 5.7% (need 90%)
- interchange of tok0 at embed.0: prediction right in 7.6% of the cases where the network's output changed (need 90%)
- edit of tok0 at embed.0: prediction right in 1.6% of the cases where the network's output changed (need 50% and twice the random-subspace control, 19.6%)
- substitution at embed.1: 5.8% (need 90%)
- interchange of tok1 at embed.1: prediction right in 6.5% of the cases where the network's output changed (need 90%)
- edit of tok1 at embed.1: prediction right in 2.1% of the cases where the network's output changed (need 50% and twice the random-subspace control, 19.1%)
- substitution at attn_out: 3.7% (need 90%)
- interchange of ab_last at attn_out: prediction right in 2.3% of the cases where the network's output changed (need 90%)
- edit of ab_last at attn_out: prediction right in 1.7% of the cases where the network's output changed (need 50% and twice the random-subspace control, 5.4%)
- substitution at resid_mid: 3.7% (need 90%)
- interchange of ab_last at resid_mid: prediction right in 2.3% of the cases where the network's output changed (need 90%)
- edit of ab_last at resid_mid: prediction right in 1.6% of the cases where the network's output changed (need 50% and twice the random-subspace control, 4.8%)
- substitution at mlp_pre: 5.6% (need 90%)
- interchange of ab_last at mlp_pre: prediction right in 2.6% of the cases where the network's output changed (need 90%)
- edit of ab_last at mlp_pre: prediction right in 2.3% of the cases where the network's output changed (need 50% and twice the random-subspace control, 5.5%)
- substitution at mlp_out: 9.7% (need 90%)
- interchange of sum_feats at mlp_out: prediction right in 7.0% of the cases where the network's output changed (need 90%)
- edit of sum_feats at mlp_out: prediction right in 1.1% of the cases where the network's output changed (need 50% and twice the random-subspace control, 19.1%)
- substitution at resid_post: 6.1% (need 90%)
- interchange of sum_feats at resid_post: prediction right in 7.2% of the cases where the network's output changed (need 90%)
- edit of sum_feats at resid_post: prediction right in 2.7% of the cases where the network's output changed (need 50% and twice the random-subspace control, 20.1%)

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261113-141703-0b38/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261113-141703-0b38/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --told --no-weights --one-shot --steps 20   # a fresh run with the same settings (needs lab/.env)
```
