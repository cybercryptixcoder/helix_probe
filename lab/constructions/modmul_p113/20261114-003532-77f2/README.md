# Construction run `20261114-003532-77f2` on `modmul_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer C (226,048 weights). Known answer (never shown to a blinded reader): (a * b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 20; used 4 steps, 1 submissions, 394 s, $0.050.
- Weights: original. Reader was told the task, had NO weights and could not run the network (prior-only control), and had a single submission with no report back.
- Title: v1.1: prior-only (rerun). Status: done.

## Result

**0 of 4 stages verified**.

Run in place of the network, the construction makes the same decision on 100.0% of 6385 held-out inputs (a constant output: 1.0%). Construction length: 1,240 characters.

## The mechanism, in the reader's words

Computes (a*b) mod 113. The token embeddings act as one-hot codes for a and b; attention copies those codes to the last position, so the residual stream after attention is an affine function of onehot(a) and onehot(b). The MLP turns the sum of their discrete logs into a lookup keyed by the product c=(a*b)%113, and the readout selects c. The construction tracks the one-hot code of a, of b, and of the product c.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | named, failing | embed.0, embed.1 |
| attention | named, failing | attn_out, resid_mid |
| mlp neurons | named, failing | mlp_pre |
| readout | named, failing | mlp_out |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `a_oh` | 113 | embed.0, attn_out, resid_mid, mlp_pre |
| `b_oh` | 113 | embed.1, attn_out, resid_mid, mlp_pre |
| `c_oh` | 113 | mlp_out |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 112 / 7 | 1.00 | 100.0% | 1.8% | 1.8% | no |
| `embed.1` | 112 / 7 | 1.00 | 100.0% | 1.8% | 1.8% | no |
| `attn_out` | 128 / 9 | 0.96 | 99.5% | 0.8% | 0.8% | no |
| `resid_mid` | 128 / 9 | 0.96 | 99.5% | 0.8% | 0.8% | no |
| `mlp_pre` | 128 / 8 | 0.98 | 99.5% | 3.2% | 3.2% | no |
| `mlp_out` | 112 / 7 | 0.89 | 100.0% | 1.6% | 1.6% | no |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `a_oh` | `embed.0` | 100.0% | 1.8% | 31.8% | yes |
| edit | `a_oh` | `embed.0` | 39.2% | 1.1% | 28.9% | no |
| interchange | `b_oh` | `embed.1` | 100.0% | 1.6% | 32.1% | yes |
| edit | `b_oh` | `embed.1` | 39.2% | 0.9% | 30.0% | no |
| interchange | `all variables` | `attn_out` | 95.7% | 95.7% | 3.7% | yes |
| partial | `a_oh` | `attn_out` | 8.2% | 2.5% | 29.7% | no |
| partial | `b_oh` | `attn_out` | 9.0% | 3.3% | 30.5% | no |
| edit | `all variables` | `attn_out` | 21.4% | 8.2% | 21.7% | no |
| interchange | `all variables` | `resid_mid` | 95.7% | 95.7% | 3.7% | yes |
| partial | `a_oh` | `resid_mid` | 8.2% | 2.5% | 29.7% | no |
| partial | `b_oh` | `resid_mid` | 9.0% | 3.3% | 30.5% | no |
| edit | `all variables` | `resid_mid` | 21.2% | 7.8% | 21.4% | no |
| interchange | `all variables` | `mlp_pre` | 94.0% | 94.0% | 3.5% | yes |
| partial | `a_oh` | `mlp_pre` | 7.5% | 2.6% | 29.6% | no |
| partial | `b_oh` | `mlp_pre` | 8.5% | 3.4% | 30.7% | no |
| edit | `all variables` | `mlp_pre` | 22.5% | 7.8% | 21.0% | no |
| interchange | `c_oh` | `mlp_out` | 100.0% | 100.0% | 100.0% | yes |
| edit | `c_oh` | `mlp_out` | 39.9% | 29.8% | 100.0% | no |

## What fails

- size at embed.0: you named 112 dimensions, but the 7 largest principal components of this site already keep 90% of decisions (limit 14): the variables must be more compact
- edit of a_oh at embed.0: prediction right in 39.2% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- size at embed.1: you named 112 dimensions, but the 7 largest principal components of this site already keep 90% of decisions (limit 14): the variables must be more compact
- edit of b_oh at embed.1: prediction right in 39.2% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- size at attn_out: you named 128 dimensions, but the 9 largest principal components of this site already keep 90% of decisions (limit 18): the variables must be more compact
- partial of a_oh at attn_out: prediction right in 8.2% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- partial of b_oh at attn_out: prediction right in 9.0% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- edit of all variables at attn_out: prediction right in 21.4% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- (at attn_out it is enough that EITHER every partial test OR the edit of all variables passes)
- size at resid_mid: you named 128 dimensions, but the 9 largest principal components of this site already keep 90% of decisions (limit 18): the variables must be more compact
- partial of a_oh at resid_mid: prediction right in 8.2% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- partial of b_oh at resid_mid: prediction right in 9.0% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- edit of all variables at resid_mid: prediction right in 21.2% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- (at resid_mid it is enough that EITHER every partial test OR the edit of all variables passes)
- size at mlp_pre: you named 128 dimensions, but the 8 largest principal components of this site already keep 90% of decisions (limit 16): the variables must be more compact
- partial of a_oh at mlp_pre: prediction right in 7.5% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- partial of b_oh at mlp_pre: prediction right in 8.5% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- edit of all variables at mlp_pre: prediction right in 22.5% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- (at mlp_pre it is enough that EITHER every partial test OR the edit of all variables passes)
- size at mlp_out: you named 112 dimensions, but the 7 largest principal components of this site already keep 90% of decisions (limit 14): the variables must be more compact
- edit of c_oh at mlp_out: prediction right in 39.9% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modmul_p113 lab/constructions/modmul_p113/20261114-003532-77f2/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modmul_p113 lab/constructions/modmul_p113/20261114-003532-77f2/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modmul_p113 --told --no-weights --one-shot --steps 20   # a fresh run with the same settings (needs lab/.env)
```
