# Construction run `20261114-114450-62b2` on `gpt2_be_verb`

*Written by `lab/results.py` from the files in this folder. Network: gpt2_be_verb (124,439,808 weights). Known answer (never shown to a blinded reader): GPT-2 small prefers the form of 'to be' that agrees with the noun's number and the cue's tense: is / are / was / were..*

## The run

- Reader: deepseek-ai/DeepSeek-V4.1-Flash, reasoning effort high; step budget 100; used 22 steps, 4 submissions, 2638 s, $0.045.
- Weights: original. Reader was blinded (not told what the network does).
- Title: blinded run A. Status: stopped.

## Result

**2 of 5 stages verified**.

Run in place of the network, the construction makes the same decision on 100.0% of 360 held-out inputs (a constant output: 20.0%). Construction length: 1,778 characters.

## The mechanism, in the reader's words

Prompt: '<|endoftext|><cue>, the <noun>' (5 tokens; cue at position 1, noun at position 4 = last). Answer in [' is',' are',' was',' were'] = 2*TENSE + NUMBER, TENSE=1 iff cue in {Yesterday, Earlier, Previously, Once, Before, Originally} (cue index>=6), NUMBER=1 iff noun is a plural token (noun index>=30). Held quantities: (a) at the embedding, which cue word is at position 1 and which noun at position 4 - the residual there is just token+position embedding, so a one-hot of each token identity predicts it exactly; (b) through the middle layers the caret/copy path carries, at the last position, the answer class (tense,number); by layer 11 the last position holds exactly the 4-way answer class and nothing else is needed. model() turns the cue identity into a tense bit, the noun identity into a number bit, combines them into the 4-way class one-hot and reads the four answer scores off that class.

## Stages

| Stage | Status | Sites |
|---|---|---|
| embedding | named, failing | cut0 |
| layers 0-2 | named, failing | cut3 |
| layers 3-5 | named, failing | cut6 |
| layers 6-8 | verified | cut9 |
| layers 9-11 | verified | cut12 |

## Where each variable lives

| Variable | Dimensions | Sites |
|---|---|---|
| `cue_id` | 12 | resid0@1, resid3@1, resid3@2, resid6@1, resid6@2, resid9@1, resid9@2 |
| `noun_id` | 60 | resid0@4, resid3@4, resid6@2 |
| `anscls` | 4 | resid6@4, resid9@4, resid12@4 |

## Site tests

Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.

| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |
|---|---|---|---|---|---|---|
| `cut0` | 40 / 36 | 0.39 | 51.7% | 50.0% | 20.0% | no |
| `cut3` | 40 / 34 | 0.44 | 40.0% | 44.4% | 20.0% | no |
| `cut6` | 14 / 29 | 0.53 | 100.0% | 49.7% | 20.0% | no |
| `cut9` | 14 / 26 | 0.57 | 100.0% | 52.5% | 20.0% | yes |
| `cut12` | 3 / 12 | 0.09 | 100.0% | 42.8% | 20.0% | yes |

## Intervention tests

Share of cases where the predictor named the network's new decision, among cases where the decision changed ("no change" scores 0 on these by definition).

| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |
|---|---|---|---|---|---|---|
| interchange | `all variables` | `cut0` | 95.7% | 93.0% | 0.4% | yes |
| partial | `cue_id` | `cut0` | 100.0% | 50.2% | 0.5% | yes |
| partial | `noun_id` | `cut0` | 100.0% | 46.5% | 0.0% | yes |
| interchange | `all variables` | `cut3` | 100.0% | 100.0% | 2.7% | yes |
| partial | `cue_id` | `cut3` | 100.0% | 50.2% | 8.1% | yes |
| partial | `noun_id` | `cut3` | 100.0% | 50.2% | 0.0% | yes |
| interchange | `all variables` | `cut6` | 99.3% | 99.2% | 4.7% | yes |
| partial | `cue_id` | `cut6` | 98.9% | 48.0% | 11.5% | yes |
| partial | `noun_id` | `cut6` | 50.2% | 25.5% | n/a | no |
| partial | `anscls` | `cut6` | 50.0% | 50.5% | 0.5% | yes |
| interchange | `all variables` | `cut9` | 98.6% | 97.0% | 30.0% | yes |
| partial | `cue_id` | `cut9` | 100.0% | 38.2% | 62.0% | yes |
| partial | `anscls` | `cut9` | 61.6% | 59.8% | 28.1% | yes |
| interchange | `anscls` | `cut12` | 100.0% | 99.8% | 99.7% | yes |

## What fails

- substitution at cut0: 51.7% (need 90%)
- substitution at cut3: 40.0% (need 90%)
- partial of noun_id at cut6: the network's output changed in only 0.0% of cases, but the construction predicted changes: at this site the network's output does not depend on this variable

## Files

- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).
- `report.txt`, `report.json`: the judge's report on it.
- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.
- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.
- `predict.json` (if present): the held-out intervention benchmark.

## Reproduce

```bash
python3 lab/judge.py gpt2_be_verb lab/constructions/gpt2_be_verb/20261114-114450-62b2/construction.py        # re-run every test on the delivered construction
python3 lab/predict.py gpt2_be_verb lab/constructions/gpt2_be_verb/20261114-114450-62b2/construction.py              # held-out interventions against the baselines
python3 lab/constructor.py gpt2_be_verb --steps 100   # a fresh run with the same settings (needs lab/.env)
```
