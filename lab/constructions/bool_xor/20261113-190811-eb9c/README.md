# Construction run `20261113-190811-eb9c` on `bool_xor`

*Written by `lab/results.py` from the files in this folder. Network: XOR of two bits (9 weights). Known answer (never shown to a blinded reader): x1 XOR x2.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 10; used 2 steps, 1 submissions, 13 s, $0.003.
- Weights: original. Reader was blinded (not told what the network does).
- Title: frontend live test. Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 4 held-out inputs (a constant output: 50.0%). Construction length: 395 characters.

## The mechanism, in the reader's words

Computes s=x0+x1. Hidden unit 1 is relu(s), hidden unit 2 is relu(s-1); the output is h1 - 2*h2 - 0.5, i.e. positive exactly when the two binary inputs differ.

## The reader's final summary

**Mechanism.** Both inputs are binary. The network's first hidden unit is `u = relu(x₀+x₁)` and the second is `v = relu(x₀+x₁−1)` — i.e. the same sum, clipped at 0 and at 1, so `u−v = min(x₀+x₁, 1)` is exactly XOR-OR and the two units encode the sum. The output layer `out = u − 2v − 0.5` turns that into a parity test: it is +0.5 when the inputs differ (sum = 1) and −0.5 when they agree (sum = 0 or 2). So the network computes XOR.

**Construction.** `model()` recomputes `s = x₀+x₁` from the inputs and names the two ReLU features `u = relu(s)`, `v = relu(s−1)` at the single site `h1`, then returns `u − 2v − 0.5`. Both variables are aligned to `h1`, which is verified: behaviour matches exactly (R² = 1.0), the subspace fully explains the site, substitution/interchange/partial tests all pass at 100%, and removing it destroys the decision. Every stage of the network is explained.

## Stages

| Stage | Status | Sites |
|---|---|---|
| hidden layer 1 | verified | h1 |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `u` | 1 | h1 |
| `v` | 1 | h1 |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `h1` | 2 / 2 | 1.00 | 100.0% | 25.0% | 50.0% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `h1` | 100.0% | 100.0% | 100.0% | yes |
| partial | `u` | `h1` | 100.0% | 69.5% | 100.0% | yes |
| partial | `v` | `h1` | 100.0% | 67.7% | 100.0% | yes |
| edit | `all variables` | `h1` | 100.0% | 69.9% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py bool_xor lab/constructions/bool_xor/20261113-190811-eb9c/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py bool_xor lab/constructions/bool_xor/20261113-190811-eb9c/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py bool_xor --steps 10   # a fresh run with the same settings (needs lab/.env)
```
