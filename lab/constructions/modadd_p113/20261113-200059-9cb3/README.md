# Construction run `20261113-200059-9cb3` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 20; used 4 steps, 1 submissions, 376 s, $0.046.
- Weights: original. Reader was told the task, had NO weights and could not run the network (prior-only control), and had a single submission with no report back.
- Title: v1.1: prior-only C. Status: done.

## Result

**0 of 4 stages verified**.

Run in place of the network, the construction makes the same decision on 100.0% of 6385 held-out inputs (a constant output: 1.1%). Construction length: 2,267 characters.

## The mechanism, in the reader's words

The network computes (a+b) mod 113 for the sequence 'a b =' and reads 113 logits at the '=' position. Tokens are carried by Fourier features: token t is the 112 numbers cos(2*pi*k*t/113), sin(2*pi*k*t/113) for k=1..56 (an invertible, complete code for a number mod 113). EMBEDDING: the residual at position 0 (resp. 1) is an affine function of the Fourier code of a (resp. b). ATTENTION: the last position's query is fixed ('=' plus position 2), so the heads mainly copy the a- and b-embeddings forward; attn_out and resid_mid at the last position therefore carry the two token codes. MLP: using cos(w(a+b)) = cos(wa)cos(wb) - sin(wa)sin(wb) and sin(w(a+b)) = sin(wa)cos(wb) + cos(wa)sin(wb) the MLP turns the two token codes into the Fourier code of the sum s = (a+b) mod 113; those sum features appear in mlp_post and mlp_out. READOUT: resid_post holds the code of s and the unembedding scores class c by logit_c = sum_k cos(2*pi*k*(s-c)/113), whose unique maximum is c = s.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | named, failing | embed.0, embed.1 |
| attention | named, failing | attn_out, resid_mid |
| mlp neurons | named, failing | mlp_pre, mlp_post |
| readout | named, failing | mlp_out, resid_post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `tok_a` | 112 | embed.0, attn_out, resid_mid, mlp_pre |
| `tok_b` | 112 | embed.1, attn_out, resid_mid, mlp_pre |
| `sum_feat` | 112 | mlp_post, mlp_out, resid_post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 112 / 7 | 1.00 | 100.0% | 0.9% | 0.9% | no |
| `embed.1` | 112 / 7 | 1.00 | 100.0% | 0.8% | 0.8% | no |
| `attn_out` | 128 / 10 | 0.94 | 95.7% | 0.9% | 0.9% | no |
| `resid_mid` | 128 / 10 | 0.94 | 95.7% | 0.9% | 0.9% | no |
| `mlp_pre` | 119 / 9 | 0.96 | 97.5% | 1.6% | 1.6% | no |
| `mlp_post` | 112 / 17 | 0.14 | 100.0% | 1.6% | 1.7% | no |
| `mlp_out` | 112 / 7 | 0.90 | 100.0% | 1.7% | 1.7% | no |
| `resid_post` | 112 / 7 | 0.86 | 100.0% | 1.1% | 1.1% | no |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `tok_a` | `embed.0` | 100.0% | 0.9% | 36.1% | yes |
| edit | `tok_a` | `embed.0` | 15.9% | 1.0% | 31.7% | no |
| interchange | `tok_b` | `embed.1` | 100.0% | 0.7% | 33.5% | yes |
| edit | `tok_b` | `embed.1` | 15.2% | 0.9% | 29.5% | no |
| interchange | `all variables` | `attn_out` | 70.9% | 70.4% | 4.4% | no |
| partial | `tok_a` | `attn_out` | 4.9% | 2.5% | 31.8% | no |
| partial | `tok_b` | `attn_out` | 5.2% | 2.5% | 32.9% | no |
| edit | `all variables` | `attn_out` | 4.1% | 2.6% | 19.1% | no |
| interchange | `all variables` | `resid_mid` | 70.9% | 70.4% | 4.4% | no |
| partial | `tok_a` | `resid_mid` | 4.9% | 2.5% | 31.8% | no |
| partial | `tok_b` | `resid_mid` | 5.2% | 2.5% | 32.9% | no |
| edit | `all variables` | `resid_mid` | 4.3% | 3.2% | 17.4% | no |
| interchange | `all variables` | `mlp_pre` | 71.8% | 71.3% | 4.1% | no |
| partial | `tok_a` | `mlp_pre` | 3.7% | 1.9% | 36.1% | no |
| partial | `tok_b` | `mlp_pre` | 4.4% | 2.4% | 33.8% | no |
| edit | `all variables` | `mlp_pre` | 4.0% | 3.4% | 17.4% | no |
| interchange | `sum_feat` | `mlp_post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `sum_feat` | `mlp_post` | 15.5% | 21.9% | 100.0% | no |
| interchange | `sum_feat` | `mlp_out` | 100.0% | 100.0% | 100.0% | yes |
| edit | `sum_feat` | `mlp_out` | 14.3% | 20.3% | 100.0% | no |
| interchange | `sum_feat` | `resid_post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `sum_feat` | `resid_post` | 15.0% | 20.3% | 100.0% | no |

## What fails

- size at embed.0: you named 112 dimensions, but the 7 largest principal components of this site already keep 90% of decisions (limit 14): the variables must be more compact
- edit of tok_a at embed.0: prediction right in 15.9% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- size at embed.1: you named 112 dimensions, but the 7 largest principal components of this site already keep 90% of decisions (limit 14): the variables must be more compact
- edit of tok_b at embed.1: prediction right in 15.2% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- size at attn_out: you named 128 dimensions, but the 10 largest principal components of this site already keep 90% of decisions (limit 20): the variables must be more compact
- interchange of all variables at attn_out: prediction right in 70.9% of the cases where the network's output changed (need 90%)
- partial of tok_a at attn_out: prediction right in 4.9% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- partial of tok_b at attn_out: prediction right in 5.2% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- edit of all variables at attn_out: prediction right in 4.1% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- (at attn_out it is enough that EITHER every partial test OR the edit of all variables passes)
- size at resid_mid: you named 128 dimensions, but the 10 largest principal components of this site already keep 90% of decisions (limit 20): the variables must be more compact
- interchange of all variables at resid_mid: prediction right in 70.9% of the cases where the network's output changed (need 90%)
- partial of tok_a at resid_mid: prediction right in 4.9% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- partial of tok_b at resid_mid: prediction right in 5.2% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- edit of all variables at resid_mid: prediction right in 4.3% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- (at resid_mid it is enough that EITHER every partial test OR the edit of all variables passes)
- size at mlp_pre: you named 119 dimensions, but the 9 largest principal components of this site already keep 90% of decisions (limit 18): the variables must be more compact
- interchange of all variables at mlp_pre: prediction right in 71.8% of the cases where the network's output changed (need 90%)
- partial of tok_a at mlp_pre: prediction right in 3.7% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- partial of tok_b at mlp_pre: prediction right in 4.4% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- edit of all variables at mlp_pre: prediction right in 4.0% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- (at mlp_pre it is enough that EITHER every partial test OR the edit of all variables passes)
- size at mlp_post: you named 112 dimensions, but the 17 largest principal components of this site already keep 90% of decisions (limit 34): the variables must be more compact
- edit of sum_feat at mlp_post: prediction right in 15.5% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- size at mlp_out: you named 112 dimensions, but the 7 largest principal components of this site already keep 90% of decisions (limit 14): the variables must be more compact
- edit of sum_feat at mlp_out: prediction right in 14.3% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- size at resid_post: you named 112 dimensions, but the 7 largest principal components of this site already keep 90% of decisions (limit 14): the variables must be more compact
- edit of sum_feat at resid_post: prediction right in 15.0% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261113-200059-9cb3/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261113-200059-9cb3/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --told --no-weights --one-shot --steps 20   # a fresh run with the same settings (needs lab/.env)
```
