# FIND results: dev1

Sample: `bench/find/dev`; up to 20 learn steps per function; exam of 4 probes (v2 arms). Scores are FIND's official code-based metrics: numeric = share of functions with normalised error < 0.1 on x in [-127.5, 127.5]; strings = share of FIND's test pairs reproduced exactly. `at 3` / `at 10` = the score of the model each run had after 3 / 10 experiments (FIND's GPT-4 agent used a median of about 3). `experiments` excludes the exam, which adds 4 probes per v2 run; `inputs` is every value sent to the function, exam included. Cost at DeepSeek's list price.

## numeric

| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |
|---|---|---|---|---|---|---|---|---|---|
| v1 | 7 | **1.00** | 0.86 | 1.00 | 20.0 | 320 | 28 | $0.28 | 1.00 |
| v2 | 8 | **1.00** | 1.00 | 1.00 | 12.9 | 285 | 23 | $0.34 | 1.00 |
| v2-no-exam | 8 | **1.00** | 1.00 | 1.00 | 12.4 | 242 | 20 | $0.33 | 1.00 |
| v2-no-theorist | 8 | **1.00** | 0.88 | 1.00 | 12.2 | 273 | 19 | $0.26 | 1.00 |
| v2-random | 8 | **0.88** | 0.88 | 0.88 | 13.5 | 175 | 7 | $0.26 | 0.92 |

## strings

| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |
|---|---|---|---|---|---|---|---|---|---|
| v2 | 8 | **1.00** | 0.78 | 0.90 | 15.4 | 177 | 26 | $0.46 | 1.00 |
| v2-no-theorist | 8 | **1.00** | 0.62 | 0.96 | 17.2 | 196 | 30 | $0.46 | 1.00 |
| v2-random | 8 | **1.00** | 1.00 | 1.00 | 12.0 | 96 | 4 | $0.11 | 0.98 |
| v1 | 8 | **0.90** | 0.34 | 0.68 | 19.9 | 189 | 32 | $0.31 | 0.78 |
| v2-no-exam | 7 | **0.89** | 0.74 | 0.89 | 14.9 | 148 | 26 | $0.41 | 0.88 |
