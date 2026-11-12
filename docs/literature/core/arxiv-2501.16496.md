# Open Problems in Mechanistic Interpretability

- **Key:** arxiv-2501.16496
- **Authors / organisation:** Lee Sharkey, Bilal Chughtai (leads, Apollo Research) and many co-authors from Anthropic (incl. Joshua Batson, Jack Lindsey), Google DeepMind (Arthur Conmy, Neel Nanda), MIT, Northeastern, Tel Aviv U., Timaeus, Goodfire, EleutherAI, FAR AI, METR, U. Melbourne, Pr(AI)r group and others; prepared by Apollo Research on behalf of Schmidt Sciences
- **Date:** 2025-01-27
- **Link:** https://arxiv.org/abs/2501.16496
- **Kind:** survey/agenda
- **Read from:** full text (HTML, read in parts; methods and applications sections in detail, socio-technical section in summary)
- **Relevance to us:** 3 (central)

## What they wanted, and why
A forward-looking, multi-lab map of what mechanistic interpretability still cannot do and which directions should be prioritised, rather than a catalogue of the state of the art. The authors define the goal of the field as understanding a network's mechanisms well enough to predict its behaviour, even on arbitrary inputs, or to achieve practical aims such as control and better design. They separate this "mechanistic" thread from older interpretable-by-design and local-attribution work. The larger aim is to make interpretability useful for monitoring, control, prediction of behaviour and capabilities, scientific discovery ("microscope AI"), and governance.

## What they studied
No new experiments; a review. Unit of analysis ranges over neurons, attention heads, SAE/transcoder/crosscoder latents, directions and subspaces, circuits/subgraphs, and (as an open gap) weights/parameters. Examples cited span CNNs, BERT, GPT-2, GPT-4 SAEs, modular-addition toy transformers, AlphaZero, and some diffusion/ViT/SSM work.

## How they did it
They organise the field as a reverse-engineering loop with three steps: (1) decompose the network into components, (2) describe each component's functional role, (3) validate those descriptions, returning to step 1 or 2 when validation fails. For each step they list methods and their known failure modes. Decomposition covers architectural units, dimensionality reduction, sparse dictionary learning (SDL), and intrinsically interpretable architectures. Description covers input-side methods (top-activating examples, gradient attribution, feature synthesis) and output-side methods (logit lens, tuned lens, direct logit attribution, activation/path patching, causal scrubbing, distributed alignment search, steering, patchscopes). Validation covers predicting activations and counterfactuals, predicting failures/adversarial examples, handcrafting replacement components, ground-truth toy models (including programs compiled into weights), and downstream engineering use. They separately treat concept-based (probing) interpretability, a five-step circuit-discovery pipeline as a case study, automation (auto-interp, ACDC), applications, and socio-technical issues.

## What counts as an explanation here
A decomposition into components plus validated descriptions of each component's role and of how components interact (a circuit or mechanism). Descriptions are explicitly hypotheses until validated causally; the bar for "understanding" is predictive: the explanation should let you forecast activations, counterfactual behaviour and failures. Explanations are expected to be partial today; complete enumeration ("enumerative safety") and formal guarantees are aspirations.

## How they judged success
As a review, they list the field's criteria: circuit faithfulness, minimality and completeness; loss/performance recovered when a dictionary is spliced in (reconstruction error); simulation-style scoring of natural-language feature descriptions (how well a human or model predicts activations from the description); sanity checks for attribution; ground-truth recovery on toy or compiled models; and downstream utility (editing, debugging, unlearning). They stress that competitive evaluation against non-interpretability baselines on non-cherry-picked tasks is rare.

## What they found
- SDL has large reconstruction error: a 16M-latent dictionary in GPT-4 yields loss comparable to a model trained with about 10% of GPT-4's pretraining compute; on GPT-2 small, Makelov et al. report roughly 10% performance drop on task data and 40% on the full distribution. The errors are partly linearly predictable, so not pure noise.
- Sparsity is a weak proxy for interpretability (feature splitting, absorption, composition); SDL ignores feature geometry, struggles with attention and cross-layer structure, depends on its training data, and decomposes activations rather than the weights that compute them.
- Top-activating examples produce interpretability illusions; gradient attribution often fails sanity checks; logit lens sees only direct effects; probes find correlation, not causal use.
- Circuit work: task definitions are human-chosen and circuits fit averages but poorly describe individual inputs; faithfulness metrics depend on the ablation/intervention implementation; backup and negative components are missed; studied tasks are "streetlight" cases.
- Auto-interp can describe latents but fully automated pipelines do not yet give satisfactory explanations.
- Formal behavioural guarantees exist only for tiny cases (accuracy bounds proven for a one-layer transformer on a synthetic task, with great difficulty).
- Mechanistic edits to activations for unlearning have not been competitive; steering works moderately.

## Limits and open problems they name
Missing theory of what a "feature" is; decomposition methods that handle geometry, computation in superposition, attention and cross-layer structure; explaining mechanisms through weights rather than activations; reliable validation beyond correlation; agreed model organisms (open, cheap, multiple seeds, open data); intrinsically decomposable models that do not lose performance or let superposition leak back in; scaling behavioural prediction and verification to frontier models; comparing against black-box baselines; universality across model families.

## What we take from it
- Framing: the field's own definition of understanding is prediction of behaviour on arbitrary inputs, which is exactly our target; we can cite it to justify a predictive white-box model as the evaluation standard.
- Gap we can claim: they explicitly flag that SDL describes activations, not how weights compute them; a weight-reading reconstruction addresses a named open problem.
- Validation menu to adopt: predict activations and counterfactuals, predict failures, handcraft replacement components, recover ground truth on compiled/toy models, compete against black-box baselines.
- Warnings: report reconstruction/performance-recovered honestly; specify the ablation used; evaluate per-input not just averaged; avoid streetlight tasks; treat descriptions as hypotheses.
- Model-organism criteria (open, cheap, multiple seeds) are a checklist for choosing our test networks.

## Tags
unit: neuron | feature | direction | head | circuit | weights | whole-model
form: dictionary | graph | description | probe | steering | causal-abstraction
method: SAE | transcoder | attribution | patching | ablation | probing | steering | agent | weight-analysis | decomposition | training-interpretable
eval: ablation | patching | prediction/simulation | faithfulness | completeness | downstream-task | benchmark
goal: understanding | safety/auditing | control/editing | science | evaluation-of-methods
