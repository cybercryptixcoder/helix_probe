# Construction run `20261113-190435-48d0` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 80 steps, 12 submissions, 2697 s, $0.363.
- Weights: permuted. Reader was blinded (not told what the network does).
- Title: v1 official: control permuted. Status: done.

## Result

**3 of 4 stages verified** (every site the delivered construction names passes).

Run in place of the network, the construction makes the same decision on 100.0% of 6385 held-out inputs (a constant output: 1.1%). Construction length: 2,751 characters.

## The mechanism, in the reader's words

Network computes (i+j) mod 113 for input [i,j,113]. Every token t is coded by 4 orthogonal Fourier pairs: cos/sin(2*pi*k*t/113) for k in {8,11,23,25}; embed.0/embed.1 carry the 8-dim code of i and of j. Attention at the last position (weights softmax over s_h(i), s_h(j), const, with s_h a Fourier mode) passes the i-code and the j-code, gated per head, into the residual stream; attn_out/resid_mid are spanned by the 16 numbers [cos_k i, sin_k i, cos_k j, sin_k j] plus their gate modulation. The MLP multiplies the k-th i-code with the k-th j-code, so the residual stream after the MLP carries, for each k, cos/sin of 2*pi*k*s_k/113 with s_k=(i+j) mod 113. The unembedding reads each pair out as 12.5/6.2/9.8/6.7*cos(2*pi*k*(s_k-c)/113).

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed.1 |
| attention | not explained | attn_pattern, attn_out, resid_mid |
| mlp neurons | verified | mlp_post |
| readout | verified | mlp_out, resid_post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `i8` | 2 | (not aligned) |
| `j8` | 2 | embed.1 |
| `i11` | 2 | (not aligned) |
| `j11` | 2 | embed.1 |
| `i23` | 2 | (not aligned) |
| `j23` | 2 | embed.1 |
| `i25` | 2 | (not aligned) |
| `j25` | 2 | embed.1 |
| `ai8` | 2 | (not aligned) |
| `aj8` | 2 | (not aligned) |
| `ai11` | 2 | (not aligned) |
| `aj11` | 2 | (not aligned) |
| `ai23` | 2 | (not aligned) |
| `aj23` | 2 | (not aligned) |
| `ai25` | 2 | (not aligned) |
| `aj25` | 2 | (not aligned) |
| `k8` | 2 | mlp_post, mlp_out, resid_post |
| `k11` | 2 | mlp_post, mlp_out, resid_post |
| `k23` | 2 | mlp_post, mlp_out, resid_post |
| `k25` | 2 | mlp_post, mlp_out, resid_post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.1` | 8 / 7 | 0.87 | 100.0% | 0.5% | 0.8% | yes |
| `mlp_post` | 8 / 17 | 0.15 | 100.0% | 2.2% | 1.7% | yes |
| `mlp_out` | 8 / 7 | 0.90 | 100.0% | 2.1% | 1.7% | yes |
| `resid_post` | 8 / 7 | 0.86 | 100.0% | 1.8% | 1.1% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `embed.1` | 99.6% | 0.7% | 30.4% | yes |
| partial | `j8` | `embed.1` | 56.1% | 0.6% | 27.0% | yes |
| partial | `j11` | `embed.1` | 64.7% | 1.1% | 25.2% | yes |
| partial | `j23` | `embed.1` | 88.0% | 0.8% | 39.4% | yes |
| partial | `j25` | `embed.1` | 51.5% | 0.9% | 23.8% | yes |
| interchange | `all variables` | `mlp_post` | 100.0% | 100.0% | 100.0% | yes |
| partial | `k8` | `mlp_post` | 58.2% | 5.4% | 100.0% | yes |
| partial | `k11` | `mlp_post` | 81.8% | 3.0% | 100.0% | yes |
| partial | `k23` | `mlp_post` | 90.6% | 3.1% | 100.0% | yes |
| partial | `k25` | `mlp_post` | 55.8% | 3.0% | 100.0% | yes |
| interchange | `all variables` | `mlp_out` | 100.0% | 100.0% | 100.0% | yes |
| partial | `k8` | `mlp_out` | 59.5% | 5.5% | 100.0% | yes |
| partial | `k11` | `mlp_out` | 82.7% | 3.0% | 100.0% | yes |
| partial | `k23` | `mlp_out` | 91.3% | 3.1% | 100.0% | yes |
| partial | `k25` | `mlp_out` | 55.6% | 3.0% | 100.0% | yes |
| interchange | `all variables` | `resid_post` | 100.0% | 100.0% | 100.0% | yes |
| partial | `k8` | `resid_post` | 60.0% | 5.9% | 100.0% | yes |
| partial | `k11` | `resid_post` | 83.1% | 3.1% | 100.0% | yes |
| partial | `k23` | `resid_post` | 90.1% | 3.1% | 100.0% | yes |
| partial | `k25` | `resid_post` | 55.8% | 3.0% | 100.0% | yes |

Sites the reader's best submission named that failed, and that the delivered construction therefore does not claim: embed.0, attn_out, resid_mid.

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261113-190435-48d0/construction.py --variant permuted        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261113-190435-48d0/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --variant permuted --steps 80   # a fresh run with the same settings (needs lab/.env)
```
