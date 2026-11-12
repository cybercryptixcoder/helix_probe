# The Circuits Research Landscape: Results and Perspectives

- **Key:** neuronpedia-2025-circuits-research-landscape
- **Authors / organisation:** Jack Lindsey, Emmanuel Ameisen, Neel Nanda, Stepan Shabalin, Mateusz Piotrowski, Tom McGrath, Michael Hanna, Owen Lewis, Curt Tigges, Jack Merullo, Connor Watts, Gonçalo Paulo, Joshua Batson, Liv Gorton, Elana Simon, Max Loeffler, Callum McDougall, Johnny Lin; Anthropic, Decode, EleutherAI, Goodfire AI, Google DeepMind (hosted by Neuronpedia)
- **Date:** 2025-08
- **Link:** https://www.neuronpedia.org/graph/info (the scout's Goodfire URL redirects here)
- **Kind:** survey/agenda (multi-lab research report)
- **Read from:** full text (single-pass summary of the whole page; fine details of every case study not re-checked)
- **Relevance to us:** 3 (central)

## What they wanted, and why
After Anthropic's attribution-graph ("circuit tracing") papers, several labs replicated and extended the method on
open models. This joint report pools their results to assess what the circuits paradigm can and cannot do, share
engineering lessons for training transcoders, and set an agenda. The larger goal is scalable, faithful
mechanistic explanations of specific model behaviours.

## What they studied
Gemma-2 2B, Llama-3.2 1B (and Llama-3.1 1B in tooling), Qwen3-4B, GPT-2 (Goodfire experiments), and the original
Claude 3.5 Haiku studies. Units: transcoder features (per-layer transcoders, PLTs, and cross-layer transcoders,
CLTs) and the per-prompt attribution graphs connecting them.

## How they did it
Train a sparse replacement model: transcoders that reconstruct MLP outputs from sparse features (PLTs per layer,
CLTs writing to all later layers). For a single prompt, build an attribution graph of linear feature-to-feature
effects, with "error nodes" holding what the transcoders fail to reconstruct, then prune it to the most influential
paths. Validate hypotheses from the graph with interventions on the real model (steering, activation patching,
ablation) and with supervised tools such as probes. Case studies: two-hop reasoning in Gemma-2 2B; clause-boundary
features in Llama-3.2 1B; letter and rhyme features; the greater-than circuit in GPT-2. Architecture study (GPT-2):
transcoder variants trained for 100M tokens at roughly matched parameter counts and compared on replacement score
over 260 curated prompts; plus systems work on memory, sparse kernels and distributed training.

## What counts as an explanation here
An attribution graph: a pruned, per-prompt execution trace through an interpretable replacement model, grouped into
supernodes and checked by intervention. Explicitly partial and local — it explains one prompt, not a general
algorithm, and it shows why an output happened rather than why an alternative did not.

## How they judged success
Replacement score (share of the computation captured by the replacement model) as the main architecture metric;
also KL divergence and unexplained variance of reconstructions. Graph claims validated by intervention outcomes on
the original model. They propose downstream benchmarks: auditing games with hidden knowledge, time from observing a
behaviour to a validated hypothesis, and fake-fact fine-tuning.

## What they found
- CLTs generally beat PLTs at the sparsities of interest; JumpReLU worked best for CLTs, TopK is an easier
  alternative. Recommendation: train with roughly 5–10× higher L0 than the target post-pruning sparsity and let
  pruning do the rest.
- Skip-PLTs lowered reconstruction error but did not raise replacement score except at very high sparsity;
  weight-tied incremental CLTs did not beat standard CLTs.
- KL fine-tuning of a skip-PLT cut KL from 0.33 to 0.20 with unexplained variance about flat (0.226→0.23) but
  replacement score fell (0.723→0.705) — lower reconstruction loss did not mean a better replacement.
- Gemma-2 2B two-hop reasoning shows both a genuine intermediate hop and shortcut paths; non-English prompts use a
  language-agnostic mechanism with language-specific features added late.
- GPT-2 greater-than: narrow input features, a general "larger number" heuristic, and a parity detector.
- Transcoders can shatter geometric structure: a helical number representation was not recovered, lookup-table
  features appeared instead.
- Costs: storing 1B tokens of Llama-1B activations needs over 130TB; bfloat16 decoders/activations gave about 2×
  speedup; best distributed setup reached 65.3% FLOPs utilisation.
- Over 7,000 graphs generated on Neuronpedia; open tools: circuit-tracer, EleutherAI's attribute and clt-training.

## Limits and open problems they name
Error nodes are often too prevalent and hide circuits; graphs are per-prompt and need aggregation for global
structure; suppressive edges and counterfactual "why not" questions are not captured; attention-computation
(QK) extensions not reproduced on open models; small-model findings less striking than Haiku's. Open: scaling to
long context, automating graph analysis and validation (including with LLM agents), merging graphs across prompts,
attribution to probe or feature targets rather than logits, hierarchical (Matryoshka) transcoders, decomposing MLPs
without transcoders (e.g. Jacobian SVD), sparse mixtures of linear transforms; mechanistic questions such as
variable binding, state tracking, planning and where facts are stored; CoT faithfulness.

## What we take from it
- **Warning (central for us):** reconstruction metrics and replacement quality diverge; a white-box model must be
  scored on what it predicts (intervention outcomes, outputs), not only on reconstruction error.
- **Gap we could fill:** graphs are per-prompt traces; a global, weight-derived model that generalises across
  prompts and predicts "why not" alternatives is named as open.
- **Warning:** learned dictionaries can destroy geometric structure (helix → lookup table); reading weights directly
  may preserve it.
- **Reusable:** replacement score, intervention-based validation, open CLTs and circuit-tracer for Gemma-2 2B /
  Qwen3-4B as baselines; Jacobian-SVD as a transcoder-free decomposition idea.

## Tags
unit: feature | circuit | layer
form: graph | replacement-model | dictionary
method: transcoder | attribution | patching | steering | ablation
eval: patching | faithfulness | completeness | benchmark
goal: understanding | science | evaluation-of-methods
