# Construction run `20261114-003532-8fe7` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 80 steps, 11 submissions, 3170 s, $0.405.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1.1: blinded, replicate B (rerun). Status: done.

## Result

**3 of 4 stages verified** (every site the delivered construction names passes).

Run in place of the network, the construction makes the same decision on 100.0% of 6385 held-out inputs (a constant output: 1.1%). Construction length: 2,214 characters.

## The mechanism, in the reader's words

Input [i, j, 113]; argmax output is c = (i+j) mod 113. Token t<113 is a Fourier code at frequencies 8, 11, 23, 25 of 113 (cos and sin); positions/last-position query are constants. Attention at the last position mixes the two tokens' codes into the residual stream (a softmax-weighted mixture, well described by a linear function of [code(i), code(j)]). The MLP multiplies the two codes (angle addition) so mlp_post/mlp_out/resid_post carry the sum code cos/sin of (i+j); the readout is cos(2*pi*f*(c-(i+j))/113).

## The reader's final summary

I cannot improve it further in one step: verifying the attention stage needs the 16 principal-component literals of `attn_out` (measured substitution 100%, interchange ≈99%), which cannot be both measured and submitted in a single remaining step, and every literal-free alternative I tested fails substitution (80.8%) or the off-manifold tests, so the current 3-of-4-stage construction (behaviour 100%) stands as my best.

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
| `e0` | 10 | embed.0 |
| `e1` | 10 | embed.1 |
| `att` | 20 | (not aligned) |
| `code` | 8 | mlp_post, mlp_out, resid_post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 10 / 7 | 0.87 | 100.0% | 0.6% | 0.9% | yes |
| `embed.1` | 10 / 7 | 0.87 | 100.0% | 0.5% | 0.8% | yes |
| `mlp_post` | 8 / 17 | 0.15 | 100.0% | 2.2% | 1.7% | yes |
| `mlp_out` | 8 / 7 | 0.90 | 100.0% | 2.1% | 1.7% | yes |
| `resid_post` | 8 / 7 | 0.86 | 100.0% | 1.8% | 1.1% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `e0` | `embed.0` | 99.9% | 0.9% | 33.5% | yes |
| edit | `e0` | `embed.0` | 63.6% | 1.1% | 32.6% | yes |
| interchange | `e1` | `embed.1` | 99.6% | 0.7% | 30.2% | yes |
| edit | `e1` | `embed.1` | 62.1% | 0.8% | 28.7% | yes |
| interchange | `code` | `mlp_post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `code` | `mlp_post` | 72.0% | 19.4% | 100.0% | yes |
| interchange | `code` | `mlp_out` | 100.0% | 100.0% | 100.0% | yes |
| edit | `code` | `mlp_out` | 70.4% | 19.7% | 100.0% | yes |
| interchange | `code` | `resid_post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `code` | `resid_post` | 70.4% | 20.4% | 100.0% | yes |

Sites the reader's best submission named that failed, and that the delivered construction therefore does not claim: attn_out, resid_mid.

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261114-003532-8fe7/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261114-003532-8fe7/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --steps 80   # a fresh run with the same settings (needs lab/.env)
```
