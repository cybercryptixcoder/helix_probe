# FIND: Helix Probe vs the same model in FIND's own protocol

AIA control: `results/find/aia-none-r2` (80 functions). Scores: FIND's official scorer. Paired over the functions both finished. CI: 95% bootstrap of the mean difference. p: exact two-sided sign test on the functions that differ.

## numeric

| Helix Probe arm | n | AIA (same model) | Helix final | Helix at the AIA's inputs | diff [95% CI] | wins / losses / ties | p | Helix at the AIA's experiments | published GPT-4 |
|---|---|---|---|---|---|---|---|---|---|
| find-v3/v3 | 40 | 0.38 | 0.82 | **0.53** | +0.15 [+0.03, +0.28] | 7 / 1 / 32 | 0.0703 | 0.55 | 0.20 |
| find-v3/v3-exam | 40 | 0.38 | 0.88 | **0.45** | +0.07 [-0.07, +0.23] | 6 / 3 / 31 | 0.508 | 0.60 | 0.20 |
| find-v3-s1/v3 | 40 | 0.38 | 0.88 | **0.55** | +0.17 [+0.05, +0.33] | 8 / 1 / 31 | 0.0391 | 0.57 | 0.20 |
| find-v2/v1 | 40 | 0.38 | 0.88 | **0.55** | +0.17 [+0.03, +0.33] | 9 / 2 / 29 | 0.0654 | 0.60 | 0.20 |
| find-v2/v2 | 40 | 0.38 | 0.88 | **0.45** | +0.07 [-0.10, +0.25] | 8 / 5 / 27 | 0.581 | 0.62 | 0.20 |
| find-v2/v2-directed | 40 | 0.38 | 0.80 | **0.38** | +0.00 [-0.15, +0.15] | 5 / 5 / 30 | 1 | 0.57 | 0.20 |
| find-v2/v2-no-theorist | 40 | 0.38 | 0.90 | **0.47** | +0.10 [-0.05, +0.28] | 8 / 4 / 28 | 0.388 | 0.62 | 0.20 |
| find-v2/v2-random | 40 | 0.38 | 0.75 | **0.38** | +0.00 [-0.15, +0.15] | 5 / 5 / 30 | 1 | 0.50 | 0.20 |

Budget per function (first arm): AIA 8.3 experiments / 90 inputs; Helix Probe 17.6 experiments / 253 inputs (exam included).

## strings

| Helix Probe arm | n | AIA (same model) | Helix final | Helix at the AIA's inputs | diff [95% CI] | wins / losses / ties | p | Helix at the AIA's experiments | published GPT-4 |
|---|---|---|---|---|---|---|---|---|---|
| find-v3/v3 | 40 | 0.40 | 0.91 | **0.46** | +0.06 [-0.03, +0.16] | 6 / 1 / 33 | 0.125 | 0.46 | 0.01 |
| find-v3/v3-exam | 40 | 0.40 | 0.97 | **0.39** | -0.01 [-0.12, +0.09] | 5 / 4 / 31 | 1 | 0.49 | 0.01 |
| find-v3-s1/v3 | 40 | 0.40 | 0.93 | **0.43** | +0.03 [-0.05, +0.12] | 6 / 2 / 32 | 0.289 | 0.43 | 0.01 |
| find-v2/v1 | 40 | 0.40 | 0.85 | **0.35** | -0.05 [-0.14, +0.03] | 3 / 4 / 33 | 1 | 0.39 | 0.01 |
| find-v2/v2 | 40 | 0.40 | 0.92 | **0.36** | -0.04 [-0.15, +0.08] | 4 / 6 / 30 | 0.754 | 0.46 | 0.01 |
| find-v2/v2-directed | 40 | 0.40 | 0.96 | **0.31** | -0.09 [-0.21, +0.03] | 3 / 8 / 29 | 0.227 | 0.39 | 0.01 |
| find-v2/v2-no-theorist | 40 | 0.40 | 0.91 | **0.31** | -0.08 [-0.21, +0.03] | 3 / 8 / 29 | 0.227 | 0.43 | 0.01 |
| find-v2/v2-random | 40 | 0.40 | 0.89 | **0.32** | -0.07 [-0.19, +0.04] | 3 / 8 / 29 | 0.227 | 0.43 | 0.01 |

Budget per function (first arm): AIA 3.9 experiments / 38 inputs; Helix Probe 12.8 experiments / 101 inputs (exam included).

