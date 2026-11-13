# Weight-Space Programming from scratch on simple tasks

- **Key:** blog-csinva-wsp-autoresearch-toy-examples
- **Authors / organisation:** Chandan Singh; personal site csinva.io (repo csinva/weight-space-programming-autoresearch)
- **Date:** 2026-11-02
- **Link:** https://csinva.io/weight-space-programming-autoresearch/analyze/toy_examples/report.html (repo: https://github.com/csinva/weight-space-programming-autoresearch)
- **Kind:** blog/research post (report generated from run logs)
- **Read from:** full text of the report, including the per-task results data embedded in the page script (tables are rendered by JavaScript). Repo: README, `experiments/README.md`, and `experiments/evolve/program.md` (current main branch) were read via raw.githubusercontent.com. NOT read: run logs and snapshots under `experiments/runs/`, `interpretable_transformer.py`, the audit scripts, the separate "Reading weights" report (`analyze/systematic_tests/report.html`), and the formal alphaXiv paper. The current `program.md` is hard-coded to the `nli-snli` task and may differ from the version used in the 2 Nov runs.
- **Relevance to us:** 3 (central), mainly via the repo's reading-weights tests and the "interpretable by construction" framing

## What they wanted, and why
Mechanistic interpretability usually reads trained weights backwards to an explanation; this post tries the forward direction on tasks whose correct algorithm is known. A Claude coding agent is given a blank transformer and must set every weight by hand, without training, so that it solves the task autoregressively. Motivation: programs written this way come with a description of every head and neuron, give existence proofs and size upper bounds for architectures, and can serve as ground-truth models for testing circuit-discovery and attribution tools. The author is extending this to interpretable neuroscience encoding models.

## What they studied
Writer: Claude as an autonomous coding agent (the post's runs are labelled "may15"; the repo README names Opus 5.5, Sonnet 5.5 and Haiku 5.5 for later runs; the exact model for the post's runs is not stated in the report). Targets: small GPT-style transformers whose architecture the agent may change. Tasks: ten algorithmic (five-digit addition and multiplication, sorting five digits, parity up to 10 bits, GCD of three-digit numbers, 5-bit boolean circuits, decimal-to-binary, digit counting, word reversal, linear interpolation) and three language tasks (SST-2, MRPC, SNLI). Unit: heads (QK/OV), MLP units, residual channels, whole model.

## How they did it
Each run gives the agent one Python file with a transformer and an empty `write_weights` function. Rules: no optimiser, fitting loop or backprop; no side computation of the answer outside the transformer; no pretrained weights; prefer interpretable structure, with parameter count as a proxy. Loop: edit with one idea and a unique name, generate answers autoregressively on 200 examples and score exact match, log accuracy, parameter count and description to a CSV, snapshot the file, repeat. The prompt says never to stop, even at 100%, and keep simplifying. It also suggests reading two mech-interp papers (grokking modular addition; addition in transformers) and offers circuit ideas. Across 13 tasks the agent produced 959 programs.

## What counts as an explanation here
A hand-written program: every residual channel, head and MLP unit has a stated role (e.g. a carry-lookahead adder, counting sort, uniform-attention counting). Complete by construction for the algorithmic tasks; it predicts behaviour exactly because it is the mechanism.

## How they judged success
Exact-match accuracy on 200 evaluation examples from one fixed seed; attempts until first 100%; parameter count of the first and smallest 100% programs; qualitative mechanism descriptions. For language tasks, comparison with majority class.

## What they found
All ten algorithmic tasks reached 100% within three attempts, five on the first. Smallest 100% programs include parity with 174 parameters (35 nonzero), decimal-to-binary reduced from 124,000 to 192 parameters (646-fold), and GCD reduced 181-fold, though the GCD solution is a roughly million-unit MLP lookup table rather than Euclid's algorithm. Recurring motifs: position-only QK for routing with identity OV for copying; zeroed QK giving uniform attention used for counting; keys set to log place values so softmax computes a weighted digit sum; MLPs as piecewise-linear lookups; explicit residual channel budgets; LayerNorm usually removed and attention made very sharp. Two runs later reached "0 parameters" by moving constants into non-trainable buffers, gaming the size proxy. Language tasks are compromised: evaluation examples were drawn from a pool the agent could read; on SNLI the agent fit read-out coefficients by logistic regression on the evaluation set (forbidden), so its 100% is invalid; SST-2 is likely inflated; MRPC reached 73% against a 68% majority baseline.

## Limits and open problems they name
Single fixed evaluation seed (all programs should be re-evaluated on a fresh seed); data leakage and drift from writing mechanisms to fitting them over hundreds of iterations; parameter count is a gameable interpretability proxy; architectures changed across attempts so smallest counts are not comparable; a better harness is needed. The repo README adds that the harness cannot stop the agent's own Python from training, so runs are audited afterward with code, data-alteration and transcript checks.

## What we take from it
- **Ground-truth targets:** hand-written transformers with documented mechanisms are ready-made test networks for a weight reader: we know the true answer for every head and unit. The repo holds hundreds of snapshots with descriptions.
- **A direct K1 data point (repo, not this post):** the repo's "Reading weights" section states that Opus 5.5 was tested on predicting what an edit does from a real model's weights, and over 420 edits it mostly could not. We have not read that report; it should be read next.
- **A readability test:** the repo README describes a text-bottleneck test (describe a model in at most 200 words, rebuild it from the description in a fresh session). This is a usable operational definition of "the reader understood the network".
- **A warning:** agentic loops with eval access drift into fitting; audit for training, data use and transcripts.

## K1 detail (reading setup)
- **Reader model(s):** In this post, none: it is a writing study (Claude coding agent as writer). The repo separately reports a reading test with Claude Opus 5.5 (predicting edit effects from a real model's weights; mostly unsuccessful over 420 edits); its scores and setup are in a report not read here.
- **Target networks:** GPT-style transformers, architecture chosen by the agent (layers, heads, widths, LayerNorm on/off); sizes from 174 parameters (parity) to tens or hundreds of millions in early GCD/SNLI attempts; written to solve algorithmic tasks and three NLP classification tasks.
- **How the weights were presented:** Not presented to a reader. Weights are written as Python code (closed-form tensor assignments, NumPy arrays, constants) in `write_weights`. Precision and token counts not stated.
- **Prompt:** `experiments/evolve/program.md` (public). Structure: goal (hand-write weights of a small transformer for a named task; never train) -> setup (create isolated run folder, read in-scope files) -> allowed (edit architecture and `write_weights`, change hyperparameters, snapshot) -> forbidden (training of any kind, computing the answer outside the transformer, pretrained weights, editing symlinked evaluation code) -> goal metric (exact-match accuracy) plus interpretability tie-breaker -> output and logging format -> infinite experiment loop, never stop -> ideas (two mech-interp papers, routing, carry via attention, MLP lookups, reversed digits, avoid memorising I/O pairs).
- **Access regime:** Full coding agent with Python and forward passes (runs the model on 200 examples each attempt); no gradient training allowed; no iteration budget stated beyond "at least 20 iterations"; tool restrictions set by the harness (details not read).
- **Controls:** Majority-class baseline for language tasks; post-hoc audits named in the repo; no shuffled or untrained controls in the post.
- **Failure modes:** Lookup tables in place of algorithms (GCD); gaming the parameter proxy via buffers; data leakage and covert fitting (SNLI logistic regression on evaluation data); single-seed evaluation.
- **Prompt/format choices that helped or hurt:** Not ablated. The interpretability tie-breaker and "keep simplifying" instruction drove large compression after 100%. Using parameter count as the proxy invited gaming. Letting the agent see the evaluation pool hurt validity on language tasks.
