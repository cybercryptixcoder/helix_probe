# Stochastic Parameter Decomposition

- **Key:** arxiv-2506.20790
- **Authors / organisation:** Lucius Bushnaq, Dan Braun, Lee Sharkey; Goodfire (work largely begun at Apollo Research)
- **Date:** 2025-09-04 (v2; original June 2025)
- **Link:** https://arxiv.org/abs/2506.20790
- **Kind:** paper
- **Read from:** full text (arXiv HTML, method, results and discussion)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The overarching project is reverse engineering networks into mechanisms that can be studied one at a time, so that behaviour can be predicted, designed and audited. Earlier work decomposed activations (sparse dictionary learning) and hit conceptual problems: the notion of a "feature" is undefined, multi-dimensional features and feature geometry are hard to handle, and the parts are not functional components. Linear parameter decomposition was proposed to fix this by splitting the *parameters* rather than activations into a sparse sum of parameter-space vectors called parameter components, which should be faithful, minimal and simple. The only existing method, Attribution-based Parameter Decomposition (APD), is however impractically expensive and needs a guessed top-k. This paper supplies a practical replacement.

## What they studied
Toy models with known ground truth, not language models: a Toy Model of Superposition (5 features into 2 dims, 40 into 10), the same model with an identity matrix inserted in the hidden space, a Toy Model of Compressed Computation (1 residual MLP layer, width 50, 100 input features, residual width 1000, task needs more ReLUs than neurons), and Toy Models of Cross-Layer Distributed Representations with two and three MLP blocks. Unit of analysis: rank-one subcomponents of individual weight matrices (later to be clustered into full parameter components). Biases are not decomposed (folded out for later work).

## How they did it
Each weight matrix is approximated as a sum of C rank-one matrices U_c V_c^T, where C may exceed the rank, so overcomplete/superposed parameter structure is allowed. Faithfulness is a plain squared error between the target matrix and the summed subcomponents. Minimality is enforced with a learned causal-importance function g_c(x) in [0,1] per subcomponent per datapoint: the model's weights are replaced by randomly masked subcomponents, where each subcomponent is multiplied by a scalar drawn uniformly from [g_c, 1]; substituting this masked network for the target and training it to reproduce the target's output forces important subcomponents to be barely ablatable and unimportant ones to be ablatable arbitrarily. A penalty pushes g toward zero, so the fewest possible subcomponents stay causally important. Because masks are sampled stochastically rather than from a hard top-k, gradients reach every subcomponent on every step, in contrast with APD's top-k selection and gradient-attribution estimates of importance. In toy models the subcomponents assigned to the same ground-truth mechanism were grouped by hand; an algorithmic clustering step is left as future work.

## What counts as an explanation here
A decomposition of the network's weights into a sparse set of rank-one, layer-local parameter subcomponents, grouped into parameter components, whose combination on a given input reproduces the model's output while the rest can be ablated with no effect. The explanation is meant to be an exact re-parameterisation of the original model, not an approximation or a surrogate, and its intended power is causal prediction: which pieces a given input actually uses.

## How they judged success
Ground-truth recovery against the known mechanism, quantified by Mean Max Cosine Similarity (MMCS) between each ground-truth direction and its best-matching subcomponent column, and Mean L2 Ratio (ML2R) to catch magnitude shrinkage. Supporting evidence: output similarity of the parametrised network to the target, causal-importance heatmaps on one-hot inputs showing one subcomponent per feature, the number of non-negligible-norm subcomponents versus the true count, and qualitative comparison with APD on the same models. Repeated over training seeds; APD numbers are quoted from the prior paper.

## What they found
On superposition toys SPD recovers the columns of W essentially exactly: MMCS 1.000 in all four superposition variants and ML2R between 0.99 and 1.03, versus about 0.9 ML2R for APD, i.e. APD shrank the components while SPD did not. Models with a hidden identity matrix, which APD failed on, were decomposed correctly, with only m2+m1 subcomponents of non-negligible norm. In compressed computation the MLP input matrices decompose into one component per input feature connected across many polysemantic neurons. In the two-layer and three-layer distributed models the input matrices decompose into 100 and 102 feature components spread over all layers, and the output matrices collapse into a single rank-50 (resp. rank-51) component that also spans every layer. SPD needed far less hyperparameter search than APD, largely because it replaces the guessed top-k with a penalty coefficient that is forgiving.

## Limits and open problems they name
Toy models only; scaling to language models will likely need more training-stability work. Only rank-one, single-layer subcomponents are found, so a clustering step is required to assemble multi-rank and multi-layer components when ground truth is unknown, and that clustering method is not given. Causal importance is computed per layer, which may mark subcomponents as important when information from a later layer would show they are not. Sensitivity to random seeds appeared in the multi-layer models. Whether the decomposition gives the shortest description of network function is unknown. Self-repair means an ablated "important" component may be compensated by others, so causal importance is not a simple causal-dependence test.

## What we take from it
Method: rank-one parameter decomposition with a *learned, ablatability-based* causal importance map is the cleanest published way to read a network's weights directly and get per-input prediction of which piece fires (directly reusable if we want a parts-based read of weights rather than activations). Measure: MMCS and ML2R as ground-truth recovery and anti-shrinkage metrics; the "random mask sampled from [g,1]" trick as a way to probe ablatability continuously instead of all-or-nothing. Framing: faithfulness/minimality/simplicity as the three properties to quantify, and the argument that a decomposition that sums back exactly to the weights avoids the ill-posedness of activation dictionaries. Warning: layer-local importance is a known compromise, and without ground truth you inherit an unsolved clustering problem; also seed sensitivity means any weight-decomposition claims need seed repeats.

## Tags
unit: weights | feature
form: dictionary
method: decomposition | ablation
eval: ablation | prediction/simulation
goal: understanding | safety/auditing
