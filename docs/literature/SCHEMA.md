# Literature survey: what each paper entry must contain

*Shared by every reader (the core survey, Aether, Helix Research), so all entries can be merged. Nov 12, 2026.*

## Why this survey exists

We want to build a **white-box model of a black-box network**: something that does not just record what probing
found, but predicts what the network will do. Before designing anything, we learn from the field:
- what interpretability researchers are ultimately trying to build, and why;
- what they count as an explanation, and what form it takes;
- how they set up experiments, what they measure, what baselines and controls they use, which benchmarks;
- what blocks them, and what they have already solved that we can reuse.

We are not cataloguing metadata. Each entry should let someone who has not read the paper understand **what the
authors wanted, what they did, how they judged it, and what we can take from it**. Methodology matters as much as
findings: our paper must use methods and measures this field recognises.

## Files and keys

- One file per paper: `<folder>/<key>.md`, where `<folder>` is `core`, `aether` or `helix_research`.
- `<key>`: `arxiv-<id>` (e.g. `arxiv-2501.16496`), else `doi-<doi with / replaced by _>`, else a short slug of the
  URL host and path (e.g. `tcpub-2025-attribution-graphs-methods`). Lowercase, no spaces.
- Each folder has an `INDEX.md`: one line per entry, `key | title | org | date | relevance`.
- Before reading a paper, check that `<key>.md` does not already exist in your own folder.

## Entry template

```markdown
# <Title>

- **Key:** <key>
- **Authors / organisation:** <names; organisation>
- **Date:** <YYYY-MM-DD or YYYY-MM>
- **Link:** <URL>
- **Kind:** paper | blog/research post | essay | survey/agenda | benchmark | tool
- **Read from:** full text | abstract and sections | abstract only
- **Relevance to us:** 3 (central) | 2 (useful) | 1 (background)

## What they wanted, and why
The question and the motivation in plain words. What larger goal is this a step toward? (3–6 sentences.)

## What they studied
Models (names, sizes), data, and the unit of analysis (neurons, features, directions, heads, circuits, layers,
weights/parameters, whole model).

## How they did it
The experimental setup, step by step, in your own words: what was trained or measured, what was intervened on,
what was compared with what. Enough that someone could sketch the experiment. (5–12 sentences.)

## What counts as an explanation here
The form the understanding takes: text descriptions, a feature dictionary, directions, a circuit or attribution
graph, a replacement or surrogate model, a causal abstraction, a program, a probe, a steering vector, something
else. Is it meant to be complete or partial? Can it predict anything?

## How they judged success
Metrics, baselines, controls, ablations, datasets and benchmarks, statistics. Name them precisely (e.g. "KL
recovered under mean ablation", "faithfulness/completeness of a circuit", "simulation score", "human rating").

## What they found
Main results, paraphrased, with the key numbers.

## Limits and open problems they name
What failed, what they could not do, what they say is still open.

## What we take from it
Concretely, for our goal (a predictive white-box model; reading weights; prediction under intervention): a
method, a measure, a framing, a dataset, a warning, a shortcut. Say which.

## Tags
unit: neuron | feature | direction | head | circuit | layer | weights | whole-model
form: description | dictionary | direction | graph | replacement-model | causal-abstraction | program | probe | steering
method: SAE | transcoder | attribution | patching | ablation | probing | steering | agent | weight-analysis | decomposition | training-interpretable | other
eval: ablation | patching | prediction/simulation | faithfulness | completeness | human-rating | downstream-task | benchmark
goal: understanding | safety/auditing | control/editing | debugging | science | evaluation-of-methods
```

## Rules

- **Paraphrase.** Never copy more than one short phrase (under 15 words) from a paper, and at most one per entry.
- **Say what you did not read.** If only the abstract was available, set "Read from" accordingly and keep the
  entry short. Never invent details.
- **No numbers from memory.** Every number comes from the paper.
