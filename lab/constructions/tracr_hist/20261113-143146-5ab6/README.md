# Construction run `20261113-143146-5ab6` on `tracr_hist`

*Written by `lab/results.py` from the files in this folder. Network: Compiled program H (1,161 weights). Known answer (never shown to a blinded reader): histogram: output i is the number of tokens equal to token i.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 60; used 21 steps, 3 submissions, 432 s, $0.085.
- Weights: original. Reader was blinded (not told what the network does).
- Title: dev1 blinded. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 122 held-out inputs (a constant output: 0.0%). Construction length: 2,406 characters.

## The mechanism, in the reader's words

The network counts tokens: at each position p in 1..5 the output is the one-hot of class m_p = number of occurrences of the token at p among positions 1..5. The single attention head attends uniformly over {position 0} U {positions whose token equals the query token}; its value is non-zero only at token 0, so the attention output at p is q_p * v0 with q_p = 1/(m_p+1) (q_0 = 1). The MLP pre-activation is affine in q_p alone (the token/position part of the embedding is annihilated by W_in), so the MLP output at p is a degree-4 polynomial in q_p, and the final projection turns that into the one-hot of m_p. The coefficients below are solved from the identity logits = one-hot(m) on the 5 attainable values of q. Variables: token code per position (2 coordinates: [t==2],[t==3]) at embed and a terminal copy at resid0.mid, q_p at attn0.out / resid0.mid / mlp0.pre, and the powers q..q^4 per position at mlp0.out.

## The reader's final summary

VERIFIED AND COMPLETE.

**What the network computes:** for each position p∈1..5, a one-hot over classes 0..5 giving m_p = the number of times the token at p occurs among positions 1..5.

**How:**
- **Embedding** — each position carries its token, encoded as two coordinates ([t==2], [t==3]); ≫tok 1 ≪ has the same code. Positions 1..5 share one embedding code up to a constant.
- **Attention** — the head is token-match based: it attends uniformly over position 0 plus all positions whose token equals the query token, so with v0 the only nonzero value vector the attention output at p is q_p·v0 with q_p = 1/(m_p+1); q is read off as one coordinate per position.
- **MLP** — the token/position part of the residual is annihilated by W_in, so each pre-activation is affine in q_p alone; after ReLU the MLP output at p is a degree-4 polynomial in q_p (5 attainable values). Those power coordinates q..q⁴ at mlp0.out carry the count.
- **Output** — W_U already holds the one-hot basis for these token/position embeddings (v0 and the token differences have zero ·W_U), so the final projection of the MLP's polynomial gives exactly the one-hot of m_p, with coefficients solved

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed |
| layer 0 attention | verified | attn0.out, resid0.mid |
| layer 0 mlp neurons | verified | mlp0.pre |
| layer 0 output | verified | mlp0.out |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `c1` | 2 | embed |
| `c2` | 2 | embed |
| `c3` | 2 | embed |
| `c4` | 2 | embed |
| `c5` | 2 | embed |
| `r1` | 2 | resid0.mid |
| `r2` | 2 | resid0.mid |
| `r3` | 2 | resid0.mid |
| `r4` | 2 | resid0.mid |
| `r5` | 2 | resid0.mid |
| `q` | 5 | attn0.out, resid0.mid, mlp0.pre |
| `v1` | 4 | mlp0.out |
| `v2` | 4 | mlp0.out |
| `v3` | 4 | mlp0.out |
| `v4` | 4 | mlp0.out |
| `v5` | 4 | mlp0.out |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed` | 10 / 10 | 1.00 | 100.0% | 0.0% | 0.0% | yes |
| `attn0.out` | 5 / 5 | 1.00 | 100.0% | 0.0% | 0.0% | yes |
| `resid0.mid` | 15 / 15 | 1.00 | 100.0% | 0.0% | 0.0% | yes |
| `mlp0.pre` | 5 / 5 | 1.00 | 100.0% | 0.0% | 0.0% | yes |
| `mlp0.out` | 16 / 10 | 1.00 | 100.0% | 0.0% | 0.0% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `embed` | 100.0% | 100.0% | 0.0% | yes |
| partial | `c1` | `embed` | 100.0% | 6.0% | 0.0% | yes |
| partial | `c2` | `embed` | 100.0% | 4.8% | 0.0% | yes |
| partial | `c3` | `embed` | 100.0% | 5.2% | 0.0% | yes |
| partial | `c4` | `embed` | 100.0% | 5.1% | 0.0% | yes |
| partial | `c5` | `embed` | 100.0% | 4.5% | 0.0% | yes |
| edit | `all variables` | `embed` | 72.7% | 11.4% | 0.0% | yes |
| interchange | `q` | `attn0.out` | 100.0% | 100.0% | 0.0% | yes |
| edit | `q` | `attn0.out` | 100.0% | 12.4% | 0.0% | yes |
| interchange | `all variables` | `resid0.mid` | 100.0% | 100.0% | 0.0% | yes |
| partial | `r1` | `resid0.mid` | 100.0% | 4.6% | n/a | yes |
| partial | `r2` | `resid0.mid` | 100.0% | 4.6% | n/a | yes |
| partial | `r3` | `resid0.mid` | 100.0% | 4.6% | n/a | yes |
| partial | `r4` | `resid0.mid` | 100.0% | 4.6% | n/a | yes |
| partial | `r5` | `resid0.mid` | 100.0% | 4.6% | n/a | yes |
| partial | `q` | `resid0.mid` | 100.0% | 100.0% | 0.0% | yes |
| edit | `all variables` | `resid0.mid` | 100.0% | 14.8% | 0.0% | yes |
| interchange | `q` | `mlp0.pre` | 100.0% | 100.0% | 0.0% | yes |
| edit | `q` | `mlp0.pre` | 100.0% | 11.7% | 0.0% | yes |
| interchange | `all variables` | `mlp0.out` | 100.0% | 100.0% | 100.0% | yes |
| partial | `v1` | `mlp0.out` | 96.4% | 4.6% | 100.0% | yes |
| partial | `v2` | `mlp0.out` | 96.2% | 4.6% | 100.0% | yes |
| partial | `v3` | `mlp0.out` | 95.8% | 4.6% | 100.0% | yes |
| partial | `v4` | `mlp0.out` | 96.2% | 4.6% | 100.0% | yes |
| partial | `v5` | `mlp0.out` | 96.2% | 4.6% | 100.0% | yes |
| edit | `all variables` | `mlp0.out` | 3.7% | 4.9% | 100.0% | no |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py tracr_hist lab/constructions/tracr_hist/20261113-143146-5ab6/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py tracr_hist lab/constructions/tracr_hist/20261113-143146-5ab6/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py tracr_hist --steps 60   # a fresh run with the same settings (needs lab/.env)
```
