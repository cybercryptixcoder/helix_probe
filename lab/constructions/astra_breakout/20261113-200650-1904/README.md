# Construction run `20261113-200650-1904` on `astra_breakout`

*Written by `lab/results.py` from the files in this folder. Network: Hand-written game policy (20,486 weights). Known answer (never shown to a blinded reader): a policy for MinAtar Breakout: move the paddle under where the ball will land.*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 80; used 14 steps, 2 submissions, 0 s, $0.023.
- Weights: original. Reader was blinded (not told what the network does).
- Title: v1.1: blinded, held-out game policy. Status: interrupted.

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
python3 lab/judge.py astra_breakout lab/constructions/astra_breakout/20261113-200650-1904/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py astra_breakout lab/constructions/astra_breakout/20261113-200650-1904/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py astra_breakout --steps 80   # a fresh run with the same settings (needs lab/.env)
```
