# Construction run `20261114-114434-f065` on `gpt2_countdown`

*Written by `lab/results.py` from the files in this folder. Network: gpt2_countdown (124,439,808 weights). Known answer (never shown to a blinded reader): GPT-2 small continues the run: n4 + 1 after an increasing run, n4 - 1 after a decreasing run..*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 5 steps, 1 submissions, 1066 s, $0.063.
- Weights: original. Reader was told the task, had NO weights and could not run the network (prior-only control), and had a single submission with no report back.
- Title: prior-only control 1. Status: done.

## Result

No submission could be judged.


## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py gpt2_countdown lab/constructions/gpt2_countdown/20261114-114434-f065/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py gpt2_countdown lab/constructions/gpt2_countdown/20261114-114434-f065/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py gpt2_countdown --told --no-weights --one-shot --steps 80   # a fresh run with the same settings (needs lab/.env)
```
