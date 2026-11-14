# Construction run `20261113-190435-ec84` on `modmul_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer C (226,048 weights). Known answer (never shown to a blinded reader): (a * b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 76 steps, 14 submissions, 2388 s, $0.324.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1 official: blinded, held-out. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 97.3% of 6385 held-out inputs (a constant output: 1.0%). Construction length: 2,898 characters.

## The mechanism, in the reader's words

The network computes (i*j) mod 113 for input [i, j, 113]; token 113 is an operation marker attended to only slightly. attn_out/resid_mid are an additive code const + h(i) + h(j) where h(t) = cos/sin(2*pi*m*dlog_3(t)/112) for m = 4, 28, 31, 41, 8, 56, 30, 50 (16 numbers per token), so the sum of the two tokens' codes ('code') is a linear image of the site; its last two coordinates are the difference clock cos/sin(4*(dlog i - dlog j)), which cover the pair-dependent part of the attention. The MLP turns that into the clock of the product p = i*j, whose discrete log is dlog(i)+dlog(j): its clock at m follows from the sum code at m and at 2m by angle addition, cos(a+b) = (C^2-S^2)/2 - C_2m/2, sin(a+b) = C*S - S_2m/2 (2m folded mod 112, which is why 8, 56, 30, 50 appear). That product clock ('pcode') is what the MLP releases into mlp_post/mlp_out/resid_post, and the unembedding reads the class of the product out of it, so the model nearest-neighbour decodes p from pcode.

## The reader's final summary

**The mechanism, verified at every stage.**

The network computes **(i·j) mod 113**, read at the last position; token 113 is an operation marker whose attention is nearly uniform over the two operand positions.

1. **Embedding** — each operand token's embedding is a Fourier code over the *discrete log base 3 mod 113*: cos/sin(2π·m·dlog(t)/112) for the frequencies m = 4, 28, 31, 41 (8 dims per token, ~75% of the site variance).

2. **Attention** — because the pattern is nearly uniform, `attn_out` and `resid_mid` are an *additive* code: const + h(i) + h(j). With the extra frequencies {8, 56, 30, 50} (needed because the doubling 2m must also be present) plus the difference clock cos/sin(4(dlog i − dlog j)) for the pair-dependent part, a 17-dim `code` explains 93.5% of the site, keeps 100% of decisions and removal destroys them.

3. **MLP** — the key step is **angle addition on the sum of the two logs**: since dlog(i·j) = dlog i + dlog j, the product's clock at frequency m follows from the sum code at m and at 2m,
   cos(a+b) = (C²−S²)/2 − C₂m/2, sin(a+b) = C·S − S₂m/2
   (2m folded mod 112, which is exactly why 8, 56, 30, 50 sit in the embedding). The MLP releases this 8-dim **product clock** (`pcode`) into mlp_post / mlp_out / resid_post.

4. **Readout** — the unembedding decodes the product's class from that clock (trigonometric/ring readout), so the model recovers p by nearest neighbour in the product-clock table.

Overall behaviour 97.3% (the residue is token-0 rows, where the discrete log is undefined and handled by a placeholder).

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed.0, embed.1 |
| attention | verified | attn_out, resid_mid |
| mlp neurons | verified | mlp_post |
| readout | verified | mlp_out, resid_post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `tok0` | 8 | embed.0 |
| `tok1` | 8 | embed.1 |
| `code` | 18 | attn_out, resid_mid |
| `pcode` | 8 | mlp_post, mlp_out, resid_post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 8 / 7 | 0.75 | 99.0% | 1.3% | 1.8% | yes |
| `embed.1` | 8 / 7 | 0.75 | 99.0% | 1.3% | 1.8% | yes |
| `attn_out` | 17 / 9 | 0.94 | 98.1% | 1.0% | 0.8% | yes |
| `resid_mid` | 17 / 9 | 0.94 | 98.1% | 1.0% | 0.8% | yes |
| `mlp_post` | 8 / 18 | 0.12 | 98.2% | 3.3% | 1.6% | yes |
| `mlp_out` | 8 / 7 | 0.86 | 98.2% | 3.6% | 1.6% | yes |
| `resid_post` | 8 / 7 | 0.84 | 98.2% | 2.9% | 1.0% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `tok0` | `embed.0` | 98.4% | 0.8% | 30.3% | yes |
| edit | `tok0` | `embed.0` | 62.9% | 0.8% | 32.6% | yes |
| interchange | `tok1` | `embed.1` | 97.7% | 0.8% | 29.9% | yes |
| edit | `tok1` | `embed.1` | 64.3% | 1.2% | 31.2% | yes |
| interchange | `code` | `attn_out` | 93.1% | 93.2% | 3.2% | yes |
| edit | `code` | `attn_out` | 51.4% | 9.0% | 14.9% | yes |
| interchange | `code` | `resid_mid` | 93.1% | 93.2% | 3.2% | yes |
| edit | `code` | `resid_mid` | 51.1% | 8.3% | 16.9% | yes |
| interchange | `pcode` | `mlp_post` | 96.6% | 96.4% | 100.0% | yes |
| edit | `pcode` | `mlp_post` | 73.0% | 18.5% | 100.0% | yes |
| interchange | `pcode` | `mlp_out` | 96.6% | 97.2% | 100.0% | yes |
| edit | `pcode` | `mlp_out` | 73.6% | 20.2% | 100.0% | yes |
| interchange | `pcode` | `resid_post` | 96.5% | 97.2% | 100.0% | yes |
| edit | `pcode` | `resid_post` | 74.5% | 19.1% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modmul_p113 lab/constructions/modmul_p113/20261113-190435-ec84/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modmul_p113 lab/constructions/modmul_p113/20261113-190435-ec84/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modmul_p113 --steps 80   # a fresh run with the same settings (needs lab/.env)
```
