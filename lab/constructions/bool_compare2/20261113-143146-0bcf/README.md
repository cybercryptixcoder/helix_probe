# Construction run `20261113-143146-0bcf` on `bool_compare2`

*Written by `lab/results.py` from the files in this folder. Network: Two-bit comparator (13 weights). Known answer (never shown to a blinded reader): (2*x1 + x2) > (2*x3 + x4): is the 2-bit number a1a0 greater than b1b0.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 30; used 2 steps, 1 submissions, 19 s, $0.004.
- Weights: original. Reader was blinded (not told what the network does).
- Title: dev smoke. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 16 held-out inputs (a constant output: 62.5%). Construction length: 447 characters.

## The mechanism, in the reader's words

The output depends on s = 2*(x1-x3) + (x2-x4). Unit h1_0 = relu(s), h1_1 = relu(s-1). The output is h1_0 - h1_1 - 0.5, i.e. +0.5 when s>=1 and -0.5 otherwise.

## The reader's final summary

**Mechanism (verified and complete):**

The network computes a single scalar score

  s = 2(x1 − x3) + (x2 − x4)

weighted by the rows of W1: entries [2,1,−2,−1] — i.e. +2,+1 on inputs 1,2 and −2,−1 on inputs 3,4.

- **Hidden layer (h1):** two ReLU units threshold s. With b1 = [0, −1]:
  - u0 = relu(s)
  - u1 = relu(s − 1)
- **Output:** out = u0 − u1 − 0.5, with W2 = [1, −1] and b2 = −0.5.

Since u0 − u1 = min(s, 1) for s ≥ 0, the output is +0.5 when s ≥ 1 and −0.5 otherwise — a weighted threshold on the difference between the first two and last two bits (fires when 2(x1−x3)+(x2−x4) ≥ 1). The construction reproduces the decision on 100% of held-out inputs, and both hidden variables align, substitute, interchange, and edit correctly.

## Stages

| Stage | Status | Sites |
|---|---|---|
| hidden layer 1 | verified | h1 |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `u0` | 1 | h1 |
| `u1` | 1 | h1 |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `h1` | 2 / 2 | 1.00 | 100.0% | 62.5% | 62.5% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `h1` | 100.0% | 100.0% | 100.0% | yes |
| partial | `u0` | `h1` | 100.0% | 95.3% | 100.0% | yes |
| partial | `u1` | `h1` | 100.0% | 48.9% | 100.0% | yes |
| edit | `all variables` | `h1` | 100.0% | 72.2% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py bool_compare2 lab/constructions/bool_compare2/20261113-143146-0bcf/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py bool_compare2 lab/constructions/bool_compare2/20261113-143146-0bcf/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py bool_compare2 --steps 30   # a fresh run with the same settings (needs lab/.env)
```
