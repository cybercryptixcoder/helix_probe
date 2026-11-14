# Construction run `20261113-190435-0c92` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 80 steps, 13 submissions, 2713 s, $0.362.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1 official: blinded, replicate A. Status: done.

## Result

**3 of 4 stages verified** (every site the delivered construction names passes).

Run in place of the network, the construction makes the same decision on 100.0% of 6385 held-out inputs (a constant output: 1.1%). Construction length: 2,857 characters.

## The mechanism, in the reader's words

The net computes (i+j) mod 113 on [i,j,113]. Tokens are embedded as Fourier features of their index at frequencies 8, 11, 22, 23, 25 (W_E[:113] is essentially rank 10 at those five frequencies). The last position carries the constant query token 113, so the attention layer's output there is (essentially) the sum of the i- and j-feature pairs; resid_mid therefore holds, for each frequency, the pair cos/sin(f i)+cos/sin(f j), plus weaker second-order content (the already formed sum-frequency content cos/sin(f(i+j)) for f = 8, 23, 25, which is present at the site but is not read by the MLP: ablating it changes no decision). The MLP multiplies the pairs to get cos/sin of f(i+j) - the double angle of the pair's own angle atan2(sum of sines, sum of cosines) - and the readout turns those into logits peaked at k = (i+j) mod 113, plus a weaker pattern that depends on i-j (the squared length of the sum pair, which is why the site's response to a swap of one frequency is only partly complete). Hence the recorded sum pair at resid_mid determines the answer.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed.1 |
| attention | not explained | attn_pattern, attn_out, resid_mid |
| mlp neurons | verified | mlp_post |
| readout | verified | resid_post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `if8` | 2 | (not aligned) |
| `jf8` | 2 | embed.1 |
| `sp8` | 2 | (not aligned) |
| `if11` | 2 | (not aligned) |
| `jf11` | 2 | embed.1 |
| `sp11` | 2 | (not aligned) |
| `if22` | 2 | (not aligned) |
| `jf22` | 2 | embed.1 |
| `sp22` | 2 | (not aligned) |
| `if23` | 2 | (not aligned) |
| `jf23` | 2 | embed.1 |
| `sp23` | 2 | (not aligned) |
| `if25` | 2 | (not aligned) |
| `jf25` | 2 | embed.1 |
| `sp25` | 2 | (not aligned) |
| `t8` | 2 | (not aligned) |
| `t23` | 2 | (not aligned) |
| `t25` | 2 | (not aligned) |
| `tf8` | 2 | mlp_post, resid_post |
| `tf11` | 2 | mlp_post, resid_post |
| `tf22` | 2 | mlp_post, resid_post |
| `tf23` | 2 | mlp_post, resid_post |
| `tf25` | 2 | mlp_post, resid_post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.1` | 10 / 7 | 0.94 | 100.0% | 0.8% | 0.8% | yes |
| `mlp_post` | 10 / 17 | 0.16 | 100.0% | 1.8% | 1.7% | yes |
| `resid_post` | 10 / 7 | 0.86 | 100.0% | 1.2% | 1.1% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `embed.1` | 100.0% | 0.7% | 32.1% | yes |
| partial | `jf8` | `embed.1` | 55.2% | 0.6% | 26.7% | yes |
| partial | `jf11` | `embed.1` | 64.0% | 1.1% | 24.9% | yes |
| partial | `jf22` | `embed.1` | 100.0% | 1.2% | n/a | yes |
| partial | `jf23` | `embed.1` | 88.0% | 0.8% | 39.3% | yes |
| partial | `jf25` | `embed.1` | 50.2% | 0.9% | 23.9% | yes |
| interchange | `all variables` | `mlp_post` | 100.0% | 100.0% | 100.0% | yes |
| partial | `tf8` | `mlp_post` | 57.8% | 5.4% | 100.0% | yes |
| partial | `tf11` | `mlp_post` | 80.8% | 3.0% | 100.0% | yes |
| partial | `tf22` | `mlp_post` | 100.0% | 1.2% | n/a | yes |
| partial | `tf23` | `mlp_post` | 90.6% | 3.1% | 100.0% | yes |
| partial | `tf25` | `mlp_post` | 53.7% | 3.0% | 100.0% | yes |
| interchange | `all variables` | `resid_post` | 100.0% | 100.0% | 100.0% | yes |
| partial | `tf8` | `resid_post` | 58.5% | 5.9% | 100.0% | yes |
| partial | `tf11` | `resid_post` | 82.5% | 3.1% | 100.0% | yes |
| partial | `tf22` | `resid_post` | 100.0% | 1.2% | n/a | yes |
| partial | `tf23` | `resid_post` | 90.1% | 3.1% | 100.0% | yes |
| partial | `tf25` | `resid_post` | 53.1% | 3.0% | 100.0% | yes |

Sites the reader's best submission named that failed, and that the delivered construction therefore does not claim: embed.0, resid_mid.

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261113-190435-0c92/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261113-190435-0c92/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --steps 80   # a fresh run with the same settings (needs lab/.env)
```
