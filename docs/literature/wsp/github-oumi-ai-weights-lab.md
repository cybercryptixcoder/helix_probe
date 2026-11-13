# Oumi Weights Lab: agent skill and worker for experimenting on open LLM weights, with a planted-mechanism proving ground

- **Key:** github-oumi-ai-weights-lab
- **Authors / organisation:** Oumi (oumi.ai)
- **Date:** 2026-11 (version 0.5; latest commit read: 2026-11-07)
- **Link:** https://github.com/oumi-ai/weights-lab
- **Kind:** tool
- **Read from:** README in full; `skills/oumi-weights-lab/SKILL.md` (first ~6 KB of ~17 KB); `docs/proving-ground.md` (by keyword search plus the score and weight-forensics sections); method map in `references/method-map.md` (keyword search). Not read: `docs/api.md`, the other 27 skill reference files, `src/`, tests, examples.
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The lab gives a coding agent (Claude Code, Codex, Cursor and others) a persistent Python worker over a loaded open LLM, with tested calls for ablation scans, attribution, circuit finding, SAEs, reversible weight edits with exact undo, evaluation and export. It is inspired by WSP but is broader mechanistic interpretability tooling. A separate "proving ground" measures whether the skill actually helps an agent find which parts of a model carry a behaviour, by grading the agent's written claim against a hidden key.

## What they studied
Any Hugging Face causal LM (tested on GPT-2, SmolLM2-135M, Qwen3-0.6B, Qwen3.5-0.8B, up to a 72B model across eight H100s). Proving ground: six tiny GPT-2-shaped models (6 layers, 4 heads, width 64) built from zero weights with one hand-planted mechanism each, and two families that plant four heads inside GPT-2 small; plus IOI and induction calibration tasks. Unit: heads, MLP layers, neurons, directions.

## How they did it
1. Agent loads a model once (`start`), sends Python snippets that share a `lab` object; every snippet's source, output and forward-pass count are saved.
2. The skill tells the agent to keep a belief file (established findings, rival hypotheses, untested assumptions) and to pick the experiment that best separates hypotheses for its cost; reading weights (parts, head weights, comparisons) is described as free of forward passes, while only interventions with a control show causation.
3. Proving ground: an agent receives a model, a question and 200 rows, and writes a claim naming heads/MLPs/neurons/directions plus an ablation result. The scorer compares the claim with the key and reruns the ablation on its own rows. Skill and no-skill arms are run several times per task and compared with paired bootstrap and sign-flip tests.
4. Each planted model includes a decoy part that looks like the mechanism but is unused.
5. Weight-forensics hardening: the first GPT-2 plant left statistical fingerprints (e.g. QK top singular value 7–40 times the layer's largest; many tiny OV singular values); a 20-line weights-only script read the key, the decoy and the family off the weights. The builders then constrained fifteen per-head statistics to lie within the layer's natural range and attack every build with a weights-only ranking.
6. Agents run in containers with a proxy that blocks Hugging Face and package hosts, so they cannot diff against stock GPT-2.

## What counts as an explanation here
A written claim of the components carrying a behaviour, with an ablation that the scorer can reproduce; faithfulness means zeroing the claimed parts brings accuracy near chance.

## How they judged success
Score = identification F1 (claimed heads/MLPs vs key; direction F1 for feature tasks) × 1 or 0.5 (ablation reproduced within tolerance) × 1 or 0.5 (faithful). "Solved" requires F1 of 1 and a reproduced, faithful claim. Planted models must pass validity checks (baseline ≥ 0.95 or 0.9, key ablation near chance, decoy ablation no effect).

## What they found
- Tiny planted models were too easy: keeping a few candidate heads and narrowing down solves them.
- In early GPT-2 plants, weights alone gave the answer away; after hardening, the weights-only ranking on one dev seed per family placed key heads at ranks such as 5th, 40th and 75th of 144 and flagged none.
- A weights-only "copying score" (project each head's OV product onto the task's flag-word unembeddings) did put the three key heads first on one dev task; the authors count this as legitimately finding the mechanism, not spotting an edit.
- Replaying the released Qwen3.5-0.8B WSP edit gave 51.25% vs 7.85% on MATH-500 (H200, 4 samples), cap hits 92.90% → 30.55%.
- No skill-vs-no-skill results are published in what was read.

## Limits and open problems they name
Dev tasks are public and only smoke tests; only held-out tasks (secret seeds) measure the skill. One dev seed per family for the weight-forensics check says little about how often a ranking finds the key. Snippets run as trusted Python.

## What we take from it
- **Method:** planted-mechanism tasks with decoys and secret seeds are a clean ground truth for weight reading; we can reuse the design for K1-style "where is the mechanism" reads.
- **Warning:** hand-planted circuits leave spectral fingerprints (outlier singular values, low effective rank, bias norms) that a reader can exploit without understanding; any planted benchmark needs a weights-only attack baseline and a network block against stock-model diffs.
- **Measure:** score claims by component F1 × reproducible ablation × faithfulness.
- **Framing:** "reading costs no forward passes; only intervention with a control shows cause" is a useful cost model for an interactive reading lab.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** proving-ground agents are configurable (example command uses Claude Code with Sonnet); no scores published in what was read. A scripted 20-line weights-only solver read the key heads, decoy and family off the first-version GPT-2 plants (exact rate not stated).
- **Target networks:** tiny GPT-2 (6 layers, 4 heads, d=64, MLP 256) with planted mechanisms; GPT-2 small (124M) with four planted heads in layers 4–11; trained to answer a flag word in a 14-word list, copy tasks, IOI, induction.
- **How the weights were presented:** as tensors via Python (`parts`, `measure`, `compare`, `head_weights`), not as text; precision is the model dtype; agent chooses what to print. Tokens not stated.
- **Prompt:** same for both arms: the task's question, the claim format and the time budget; family never named. Prompt text not in what was read.
- **Access regime:** Python on weights plus forward passes (counted, not hard-capped in what was read); network blocked; time budget per run.
- **Controls:** decoy components; validity checks on each plant; skill vs no-skill arms; weights-only attack baselines; stock-model diff blocked.
- **Failure modes observed:** reading planted edits by their statistical fingerprints instead of the mechanism; tiny models solvable by exhaustive narrowing; a misplaced prompt placeholder made every run score 0.
- **Anything about which prompt or format choices helped or hurt:** keeping planted head statistics within the layer's range removed the giveaway; no reader-prompt ablation reported.
