# dspy-wsp: weight-space programming as a DSPy optimizer

- **Key:** github-cmpnd-ai-dspy-wsp
- **Authors / organisation:** cmpnd-ai (DSPy ecosystem); GEPA search contributed by Michael Isaac
- **Date:** 2026-11-08 (v0.1.0 on PyPI); v0.1.2 2026-11-10
- **Link:** https://pypi.org/project/dspy-wsp/ ; source https://github.com/cmpnd-ai/dspy-wsp
- **Kind:** tool
- **Read from:** README in full (identical to the PyPI description); PyPI metadata; file listing. Not read: the results folder README (`results/2026-11-07-typed-decisions-astra/`), `prompts.py` (the writer's task prompt), the proof-of-concept MATH-500 run folder, source code.
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The package turns the Sparks Exp 8 harness into a DSPy optimizer: a frontier "writer" LM reads a student model's weights in a sandboxed Python kernel, runs the user's DSPy program on practice examples through a budgeted forward-pass tool, and saves targeted edits, with no gradients. The goal is to make WSP usable on any DSPy program and metric, especially small "decision models" that output option probabilities rather than text.

## What they studied
Three decision models on the Typed Decisions benchmark: d1-omni-600M (encoder with a decision head), NanoJev (Qwen3 backbone with a decision head), d1-2B (LFM3-based LM answering at answer positions). Also a reduced Exp 8 path for Qwen3.5-0.8B (vLLM, HF, MLX backends). Unit: tensors chosen by the writer (in practice the decision head or d1-2B's last block).

## How they did it
1. User supplies a DSPy module, metric, trainset (practice) and valset (hidden); a holdout fraction of practice becomes a validation set whose examples the writer never sees.
2. Each turn the writer explains its step and sends one block: `python` (persistent kernel with `load`, `save_edit`, etc., gradients disabled, no network under bubblewrap/sandbox-exec) or `forward` (JSON request: `generate` up to 512 items with original/edited/both weights and paired gain, or `teacher_forced` up to 1,024 texts returning log-probs, hidden states, MLP activations or attention).
3. Guardrails copied from the paper: no edits to embeddings, output layer, final norm; no whole-tensor rescaling; 300 Python runs; handoff every 40 turns with notes.
4. Decision models add `decide` and `read` passes (option logits and head inputs). By default the writer may recompute the head from reads and fit edits in closed form; `simulate_head=False` enforces the paper's rule.
5. Optional GEPA population search: short writer sessions propose child edits from Pareto-frontier parents, scored on minibatches then validation.
6. Final check compares original and edited weights once on the hidden valset with paired seeds; patches store changed entries with hashes.

## What counts as an explanation here
A patch plus the writer's `final_answer.md` account of the edit and its evidence; judged by held-out metric.

## How they judged success
Paired gain on 400 held-out Typed Decisions test cases over the unoptimized program (SEs 1.1–1.3 points); comparison with ReAnchor (threshold fitting, no weight change) and with a second writer.

## What they found
- GPT-6 Astra (max effort, 25 passes) raised test accuracy of the three decision models by 13 to 16 points; with ReAnchor stacked, 17 to 18.
- GPT-6.1 Sol as writer: +5.8, +12.1 and −0.6 points.
- Under the paper's rule (no recomputing the head in the kernel), Astra's d1-omni-600M edit gained only 2.8 ± 0.7 points and added nothing over ReAnchor. Most of the default gain came from closed-form fitting in the kernel.
- A 25-pass run took 78–167 minutes and $5.42–$7.63 in writer calls; 33–43 Python runs used.
- The paper's full Exp 8 result has not been repeated here.

## Limits and open problems they name
Early release; MATH-500 path less tested and slow; editing removes obstacles rather than adding abilities (cites Gemma 3 270M); patches lack the paper's low-rank form; leaderboard numbers differ because of request format and measure.

## What we take from it
- **Warning (central for any "LLM reads weights" claim with tools):** when the reader can simulate part of the network in its kernel, gains largely come from fitting, not understanding. Our K1 tool regime must state whether the reader can compute forward passes in code, and report both arms.
- **Shortcut:** a clean `python`/`forward` block protocol, paired base-vs-edited passes, and hashed sparse patches.
- **Measure:** compare against a no-weight-change baseline (ReAnchor) that fits only the readout.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** used as editors: GPT-6 Astra (max) +13 to +16 points on three models (+2.8 ± 0.7 on d1-omni-600M under the no-simulation rule); GPT-6.1 Sol +5.8, +12.1, −0.6. No standalone reading score.
- **Target networks:** d1-omni-600M, NanoJev, d1-2B decision models trained to answer typed questions (Choice, yes/no, Score); Qwen3.5-0.8B for the Exp 8 path. Parameter counts as in model names.
- **How the weights were presented:** tensors in a Python kernel (`NAMES`, `SHAPES`, `load(name)`); writer prints what it wants; output capped at 10,000 characters per run. Not as raw text.
- **Prompt:** adapted from the authors' Exp 8 prompt (CC BY 4.0), built around the DSPy program and metric; saved per run as `task_prompt.txt`; file `src/dspy_wsp/prompts.py`. Exact text not in what was read.
- **Access regime:** Python on weights; budgeted forward passes (25 in the reported runs; 3 suggested for a first test); 300 Python runs, 15 minutes each.
- **Controls:** hidden valset with paired seeds; ReAnchor baseline; writer comparison; `simulate_head` on/off; optional `fallback_if_worse`. No random-edit or shuffled-weight control stated.
- **Failure modes observed:** gains collapse when in-kernel head simulation is forbidden; weaker writer can make a model worse.
- **Anything about which prompt or format choices helped or hurt:** allowing closed-form recomputation of the head helped a lot; writer choice mattered (Astra over Sol on two of three models).
