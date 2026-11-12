# Using Degeneracy in the Loss Landscape for Mechanistic Interpretability

- **Key:** arxiv-2405.10927
- **Authors / organisation:** Lucius Bushnaq, Jake Mendel, Stefan Heimersheim, Dan Braun, Nicholas Goldowsky-Dill, Kaarel Hänni, Cindy Wu, Marius Hobbhahn; Apollo Research (Hänni: Cadenza Labs; Wu: independent)
- **Date:** 2024-05-17
- **Link:** https://arxiv.org/abs/2405.10927
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors argue that a major reason networks are hard to reverse-engineer from their weights is degeneracy: many parameter settings compute the same function, so lots of parameters (and the bases they are expressed in) carry no computational meaning and hide the real structure. Using singular learning theory (SLT), they argue that training is biased toward highly degenerate solutions, and that these generalise better. Their proposal is to find a representation of the network that is invariant to these redundant reparameterisations, on the bet that such a representation will be sparser, more modular and more interpretable. This is the theoretical groundwork for the Local Interaction Basis and later parameter-decomposition methods (APD/SPD).

## What they studied
Mostly theory. Worked examples are fully connected ReLU networks, deep linear networks and transformer attention heads (e.g. the known W_O W_V redundancy); a modular-addition transformer is cited as motivation. Unit of analysis: weights/parameters and the bases of layer activations.

## How they did it
1. Define a behavioural loss: the squared distance between a candidate parameterisation's outputs and the original network's outputs on the data, so the original weights are always a minimum and zero-loss sets are exactly function-preserving reparameterisations.
2. Use the (local) learning coefficient from SLT as a measure of degeneracy, but evaluated at a finite loss scale epsilon rather than in the limit, giving an "effective parameter count" (twice the learning coefficient) that depends on how precisely behaviour must be preserved.
3. Identify three concrete sources of degeneracy: linear dependence among a layer's activations, linear dependence among the Jacobians/gradients flowing back into a layer, and groups of ReLUs that switch on/off on the same data points (and analogous synchronised attention heads), counting the free directions each contributes.
4. Show that changing basis to remove these degeneracies yields non-interacting pairs of directions between adjacent layers (interaction sparsity).
5. Give a heuristic argument that non-interacting modules have additive degeneracy, so modular networks have lower learning coefficients, and derive a module-finding criterion: partition the interaction graph to minimise a sum of logs of cutoff-normalised interaction strengths.
6. Propose the Interaction Basis: whiten activations using their Gram matrix, diagonalise a Jacobian-based matrix in the whitened space, then rescale to remove gradient degeneracies. In deep linear networks this reduces to an SVD of each weight matrix.

## What counts as an explanation here
A reparameterisation-invariant basis (and, ideally, a modular decomposition of the interaction graph) in which the network's computation is sparse. The explanation is a change of coordinates on weights and activations plus a partition into modules, not a text description. It is meant to strip out all non-computational freedom, so in principle complete up to the noise scale epsilon; it does not on its own predict behaviour beyond the original network.

## How they judged success
Essentially by theoretical argument and toy derivations. No benchmark or quantitative metric is reported in this paper; the authors refer to a companion paper (the Local Interaction Basis work) for empirical tests of sparsity, modularity and interpretability. The conceptual yardsticks are: effective parameter count, interaction sparsity between adjacent-layer basis directions, and modularity of the interaction graph.

## What they found
- Effective parameter count depends on the precision scale; a toy example shows the learning coefficient moving between two values as epsilon changes.
- Each linear dependence in a layer's activations removes a full row's worth of effective parameters in the next weight matrix; synchronised ReLU blocks contribute a number of free directions quadratic in block size.
- Removing degeneracy via a basis change produces at least one non-interacting pair per degeneracy removed.
- The Interaction Basis is invariant to invertible linear transformations of activations (up to sign and eigenvalue ties).
- The authors report (via the companion paper) that this basis gives sparse, modular, interpretable structure on toy models but is much less useful on LLMs.

## Limits and open problems they name
Strong independence assumptions in the Hessian approximation; the three degeneracy sources are not claimed to be exhaustive; Jacobian degeneracies may not yield full free directions because of higher-order terms; the modularity argument is heuristic; choosing epsilon is unresolved; synchronisation analysis is incomplete for approximate cases; no numerical validation in this paper.

## What we take from it
A framing and a warning for reading weights directly: raw weights and neuron bases include a lot of non-computational freedom, so any white-box model read from weights should first quotient out reparameterisation symmetries (activation null-spaces, gradient null-spaces, synchronised units). "Effective parameter count at precision epsilon" is a candidate complexity measure for our reconstruction, and the behavioural loss (match the original network's outputs, not the labels) is the right fidelity target. The interaction-basis recipe (whiten, then diagonalise a Jacobian matrix) is a cheap first-pass basis to try. The reported failure on LLMs is a warning that linear-basis methods alone are insufficient at scale.

## Tags
unit: weights | layer
form: direction | other (reparameterisation-invariant basis, modules)
method: weight-analysis | decomposition | other (singular learning theory)
eval: other (theoretical; empirical tests deferred to companion paper)
goal: understanding | science
