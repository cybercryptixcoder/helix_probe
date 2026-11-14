# Construction run `20261113-141703-5649` on `modadd_p113`

*Written by `lab/results.py` from the files in this folder. Network: Mystery transformer A (226,048 weights). Known answer (never shown to a blinded reader): (a + b) mod 113.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 60; used 30 steps, 4 submissions, 0 s, $0.097.
- Weights: shuffled. Reader was blinded (not told what the network does).
- Title: control: shuffled, blinded. Status: interrupted.

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
python3 lab/judge.py modadd_p113 lab/constructions/modadd_p113/20261113-141703-5649/construction.py --variant shuffled        # re-run every test on the delivered construction
python3 lab/predict.py modadd_p113 lab/constructions/modadd_p113/20261113-141703-5649/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py modadd_p113 --variant shuffled --steps 60   # a fresh run with the same settings (needs lab/.env)
```
