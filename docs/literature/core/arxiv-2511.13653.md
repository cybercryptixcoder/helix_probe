# Weight-sparse Transformers Have Interpretable Circuits

- **Key:** arxiv-2511.13653
- **Authors / organisation:** Leo Gao, Achyuta Rajaram, Jacob Coxon, Soham V. Govande, Bowen Baker, Dan Mossing; OpenAI
- **Date:** 2025-11-17
- **Link:** https://arxiv.org/abs/2511.13653
- **Kind:** paper
- **Read from:** full text of main body (later appendices partly)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
In dense models, concepts are smeared across many weights, so circuits are large and hard to read. The authors instead
train transformers whose weights are almost all zero, so that the circuit for a behaviour has few edges and can be
followed by hand. The larger aim is interpretable "model organisms", possibly up to GPT-3-level capability, connected by
learned bridges to ordinary dense models.

## What they studied
GPT-2-style decoder-only transformers (typically 8 layers, d_model 2048, context 256, d_head 16) trained on Python code,
with all weights sparse (sparsest about 1 in 1000 nonzero) and mild activation sparsity (about 1 in 4 via AbsTopK).
Twenty hand-made binary next-token Python tasks (e.g. closing quote type, bracket nesting depth, set vs string variable
type). Unit: circuits whose nodes are neurons, attention channels and residual read/write dimensions, and whose edges are
nonzero weights.

## How they did it
Training with AdamW keeps only the largest-magnitude entries of each matrix after every step, with the nonzero fraction
annealed from dense over the first 50% (or 80%) of training. For each task, a pruning procedure learns a binary mask
over nodes (Heaviside with a sigmoid-derivative surrogate gradient), trading task loss against circuit size; pruned
nodes are mean-ablated to their pretraining mean; the default target task loss is 0.15. They compare circuit sizes in
sparse vs dense models of matched pretraining loss, sweep width and L0 to map a capability-interpretability frontier,
hand-analyse several circuits, construct adversarial prompts predicted from the circuit, and train SAE-like "bridges"
(linear+AbsTopK encoders, linear decoders) at each sublayer to map sparse-model channels into a dense model and
intervene through them.

## What counts as an explanation here
A small subgraph of the actual weights (a circuit) that is both sufficient and necessary for a task, read by a human
as a step-by-step algorithm. Partial (per task), but literally made of the model's own weights, so it predicts
behaviour, including failure cases.

## How they judged success
Geometric mean number of circuit edges at the target loss (main interpretability proxy); sufficiency (mean-ablating
everything else preserves task loss) and necessity (deleting the circuit wrecks it); pretraining loss as capability;
residual-stream kurtosis as an activation-sparsity proxy; adversarial prompts derived from the circuit; behaviour change
in a dense model when editing through bridges.

## What they found
Circuits in weight-sparse models are about 16 times smaller than in dense models of comparable pretraining loss.
Widening at fixed L0 improves both capability and interpretability; lowering L0 trades capability for interpretability.
The quote-closing circuit uses two layer-0 neurons and one layer-10 head (about 9 of 41 edges used). Bracket depth is
computed by a head averaging an open-bracket detector plus a later thresholding head (about 283 edges); a distractor
prompt predicted from this circuit fooled the model and also similarly capable dense models. Variable-type tracking is a
two-hop, two-head mechanism (about 100 edges). Bridge interventions shifted dense-model behaviour (quote type fully,
colon vs newline partly).

## Limitations and open problems they name
Sparse models cost roughly 100 to 1000 times more compute; many neurons die; some concepts remain spread across
nodes; some features are graded, not binary; mean ablation is an imperfect faithfulness test (causal scrubbing
suggested); edge count is only a proxy for understandability; node-level pruning needed manual cleanup; scaling past
tens of millions of nonzero parameters while staying interpretable is open.

## What we take from it
An existence proof that when weights are sparse, circuits can be read straight from weights and used to predict novel
failures (the distractor prompt) - the kind of prediction we want our white-box model to make. Reusable measures:
circuit edge count at fixed task loss, sufficiency/necessity under mean ablation, and the capability-interpretability
frontier. The "bridge" idea suggests a route to explaining a dense black box via an interpretable sibling. Caveat: it
requires training the model, so it does not directly apply to an existing black box.

## Tags
unit: circuit | weights | neuron | head
form: graph | program
method: training-interpretable | ablation | weight-analysis
eval: ablation | faithfulness | completeness | prediction/simulation
goal: understanding | safety/auditing
