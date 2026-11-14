# Construction run `20261113-143146-d2db` on `bool_parity3`

*Written by `lab/results.py` from the files in this folder. Network: Parity of three bits (16 weights). Known answer (never shown to a blinded reader): x1 XOR x2 XOR x3 (odd number of ones).*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 30; used 2 steps, 1 submissions, 14 s, $0.002.
- Weights: original. Reader was blinded (not told what the network does).
- Title: dev smoke. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 8 held-out inputs (a constant output: 50.0%). Construction length: 777 characters.

## The mechanism, in the reader's words

The three hidden ReLU units are all driven by the same scalar s = x0+x1+x2, with biases 0,-1,-2: h1 = [relu(s), relu(s-1), relu(s-2)]. These three shifted/thresholded copies of s are the site's three coordinates. The output weights (1,-2,2) with bias -0.5 make out = relu(s) - 2relu(s-1) + 2relu(s-2) - 0.5, which equals +0.5 when s is odd and -0.5 when s is even (parity of the input).

## The reader's final summary

The network computes parity of the 3 binary inputs.

All three hidden units share the same prefactor row (W1 is all ones), so each is a shifted copy of the scalar sum s = x₀+x₁+x₂:
- h1 = [relu(s), relu(s−1), relu(s−2)] with biases 0, −1, −2.

The output combines them with weights (1, −2, 2) and bias −0.5:
out = relu(s) − 2·relu(s−1) + 2·relu(s−2) − 0.5.

For integer s ∈ {0,1,2,3} this double-difference yields +0.5 when s is odd and −0.5 when s is even — i.e. the sign of the output is the parity of the input. The construction reproduces the three hidden activations as named variables (verified at site h1) and applies this output map, matching the network exactly.

## Stages

| Stage | Status | Sites |
|---|---|---|
| hidden layer 1 | verified | h1 |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `u0` | 1 | h1 |
| `u1` | 1 | h1 |
| `u2` | 1 | h1 |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `h1` | 3 / 3 | 1.00 | 100.0% | 25.0% | 50.0% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `u0` | `h1` | 100.0% | 62.4% | n/a | yes |
| interchange | `u1` | `h1` | 100.0% | 68.0% | n/a | yes |
| interchange | `u2` | `h1` | 100.0% | 58.8% | n/a | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py bool_parity3 lab/constructions/bool_parity3/20261113-143146-d2db/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py bool_parity3 lab/constructions/bool_parity3/20261113-143146-d2db/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py bool_parity3 --steps 30   # a fresh run with the same settings (needs lab/.env)
```
