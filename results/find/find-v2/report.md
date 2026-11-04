# FIND results: find-v2

Sample: `bench/find/data`; up to 25 learn steps per function; exam of 4 probes (v2 arms). Scores are FIND's official code-based metrics: numeric = share of functions with normalised error < 0.1 on x in [-127.5, 127.5]; strings = share of FIND's test pairs reproduced exactly. `at 3` / `at 10` = the score of the model each run had after 3 / 10 experiments (FIND's GPT-4 agent used a median of about 3). `experiments` excludes the exam, which adds 4 probes per v2 run; `inputs` is every value sent to the function, exam included. Cost at DeepSeek's list price.

## numeric

| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |
|---|---|---|---|---|---|---|---|---|---|
| v2-no-theorist | 24 | **1.00** | 0.79 | 0.92 | 17.4 | 288 | 19 | $1.40 | 0.94 |
| v1 | 24 | **0.96** | 0.67 | 0.96 | 25.0 | 453 | 40 | $2.02 | 0.89 |
| v2 | 24 | **0.96** | 0.79 | 0.96 | 18.1 | 298 | 24 | $2.17 | 0.90 |
| v2-random | 24 | **0.88** | 0.62 | 0.79 | 15.6 | 196 | 15 | $2.01 | 0.85 |
| v2-directed | 23 | **0.87** | 0.87 | 0.87 | 16.3 | 355 | 32 | $2.41 | 0.85 |
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
