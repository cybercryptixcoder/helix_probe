# What is weight-space programming?

- **Key:** blog-learnagentic-what-is-weight-space-programming
- **Authors / organisation:** Kanishk Patel; Learn Agentic AI (Substack)
- **Date:** 2026-11-10
- **Link:** https://learnagentic.substack.com/p/what-is-weight-space-programming
- **Kind:** blog/research post (explainer of a reproduction study)
- **Read from:** full text (via WebFetch paraphrase). The study it describes is arXiv 2611.09382 (WSP-Scope), so per
  instructions its primary was not read in this batch.
- **Relevance to us:** 2 (useful)

## What they wanted, and why
To explain weight-space programming to practitioners through the reproduction study "Exploring Weight-Space
Programming: Capabilities, Generalization, and Limitations" (Hu, Tang, Li, Zhu, Feng, Zhang, Chen, Hu; Shanghai AI
Laboratory, Tongji, Fudan; arXiv 2611.09382), whose headline is a 1,023-weight edit. The post wants readers to know
when the method is worth trying and how to evaluate it.

## What they studied
Qwen3.5-0.8B and Qwen3.5-9B as targets, GPT-6 Astra as editor, seven benchmarks (MATH-500, MMLU-Pro, IFEval, GPQA
Diamond, MedXpertQA, SciBench, SciCode). Unit: single MLP output columns, per-head attention output blocks, and some
query rows (9B).

## How they did it
As reported: Astra at maximum reasoning effort in a persistent Python environment, up to 300 analyses per search,
50 forward requests per search (generation requests returning task scores; teacher-forced requests returning
log-probs and activations). No gradients. Only transformer-block parameters editable; embeddings, final norm and
output head frozen. Maths in float32, stored as BF16. Agent sees only development data, finds a candidate on one
batch, confirms on fresh dev questions, then keeps the edit or the original; test sets touched once.

## What counts as an explanation here
A diagnosed failure plus a direction and a site: e.g. a "doubt minus progress" vector built from word embeddings,
subtracted through neuron 507 of the layer-23 MLP output matrix. The edit is meant to be inspectable and disputable,
unlike a fine-tune delta.

## How they judged success
Held-out benchmark accuracy; on a 48-question batch: base vs edit vs neuron ablation vs random orthogonal direction
of equal size vs dose sweep (0-2x) vs a counter-edit.

## What they found
Control batch: base 6/48, edit 20, full ablation 4, random direction 10, dose peak at exactly 1x. Across six
disjoint dev sets (1,152 questions) correct answers 126 to 484; MATH-500 test 8.35% to 37.80%. IFEval 21.40% to
58.12% via one direction in head 7 of layer 15 (258,128 values). SciBench +17.11, GPQA +4.42, SciCode unchanged at
0, MMLU-Pro and MedXpertQA edits discarded. 9B: small kept gains; four runs kept the original weights. Three maths
runs on 0.8B gave very different edits and gains (e.g. 1,037,572 values for +5.00; 1,981,083 for +27.30).

## Limits and open problems they name
Dev gains can vanish on test (9B maths +29.69 dev, -0.35 test); larger models fail diffusely; cost unreported; one
run per model-benchmark pair; no LoRA/fine-tune baseline; blog's 7.9-to-48.1 not reconciled with 8.35-to-37.80.

## What we take from it
The control set (ablation, random equal-norm direction, dose sweep, fresh-question confirmation) is a good template
for testing any edit we claim derives from reading weights. Run-to-run variance argues for multiple seeds per
condition.

## K1 detail (reading setup)
- **Reader model(s):** GPT-6 Astra (maximum reasoning effort) only. No per-reader read score; scores are edit
  outcomes (above).
- **Target networks:** Qwen3.5-0.8B and Qwen3.5-9B language models (pretrained/released), improved on reasoning and
  instruction benchmarks.
- **How the weights were presented:** as tensors in a Python environment, not as text. Float32 for computation, BF16
  storage. Tokens: not stated.
- **Prompt:** not stated in the post (task framing: improve a benchmark using dev data only). Prompt files: not
  given; trajectories expected at github.com/WSP-Scope/WSP-Scope-Project.
- **Access regime:** Python on weights (up to 300 analyses), 50 forward requests per search, generation and
  teacher-forced modes, no gradients.
- **Controls:** neuron ablation, random orthogonal direction of equal size, dose sweep, counter-edit, fresh dev
  confirmation, single-touch held-out test.
- **Failure modes:** dev-to-test collapse; no improvement where errors are diffuse; large variance across sessions.
- **What helped or hurt:** a single visible dominant failure (non-terminating reasoning) made the method work; a
  strong baseline (9B at 97.70% MATH-500) left nothing to fix. Nothing on raw-text weight formats.

## Tags
unit: weights | direction
form: direction | steering
method: agent | weight-analysis | ablation
eval: ablation | downstream-task | benchmark
goal: control/editing | evaluation-of-methods
