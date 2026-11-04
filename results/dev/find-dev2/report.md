# FIND results: dev2

Sample: `bench/find/dev`; up to 20 learn steps per function; exam of 4 probes (v2 arms). Scores are FIND's official code-based metrics: numeric = share of functions with normalised error < 0.1 on x in [-127.5, 127.5]; strings = share of FIND's test pairs reproduced exactly. `at 3` / `at 10` = the score of the model each run had after 3 / 10 experiments (FIND's GPT-4 agent used a median of about 3). `experiments` excludes the exam, which adds 4 probes per v2 run; `inputs` is every value sent to the function, exam included. Cost at DeepSeek's list price.

## numeric

| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |
|---|---|---|---|---|---|---|---|---|---|
| v2 | 8 | **1.00** | 1.00 | 1.00 | 12.5 | 282 | 24 | $0.35 | 1.00 |
| v2-mixed | 8 | **1.00** | 0.88 | 1.00 | 13.5 | 225 | 15 | $0.26 | 1.00 |

## strings

| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |
|---|---|---|---|---|---|---|---|---|---|
| v2 | 8 | **1.00** | 0.90 | 1.00 | 14.5 | 169 | 22 | $0.33 | 1.00 |
| v2-mixed | 8 | **1.00** | 0.88 | 0.99 | 14.2 | 136 | 16 | $0.25 | 1.00 |
