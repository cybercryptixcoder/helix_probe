# Construction run `20261113-134430-3f45` on `bool_xor`

*Written by `lab/results.py` from the files in this folder. Network: XOR of two bits (9 weights). Known answer (never shown to a blinded reader): x1 XOR x2.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 12; used 2 steps, 1 submissions, 12 s, $0.003.
- Weights: original. Reader was blinded (not told what the network does).
- Title: (none). Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 4 held-out inputs (a constant output: 50.0%). Construction length: 522 characters.

## The mechanism, in the reader's words

XOR-like network. Both hidden units see the same pre-activation s = x1 + x2 (row 1 of W1 is [1,1], b1 = [0,-1]). Unit 1 is relu(s), unit 2 is relu(s-1). The output is h1_1 - 2*h1_2 - 0.5, which equals 0.5 when s == 1 (exactly one input is 1) and -0.5 otherwise.

## The reader's final summary

**Mechanism (verified):** The network computes an XOR/parity-like function on two binary inputs.

- Both hidden units share the same pre-activation `s = x1 + x2` (W1 row 1 = [1,1], row 2 = [1,1]; biases [0, -1]).
- Unit 1 = `relu(s)`, Unit 2 = `relu(s - 1)`.
- Output = `h1_1 - 2·h1_2 - 0.5` = `s - 2·max(s-1,0) - 0.5`, which gives **+0.5 when exactly one input is 1** and **-0.5 otherwise** (both 0 or both 1).

The two variables `s_lin = s` and `s_big = relu(s-1)` fully span the hidden layer, so the single stage is verified and the construction reproduces the network exactly.

## Stages

| Stage | Status | Sites |
|---|---|---|
| hidden layer 1 | verified | h1 |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `s_lin` | 1 | h1 |
| `s_big` | 1 | h1 |

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
| partial | `s_lin` | `h1` | 100.0% | 69.5% | 100.0% | yes |
| partial | `s_big` | `h1` | 100.0% | 67.7% | 100.0% | yes |
| edit | `all variables` | `h1` | 100.0% | 69.9% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py bool_xor lab/constructions/bool_xor/20261113-134430-3f45/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py bool_xor lab/constructions/bool_xor/20261113-134430-3f45/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py bool_xor --steps 12   # a fresh run with the same settings (needs lab/.env)
```
