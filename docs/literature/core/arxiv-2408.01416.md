# The Quest for the Right Mediator: Surveying Mechanistic Interpretability Through the Lens of Causal Mediation Analysis

- **Key:** arxiv-2408.01416
- **Authors / organisation:** Aaron Mueller, Jannik Brinkmann, Millicent Li, Samuel Marks, Koyena Pal, Nikhil Prakash, Can Rager, Aruna Sankaranarayanan, Arnab Sen Sharma, Jiuding Sun, Eric Todd, David Bau, Yonatan Belinkov; Boston University, University of Mannheim, Northeastern University, Anthropic, MIT, Stanford, Technion
- **Date:** 2024-08 (v1; v3 of 2025-09 read, accepted as an MIT Press article)
- **Link:** https://arxiv.org/abs/2408.01416
- **Kind:** survey/agenda
- **Read from:** full text (HTML v3, read in three parts; the v1 title was "A History, Survey, and Theoretical Grounding of Causal Interpretability")
- **Relevance to us:** 3 (central)

## What they wanted, and why
The field of mechanistic interpretability lacks a shared vocabulary, so studies using different units and
different interventions are hard to compare. The authors recast the whole field as causal mediation analysis: a
network's computation graph is the full causal graph, and an interpretation is a smaller, task-specific causal
graph whose nodes ("mediators") explain how inputs affect outputs. They organise prior work by the kind of mediator
used and by how the mediator was searched for, and ask which mediator suits which goal. The larger aim is a common
theoretical footing and standard benchmarks for measuring progress.

## What they studied
Literature, not models. Mediator types: full layers and submodules; neurons; basis-aligned multidimensional
subspaces; attention heads; non-basis-aligned subspaces; single directions; non-linear mediators. Search methods:
exhaustive search (activation patching / causal tracing), gradient attributions (attribution patching and
integrated-gradients variants), supervised optimisation (probing; mask learning such as subnetwork probing and DCM;
DAS and Boundless DAS), and unsupervised optimisation (sparse autoencoders, clustering). Also a history from 1980s
rule extraction through visualisation, probing, and the post-2017 return of causal intervention.

## How they did it
They ground the framing in Lewis's counterfactual account of causation and Pearl's direct and indirect effects: a
mediator's indirect effect is the change in output when that mediator is set to a counterfactual value while the
input is held fixed. They separate the choice of mediator from the choice of counterfactual value (activation from
an alternate input, dataset mean, zero, scaled noise), noting the latter strongly changes what is found. An
appendix classifies interventions as deterministic input-dependent (minimal pairs, precise but low recall),
stochastic (noise, run-to-run variance, harder to interpret), constant, and class-dependent. For each mediator type
they tabulate search cost (e.g. O(l*d) neurons, O(l*|A|) heads, 2^(l*d) basis-aligned subspaces, infinite search for
directions) and pros and cons. They then map mediator plus search method onto three research goals.

## What counts as an explanation here
A causal graph over chosen mediators that is a simplification of the network's computation graph; for hypothesis
verification, a high-level causal model aligned to the network (causal abstraction). Explanations are partial by
design (task-specific) and are predictive in the counterfactual sense: they claim what the output becomes under
interventions on the mediators.

## How they judged success
They propose four criteria that apply to any mediator set: sparsity (minimality), generality (out-of-distribution
performance), selectivity (explaining only the phenomenon of interest), and faithfulness to the original model, plus
human understandability; the ideal is a Pareto optimum across them. Goal-specific emphasis: explaining behaviour
(all four; faithfulness is standard, generality and selectivity rarely measured); verifying a hypothesis
("counterfactual faithfulness", measured by interchange intervention accuracy, IIA); localisation/editing
(downstream task performance, faithfulness trivially satisfied if the edit works). Points to the Mechanistic
Interpretability Benchmark (MIB) for comparing mediators and search methods.

## What they found
Finer-grained mediators are sparser and more selective but harder to search and, when optimised, at higher risk of
being unfaithful; coarser ones are general and cheap but unselective. Neurons and heads suffer polysemanticity and
compensation (the Hydra effect). Probes give false positives unless causally checked (indirect effect of the probe
direction, concept erasure such as LEACE). SAE features reach higher faithfulness with fewer components than
neurons but are correlational and reconstruction is only a proxy. Recommended pairings: unsupervised search over
non-basis-aligned directions for open-ended explanation; counterfactual optimisation over multidimensional subspaces
(alignment search) for verifying a hypothesis; exhaustive patching over layers or basis-aligned units for
localisation and editing.

## Limits and open problems they name
Non-linear and multidimensional mediators (e.g. circular day-of-week codes) are poorly handled; automatic subgraph
search is missing; better-than-greedy search over sets of mediators is needed; fast approximations need validation;
optimised directions may not reflect the model; generality and selectivity lack scalable measures; inherently
interpretable architectures (transcoders, backpack LMs, concept bottlenecks) may cost performance. Tooling biases
what is studied (TransformerLens favours neurons/heads; pyvene favours learned subspaces).

## What we take from it
A framing and a checklist. Our white-box model is a candidate causal graph over mediators, so we should state its
mediator type and intervention type explicitly and report sparsity, generality, selectivity and faithfulness rather
than one score. IIA is the field-recognised measure for "the reconstruction predicts the network under
intervention". Warning: results depend on the counterfactual value, so pick and report it deliberately. Weights are
not a mediator type in their taxonomy; weight-derived mediators are a gap we could position into.

## Tags
unit: neuron | head | direction | layer | circuit | feature
form: graph | causal-abstraction
method: patching | attribution | probing | SAE | ablation | decomposition
eval: faithfulness | patching | benchmark
goal: evaluation-of-methods | understanding | science
