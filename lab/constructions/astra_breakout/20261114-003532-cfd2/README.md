# Construction run `20261114-003532-cfd2` on `astra_breakout`

*Written by `lab/results.py` from the files in this folder. Network: Hand-written game policy (20,486 weights). Known answer (never shown to a blinded reader): a policy for MinAtar Breakout: move the paddle under where the ball will land.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 33 steps, 5 submissions, 594 s, $0.128.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1.1: blinded, held-out game policy (rerun). Status: done.

## Result

**VERIFIED AND COMPLETE**: every stage of the network has a verified site.

Run in place of the network, the construction makes the same decision on 100.0% of 3000 held-out inputs (a constant output: 46.7%). Construction length: 3,978 characters.

## The mechanism, in the reader's words

A gated three-way comparison on a 0/1 input laid out as 100 groups of 6 (index 6k+r; data in r=3 and r=4). h1: only columns 0..5 of W1 are nonzero (units 6..31 dead, b1=0 except b1[5]=5). Units 0..3 are small linear forms of the input (|h1|<=0.18, i.e. essentially their preactivation): unit j sums the r=3 position of each group with a drifting triangular 0.02-valued profile (plus a shared ramp on the last nine even positions). Units 4 and 5 have huge norms (1499, 745), so they saturate to +-1: they are two selectors, a = h1[4] (period-10 ramp on r=3 / r=4 pairs) and b = h1[5] (level k//10 of the group index, the r=4 side negated, plus bias 5). h2: W2 uses rows 0..5 and columns 0..7 only with b2 = -415, so each h2 unit is a threshold detector pre2 = -1000*h1[j//2]*(+1 for even j, -1 for odd) + 200*(sA_j*a + sB_j*b) - 415. Pair (2i,2i+1) can be armed only by one (sign a, sign b) combination: (+,+)->i=0, (-,+)->i=1, (+,-)->i=2, (-,-)->i=3, and then h2[2i] = +1 iff h1[i] < -0.015, h2[2i+1] = +1 iff h1[i] > +0.015 (the other pairs stay at -1). out: W3 puts 30 on h2 units 0,2,4,6 into out1 and on 1,3,5,7 into out3, b3 = [0,90,-100,90,-100,-100], hence out1 = 60*S1-30, out3 = 60*S3-30 with S in {0,1}, out0 = 0 and out2 = out4 = out5 = -100. Decision: the selectors pick one of h1[0..3]; out3 wins if it exceeds +0.015, out1 if it is below -0.015, and the constant out0 = 0 if it lies in between.

## The reader's final summary

**Mechanism (verified complete, 100% decision agreement, R²=1.000).**

The network is a gated three-way comparison on a 0/1 input laid out as 100 groups of 6 (`index = 6k+r`, data at r=3 and r=4).

- **h1 (only 6 live units).** `W1` columns 6–31 are zero and `b1=0` except `b1[5]=5`. Units 0–3 are small linear forms (|h1|≤0.18, so essentially their preactivation): each sums the r=3 slot of every group with a drifting triangular 0.02-valued profile, plus a shared linear ramp over the last nine even positions. Units 4 and 5 have huge weight norms (1499, 745) so they saturate to ±1 — two **selectors**: `a = h1[4]` (a period-10 ramp on r=3/r=4 pairs) and `b = h1[5]` (the level `k//10` of the group index, r=4 side negated, plus bias 5).

- **h2 (only 8 live units).** `W2` touches rows 0–5 and columns 0–7, with `b2=-415`, making each a threshold detector `pre2 = ∓1000·h1[j//2] + 200(±a ±b) − 415`. The pair (2i, 2i+1) is armed by exactly one (sign a, sign b) combination — (+,+)→i=0, (−,+)→i=1, (+,−)→i=2, (−,−)→i=3 — and then reports `h1[i] < −0.015` on the even unit and `h1[i] > +0.015` on the odd one.

- **out.** `W3` puts 30 on h2 units 0,2,4,6 into output 1 and on 1,3,5,7 into output 3, with `b3 = [0,90,−100,90,−100,−100]`; out0 = 0 and outputs 2,4,5 are the constant −100. So out1 = 60·S1−30 and out3 = 60·S3−30 (S ∈ {0,1}): the selectors pick one of h1[0..3], output 3 wins if it exceeds +0.015, output 1 if it is below −0.015, and the constant output 0 if it lies in between.

Both stages verified: the seven variables (four h1 linear forms, two selectors, the 8-unit h2 pattern) reconstruct every site exactly and survive all interchange, partial-substitution and edit tests.

## Stages

| Stage | Status | Sites |
|---|---|---|
| hidden layer 1 | verified | h1 |
| hidden layer 2 | verified | h2 |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `h1u0` | 1 | h1 |
| `h1u1` | 1 | h1 |
| `h1u2` | 1 | h1 |
| `h1u3` | 1 | h1 |
| `sel_a` | 1 | h1 |
| `sel_b` | 1 | h1 |
| `h2` | 8 | h2 |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `h1` | 6 / 5 | 1.00 | 100.0% | 46.7% | 46.7% | yes |
| `h2` | 8 / 5 | 1.00 | 100.0% | 46.7% | 46.7% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `h1` | 100.0% | 100.0% | 0.0% | yes |
| partial | `h1u0` | `h1` | 100.0% | 36.4% | 0.0% | yes |
| partial | `h1u1` | `h1` | 100.0% | 39.4% | 0.0% | yes |
| partial | `h1u2` | `h1` | 100.0% | 40.7% | 0.0% | yes |
| partial | `h1u3` | `h1` | 100.0% | 39.6% | 0.0% | yes |
| partial | `sel_a` | `h1` | 100.0% | 37.5% | 0.0% | yes |
| partial | `sel_b` | `h1` | 100.0% | 37.4% | 0.0% | yes |
| edit | `all variables` | `h1` | 100.0% | 54.3% | 0.0% | yes |
| interchange | `h2` | `h2` | 100.0% | 100.0% | 100.0% | yes |
| edit | `h2` | `h2` | 99.7% | 62.6% | 100.0% | yes |

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py astra_breakout lab/constructions/astra_breakout/20261114-003532-cfd2/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py astra_breakout lab/constructions/astra_breakout/20261114-003532-cfd2/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py astra_breakout --steps 80   # a fresh run with the same settings (needs lab/.env)
```
