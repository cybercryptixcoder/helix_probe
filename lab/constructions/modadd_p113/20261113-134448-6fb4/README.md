# Construction run `20261113-134448-6fb4` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 40; used 40 steps, 0 submissions, 676 s, $0.087.
- Weights: original. Reader was blinded (not told what the network does).
- Title: dev1 blinded. Status: done.

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
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261113-134448-6fb4/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261113-134448-6fb4/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --steps 40   # a fresh run with the same settings (needs lab/.env)
```
