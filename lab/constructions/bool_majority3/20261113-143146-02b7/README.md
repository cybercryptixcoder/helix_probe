# Construction run `20261113-143146-02b7` on `bool_majority3`

*Written by `lab/results.py` from the files in this folder. Network: Majority of three bits (11 weights). Known answer (never shown to a blinded reader): majority(x1, x2, x3): 1 if at least two inputs are 1.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 30; used 2 steps, 1 submissions, 8 s, $0.002.
- Weights: original. Reader was blinded (not told what the network does).
- Title: dev smoke. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 8 held-out inputs (a constant output: 50.0%). Construction length: 433 characters.

## The mechanism, in the reader's words

Network counts how many of the 3 binary inputs are 1 (s=sum x). Hidden unit 1 is relu(s-1), hidden unit 2 is relu(s-2). Output is h1+h2-0.5, i.e. positive iff at least two inputs are 1.

## The reader's final summary

Verified and complete.

**Mechanism:** The network's inputs are 3 binary values; it computes their count s = x1+x2+x3. The two hidden ReLU units are threshold indicators of that count: h1 = relu(s−1) (fires once at least two inputs are 1) and h2 = relu(s−2) (fires only when all three are 1). The output is h1 + h2 − 0.5, so it is positive exactly when at least two of the three inputs are 1. Both hidden units were placed and verified at site h1, with correct interchange behaviour.

## Stages

| Stage | Status | Sites |
|---|---|---|
| hidden layer 1 | verified | h1 |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `s` | 1 | (not aligned) |
| `h1` | 1 | h1 |
| `h2` | 1 | h1 |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `h1` | 2 / 1 | 1.00 | 100.0% | 50.0% | 50.0% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `h1` | 100.0% | 100.0% | 100.0% | yes |
| partial | `h1` | `h1` | 100.0% | 93.3% | 100.0% | yes |
| partial | `h2` | `h1` | 100.0% | 54.8% | 100.0% | yes |
| edit | `all variables` | `h1` | 100.0% | 73.5% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py bool_majority3 lab/constructions/bool_majority3/20261113-143146-02b7/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py bool_majority3 lab/constructions/bool_majority3/20261113-143146-02b7/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py bool_majority3 --steps 30   # a fresh run with the same settings (needs lab/.env)
```
