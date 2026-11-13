# OpenWSP: open tooling and an audited replication of the Sparks WSP experiments

- **Key:** github-openwsp-openwsp
- **Authors / organisation:** OpenWSP maintainers (independent; states no affiliation with the MIT CSAIL authors)
- **Date:** 2026-11 (latest commit read: 2026-11-04)
- **Link:** https://github.com/openwsp/openwsp
- **Kind:** tool
- **Read from:** README in full (status, Exp 8 setup/results/controls/FAQ/differences, raw-weight section, limits); `replications/raw_weights/README.md` in full; `replications/exp1/README.md`, `replications/exp2/README.md`; `replications/raw_weights/inventory.json` and `results/summary.json` (first items only). Not read: `docs/` (architecture, MCP, edit format, editor recovery), `src/`, the Exp 8 task message and transcripts, `DECISIONS.md`, `QUESTIONS.md`, per-item answer texts.
- **Relevance to us:** 3 (central)

## What they wanted, and why
OpenWSP set out to reproduce the Sparks of Weight-Space Programming report and to build the missing infrastructure around it, so that agentic weight editing becomes as reproducible and reviewable as code changes: inspect, edit, measure, and keep an exact diff. The first target is Experiment 8 (Qwen3.5-0.8B math-loop edit); a second track re-runs the released one-reply raw-weight experiments (1, 2, 4, 5), which include the two pure weight-reading tasks. The project emphasises provenance: every number in the README links to a result file, failed and lower-scoring attempts are kept.

## What they studied
Exp 1 (identify which MinAtar-style game a small MLP policy was trained on; 4 items), Exp 2 (identify the image family a small diffusion MLP generates; 3 items), Exp 4 (repair a Kinetix car policy, 171,664 weights), Exp 5 (write MinAtar policies, 600-32-32-6 tanh actor). Exp 8: the text part of Qwen3.5-0.8B at a pinned revision, edited by GPT-6 Astra (max effort) through Codex. A second editor, Claude Fable 5.1, is planned but blocked on credentials. Unit: whole small networks (reading), MLP down-projection weights (editing).

## How they did it
1. Pin the authors' release (lm_understand-logs at a fixed commit), hash every prompt and instruction file, and refuse to run if bytes differ.
2. Raw-weight items: each prompt sent verbatim to a fresh conversation, zero tools, one reply, no feedback, no best-of selection; same effort settings as the authors (high for 1/2/4, xhigh for 5).
3. Reconstruct scorers (the authors released none for these folders) and calibrate them by reproducing the authors' published labels and networks before scoring new replies.
4. Exp 8: a persistent sandboxed Python kernel over float32 weights (no GPU, no network), 50 forward passes and 300 Python runs, teacher-forced passes returning log-probs/hidden states/MLP activations/attention, practice sets only; edits to final norm, embeddings, output layer and whole-tensor rescaling refused.
5. Pre-declared controls for Exp 8: thinking off; a mechanical difference-of-means direction removed in the same form as the published edit; a decoding fix (repetition penalty); a random-direction version of the published edit (queued).
6. Expose the same operations (read, run, forward, save, diff, inspect, apply, export) as CLI, Python SDK and MCP server; edits are SHA-256-addressed diffs.

## What counts as an explanation here
For reading tasks: a free-text label (game name, shape family) graded by keyword. For editing: a weight diff plus the editor's stated update rule, checked algebraically (e.g. recovering the coefficient from the exported delta). No mechanistic claim is accepted from algebra alone.

## How they judged success
Raw reads: exact label match in the requested answer section (Freeway accepts Frogger; shape families circle/square/triangle with synonyms). Car: successes over 1,024 episodes. MinAtar: mean ± SE over 1,000 episodes with a predeclared seed. Exp 8: MATH-500/GSM8K/IFEval accuracy, also "finished accuracy" reported with cap-hit rate, binomial SEs, calibration within tolerance of the authors' numbers, per-edit KL on neutral text.

## What they found
- Reading replication (Astra via subscription, one reply, no tools): Exp 1 game identification 4/4; Exp 2 shape families 3/3, matching the authors. The authors note that a correct shape family does not mean the filled-versus-hollow description was right.
- Car repair one-shot failed (0/1,024 vs the authors' 1,024/1,024). MinAtar written policies: Breakout 458.73, Asterix 39.71, Seaquest 2.41 (authors' Astra 517.41, 53.18, 53.11).
- Exp 8 live edit (50 passes, one layer-23 down-proj tensor changed) scored 12.9% on MATH-500 with 84.25% of samples hitting the token cap, below the authors' 48.1% and the local 50.6% calibration of the released edit.
- Controls: base with thinking off 46.8%; mechanical difference-of-means edit 46.0%; repetition penalty 23.8%. The released edit's coefficient of 6 reverses and amplifies the removed component rather than projecting it out.
- The authors' Exp 8 prompt explicitly names repetition as an in-scope failure (prompt points at the fix's kind but not the direction).

## Limits and open problems they name
Scorers are reconstructions; original seeds unreleased; Fable comparison not run; Exps 3, 6, 7 not replicated; transport and token-count differences (their prompts tokenised ~3,480 tokens fewer than the authors' counts despite identical bytes); a single live Exp 8 attempt; the mechanical control reuses benchmark answers, so it is diagnostic, not held-out discovery.

## What we take from it
- **Shortcut:** a hash-pinned, one-reply, no-tool runner for the released reading prompts (Exp 1/2) with calibrated scorers; reusable as our K1 baseline harness.
- **Measure:** report the token cost of each reading prompt (Exp 1 prompts ~70k input tokens each) and keep reading separate from repairing.
- **Warning:** keyword scorers can pass a read that gets an important property wrong (filled vs hollow); our K1 rubric should grade more than the family label.
- **Framing:** a strong cheap control (thinking off, mechanical direction) can match a long agentic edit; any edit claim needs them.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** GPT-6 Astra (ChatGPT subscription via Codex, high effort, detailed reasoning summary, low verbosity): Exp 1 4/4, Exp 2 3/3. Claude Fable 5.1: not run (pending credentials).
- **Target networks:** Exp 1: small MLP policies trained on four grid games (Breakout, Freeway, Pac-Man, Pong); exact sizes not stated in what was read. Exp 2: small diffusion MLPs trained on one shape class each; sizes not stated in what was read.
- **How the weights were presented:** as text inside the authors' released prompt files, unchanged (about 115 KB per Exp 1 prompt; authors' counted ~73.7k input tokens, OpenWSP's receipts ~70.2k). Number format, rounding and layout: not stated in what was read (they are the authors' verbatim prompts).
- **Prompt:** the authors' released `prompt.txt` plus a neutral one-line instruction file, byte-for-byte; answer requested in a `Game` or `Images` section. Paths: `exp1_which_game/runs/<game>/prompt.txt` and `instructions.md` in RikiyaT/lm_understand-logs at commit 4d09ba6d…; whether candidate answers are listed: not stated in what was read.
- **Access regime:** no tools, one reply, no feedback, no retries that create new inferences; fresh conversation per item.
- **Controls:** none for reading (no shuffled or untrained-weight reads). Scorer calibration against the authors' released answers.
- **Failure modes observed:** none on reading; noted that shape-family credit can mask a wrong filled/hollow description.
- **Anything about which prompt or format choices helped or hurt:** not tested. Records that identical prompt bytes produced different input-token counts across clients, so token cost is client-dependent.
