# Construction run `20261113-200059-4f94` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 20; used 2 steps, 1 submissions, 473 s, $0.073.
- Weights: original. Reader was told the task, had NO weights and could not run the network (prior-only control), and had a single submission with no report back.
- Title: v1.1: prior-only B. Status: done.

## Result

**0 of 4 stages verified**.

Run in place of the network, the construction makes the same decision on 100.0% of 6385 held-out inputs (a constant output: 1.1%). Construction length: 1,471 characters.

## The mechanism, in the reader's words

Computes (a+b) mod 113. Tokens a and b are encoded with a full Fourier basis (cos/sin for all 56 nonzero frequencies). The MLP sum features are formed by the product-to-sum identity cos(k(a+b)) = cos(ka)cos(kb) - sin(ka)sin(kb) and sin(k(a+b)) = sin(ka)cos(kb) + cos(ka)sin(kb). The output logits are the inverse Fourier transform of these sum features, so class c has maximum logit at c = (a+b) mod 113. The constant embedding of '=' and the constant attention pattern are represented by constant variables.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | named, failing | embed.0, embed.1 |
| attention | named, failing | attn_pattern |
| mlp neurons | named, failing | mlp_post |
| readout | named, failing | mlp_out |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `a_ff` | 112 | embed.0 |
| `b_ff` | 112 | embed.1 |
| `eq` | 1 | (not aligned) |
| `pat` | 1 | attn_pattern |
| `s_ff` | 112 | mlp_post, mlp_out |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 112 / 7 | 1.00 | 100.0% | 0.9% | 0.9% | no |
| `embed.1` | 112 / 7 | 1.00 | 100.0% | 0.8% | 0.8% | no |
| `attn_pattern` | 0 / 2 | 0.00 | 77.5% | 100.0% | 77.5% | no |
| `mlp_post` | 112 / 17 | 0.14 | 100.0% | 1.6% | 1.7% | no |
| `mlp_out` | 112 / 7 | 0.90 | 100.0% | 1.7% | 1.7% | no |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `a_ff` | `embed.0` | 100.0% | 0.9% | 36.1% | yes |
| edit | `a_ff` | `embed.0` | 15.9% | 1.0% | 31.7% | no |
| interchange | `b_ff` | `embed.1` | 100.0% | 0.7% | 33.5% | yes |
| edit | `b_ff` | `embed.1` | 15.2% | 0.9% | 29.5% | no |
| interchange | `pat` | `attn_pattern` | 100.0% | 1.2% | n/a | yes |
| interchange | `s_ff` | `mlp_post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `s_ff` | `mlp_post` | 16.0% | 20.9% | 100.0% | no |
| interchange | `s_ff` | `mlp_out` | 100.0% | 100.0% | 100.0% | yes |
| edit | `s_ff` | `mlp_out` | 15.3% | 20.0% | 100.0% | no |

## What fails

- size at embed.0: you named 112 dimensions, but the 7 largest principal components of this site already keep 90% of decisions (limit 14): the variables must be more compact
- edit of a_ff at embed.0: prediction right in 15.9% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- size at embed.1: you named 112 dimensions, but the 7 largest principal components of this site already keep 90% of decisions (limit 14): the variables must be more compact
- edit of b_ff at embed.1: prediction right in 15.2% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- substitution at attn_pattern: 77.5% (need 90%)
- removal at attn_pattern: removing the named subspace leaves 100.0% of decisions, while mean-ablating the whole site leaves 77.5%: what you named is not what the output depends on here
- size at mlp_post: you named 112 dimensions, but the 17 largest principal components of this site already keep 90% of decisions (limit 34): the variables must be more compact
- edit of s_ff at mlp_post: prediction right in 16.0% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)
- size at mlp_out: you named 112 dimensions, but the 7 largest principal components of this site already keep 90% of decisions (limit 14): the variables must be more compact
- edit of s_ff at mlp_out: prediction right in 15.3% of the cases where the network's output changed (need 50%; guessing 'no change' gets 0% of these)

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261113-200059-4f94/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261113-200059-4f94/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --told --no-weights --one-shot --steps 20   # a fresh run with the same settings (needs lab/.env)
```
