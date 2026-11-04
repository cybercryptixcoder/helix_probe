# FIND results: find-v2

Sample: `bench/find/data`; up to 25 learn steps per function; exam of 4 probes (v2 arms). Scores are FIND's official code-based metrics: numeric = share of functions with normalised error < 0.1 on x in [-127.5, 127.5]; strings = share of FIND's test pairs reproduced exactly. `at 3` / `at 10` = the score of the model each run had after 3 / 10 experiments (FIND's GPT-4 agent used a median of about 3). `experiments` excludes the exam, which adds 4 probes per v2 run; `inputs` is every value sent to the function, exam included. Cost at DeepSeek's list price.

## numeric

| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |
|---|---|---|---|---|---|---|---|---|---|
| v2-no-theorist | 40 | **0.90** | 0.75 | 0.85 | 17.6 | 290 | 22 | $2.35 | 0.86 |
| v1 | 40 | **0.88** | 0.62 | 0.88 | 25.0 | 449 | 42 | $3.31 | 0.83 |
| v2 | 40 | **0.88** | 0.72 | 0.88 | 18.0 | 299 | 26 | $3.58 | 0.83 |
| v2-directed | 40 | **0.80** | 0.72 | 0.80 | 16.9 | 367 | 38 | $4.70 | 0.78 |
| v2-random | 40 | **0.75** | 0.55 | 0.68 | 16.7 | 207 | 21 | $5.10 | 0.75 |
| published: gpt-4 | 40 | **0.20** | - | - | 3.2 | 24 | - | - | - |
| published: gpt-3.5-turbo | 40 | **0.12** | - | - | 1.2 | 8 | - | - | - |
| published: llama-2-70b | 40 | **0.03** | - | - | 7.4 | 2 | - | - | - |
| published: llama-2-13b | 40 | **0.00** | - | - | 2.5 | 3 | - | - | - |

## strings

| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |
|---|---|---|---|---|---|---|---|---|---|
| v2 | 20 | **1.00** | 0.93 | 1.00 | 10.7 | 108 | 9 | $0.22 | 0.99 |
| v2-directed | 20 | **1.00** | 0.80 | 0.94 | 12.3 | 147 | 18 | $0.40 | 0.99 |
| v2-no-theorist | 19 | **0.99** | 0.93 | 0.99 | 11.6 | 115 | 8 | $0.16 | 1.00 |
| v2-random | 20 | **0.89** | 0.89 | 0.89 | 11.8 | 95 | 3 | $0.11 | 1.00 |
| v1 | 19 | **0.85** | 0.61 | 0.83 | 24.6 | 241 | 37 | $0.85 | 0.92 |
| published: gpt-3.5-turbo | 40 | **0.05** | - | - | 2.4 | 4 | - | - | - |
| published: llama-2-70b | 40 | **0.04** | - | - | 2.9 | 4 | - | - | - |
| published: gpt-4 | 40 | **0.01** | - | - | 3.0 | 15 | - | - | - |
| published: llama-2-13b | 36 | **0.00** | - | - | 2.4 | 4 | - | - | - |
