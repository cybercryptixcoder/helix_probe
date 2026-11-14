# Constructor runs

*Written by `lab/results.py` on 2026-11-13 19:45. Every run of `lab/constructor.py`, grouped by network, best first. Each run id links to that run's page.*

## `bool_compare2`: (2*x1 + x2) > (2*x3 + x4): is the 2-bit number a1a0 greater than b1b0

| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |
|---|---|---|---|---|---|---|---|---|
| [`20261113-143146-0bcf`](bool_compare2/20261113-143146-0bcf/README.md) | blinded | dev smoke | done | **complete** | 100.0% | 2 | 1 | $0.00 |

## `bool_majority3`: majority(x1, x2, x3): 1 if at least two inputs are 1

| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |
|---|---|---|---|---|---|---|---|---|
| [`20261113-143146-02b7`](bool_majority3/20261113-143146-02b7/README.md) | blinded | dev smoke | done | **complete** | 100.0% | 2 | 1 | $0.00 |

## `bool_parity3`: x1 XOR x2 XOR x3 (odd number of ones)

| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |
|---|---|---|---|---|---|---|---|---|
| [`20261113-143146-d2db`](bool_parity3/20261113-143146-d2db/README.md) | blinded | dev smoke | done | **complete** | 100.0% | 2 | 1 | $0.00 |

## `bool_xor`: x1 XOR x2

| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |
|---|---|---|---|---|---|---|---|---|
| [`20261113-134430-3f45`](bool_xor/20261113-134430-3f45/README.md) | blinded |  | done | **complete** | 100.0% | 2 | 1 | $0.00 |
| [`20261113-190811-eb9c`](bool_xor/20261113-190811-eb9c/README.md) | blinded | frontend live test | done | **complete** | 100.0% | 2 | 1 | $0.00 |

## `modadd_p113`: (a + b) mod 113

| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |
|---|---|---|---|---|---|---|---|---|
| [`20261113-135953-158c`](modadd_p113/20261113-135953-158c/README.md) | blinded | dev3 blinded, forced submit turns | done | 3 of 4 stages | 100.0% | 60 | 12 | $0.11 |
| [`20261113-134448-6fb4`](modadd_p113/20261113-134448-6fb4/README.md) | blinded | dev1 blinded | done | no construction | n/a | 40 | 0 | $0.09 |
| [`20261113-135657-e428`](modadd_p113/20261113-135657-e428/README.md) | blinded | dev2 blinded, submit-early rule | interrupted | no construction | n/a | 23 | 0 | $0.02 |
| [`20261113-141703-4d1e`](modadd_p113/20261113-141703-4d1e/README.md) | blinded | blinded replicate 2 | interrupted | no construction | n/a | 33 | 4 | $0.11 |
| [`20261113-143146-4fc2`](modadd_p113/20261113-143146-4fc2/README.md) | blinded | dev4 blinded, judge v2 (necessity, compactness, per-variable interchange) | interrupted | no construction | n/a | 28 | 3 | $0.05 |
| [`20261113-190435-0c92`](modadd_p113/20261113-190435-0c92/README.md) | blinded | v1 official: blinded, replicate A | running | no construction | n/a | 71 | 10 | $0.31 |
| [`20261113-141703-0b38`](modadd_p113/20261113-141703-0b38/README.md) | prior-only | control: prior-only (task named, no weights, one submission) | done | 0 of 4 stages | 100.0% | 2 | 1 | $0.05 |
| [`20261113-141703-0114`](modadd_p113/20261113-141703-0114/README.md) | untrained | control: untrained, blinded | interrupted | no construction | n/a | 53 | 8 | $0.12 |
| [`20261113-141703-5649`](modadd_p113/20261113-141703-5649/README.md) | shuffled | control: shuffled, blinded | interrupted | no construction | n/a | 30 | 4 | $0.10 |
| [`20261113-141703-a75f`](modadd_p113/20261113-141703-a75f/README.md) | permuted | control: permuted, blinded | interrupted | no construction | n/a | 27 | 3 | $0.10 |
| [`20261113-190435-2730`](modadd_p113/20261113-190435-2730/README.md) | shuffled | v1 official: control shuffled | running | no construction | n/a | 68 | 11 | $0.27 |
| [`20261113-190435-48d0`](modadd_p113/20261113-190435-48d0/README.md) | permuted | v1 official: control permuted | running | no construction | n/a | 76 | 12 | $0.30 |
| [`20261113-190435-9b22`](modadd_p113/20261113-190435-9b22/README.md) | untrained | v1 official: control untrained | running | no construction | n/a | 75 | 11 | $0.35 |

## `modmul_p113`: (a * b) mod 113

| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |
|---|---|---|---|---|---|---|---|---|
| [`20261113-190435-ec84`](modmul_p113/20261113-190435-ec84/README.md) | blinded | v1 official: blinded, held-out | done | **complete** | 97.3% | 76 | 14 | $0.32 |

## `tracr_count_greater`: output i is the number of tokens greater than token i

| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |
|---|---|---|---|---|---|---|---|---|
| [`20261113-190435-53c5`](tracr_count_greater/20261113-190435-53c5/README.md) | blinded | v1 official: blinded, held-out | done | **complete** | 100.0% | 47 | 8 | $0.18 |

## `tracr_first_match`: output i is 1 if token i equals the first token, else 0

| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |
|---|---|---|---|---|---|---|---|---|
| [`20261113-190435-e5f5`](tracr_first_match/20261113-190435-e5f5/README.md) | blinded | v1 official: blinded, held-out | done | **complete** | 100.0% | 23 | 5 | $0.09 |

## `tracr_hist`: histogram: output i is the number of tokens equal to token i

| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |
|---|---|---|---|---|---|---|---|---|
| [`20261113-143146-5ab6`](tracr_hist/20261113-143146-5ab6/README.md) | blinded | dev1 blinded | done | **complete** | 100.0% | 21 | 3 | $0.09 |

## `tracr_reverse`: reverse the sequence: output i is token N-1-i

| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |
|---|---|---|---|---|---|---|---|---|
| [`20261113-190435-5458`](tracr_reverse/20261113-190435-5458/README.md) | blinded | v1 official: blinded, held-out | done | **complete** | 100.0% | 9 | 2 | $0.03 |
