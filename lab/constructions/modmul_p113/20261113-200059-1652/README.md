# Construction run `20261113-200059-1652` on `modmul_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer C (226,048 weights). Known answer (never shown to a blinded reader): (a * b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 20; used 5 steps, 0 submissions, 0 s, $0.068.
- Weights: original. Reader was told the task, had NO weights and could not run the network (prior-only control), and had a single submission with no report back.
- Title: v1.1: prior-only. Status: interrupted.

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
python3 lab/judge.py modmul_p113 lab/constructions/modmul_p113/20261113-200059-1652/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modmul_p113 lab/constructions/modmul_p113/20261113-200059-1652/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modmul_p113 --told --no-weights --one-shot --steps 20   # a fresh run with the same settings (needs lab/.env)
```
