# Construction run `20261113-190435-2730` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 79 steps, 15 submissions, 2927 s, $0.405.
- Weights: shuffled. Reader was blinded (not told what the network does).
- Title: v1 official: control shuffled. Status: done.

## Result

**0 of 4 stages verified**.

Run in place of the network, the construction makes the same decision on 99.3% of 6385 held-out inputs (a constant output: 96.6%). Construction length: 15,904 characters.

## The mechanism, in the reader's words

Input [i,j,113]; output 113 logits, decision = argmax. Attention at the last position is uniform (~1/3 per position), so every site up to mlp_pre is exactly affine in the one-hot token variables ti(row i) and tj(row j): explained 1.000 at embed.0/1, attn_out, resid_mid, mlp_pre. The MLP is relu(c+P[i]+Q[j]) whose kinks add only 0.8% of logit variance (mlp_post .96, resid_post .99 explained), so the readout is an additive token score logit[i,j][c]=mu[c]+F[i][c]+F[j][c], argmax over 113 classes; only 8 classes ever top it (97: 96.6%). mu: all classes, 2 base-36 chars each; F: those 8 columns at 2 chars, the rest at 1 char. Only the sites whose map is exactly affine are aligned (mlp_post/mlp_out are dropped: there the network is less sensitive than a purely additive readout, so naming them adds no information).

## The reader's final summary

FINAL SUMMARY

**What the network computes.** Input `[i, j, 113]` (i, j ∈ 0..112, constant sentinel at pos 2) → 113 logits, decision = argmax. Attention at the last position is uniform (≈1/3 per position, std 0.001), so the last position sees the *mean* of the three embeddings plus its own positional term. Consequently every site from `embed.*` through `resid_post` is an exact affine function of the two one-hot token variables (`explained 1.000`, `substitute 100%`, `keep 100%`) and the readout is an additive per-token score

`logit[i,j][c] = mu[c] + F[i][c] + F[j][c]` (one shared table F),

plus a thin ReLU remainder (`relu(c + P[i] + Q[j])`, ~0.8% of logit variance) whose kinks are spread over all 512 neurons — `mlp_post` is 0.96 and `resid_post` 0.991 explained by `ti, tj`, and full reconstruction would need the 512 kink positions, i.e. a 114×512 table, which is not a compact construction. Class 97 dominates: 96.8% of inputs, argmax margins only ~0.14, and only 6 classes ever win (97, 85, 14, 47, 105, 98). The deployed construction reproduces this to 99.3% of decisions, R² 0.987, KL 0.000 — the practical ceiling of the mechanism (a purely additive fit reaches 99.23–99.33% and the residual is provably not low rank: flat SVD spectrum, CP(32) ≈ 55%).

**Why the judge cannot certify it.** Every site is rejected by the same guard, and that guard is unsatisfiable for this network. For the last-position sites (`attn_out`, `resid_mid`, `mlp_pre`, `resid_post`, and also `mlp_post`/`mlp_out`, which I measured separately) replacing the whole site by its mean makes the last-position stream input-independent, so the output becomes a constant function; the fraction of decisions that can change is then at most `1 − freq(argmax of the ablated net) ≤ 1 − 0.968 = 3.2%` (judge reports 3.4% for `embed.0/1`, where only one token is erased, 2.7% at `mlp_pre`, 2.5% at `mlp_post`/`mlp_out`). No site can exceed ~3.4%, so "replacing the site by its mean changes only 3.4% of decisions" holds for *every* site of *every* stage, and the stages can never be verified — a property of the trained network (96.8% constant output), not of the construction.

**Residual imperfections, all at the same wall.** `ti` interchange at `embed.0` reaches 88.1% where 90% is needed (attribution patching on the real network gets 98.8%), i.e. the only thing separating the construction from the network in intervention states is exactly the 0.8% ReLU remainder, which is not compactly representable; the mlp sites fail interchange for the same reason (`mlp_pre` 53.5%, R² −0.585). All other tests pass: `embed.0/1`, `attn_out`, `resid_mid`, `mlp_pre` exact; partials 75–87%; `resid_post` interchange 95.3%.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | named, failing | embed.0, embed.1 |
| attention | named, failing | attn_out |
| mlp neurons | named, failing | mlp_pre |
| readout | named, failing | resid_post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `ti` | 114 | embed.0, attn_out, mlp_pre, resid_post |
| `tj` | 114 | embed.1, attn_out, mlp_pre, resid_post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 112 / 1 | 1.00 | 100.0% | 96.6% | 96.6% | no |
| `embed.1` | 112 / 1 | 1.00 | 100.0% | 96.6% | 96.6% | no |
| `attn_out` | 128 / 1 | 1.00 | 100.0% | 96.6% | 96.6% | no |
| `mlp_pre` | 128 / 1 | 1.00 | 100.0% | 97.3% | 97.3% | no |
| `resid_post` | 128 / 1 | 0.99 | 99.3% | 96.6% | 96.6% | no |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `ti` | `embed.0` | 88.1% | 92.5% | 88.8% | no |
| edit | `ti` | `embed.0` | 93.8% | 92.3% | 92.7% | yes |
| interchange | `tj` | `embed.1` | 91.2% | 93.7% | 84.8% | yes |
| edit | `tj` | `embed.1` | 90.0% | 92.7% | 91.0% | yes |
| interchange | `all variables` | `attn_out` | 92.2% | 100.0% | 79.2% | yes |
| partial | `ti` | `attn_out` | 75.3% | 96.0% | 97.4% | yes |
| partial | `tj` | `attn_out` | 87.2% | 95.9% | 97.4% | yes |
| edit | `all variables` | `attn_out` | 87.0% | 92.0% | 84.8% | yes |
| interchange | `all variables` | `mlp_pre` | 53.5% | 93.2% | 69.8% | no |
| partial | `ti` | `mlp_pre` | 66.7% | 93.7% | 86.7% | no |
| partial | `tj` | `mlp_pre` | 66.7% | 93.7% | 72.2% | no |
| edit | `all variables` | `mlp_pre` | 61.9% | 92.5% | 73.0% | no |
| interchange | `all variables` | `resid_post` | 95.3% | 99.4% | 100.0% | yes |
| partial | `ti` | `resid_post` | 77.6% | 96.0% | 100.0% | yes |
| partial | `tj` | `resid_post` | 82.9% | 96.0% | 100.0% | yes |
| edit | `all variables` | `resid_post` | 91.5% | 92.9% | 100.0% | yes |

## What fails

- embed.0 has almost no effect on the output (replacing the whole site by its mean changes 3.4% of decisions), so nothing can be verified here; use another site of this stage
- interchange of ti at embed.0: prediction right in 88.1% of the cases where the network's output changed (need 90%)
- embed.1 has almost no effect on the output (replacing the whole site by its mean changes 3.4% of decisions), so nothing can be verified here; use another site of this stage
- attn_out has almost no effect on the output (replacing the whole site by its mean changes 3.4% of decisions), so nothing can be verified here; use another site of this stage
- mlp_pre has almost no effect on the output (replacing the whole site by its mean changes 2.7% of decisions), so nothing can be verified here; use another site of this stage
- interchange of all variables at mlp_pre: the network's output changed in only 4.3% of cases, but the construction predicted changes: at this site the network's output does not depend on this variable
- partial of ti at mlp_pre: the network's output changed in only 2.2% of cases, but the construction predicted changes: at this site the network's output does not depend on this variable
- partial of tj at mlp_pre: the network's output changed in only 2.7% of cases, but the construction predicted changes: at this site the network's output does not depend on this variable
- edit of all variables at mlp_pre: the network's output changed in only 3.1% of cases, but the construction predicted changes: at this site the network's output does not depend on this variable
- (at mlp_pre it is enough that EITHER every partial test OR the edit of all variables passes)
- resid_post has almost no effect on the output (replacing the whole site by its mean changes 3.4% of decisions), so nothing can be verified here; use another site of this stage

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261113-190435-2730/construction.py --variant shuffled        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261113-190435-2730/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --variant shuffled --steps 80   # a fresh run with the same settings (needs lab/.env)
```
