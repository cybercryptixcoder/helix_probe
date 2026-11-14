# Construction run `20261113-135953-158c` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 60; used 60 steps, 12 submissions, 944 s, $0.113.
- Weights: original. Reader was blinded (not told what the network does).
- Title: dev3 blinded, forced submit turns. Status: done.

## Result

**3 of 4 stages verified** (every site the delivered construction names passes).

Run in place of the network, the construction makes the same decision on 100.0% of 6385 held-out inputs (a constant output: 1.1%). Construction length: 2,065 characters.

## The reader's final summary

**Final construction state: 3 of 4 stages VERIFIED, behaviour 100% (R2 0.67, KL 0.00).**

**What the network computes.** It is a grokked modular-addition circuit: input `[i, j, 113]` (113 = a fixed "=" token), output argmax = `(i + j) mod 113`, read at the last position.

**How it does it, stage by stage.**

1. **Embedding.** The token embeddings of tokens 0..112 are Fourier features at five frequencies `k ∈ {8, 11, 22, 23, 25}` of the token index (cos/sin pairs, 10 dims explain 94% of each embedding; the residual is broadband noise). Position embeddings for positions 0 and 1 are nearly identical (so the layer is almost permutation-symmetric); position 2 differs but is only a constant offset.

2. **Attention.** Every head's `W_Q` and `W_K` are **rank 1**, so a head's score at a key position is just `const_h · (x_query·u_h)(x_key·v_h)`; the query is the constant "="/pos-2 embedding, so each head's logits are a scalar Fourier function `f_h(t)` of the key token alone: `L0 = f_h(i)`, `L1 = f_h(j)`, `L2 = const ≈ −5.3` (weight on position 2 ≈ 0). The observed 12 pattern entries are reproduced exactly (error < 1e-15) by `softmax(f_h(i), f_h(j), L2)`. Head outputs are linear images of the same 10 Fourier coordinates, so `attn_out` has effective rank ≈ 10–12. `resid_mid` ≈ affine in `[pattern(8), F(i)(10), F(j)(10)]` (explained 0.92) and 0.97 with the sum/difference features added.

3. **MLP (product-to-sum).** The MLP turns the two tokens' separate Fourier features into functions of the sum: `cos(k(i+j)) = cos ki cos kj − sin ki sin kj` (and `sin`, and the difference-frequency terms). Its output is ~90% a function of `(i+j) mod 113` alone and has effective rank ≈ 10–12; the 10 features `[cos_k(i+j), sin_k(i+j)]` are the whole story downstream.

4. **Readout.** `resid_post` is linear, and its logits are a pure cosine kernel in the answer: `logit[c] ≈ −42.06 + 12.53cos(8Δ) + 6.17cos(11Δ) + 9.80cos(23Δ) + 6.67cos(25Δ)`, `Δ = (c − (i+j)) mod 113` — peaking sharply at the correct class (decision accuracy 100%).

**Verified:** embedding (`embed.0/1`: 10 dims, explained 0.94, remove → 0.7%, interchange 100%, edit 67%), MLP (`mlp_post`, `mlp_out`: 10 sum-frequency dims, remove → 1.5%, interchange 100%, edit 76%), readout (`resid_post`: same features, remove → 1.2%, interchange 100%, edit 76%).

**Unresolved:** the attention stage. Its pattern alone is causally weak (removing it leaves the decision intact 78% of the time), so only `resid_mid`/`mlp_pre` can carry the stage; there my 39-dim description (pattern + both tokens' Fourier features + sum/difference features) explains 0.97/0.98, substitutes perfectly, and survives full interchange (98%), but fails the "edit" probe (27% vs 50%): when half of those coordinates are replaced by another input's values, the off-manifold mixture passes through the network's relu-MLP differently than through my product-to-sum step, so my predicted answer disagrees. Closing that would require modelling the MLP's exact relu geometry on mixed states rather than the idealized product-to-sum identity.

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
| `emb0` | 10 | embed.0 |
| `emb1` | 10 | embed.1 |
| `mid` | 43 | (not aligned) |
| `mlp` | 10 | mlp_post, mlp_out |
| `resid` | 10 | resid_post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 10 / n/a | 0.94 | 100.0% | 0.7% | 0.9% | yes |
| `embed.1` | 10 / n/a | 0.94 | 100.0% | 0.8% | 0.8% | yes |
| `mlp_post` | 10 / n/a | 0.16 | 100.0% | 1.8% | 1.7% | yes |
| `mlp_out` | 10 / n/a | 0.90 | 100.0% | 1.4% | 1.7% | yes |
| `resid_post` | 10 / n/a | 0.86 | 100.0% | 1.2% | 1.1% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `emb0` | `embed.0` | 100.0% | 0.9% | n/a | yes |
| edit | `emb0` | `embed.0` | 67.0% | 1.0% | n/a | yes |
| interchange | `emb1` | `embed.1` | 100.0% | 0.7% | n/a | yes |
| edit | `emb1` | `embed.1` | 66.1% | 0.8% | n/a | yes |
| interchange | `mlp` | `mlp_post` | 100.0% | 100.0% | n/a | yes |
| edit | `mlp` | `mlp_post` | 75.3% | 20.2% | n/a | yes |
| interchange | `mlp` | `mlp_out` | 100.0% | 100.0% | n/a | yes |
| edit | `mlp` | `mlp_out` | 77.1% | 19.0% | n/a | yes |
| interchange | `resid` | `resid_post` | 100.0% | 100.0% | n/a | yes |
| edit | `resid` | `resid_post` | 76.6% | 22.1% | n/a | yes |

Sites the reader's best submission named that failed, and that the delivered construction therefore does not claim: resid_mid, mlp_pre.

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261113-135953-158c/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261113-135953-158c/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --steps 60   # a fresh run with the same settings (needs lab/.env)
```
