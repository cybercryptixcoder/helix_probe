# Construction run `20261114-003532-fe44` on `modmul_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer C (226,048 weights). Known answer (never shown to a blinded reader): (a * b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 80 steps, 16 submissions, 2134 s, $0.297.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1.1: blinded, replicate B (rerun). Status: done.

## Result

**3 of 4 stages verified** (every site the delivered construction names passes).

Run in place of the network, the construction makes the same decision on 100.0% of 6385 held-out inputs (a constant output: 1.0%). Construction length: 7,853 characters.

## The mechanism, in the reader's words

Computes p = i*j mod 113 from tokens (i, j, 113), read at the last position. Stage 1: each of the two content tokens is a lookup code (8-dim table over the 113 tokens): the position-0/1 embeddings are a token code plus a constant position vector, and token identity is recovered by nearest code. Stage 2: attention mixes the two token codes into a residual stream (resid_mid) that is additive in the two tokens (mean + a(i) + b(j)), which is what makes the MLP able to compute the product. Stage 3: the MLP maps that to a 9-dim product code that depends only on p = i*j mod 113 (mlp_post is the codebook entry of p). Stage 4: the readout is linear in that code: logits = c + code @ M. All tables were measured on the network.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed.0, embed.1 |
| attention | not explained | attn_pattern, attn_out, resid_mid |
| mlp neurons | verified | mlp_post |
| readout | verified | mlp_out, resid_post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `tok0` | 8 | embed.0 |
| `tok1` | 8 | embed.1 |
| `post` | 9 | mlp_post |
| `code` | 9 | mlp_out, resid_post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 8 / 7 | 0.76 | 99.2% | 1.3% | 1.8% | yes |
| `embed.1` | 8 / 7 | 0.76 | 99.2% | 1.3% | 1.8% | yes |
| `mlp_post` | 9 / 18 | 0.13 | 100.0% | 1.8% | 1.6% | yes |
| `mlp_out` | 9 / 7 | 0.89 | 100.0% | 3.5% | 1.6% | yes |
| `resid_post` | 9 / 7 | 0.87 | 100.0% | 2.8% | 1.0% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `tok0` | `embed.0` | 98.3% | 0.9% | 30.2% | yes |
| edit | `tok0` | `embed.0` | 60.7% | 0.7% | 29.7% | yes |
| interchange | `tok1` | `embed.1` | 98.2% | 1.0% | 30.1% | yes |
| edit | `tok1` | `embed.1` | 57.0% | 0.6% | 30.9% | yes |
| interchange | `post` | `mlp_post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `post` | `mlp_post` | 76.3% | 23.4% | 100.0% | yes |
| interchange | `code` | `mlp_out` | 99.9% | 100.0% | 100.0% | yes |
| edit | `code` | `mlp_out` | 81.4% | 22.2% | 100.0% | yes |
| interchange | `code` | `resid_post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `code` | `resid_post` | 82.3% | 22.9% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modmul_p113 lab/constructions/modmul_p113/20261114-003532-fe44/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modmul_p113 lab/constructions/modmul_p113/20261114-003532-fe44/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modmul_p113 --steps 80   # a fresh run with the same settings (needs lab/.env)
```
