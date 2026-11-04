# FIND results: find-v2

Sample: `bench/find/data`; up to 25 learn steps per function; exam of 4 probes (v2 arms). Scores are FIND's official code-based metrics: numeric = share of functions with normalised error < 0.1 on x in [-127.5, 127.5]; strings = share of FIND's test pairs reproduced exactly. `at 3` / `at 10` = the score of the model each run had after 3 / 10 experiments (FIND's GPT-4 agent used a median of about 3). `experiments` excludes the exam, which adds 4 probes per v2 run; `inputs` is every value sent to the function, exam included. Cost at DeepSeek's list price.

## numeric

| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |
|---|---|---|---|---|---|---|---|---|---|
| v1 | 10 | **1.00** | 0.50 | 1.00 | 25.0 | 473 | 45 | $0.98 | 0.85 |
| v2 | 10 | **1.00** | 0.90 | 1.00 | 18.2 | 305 | 23 | $0.76 | 0.94 |
| v2-directed | 10 | **1.00** | 1.00 | 1.00 | 14.5 | 325 | 23 | $0.51 | 0.96 |
| v2-no-theorist | 10 | **1.00** | 0.80 | 0.90 | 18.9 | 312 | 23 | $0.66 | 0.85 |
| v2-random | 9 | **1.00** | 0.78 | 1.00 | 15.6 | 196 | 14 | $0.54 | 0.88 |
| published: gpt-4 | 40 | **0.20** | - | - | 3.2 | 24 | - | - | - |
| published: gpt-3.5-turbo | 40 | **0.12** | - | - | 1.2 | 8 | - | - | - |
| published: llama-2-70b | 40 | **0.03** | - | - | 7.4 | 2 | - | - | - |
| published: llama-2-13b | 40 | **0.00** | - | - | 2.5 | 3 | - | - | - |

## strings

| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |
|---|---|---|---|---|---|---|---|---|---|
| published: gpt-3.5-turbo | 40 | **0.05** | - | - | 2.4 | 4 | - | - | - |
| published: llama-2-70b | 40 | **0.04** | - | - | 2.9 | 4 | - | - | - |
| published: gpt-4 | 40 | **0.01** | - | - | 3.0 | 15 | - | - | - |
| published: llama-2-13b | 36 | **0.00** | - | - | 2.4 | 4 | - | - | - |
