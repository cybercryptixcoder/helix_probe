# FIND: Helix Probe vs the same model in FIND's own protocol

AIA control: `results/find/aia-none` (80 functions). Scores: FIND's official scorer. Paired over the functions both finished. CI: 95% bootstrap of the mean difference. p: exact two-sided sign test on the functions that differ.

## numeric

| Helix Probe arm | n | AIA (same model) | Helix final | Helix at the AIA's inputs | diff [95% CI] | wins / losses / ties | p | Helix at the AIA's experiments | published GPT-4 |
|---|---|---|---|---|---|---|---|---|---|
| find-v3/v3 | 40 | 0.38 | 0.82 | **0.40** | +0.03 [-0.07, +0.12] | 3 / 2 / 35 | 1 | 0.42 | 0.20 |
| find-v3/v3-exam | 40 | 0.38 | 0.88 | **0.33** | -0.05 [-0.20, +0.10] | 4 / 6 / 30 | 0.754 | 0.50 | 0.20 |
| find-v3-s1/v3 | 40 | 0.38 | 0.88 | **0.42** | +0.05 [-0.07, +0.17] | 4 / 2 / 34 | 0.688 | 0.45 | 0.20 |
| find-v2/v1 | 40 | 0.38 | 0.88 | **0.45** | +0.07 [-0.07, +0.23] | 6 / 3 / 31 | 0.508 | 0.50 | 0.20 |
| find-v2/v2 | 40 | 0.38 | 0.88 | **0.35** | -0.03 [-0.20, +0.15] | 6 / 7 / 27 | 1 | 0.53 | 0.20 |
| find-v2/v2-directed | 40 | 0.38 | 0.80 | **0.30** | -0.07 [-0.23, +0.07] | 3 / 6 / 31 | 0.508 | 0.45 | 0.20 |
| find-v2/v2-no-theorist | 40 | 0.38 | 0.90 | **0.38** | +0.00 [-0.17, +0.17] | 6 / 6 / 28 | 1 | 0.50 | 0.20 |
| find-v2/v2-random | 40 | 0.38 | 0.75 | **0.25** | -0.12 [-0.30, +0.05] | 4 / 9 / 27 | 0.267 | 0.35 | 0.20 |

Budget per function (first arm): AIA 7.2 experiments / 94 inputs; Helix Probe 17.6 experiments / 253 inputs (exam included).

## strings

| Helix Probe arm | n | AIA (same model) | Helix final | Helix at the AIA's inputs | diff [95% CI] | wins / losses / ties | p | Helix at the AIA's experiments | published GPT-4 |
|---|---|---|---|---|---|---|---|---|---|
| find-v3/v3 | 40 | 0.46 | 0.91 | **0.45** | -0.02 [-0.12, +0.08] | 3 / 5 / 32 | 0.727 | 0.47 | 0.01 |
| find-v3/v3-exam | 40 | 0.46 | 0.97 | **0.37** | -0.10 [-0.20, +0.01] | 2 / 9 / 29 | 0.0654 | 0.55 | 0.01 |
| find-v3-s1/v3 | 40 | 0.46 | 0.93 | **0.50** | +0.03 [-0.04, +0.12] | 4 / 3 / 33 | 1 | 0.53 | 0.01 |
| find-v2/v1 | 40 | 0.46 | 0.85 | **0.40** | -0.06 [-0.15, +0.04] | 2 / 7 / 31 | 0.18 | 0.45 | 0.01 |
| find-v2/v2 | 40 | 0.46 | 0.92 | **0.37** | -0.10 [-0.20, +0.01] | 2 / 9 / 29 | 0.0654 | 0.55 | 0.01 |
| find-v2/v2-directed | 40 | 0.46 | 0.96 | **0.28** | -0.18 [-0.31, -0.06] | 1 / 12 / 27 | 0.00342 | 0.51 | 0.01 |
| find-v2/v2-no-theorist | 40 | 0.46 | 0.91 | **0.36** | -0.11 [-0.21, -0.00] | 1 / 9 / 30 | 0.0215 | 0.50 | 0.01 |
| find-v2/v2-random | 40 | 0.46 | 0.89 | **0.36** | -0.11 [-0.21, -0.00] | 1 / 9 / 30 | 0.0215 | 0.50 | 0.01 |

Budget per function (first arm): AIA 2.8 experiments / 29 inputs; Helix Probe 12.8 experiments / 101 inputs (exam included).

