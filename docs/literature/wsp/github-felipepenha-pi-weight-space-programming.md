# Pi Weight-Space Programming: a Pi coding-agent extension with reading tools and live reruns of Sparks Exps 1–3

- **Key:** github-felipepenha-pi-weight-space-programming
- **Authors / organisation:** Felipe Penha (GitHub felipepenha); independent
- **Date:** 2026-11 (latest commit read: 2026-11-09)
- **Link:** https://github.com/felipepenha/pi-weight-space-programming
- **Kind:** tool
- **Read from:** README (first ~100 lines and keyword search); `evals/README.md` in full; `prompts/wsp-read-weights.md`; run records for `exp1_breakout` (state, instructions) and `exp3_english` (state, start of final answer); listing of other run folders. Not read: the extension source (`extensions/`, `harness/`), skills folder, other run transcripts and tool-call logs, examples.
- **Relevance to us:** 3 (central)

## What they wanted, and why
The repo packages WSP as an extension for the Pi coding agent: six tools (inspect weights, circuit probe, compare checkpoints, edit weights, an offline anti-training Python sandbox, a budgeted forward pass), slash commands, and presets that reproduce the Sparks experiments 1–8 with their tool modes, budgets and effort levels. It also reruns the paper's reading experiments with Gemini models and keeps the audit logs.

## What they studied
Sparks Exp 1 (four grid-game MLP policies), Exp 2 (three shape-DDPM MLPs), Exp 3 (four middle transformer blocks of character-level models trained on Python, Romaji or English text, without embeddings or output head), plus parity checks for Exps 4 and 5. Readers: Gemini 3.8 Flash and Gemini 4 Argon via Pi. Unit: whole networks; attention heads (Exp 3).

## How they did it
1. Download the released checkpoints, prompts and answer keys from lm_understand-logs.
2. Exps 1 and 2: Pi run with built-in tools disabled, tool-free mode, the paper's prompt, one turn; answers scored against the keys.
3. Exp 3: "mech-interp" mode with the custom `wsp_circuit_probe` tool (static K-composition scores between heads; a singular-value "cliff" of the final MLP output after regressing out its input subspace) plus the Python sandbox; no forward passes.
4. Score with `run_paper_evals.py`; functional tests check that the edit DSL reproduces the released Exp 4/5 networks exactly.

## What counts as an explanation here
A named label (game, shape, corpus, order) plus the heads the reader calls copying heads, with the weight evidence it cites (channels, rows, composition scores, rank).

## How they judged success
Match to `answer_key.json` (Exps 1–2) and to `heads.json` copying heads with induction score ≥ 0.2 (Exp 3); corpus and order labels.

## What they found
- Exp 1, Gemini 3.8 Flash, tool-free: 4/4 (reported confidences 98–100%). Evidence cited: agent row/column confinement, active action columns, maze reconstructed from zero-weight cells (Pac-Man), upward action bias (Freeway).
- Exp 2: reported 3/3 with Gemini 4 Argon. It called circle and triangle filled (as the keys say) but described the square as rectangular outlines, still graded a pass by the keyword rule. Whether Flash was tried on Exp 2 is not stated.
- Exp 3, Gemini 3.8 Flash with the custom probe tool: corpus 3/3, order 3/3, copying heads exact on all three (3, 1 and 1 heads). The reader's argument rested on the tool's rank-cliff and composition numbers (e.g. a cliff at rank 24 read as Romaji's smaller alphabet).
- Exps 4/5: the edit DSL reapplies the released edits with zero difference.

## Limits and open problems they name
Few limits stated in what was read; the README presents 100% across evaluated benchmarks.

## What we take from it
- **Data point:** a mid-tier model (Gemini Flash) matched Astra on the Exp 1 reads with no tools, suggesting Exp 1 is not a frontier-only task.
- **Warning:** the Exp 3 probe tool was written by someone with access to the answer keys and computes exactly the signatures that separate the three corpora; tool design can leak the answer. A fair reading lab needs tools fixed before seeing ground truth, and arms with and without them.
- **Warning:** the model was switched between experiments and only the passing runs are shown; selection is unclear. Exp 3 probabilities are identical across all three runs (0.985 / 0.999), which looks templated.
- **Shortcut:** an offline sandbox with AST guards against `.backward()`/optimizers is a cheap rule-enforcement layer.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** Gemini 3.8 Flash: Exp 1 4/4; Exp 3 corpus 3/3, order 3/3, copying heads 3/3 runs exact. Gemini 4 Argon: Exp 2 3/3 (shape family; one filled/outline error).
- **Target networks:** Exp 1: 3-layer MLP policies on a 10×10×5 grid, 17,445 parameters given (README's count). Exp 2: DDPM MLP 160→64→64→144 on 12×12 single-shape images, 23,824 weights. Exp 3: four transformer blocks, d=384, 6 heads per layer, character-level models, trained on python/romaji/english with characters kept or shuffled.
- **How the weights were presented:** Exps 1–2: raw rounded parameters as text in the paper's prompt (rounding precision not stated in what was read). Exp 3: tensors via tools and sandbox (`Checkpoint`, `W` dict), no embeddings, positional embeddings or output head.
- **Prompt:** the paper's released prompts via `--wsp-exp N`; instructions file says only to answer the request. The repo's own reading template (`prompts/wsp-read-weights.md`) tells the agent to inspect shapes, norms and spectra, probe QK/OV and induction heads for transformers, never run the network, and give step-by-step evidence and confidence. Exp 3 offers three candidate corpora and two order options.
- **Access regime:** Exps 1–2: no tools, one turn, 0 passes. Exp 3: tools and Python (39 of 100 runs used in the English run, 43 turns), 0 forward passes.
- **Controls:** none (no shuffled, untrained or decoy networks).
- **Failure modes observed:** filled square described as outlines (graded pass); otherwise none reported.
- **Anything about which prompt or format choices helped or hurt:** custom static-circuit tools appear to carry the Exp 3 inference; not ablated.
