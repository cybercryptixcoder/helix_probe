# Exploring Weight-Space Programming: Capabilities, Generalization, and Limitations

- **Key:** arxiv-2611.09382
- **Authors / organisation:** Junru Hu, Cheng Tang, Wei Li, Hongze Zhu, Chun-Mei Feng, Qi Zhang, Yirong Chen, Ming Hu; Shanghai AI Laboratory, Tongji University, Fudan University (per-author mapping not recoverable from the HTML)
- **Date:** 2026-11-06
- **Link:** https://arxiv.org/abs/2611.09382 (read via https://arxiv.org/html/2611.09382)
- **Kind:** paper
- **Read from:** full text (arXiv HTML v1, including appendices 5–10: protocol, splits, all checkpoint edits, the MATH primary search trajectory, and the editor prompt). Figures 1–7 seen only as captions. Project homepage and GitHub repo were not read.
- **Relevance to us:** 2 (useful) — an editing study, not a reading study; but it documents an agentic weight-analysis setup in detail.

## What they wanted, and why
The paper asks whether the WSP result of Takehi et al. (an LLM agent editing a small model's weights to raise MATH-500) is a general adaptation method or mainly a way to repair one identifiable failure (reasoning loops). They study three axes: capabilities (how much, and does edit size/structure matter), generalisation (do task-specific edits transfer to other tasks), and limitations (how reliably an agent finds, validates and selects edits, and how this varies across runs and model scales).

## What they studied
Editor: GPT-6 Astra at maximum reasoning effort. Targets: Qwen3.5-0.8B and Qwen3.5-9B. Seven benchmark families: MATH-500, MMLU-Pro, IFEval, GPQA Diamond, MedXpertQA, SciBench, SciCode. Unit: individual MLP down-projection columns, attention-head output blocks, a gated-query block, and rank-one directions in single weight matrices. 16 editing trajectories (one per model–benchmark pair, plus two extra reruns for 0.8B MATH).

## How they did it
1. Each search starts from the original checkpoint; the editor gets a persistent CPU Python kernel with the model's weights (read-only originals plus helper functions to load, save and drop edits) and practice/development data.
2. It has a budget of 50 successful forward requests to a separate GPU worker: generation requests (sampled answers, graded, optional averaged activations) and teacher-forced requests (token log-probs, top-k, hidden states, MLP activations, attention for short texts). Up to 300 Python analyses; the kernel may not simulate the model.
3. Edits are gradient-free: computed in float32 and stored in BF16; embeddings, final norm, LM head and architecture are out of scope; whole-tensor scaling and global sharpening/flattening of outputs are refused.
4. The editor diagnoses failures, localises components causally (with dose sweeps and controls), confirms on fresh development questions, and chooses a final checkpoint — or keeps the original.
5. Selected checkpoints are evaluated against the original on held-out test sets never shown to the editor, with paired, question-clustered standard errors.
6. Appendix 7 specifies every retained edit exactly (tensor, indices, formula, number of changed BF16 values); Appendix 9 lists all 50 requests of the primary MATH search.

## What counts as an explanation here
An edit plus the editor's stated mechanism (e.g. a "doubt vs progress" token direction written by one MLP unit). The explanation is a working hypothesis supported by causal controls on development data; it is not a full model of the network and is judged only through downstream accuracy.

## How they judged success
Held-out accuracy (benchmark-specific scoring: IFEval prompt-level strict on a fixed 270/271 split; SciBench boxed number within 5% relative tolerance; SciCode full-chain pass), paired original vs edited on the same items with seed 0, with question-clustered SE and 95% normal intervals. Development gains reported but adaptively selected and uncorrected for multiple comparisons. Within-search controls in the primary MATH run: native-unit ablation, reversed direction, one equal-norm random orthogonal direction, dose sweep.

## What they found
- 0.8B held-out gains: MATH-500 +29.45 pp (8.35→37.80) from changing 1,023 BF16 values in one column of the layer-23 MLP down-projection; GPQA Diamond +4.42; IFEval +36.72; SciBench +17.11; SciCode 0; MedXpertQA and MMLU-Pro candidates discarded.
- 9B gains were small (IFEval +1.85, SciBench +3.03, SciCode +1.54); a 9B MATH candidate with +29.69 dev gain lost 0.35 on held-out (base already 97.70%).
- Six of 16 trajectories kept the original weights.
- Three independent 0.8B MATH searches all hit the layer-23 down-projection but differed in structure: +29.45 (1,023 values), +5.00 (rank-one, ~1.04M values), +27.30 (rank-one, ~1.98M values). Edit size did not predict effect.
- Cross-task transfer was uneven: the 0.8B MATH-edited checkpoint raised GPQA Diamond, IFEval and SciBench (abstract: +3.03, +12.18, +20.10) but not SciCode; some transfers regressed.
- Primary MATH controls (8k cap, 48 items): base 6/48, chosen edit 20/48, ablation 4/48, reversed 0/48, equal-norm random 10/48; dose sweep peaked at strength 1; six reserved dev sets rose from 10.94% to 42.01%; AIME 0/64 in both arms.

## Limits and open problems they name
High variance across searches (path dependence); the 50-request budget often too small to validate a candidate; development gains often fail to hold; evaluation is costly; mechanisms of successful edits and transfer remain unclear (joint multi-site edits, role of dev data size and diversity); stronger models leave less headroom; long-horizon and agentic tasks untested.

## What we take from it
- **A protocol template (method):** the editor prompt is a well-specified agentic "read weights + limited forward passes" contract (budgets, request types, forbidden simulation in the kernel, paired evaluation with SE guidance). It is a ready model for our tool-allowed K1 condition.
- **A warning:** reading in WSP practice is heavily mediated by activations and paired generations, not weights alone; the "explanations" are hypotheses validated by behaviour. Claims of weight reading from such setups do not isolate weights-only reading.
- **A measure:** paired, question-clustered SE on identical items, plus native-ablation / reversed / random-direction controls and dose sweeps, is a solid evaluation standard for interventions predicted by a white-box model.
- **A data point:** even with a fixed target and budget, independent searches find structurally different edits — variance across runs must be reported.

## K1 detail (reading setup)
- **Reader model(s):** GPT-6 Astra at maximum reasoning effort, acting as editor. No separate reading score; outcomes are held-out accuracy deltas (see "What they found"). No other reader models.
- **Target networks:** Qwen3.5-0.8B and Qwen3.5-9B (pretrained instruction/thinking LMs; thinking mode on). Shapes stated: 0.8B down-projection 1024x3584, attention output 1024x2048, heads 256 wide; 9B down-projection 4096x12288, attention output 4096x4096, layer-19 gated query 8192x4096. Exact parameter counts beyond the names not stated.
- **How the weights were presented:** as tensors, not text: loaded in a Python kernel as float32 torch tensors by name (from safetensors files in a read-only /model folder), via helper functions; editor sees what it prints. Precision: checkpoint BF16, edits computed in float32. Layout: named per tensor. Token count not applicable / not stated.
- **Prompt:** Initial editor prompt reproduced as a template in Appendix 10. Structure: TASK (you are given an LM's weights; improve capabilities by editing weights directly, diagnose and repair failures); HOW IT WILL BE MEASURED (held-out benchmark, samples per item, metric, prompt protocol, fixed sampling settings, no previous edits or recipes); WHAT COUNTS (edits grounded in identified components — neurons, heads, directions, circuits — with evidence; example failure categories given but none preferred; out-of-scope tensors and whole-tensor scaling; no global sharpening or forced early stopping of thinking); WHAT YOU HAVE (Python kernel with listed libraries and helpers, 900 s per execution, memory cap, 10k-char output cut, 300 executions; dev data contract; forward-pass tool with JSON request formats for generation and teacher forcing and what they return); HOW TO WORK (diagnose first, localise causally with dose-response, measure with paired comparisons and SE, plan passes, work efficiently, keep notes, don't print raw vocab); RULES (no gradients/training, no simulating the network in the kernel, no internet); HOW THE SESSION RUNS (continues until 50 passes used, then final choice and justification). Architecture is given via a placeholder; candidate answers not applicable. Prompt published in the paper; homepage https://wsp-scope.github.io/ and repo https://github.com/WSP-Scope/WSP-Scope-Project (not read).
- **Access regime:** Python on the weights (up to 300 analyses; no GPU; may not simulate model computation); 50 successful forward requests (generation up to 512 generations per request, or teacher-forced up to 1,024 texts / 524,288 tokens, with optional activations, hidden states, MLP activations, attention); no gradients or optimisers; no internet. Objectives for some searches were broadened mid-run (e.g. after 46, 27, 26 requests).
- **Controls:** within-search (primary MATH): native unit-507 ablation, reversed direction, one equal-norm random orthogonal direction, dose sweep, confirmation on six disjoint reserved dev sets, AIME challenge subset. Across runs: two reruns of MATH. Evaluation: paired original vs edited on identical items with fixed seeds. No shuffled-weights, untrained-model or prompt-only controls stated.
- **Failure modes:** dev gains that vanish or reverse under broader validation (9B GPQA, 9B MMLU-Pro, 0.8B MedXpertQA; 9B MATH −0.35 held-out); budget exhaustion before a reliable edit is found (six trajectories kept original weights); a harmful first edit (layer-23 column 40); truncation cuts not translating into accuracy; zero effect on SciCode at 0.8B; path-dependent, structurally different solutions across reruns.
- **Prompt/format choices that helped or hurt:** Not ablated. The prompt itself encodes lessons (diagnose before editing, don't treat truncation as repetition, paired comparisons with SE, dose sweeps, avoid printing raw vocabulary to dodge content filters). Some searches started with a loop-focused objective that was later broadened; the paper does not isolate the effect of objective wording.
