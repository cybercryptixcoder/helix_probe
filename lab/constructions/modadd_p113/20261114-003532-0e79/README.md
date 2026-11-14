# Construction run `20261114-003532-0e79` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 80 steps, 13 submissions, 1604 s, $0.259.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1.1: blinded, replicate C (rerun). Status: done.

## Result

**3 of 4 stages verified** (every site the delivered construction names passes).

Run in place of the network, the construction makes the same decision on 100.0% of 6385 held-out inputs (a constant output: 1.1%). Construction length: 4,211 characters.

## The mechanism, in the reader's words

Input [i, j, '='] -> class (i+j) mod 113. Positions 0,1 embed tokens i,j as cos/sin of 2*pi*k*n/113 for k in {8,11,22,23,25} (10 of 128 dims). Attention at the last position mixes the two; the MLP computes cos/sin of k*(i+j) by angle addition: its 512 neurons are a rank-11 map, so mlp_post matters only through 11 coordinates z (the row space of W_out) and z is an affine function of cos/sin of the sum. resid_post therefore carries cos/sin of k(i+j) and the unembedding is a Fourier readout at the same freqs: logits[c] = G[0] + sum_k G[2k-1]cos(kc) + G[2k]sin(kc) with G affine in z (measured 11x11 matrix).

## The reader's final summary

I'm at the end of my step budget, so I'll stop with my best verified construction (submission #10).

**Final summary of the mechanism found**

The network computes **`(i + j) mod 113`** for input tokens `[i, j, 113]`, read out at the last position, using a Fourier representation at freqs `{8, 11, 22, 23, 25}`:

1. **embedding** (`embed.0/1`, VERIFIED): token `n` at position `p` is carried by `cos/sin(2πkn/113)`, k in {8,11,22,23,25} — 10 dims out of 128 (7 PCs suffice, `W_E`'s spectrum has a sharp gap after 10).
2. **attention** (not aligned, partly characterised): 4 heads, causal, at the last position; the query is the fixed token 113, so the 12 attention weights depend only on the two key tokens. They are ~0.5/0.5 for i≈j but range from 0.01 to 0.99 as a function of `i−j` (deviations matter: fixing them to 0.5/0.5 or patching them from another input breaks the answer). `attn_out` is a fixed-subspace-affine function of the interpolated token embeddings `m_h = Σ_p w_hp·feats(token_p)`; `[1, w, m_h]` explains 99.4% of `resid_mid`'s variance, but the MLP-nonlinearity that maps that state to the answer could not be compressed into a writable surrogate (the weights-free reproduction of `w` from 10 Fourier features is only accurate to 0.19, and I ran out of steps).
3. **mlp neurons** (`mlp_post`, VERIFIED): the 512 ReLU neurons matter only through the 11-dim row space of `W_out` (`z`), and `z` is an affine function of `cos/sin k(i+j)`. Substituting the construction's `z`, keeping only its 11-dim subspace (98.7%) or swapping it between inputs (100% right) all reproduce the network, while removing it destroys the decision (1.8%).
4. **readout** (`resid_post`, VERIFIED): `resid_post` carries `cos/sin k(i+j)` and `W_U` is a Fourier readout at the same frequencies: `logits[c] = G[0] + Σ_k G[2k−1]cos(2πkc/113) + G[2k]sin(2πkc/113)` with `G` an affine (11×11) function of `z`.

Behaviour of the construction: **same decision as the network on 100% of inputs**, output R² 0.79; stages verified: embedding, mlp neurons, readout (3 of 4); the attention stage is the one left unexplained.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed.0, embed.1 |
| attention | not explained | attn_pattern, attn_out, resid_mid |
| mlp neurons | verified | mlp_post |
| readout | verified | resid_post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `fi` | 10 | embed.0 |
| `fj` | 10 | embed.1 |
| `z` | 11 | mlp_post |
| `sfun` | 10 | resid_post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed.0` | 10 / 7 | 0.94 | 100.0% | 0.7% | 0.9% | yes |
| `embed.1` | 10 / 7 | 0.94 | 100.0% | 0.8% | 0.8% | yes |
| `mlp_post` | 10 / 17 | 0.16 | 100.0% | 1.8% | 1.7% | yes |
| `resid_post` | 10 / 7 | 0.86 | 100.0% | 1.2% | 1.1% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `fi` | `embed.0` | 100.0% | 0.9% | 35.6% | yes |
| edit | `fi` | `embed.0` | 52.9% | 1.0% | 31.7% | yes |
| interchange | `fj` | `embed.1` | 100.0% | 0.7% | 32.1% | yes |
| edit | `fj` | `embed.1` | 52.3% | 0.8% | 28.4% | yes |
| interchange | `z` | `mlp_post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `z` | `mlp_post` | 53.8% | 23.1% | 100.0% | yes |
| interchange | `sfun` | `resid_post` | 100.0% | 100.0% | 100.0% | yes |
| edit | `sfun` | `resid_post` | 55.6% | 20.8% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261114-003532-0e79/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261114-003532-0e79/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --steps 80   # a fresh run with the same settings (needs lab/.env)
```
