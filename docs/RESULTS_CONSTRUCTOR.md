# Constructor results

*Written by `lab/results.py` on 2026-11-13 19:45 from the run folders in `lab/constructions/`. Do not edit by hand; rerun the script. The reader is DeepSeek V4.1 Flash. "Blinded" means the reader was given the architecture, the weights and the input set, and was not told what the network does. Development networks are the ones the constructor's prompt and the judge were worked out on; held-out networks were run only after both were frozen.*

## Best blinded run per network (trained weights)

| Network | What it computes (hidden from the reader) | Used in development? | Stages verified | Behaviour match | Steps | Run |
|---|---|---|---|---|---|---|
| `bool_compare2` | (2*x1 + x2) > (2*x3 + x4): is the 2-bit number a1a0 greater than b1b0 | yes | **all 1 (complete)** | 100.0% | 2 | [`20261113-143146-0bcf`](../lab/constructions/bool_compare2/20261113-143146-0bcf/README.md) (best of 1) |
| `bool_majority3` | majority(x1, x2, x3): 1 if at least two inputs are 1 | yes | **all 1 (complete)** | 100.0% | 2 | [`20261113-143146-02b7`](../lab/constructions/bool_majority3/20261113-143146-02b7/README.md) (best of 1) |
| `bool_parity3` | x1 XOR x2 XOR x3 (odd number of ones) | yes | **all 1 (complete)** | 100.0% | 2 | [`20261113-143146-d2db`](../lab/constructions/bool_parity3/20261113-143146-d2db/README.md) (best of 1) |
| `bool_xor` | x1 XOR x2 | yes | **all 1 (complete)** | 100.0% | 2 | [`20261113-134430-3f45`](../lab/constructions/bool_xor/20261113-134430-3f45/README.md) (best of 1) |
| `modadd_p113` | (a + b) mod 113 | yes | 3 of 4 | 100.0% | 60 | [`20261113-135953-158c`](../lab/constructions/modadd_p113/20261113-135953-158c/README.md) (best of 5) |
| `modmul_p113` | (a * b) mod 113 | **no (held out)** | **all 4 (complete)** | 97.3% | 76 | [`20261113-190435-ec84`](../lab/constructions/modmul_p113/20261113-190435-ec84/README.md) (best of 1) |
| `tracr_count_greater` | output i is the number of tokens greater than token i | **no (held out)** | **all 4 (complete)** | 100.0% | 47 | [`20261113-190435-53c5`](../lab/constructions/tracr_count_greater/20261113-190435-53c5/README.md) (best of 1) |
| `tracr_first_match` | output i is 1 if token i equals the first token, else 0 | **no (held out)** | **all 4 (complete)** | 100.0% | 23 | [`20261113-190435-e5f5`](../lab/constructions/tracr_first_match/20261113-190435-e5f5/README.md) (best of 1) |
| `tracr_hist` | histogram: output i is the number of tokens equal to token i | yes | **all 4 (complete)** | 100.0% | 21 | [`20261113-143146-5ab6`](../lab/constructions/tracr_hist/20261113-143146-5ab6/README.md) (best of 1) |
| `tracr_reverse` | reverse the sequence: output i is token N-1-i | **no (held out)** | **all 9 (complete)** | 100.0% | 9 | [`20261113-190435-5458`](../lab/constructions/tracr_reverse/20261113-190435-5458/README.md) (best of 1) |

## Controls

Shuffled and untrained weights should give no verified construction; permuted weights (the same function, units reordered) should give the same one; the prior-only reader (task named, no weights, one submission) shows what memory alone gives.

| Network | Control | Stages verified | Behaviour match | Steps | Run |
|---|---|---|---|---|---|
| `modadd_p113` | permuted | no construction | n/a | 27 | [`20261113-141703-a75f`](../lab/constructions/modadd_p113/20261113-141703-a75f/README.md) control: permuted, blinded |
| `modadd_p113` | prior-only | 0 of 4 | 100.0% | 2 | [`20261113-141703-0b38`](../lab/constructions/modadd_p113/20261113-141703-0b38/README.md) control: prior-only (task named, no weights, one submission) |
| `modadd_p113` | shuffled | no construction | n/a | 30 | [`20261113-141703-5649`](../lab/constructions/modadd_p113/20261113-141703-5649/README.md) control: shuffled, blinded |
| `modadd_p113` | untrained | no construction | n/a | 53 | [`20261113-141703-0114`](../lab/constructions/modadd_p113/20261113-141703-0114/README.md) control: untrained, blinded |

All runs, including failed and superseded ones: [`lab/constructions/INDEX.md`](../lab/constructions/INDEX.md). What each experiment was for and what was concluded: [`EXPERIMENT_LOG.md`](EXPERIMENT_LOG.md).
