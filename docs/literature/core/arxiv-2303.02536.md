# Finding Alignments Between Interpretable Causal Variables and Distributed Neural Representations

- **Key:** arxiv-2303.02536
- **Authors / organisation:** Atticus Geiger, Zhengxuan Wu (equal contribution), Christopher Potts, Thomas Icard, Noah D. Goodman; Stanford University (Pr(Ai)²R group)
- **Date:** 2023-03
- **Link:** https://arxiv.org/abs/2303.02536
- **Kind:** paper
- **Read from:** full text (HTML version)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Causal abstraction tests whether a small, human-readable causal model (variables plus mechanisms) is a faithful
high-level description of a neural network. Earlier work had to search by brute force for which neurons realise
each high-level variable, and assumed each variable lives in its own disjoint set of neurons (a "localist"
alignment). Real networks often store variables in distributed, non-axis-aligned form. The authors want a
gradient-based way to find such distributed alignments, so causal-abstraction analysis can scale and stop
depending on the neuron basis. The larger goal is to verify that a network implements a specific interpretable
algorithm.

## What they studied
(1) A three-layer ReLU feed-forward network trained to 100% accuracy on hierarchical equality (is "w = x"
equal to "y = z"?) with random-vector inputs. (2) Uncased BERT-base (12 layers, 768 hidden) fine-tuned on
MultiNLI then on MoNLI, a monotonicity NLI dataset where negation flips lexical entailment; only the [CLS]
representation was analysed. Unit of analysis: learned subspaces (rotated directions) of a layer's hidden
vector.

## How they did it
They write candidate high-level causal models (e.g. "compute both equality relations, then compare"; "only the
left equality"; "identity of the first argument"; for MoNLI "negation and lexical entailment", "lexical
entailment only", "lexeme identity"). They generate interchange-intervention data from the high-level model:
for a base input and a source input, what the output should be if a given variable took its value from the
source. In the network, a hidden vector is rotated by a learned orthogonal matrix, a chosen block of rotated
dimensions is swapped in from the source run, and the result is rotated back (a distributed interchange
intervention). Only the rotation is trained (SGD, PyTorch orthogonal parametrisation), with cross-entropy
between the network's counterfactual output and the high-level model's predicted counterfactual output; the
network stays frozen. Discrete choices (layer, number of neurons N, subspace size per variable) are swept.
Baselines: brute-force search over sliding windows of neurons, and the axis-aligned (permutation/reflection)
matrix closest to the learned rotation. A frozen random network serves as a control. They also test whether a
found subspace further decomposes into sub-variables.

## What counts as an explanation here
A causal abstraction: an explicit high-level causal model plus an alignment map from each high-level variable to
a linear subspace of a specific layer. It is a hypothesis about the algorithm, and it is predictive: it says what
the network will output under counterfactual interventions on those subspaces. It can be partial (only some
variables aligned), and fit is graded rather than all-or-nothing.

## How they judged success
Interchange intervention accuracy (IIA): the share of interventions where the network's counterfactual output
matches the high-level model's. Compared against brute-force and localist baselines; random-network control
(can DAS manufacture alignment from nothing?); comparisons between rival high-level models by relative IIA;
runtime comparisons. Best of three seeds reported.

## What they found
Hierarchical equality: the "both equality relations" model reaches IIA 1.00 at layer 1 with DAS, versus 0.60
for brute force and 0.73 for the localist alignment; "identity of first argument" stays near chance (~0.5),
so the network represents abstract equality, not just the input identities. MoNLI: at BERT layer 9 with a
256-dimensional intervention, the negation-and-lexical-entailment model reaches IIA 1.00; localist alignment
scores about 0.5. The lexical-entailment subspace further decomposes into word-identity subspaces (IIA
0.97–0.98), so the network stores a structure of the two words rather than a pure relation. On a random
network, DAS gains IIA only when the hidden layer is far larger than the input, which the authors take as
evidence DAS does not create behaviour from scratch in normal regimes. DAS cost (502 s, 1105 s) does not grow
with the number of hypotheses, unlike brute force.

## Limits and open problems they name
Rotations are linear; nonlinear manifolds would need invertible nonlinear maps. The full d×d rotation does not
scale (whole-sequence BERT would need billions of parameters); low-rank or subspace-only parametrisations are
suggested. Results are seed-sensitive. Only two tasks with two binary variables each. It requires a causal model
of the task and the ability to sample counterfactual inputs. No theory for interpreting IIA strictly between
chance and 1. (The HTML version also shows a duplicated table row, likely a copy error.)

## What we take from it
A method and a measure. IIA is exactly the kind of "prediction under intervention" score we want for a white-box
model: our reconstruction should state counterfactual outcomes, and IIA checks them. DAS is a way to locate where
a hypothesised variable lives without assuming the neuron basis. Warning: DAS is optimised end-to-end on outputs,
so a high IIA can be overfit or illusory (see arxiv-2311.17030); the random-network control and held-out
evaluation are controls we should copy. It finds alignments from activations and gradients, not by reading
weights, so it serves as a check on a weight-derived model, not a substitute.

## Tags
unit: direction | layer
form: causal-abstraction | direction
method: patching | other
eval: patching | prediction/simulation | faithfulness
goal: understanding | science
