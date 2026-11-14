# Construction run `20261113-190435-9b22` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 80 steps, 12 submissions, 2549 s, $0.381.
- Weights: untrained. Reader was blinded (not told what the network does).
- Title: v1 official: control untrained. Status: done.

## Result

**1 of 4 stages verified**.

Run in place of the network, the construction makes the same decision on 94.8% of 6385 held-out inputs (a constant output: 40.3%). Construction length: 7,176 characters.

## The mechanism, in the reader's words

Input is [i, j, 113] with the marker 113 fixed at position 2, so embed.2 holds no variable. Attention is essentially uniform (each head puts ~1/3 on each of the 3 positions; replacing all weights by exactly 1/3 changes the logits at R2 0.99999), so attn_out = mean_pos(x) @ M, M = sum_h W_V[h] W_O[h], and both the residual stream after attention and the MLP pre-activations are EXACT affine functions of the token pair sum onehot(i)+onehot(j). The 113 logits are read through a linear unembedding that is almost additive in the two tokens: out = C + T[token at position 0] + T[token at position 1], with a per-token table T (113x18) over the 18 classes that ever win; this reproduces the network's decision on ~95% of inputs (the rest is the small nonlinear part contributed by the 512 relu neurons, which I could not compress). The table is stored as fixed-point literals. tok0/tok1 are the token identity codes at the two embedding sites.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed.0, embed.1 |
| attention | not explained | attn_pattern, attn_out, resid_mid |
| mlp neurons | not explained | mlp_pre, mlp_post |
| readout | not explained | mlp_out, resid_post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `tok0` | 113 | embed.0 |
| `tok1` | 113 | embed.1 |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 112 / 69 | 1.00 | 100.0% | 61.7% | 61.7% | yes |
| `embed.1` | 112 / 66 | 1.00 | 100.0% | 60.8% | 60.8% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `tok0` | `embed.0` | 94.1% | 47.2% | 86.9% | yes |
| edit | `tok0` | `embed.0` | 92.6% | 39.1% | 87.5% | yes |
| interchange | `tok1` | `embed.1` | 93.5% | 50.3% | 86.1% | yes |
| edit | `tok1` | `embed.1` | 93.7% | 40.0% | 87.1% | yes |

## What fails

- behaviour: the construction's output agrees with the network on 94.8% of inputs (need 95%)

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261113-190435-9b22/construction.py --variant untrained        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261113-190435-9b22/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --variant untrained --steps 80   # a fresh run with the same settings (needs lab/.env)
```
