# FIND results: find-v2

Sample: `bench/find/data`; up to 25 learn steps per function; exam of 4 probes (v2 arms). Scores are FIND's official code-based metrics: numeric = share of functions with normalised error < 0.1 on x in [-127.5, 127.5]; strings = share of FIND's test pairs reproduced exactly. `at 3` / `at 10` = the score of the model each run had after 3 / 10 experiments (FIND's GPT-4 agent used a median of about 3). `experiments` excludes the exam, which adds 4 probes per v2 run; `inputs` is every value sent to the function, exam included. Cost at DeepSeek's list price.

## numeric

| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |
|---|---|---|---|---|---|---|---|---|---|
| v2 | 36 | **0.92** | 0.75 | 0.92 | 18.0 | 298 | 25 | $2.99 | 0.87 |
| v2-no-theorist | 36 | **0.92** | 0.78 | 0.86 | 17.7 | 292 | 21 | $2.10 | 0.87 |
| v1 | 36 | **0.89** | 0.64 | 0.89 | 25.0 | 450 | 42 | $3.04 | 0.84 |
| v2-directed | 37 | **0.81** | 0.73 | 0.81 | 17.1 | 372 | 38 | $4.52 | 0.79 |
| v2-random | 35 | **0.77** | 0.57 | 0.69 | 16.6 | 206 | 20 | $4.16 | 0.77 |
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
