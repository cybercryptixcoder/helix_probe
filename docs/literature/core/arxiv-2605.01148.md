# Arithmetic in the Wild: Llama uses Base-10 Addition to Reason About Cyclic Concepts (Goodfire blog: "A Geometric Calculator Inside a Neural Network")

- **Key:** arxiv-2605.01148
- **Authors / organisation:** Sheridan Feucht, Tal Haklay (co-first), Usha Bhalla, Daniel Wurgaft, Can Rager, Raphaël Sarfati, Jack Merullo, Thomas McGrath, Owen Lewis, Ekdeep Singh Lubana, Thomas Fel, Atticus Geiger (co-senior: Lubana, Fel, Geiger); Goodfire with Northeastern, Technion, Harvard, Stanford
- **Date:** 2026-05 (blog 2026-05-14)
- **Link:** https://arxiv.org/abs/2605.01148 (blog: https://www.goodfire.com/research/a-geometric-calculator)
- **Kind:** paper (with blog/research post, part of Goodfire's "Neural Geometry" series)
- **Read from:** abstract and sections (blog in full; arXiv HTML methods and results, first ~27% of the page; formal limitations section not reached)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Earlier work showed that language models represent numbers and cyclic quantities on circles/Fourier features. This
paper asks how a model *computes* with those representations in natural prompts, e.g. "six months after August".
The goal is to connect representation geometry to an actual mechanism, which the authors argue is needed to explain,
debug and control behaviour. Note: the blog is titled "A Geometric Calculator Inside a Neural Network"; the arXiv
paper carries the title above.

## What they studied
Llama-3.1-8B. Tasks: months, weekdays, 24-hour times (offsets 1 to 2p for cycle length p) and plain addition a+b with
a,b in 1..100. Unit: residual-stream subspaces at the last token per sublayer, and individual MLP neurons in layer 18.

## How they did it
First they measured behaviour (in-cycle accuracy 82% months, 92% weekdays, 97% hours; explicit mod-7/12/24
arithmetic is unreliable). Then they ran Distributed Alignment Search: learn a low-rank orthonormal subspace (k=1-8
for months/weekdays, 1-16 for hours/addition) that, under interchange interventions, makes the frozen network agree
with an abstract causal model with variables for input concept, offset and output concept; swept over every
attention and MLP sublayer at the last token. They trained affine Fourier probes on addition for periods 1-150, and
circular probes in PCA space (after Engels et al.). Cross-task patching tested reuse: patch the addition sum into a
cyclic prompt and vice versa. Each layer-18 MLP neuron was scored by how much its down-projection lies in the DAS
output subspace; high-scoring neurons were ablated or kept alone, and grouped by Fourier period. Finally they steered
the layer-18 output by scaling the Fourier features.

## What counts as an explanation here
A causal abstraction: a high-level algorithm (convert cyclic concept to a number, add the offset in base 10 using
parallel Fourier components of periods 2, 5, 10, 20, 50, 100, later map back to the cycle) aligned to subspaces and a
small named neuron set. Partial (one module, one model) but predictive: it predicts the output of cross-task patches,
including specific errors.

## How they judged success
Interchange intervention accuracy (IIA) per layer; cross-task patching accuracy compared with clean accuracy;
neuron zero-ablation and keep-only accuracy on addition; Fourier-plane alignment of neurons against a baseline of the
average over all layer-18 neurons; steering effect on predicted month. Standard addition acts as a non-cyclic control.

## What they found
Input concept and offset are causally readable at >95% IIA up to the layer-18 MLP, then drop by about 80 points; the
output concept reaches 100% IIA after layer 18, so layer 18 is where the sum is computed. Patching addition into
cyclic prompts gives the right concept at >=40% (for months comparable to clean accuracy), with >60% of outputs being
the predicted sum, including "+100 echo" outputs like 114. Reverse patching recovers the pre-modulo sum (e.g. 30 for
"twenty months after October") in 63% of failed months prompts. About 28 neurons (~0.2% of the MLP) carry addition;
ablating them drops addition accuracy from 95% to 24%, keeping only them retains 86%. Neurons cluster by Fourier
period and write to features of the same period. So the model reuses one base-10 addition module for months, days
and hours rather than doing modular arithmetic natively.

## Limitations and open problems they name
Steering needs a scale (alpha=10) far above natural magnitudes, so these features do not fully control downstream
computation; the story is called compelling but incomplete. Circular output geometry only appears at layers 22-25,
so the layer-18 step itself is not circular. Larger Fourier periods may be missed; the "echo" is explained only
tentatively. Discovery relied on prior knowledge of Fourier number geometry. Open: methods to find such geometric
mechanisms at scale; why coarse and fine periods coexist (they suggest a Weber's-law-like precision argument).

## What we take from it
A model case of the form our white-box model should take: an algorithm plus a map to subspaces and a sparse neuron
set, validated by IIA, by keep-only/ablate accuracy (a completeness/sufficiency pair), and by predicting the outputs
of off-distribution cross-task patches, including the model's characteristic errors. The neuron score (overlap of a
neuron's output weights with a causal subspace) is a weight-reading tool we can reuse. Warning: the mechanism was
found with a hypothesis in hand; unsupervised discovery remains open.

## Tags
unit: neuron | direction | layer
form: causal-abstraction | direction
method: patching | probing | ablation | steering | weight-analysis
eval: patching | ablation | completeness | prediction/simulation
goal: understanding | science
