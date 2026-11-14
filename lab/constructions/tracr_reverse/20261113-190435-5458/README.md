# Construction run `20261113-190435-5458` on `tracr_reverse`

*Written by `lab/results.py` from the files in this folder. Network: Compiled program R (12,135 weights). Known answer (never shown to a blinded reader): reverse the sequence: output i is token N-1-i.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 9 steps, 2 submissions, 157 s, $0.030.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1 official: blinded, held-out. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 81 held-out inputs (a constant output: 1.2%). Construction length: 2,479 characters.

## The mechanism, in the reader's words

The network reverses the sequence: output block i (position i+1) is the one-hot class of the token at input position 4-i (i=0..3). All input dependence lives in the embedding (token+position); layers 0,1,2 attention patterns and every MLP (layers 0,1,2,3) and layer-1/2 attention outputs are input-independent constants (attn1.out = attn2.out = 0). Their stages only add fixed vectors to the residual stream, so every residual site before layer 3 equals (embedding of its own position's token) + a per-position constant. Layer 3 attention uses a fixed permutation pattern, query position p attends to key position 4-p, so it copies the token code of the token at 4-p into position p; nothing else is added. The output head W_U is affine in the 3-dim one-hot token code: logit_c = code_c - 0.25*sum(code) + 0.25, i.e. 1 for the correct class and 0 for the others, which is the whole output. Variables are one per position: tok_q (q=1..4) = 3-dim one-hot code of the token at input position q, present in the embedding and all residual sites up to layer 3; need_i = the same code for the token that output block i must report, i.e. tok_{4-i}, at the layer-3 sites.

## The reader's final summary

The construction is verified and complete.

**What the network computes:** it reverses the input sequence. Output block i (position i+1, classes 1–3) is the one-hot identity of the token at input position 4−i. Logits are 1 for the correct class and 0 for the other two (affine in the token's one-hot code: `code_c − 0.25·Σcode + 0.25`).

**How:** all input dependence sits in the embedding. Layers 0–2 have input-independent attention patterns (attn0 attends only to position 0 then uniformly; attn1/attn2 output exactly zero) and their MLPs, as well as layer 3's MLP, add fixed constant vectors (pre-activations identical for every input), so every layer is a no-op on content. The only content-routing step is layer 3's attention, whose fixed pattern makes query position p attend to key position 4−p, copying the token code of token 4−p into position p. The output head then reads out that code.

**Variables:** one per position — `tok_q` = 3-dim one-hot code of the token at input position q, alive at the embedding and every residual site up to layer 2; `need_i` = the same code for the token output block i must report (tok_{4−i}), at the layer-3 sites (`attn3.out`, `resid3.mid`, `resid3.post`). All 8 dimensions per site suffice (7 principal components), with every stage verified by interchange, partial and substitution tests.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | verified | embed |
| layer 0 attention | verified | resid0.mid |
| layer 0 output | verified | resid0.post |
| layer 1 attention | verified | resid1.mid |
| layer 1 output | verified | resid1.post |
| layer 2 attention | verified | resid2.mid |
| layer 2 output | verified | resid2.post |
| layer 3 attention | verified | attn3.out, resid3.mid |
| layer 3 output | verified | resid3.post |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `tok1` | 3 | embed, resid0.mid, resid0.post, resid1.mid, resid1.post, resid2.mid, resid2.post |
| `tok2` | 3 | embed, resid0.mid, resid0.post, resid1.mid, resid1.post, resid2.mid, resid2.post |
| `tok3` | 3 | embed, resid0.mid, resid0.post, resid1.mid, resid1.post, resid2.mid, resid2.post |
| `tok4` | 3 | embed, resid0.mid, resid0.post, resid1.mid, resid1.post, resid2.mid, resid2.post |
| `need0` | 3 | attn3.out, resid3.mid, resid3.post |
| `need1` | 3 | attn3.out, resid3.mid, resid3.post |
| `need2` | 3 | attn3.out, resid3.mid, resid3.post |
| `need3` | 3 | attn3.out, resid3.mid, resid3.post |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `embed` | 8 / 7 | 1.00 | 100.0% | 0.0% | 1.2% | yes |
| `resid0.mid` | 8 / 7 | 1.00 | 100.0% | 0.0% | 1.2% | yes |
| `resid0.post` | 8 / 7 | 1.00 | 100.0% | 0.0% | 1.2% | yes |
| `resid1.mid` | 8 / 7 | 1.00 | 100.0% | 0.0% | 1.2% | yes |
| `resid1.post` | 8 / 7 | 1.00 | 100.0% | 0.0% | 1.2% | yes |
| `resid2.mid` | 8 / 7 | 1.00 | 100.0% | 0.0% | 1.2% | yes |
| `resid2.post` | 8 / 7 | 1.00 | 100.0% | 0.0% | 1.2% | yes |
| `attn3.out` | 8 / 8 | 1.00 | 100.0% | 1.2% | 1.2% | yes |
| `resid3.mid` | 8 / 7 | 1.00 | 100.0% | 0.0% | 1.2% | yes |
| `resid3.post` | 8 / 7 | 1.00 | 100.0% | 0.0% | 1.2% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `embed` | 100.0% | 100.0% | 100.0% | yes |
| partial | `tok1` | `embed` | 100.0% | 4.2% | 100.0% | yes |
| partial | `tok2` | `embed` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok3` | `embed` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok4` | `embed` | 100.0% | 3.7% | 100.0% | yes |
| interchange | `all variables` | `resid0.mid` | 100.0% | 100.0% | 100.0% | yes |
| partial | `tok1` | `resid0.mid` | 100.0% | 4.2% | 100.0% | yes |
| partial | `tok2` | `resid0.mid` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok3` | `resid0.mid` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok4` | `resid0.mid` | 100.0% | 3.7% | 100.0% | yes |
| interchange | `all variables` | `resid0.post` | 100.0% | 100.0% | 100.0% | yes |
| partial | `tok1` | `resid0.post` | 100.0% | 4.2% | 100.0% | yes |
| partial | `tok2` | `resid0.post` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok3` | `resid0.post` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok4` | `resid0.post` | 100.0% | 3.7% | 100.0% | yes |
| interchange | `all variables` | `resid1.mid` | 100.0% | 100.0% | 100.0% | yes |
| partial | `tok1` | `resid1.mid` | 100.0% | 4.2% | 100.0% | yes |
| partial | `tok2` | `resid1.mid` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok3` | `resid1.mid` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok4` | `resid1.mid` | 100.0% | 3.7% | 100.0% | yes |
| interchange | `all variables` | `resid1.post` | 100.0% | 100.0% | 100.0% | yes |
| partial | `tok1` | `resid1.post` | 100.0% | 4.2% | 100.0% | yes |
| partial | `tok2` | `resid1.post` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok3` | `resid1.post` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok4` | `resid1.post` | 100.0% | 3.7% | 100.0% | yes |
| interchange | `all variables` | `resid2.mid` | 100.0% | 100.0% | 100.0% | yes |
| partial | `tok1` | `resid2.mid` | 100.0% | 4.2% | 100.0% | yes |
| partial | `tok2` | `resid2.mid` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok3` | `resid2.mid` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok4` | `resid2.mid` | 100.0% | 3.7% | 100.0% | yes |
| interchange | `all variables` | `resid2.post` | 100.0% | 100.0% | 100.0% | yes |
| partial | `tok1` | `resid2.post` | 100.0% | 4.2% | 100.0% | yes |
| partial | `tok2` | `resid2.post` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok3` | `resid2.post` | 100.0% | 3.9% | 100.0% | yes |
| partial | `tok4` | `resid2.post` | 100.0% | 3.7% | 100.0% | yes |
| interchange | `all variables` | `attn3.out` | 100.0% | 100.0% | 100.0% | yes |
| partial | `need0` | `attn3.out` | 100.0% | 3.7% | 100.0% | yes |
| partial | `need1` | `attn3.out` | 100.0% | 3.9% | 100.0% | yes |
| partial | `need2` | `attn3.out` | 100.0% | 3.9% | 100.0% | yes |
| partial | `need3` | `attn3.out` | 100.0% | 4.2% | 100.0% | yes |
| interchange | `all variables` | `resid3.mid` | 100.0% | 100.0% | 100.0% | yes |
| partial | `need0` | `resid3.mid` | 100.0% | 3.7% | 100.0% | yes |
| partial | `need1` | `resid3.mid` | 100.0% | 3.9% | 100.0% | yes |
| partial | `need2` | `resid3.mid` | 100.0% | 3.9% | 100.0% | yes |
| partial | `need3` | `resid3.mid` | 100.0% | 4.2% | 100.0% | yes |
| interchange | `all variables` | `resid3.post` | 100.0% | 100.0% | 100.0% | yes |
| partial | `need0` | `resid3.post` | 100.0% | 3.7% | 100.0% | yes |
| partial | `need1` | `resid3.post` | 100.0% | 3.9% | 100.0% | yes |
| partial | `need2` | `resid3.post` | 100.0% | 3.9% | 100.0% | yes |
| partial | `need3` | `resid3.post` | 100.0% | 4.2% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py tracr_reverse lab/constructions/tracr_reverse/20261113-190435-5458/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py tracr_reverse lab/constructions/tracr_reverse/20261113-190435-5458/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py tracr_reverse --steps 80   # a fresh run with the same settings (needs lab/.env)
```
