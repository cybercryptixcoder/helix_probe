# Construction run `20261113-190435-e5f5` on `tracr_first_match`

*Written by `lab/results.py` from the files in this folder. Network: Compiled program F (1,405 weights). Known answer (never shown to a blinded reader): output i is 1 if token i equals the first token, else 0.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 23 steps, 5 submissions, 421 s, $0.085.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1 official: blinded, held-out. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 512 held-out inputs (a constant output: 31.1%). Construction length: 2,990 characters.

## The mechanism, in the reader's words

Input is [BOS=0, t1..t5] with t_i in {1,2,3,5}; the readout at positions 1..5 asks whether t_p == t1. Mechanism: (1) embeddings are token one-hots per position. (2) Layer-0 attention has a FIXED pattern: query 0 attends to key 0, queries 1..5 attend to key 1 only, so the attention output at positions 1..5 is the value of token t1 alone (a zero vector for tokens 0 and 4). So the residual at position p>=1 encodes the pair (t_p, t1). (3) The 16 MLP neurons are coincidence detectors: neuron n has a token pair (a_n,b_n) and gain m_n with pre_n = m_n*([t_p==a_n] + v1[b_n] - 1), i.e. it fires with size m_n only when t_p==a_n AND t1==b_n (the 16 pairs are exactly all 4x4 combinations of {1,2,3,5}). (4) The output weights give neuron n effective weight u_n with m_n*u_n = +1 for the 4 diagonal (matching) pairs and -1 for the 12 off-diagonal pairs, while the direct residual->logit path is exactly orthogonal to the readout direction. Hence logit(class1)-logit(class0) at position p = +1 if t_p==t1 else -1, and logit(class0)=0: the network outputs (0, +-1). Variables: token one-hots (embed), v1 = the attention content written at positions 1..5, and the 16-vector of MLP neuron activities at each of the 5 readout positions.

## The reader's final summary

VERIFIED AND COMPLETE — all four stages explained.

**What the network computes:** input `[BOS=0, t1..t5]` with `t_i ∈ {1,2,3,5}`; at each position 1..5 it decides whether `t_p == t1` (output `(0, ±1)`, i.e. margin +1 if equal, −1 if not).

**How (stage by stage):**
1. **Embedding** — token one-hot at each position (6 six-dim one-hots, 13 PCs suffice).
2. **Attention** — the pattern is *fixed*, independent of input: query 0 → key 0, queries 1..5 → key 1 only. So positions 1..5 all receive the same attention content: the value vector of token `t1` (zero for tokens 0 and 4). The site is one variable `v1` = that content at positions 1..5.
3. **MLP** — the 16 ReLU neurons are **coincidence detectors** covering all 4×4 token pairs `(a_n, b_n) ∈ {1,2,3,5}²`: `pre_n = m_n·([t_p==a_n] + [t1==b_n] − 1)`, positive (size `m_n`) only when both coincide.
4. **Output** — effective output weight `u_n` satisfies `m_n·u_n = +1` for the 4 diagonal (matching) pairs and `−1` for the 12 off-diagonal ones, while the direct residual→logit path is exactly orthogonal to the readout direction. So the margin is just the sum of the position's neuron activities weighted by `u`, giving `±1`.

Two candidate sites (`resid0.mid`, `mlp0.pre`) are superpositions of the token one-hots and `v1` and were excluded because their subspaces overlap and cannot be swapped independently; the verified representatives are `embed`, `attn0.out`, `mlp0.post`/`mlp0.out`.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed |
| layer 0 attention | verified | attn0.out |
| layer 0 mlp neurons | verified | mlp0.post |
| layer 0 output | verified | mlp0.out |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `tok0` | 6 | embed |
| `tok1` | 6 | embed |
| `tok2` | 6 | embed |
| `tok3` | 6 | embed |
| `tok4` | 6 | embed |
| `tok5` | 6 | embed |
| `v1` | 6 | attn0.out |
| `mlp1` | 16 | mlp0.post, mlp0.out |
| `mlp2` | 16 | mlp0.post, mlp0.out |
| `mlp3` | 16 | mlp0.post, mlp0.out |
| `mlp4` | 16 | mlp0.post, mlp0.out |
| `mlp5` | 16 | mlp0.post, mlp0.out |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed` | 15 / 13 | 1.00 | 100.0% | 1.8% | 3.5% | yes |
| `attn0.out` | 3 / 3 | 1.00 | 100.0% | 0.0% | 0.0% | yes |
| `mlp0.post` | 51 / 42 | 1.00 | 100.0% | 31.1% | 31.1% | yes |
| `mlp0.out` | 4 / 4 | 1.00 | 100.0% | 31.1% | 31.1% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `embed` | 100.0% | 100.0% | 25.7% | yes |
| partial | `tok0` | `embed` | 100.0% | 14.9% | n/a | yes |
| partial | `tok1` | `embed` | 100.0% | 14.1% | 0.0% | yes |
| partial | `tok2` | `embed` | 100.0% | 15.5% | 100.0% | yes |
| partial | `tok3` | `embed` | 100.0% | 14.0% | 100.0% | yes |
| partial | `tok4` | `embed` | 100.0% | 14.5% | 100.0% | yes |
| partial | `tok5` | `embed` | 100.0% | 15.1% | 100.0% | yes |
| edit | `all variables` | `embed` | 55.6% | 25.4% | 33.1% | yes |
| interchange | `v1` | `attn0.out` | 100.0% | 3.8% | 100.0% | yes |
| edit | `v1` | `attn0.out` | 72.1% | 7.0% | 73.1% | yes |
| interchange | `all variables` | `mlp0.post` | 100.0% | 100.0% | 100.0% | yes |
| partial | `mlp1` | `mlp0.post` | 100.0% | 14.9% | n/a | yes |
| partial | `mlp2` | `mlp0.post` | 91.2% | 22.7% | 100.0% | yes |
| partial | `mlp3` | `mlp0.post` | 91.3% | 21.7% | 100.0% | yes |
| partial | `mlp4` | `mlp0.post` | 92.0% | 23.0% | 100.0% | yes |
| partial | `mlp5` | `mlp0.post` | 92.3% | 23.2% | 100.0% | yes |
| edit | `all variables` | `mlp0.post` | 56.0% | 38.3% | 100.0% | yes |
| interchange | `all variables` | `mlp0.out` | 100.0% | 100.0% | 100.0% | yes |
| partial | `mlp1` | `mlp0.out` | 100.0% | 14.9% | n/a | yes |
| partial | `mlp2` | `mlp0.out` | 100.0% | 23.9% | 100.0% | yes |
| partial | `mlp3` | `mlp0.out` | 100.0% | 23.1% | 100.0% | yes |
| partial | `mlp4` | `mlp0.out` | 100.0% | 24.6% | 100.0% | yes |
| partial | `mlp5` | `mlp0.out` | 100.0% | 24.6% | 100.0% | yes |
| edit | `all variables` | `mlp0.out` | 54.7% | 38.8% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py tracr_first_match lab/constructions/tracr_first_match/20261113-190435-e5f5/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py tracr_first_match lab/constructions/tracr_first_match/20261113-190435-e5f5/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py tracr_first_match --steps 80   # a fresh run with the same settings (needs lab/.env)
```
