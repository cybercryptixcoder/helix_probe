# A Survey of Weight Space Learning: Understanding, Representation, and Generation

- **Key:** arxiv-2603.10090
- **Authors / organisation:** Xiaolong Han, Zehong Wang, Bo Zhao, Binchi Zhang, Jundong Li, Damian Borth, Rose Yu, Haggai Maron, Yanfang Ye, Lu Yin, Ferrante Neri; University of Surrey, University of Notre Dame, UC San Diego, University of Virginia, University of St. Gallen, Technion / Nvidia
- **Date:** 2026-03
- **Link:** https://arxiv.org/abs/2603.10090
- **Kind:** survey/agenda
- **Read from:** abstract and sections (taxonomy sections 1-3 in detail; benchmark section partly; open questions and conclusion; generation section body only partly visible)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors argue that trained weights should be treated as a data modality in their own right, and they name the
field Weight Space Learning (WSL). Work on this has been scattered under labels like neural functionals or "neural
representations for neural networks", so they propose one taxonomy to unify it. The larger goal is a field in
which large public model zoos can be analysed, embedded, searched, compared and generated directly from their
parameters, rather than only by running them on data.

## What they studied
The literature, not models. The unit is the whole weight vector of a network (MLPs, CNNs, RNNs/LSTMs,
Transformers, INRs/NeRFs, LoRA adapters), and the model zoos built to study it.

## How they did it
A literature review organised along three axes. (1) Weight Space Understanding: the symmetries of weights
(neuron permutation, positive rescaling, sign flips, head permutation, rotations; six examples in a table) and
uses such as compression, symmetry-based optimisation and weight-space augmentation. (2) Weight Space
Representation: mapping weights to an embedding plus a task head. Model-based encoders run from
symmetry-agnostic ones (weight statistics, flattened-weight MLP/CNN, transformer hyper-representations) to
permutation-equivariant ones (DWSNets, NFN, Neural Functional Transformers, UNFs) and graph metanetworks (Neural
Graphs, Graph Metanetworks, Scale-GMN). Model-free approaches (ProbeLog, ProbeGen, ProbeX) embed a network from
its responses to probe inputs instead. Uses: behaviour/accuracy prediction, model retrieval, editing.
(3) Weight Space Generation: hypernetworks and diffusion models over weights, for conditional generation,
merging, initialisation and so on. A benchmark section lists model zoos by architecture, and a final section
lists open questions.

## What counts as an explanation here
Mostly not explanation in the interpretability sense. "Understanding" here means characterising weight-space
geometry and symmetry (why minima are connected, why subnetworks are redundant). "Representation" means a
learned embedding that predicts properties such as accuracy or generalisation gap. These predict coarse
properties of a network, not its input-by-input behaviour or mechanism.

## How they judged success
No unified metric suite. The reviewed work uses regression/classification of model properties (test accuracy,
generalisation gap, hyperparameters), retrieval by embedding distance, and zero-shot performance prediction.
Benchmarks are model zoos, for example: Schürholt et al. (2021) 3.9K small MLPs; Unterthiner et al. (2020) about
120K CNNs over MNIST, Fashion-MNIST, CIFAR-10 and SVHN; NWS (Eilertsen et al., 2020) 16K CNNs, 320K with
checkpoints; Schürholt et al. (2022b) 27 CNN zoos; Honegger et al. (2023) 1.7M+ sparsified CNNs; Implicit-Zoo;
an LSTM zoo (Herrmann et al., 2024) with 9 checkpoints per run; a ViT zoo (Falk et al., 2025) fine-tuned on
CIFAR-100 under 24 configurations; w2w with 60K LoRA-tuned diffusion models.

## What they found
The field has moved from symmetry-blind encoders toward encoders that build in permutation (and scaling)
symmetries, and these generally do better. Model-free probing is a complementary route when weights are
unavailable; interactive probing for RNNs is reported to be far more efficient than static probes. Accuracy
prediction is described as only a partial signal of representation quality.

## Limits and open problems they name
Heterogeneous architectures resist a single representation; millions of weights make inputs huge; symmetry
theory is incomplete for transformers (couplings break simple group structure) and for real models with
normalisation and residuals; working in quotient space can need costly matching; a general meta-model that
handles any architecture is largely unsolved. Future directions: architecture-agnostic learners, scaling
(hierarchical processing, working on LoRA/fine-tuning modules, low-dimensional subspaces), and safety (detecting
adversarial edits or injected subspaces, auditable weight generation). Backdoor detection and mechanistic
interpretability are barely covered.

## What we take from it
A map and a vocabulary: our project sits in "weight space representation" but aims at a much finer target
(predicting behaviour per input, and under intervention) than the field's usual targets (accuracy,
hyperparameters). Reusable pieces: the symmetry list (any weight reader must be invariant to them, or we must
canonicalise first), the equivariant baselines (DWSNets, NFN, Graph Metanetworks) we would be compared against,
and existing model zoos as ready-made test sets. Warning: the field barely connects to mechanistic
interpretability, which is both a gap we can occupy and a sign that reviewers from each side will want the other
side's baselines.

## Tags
unit: weights | whole-model
form: description | other
method: weight-analysis | other
eval: prediction/simulation | benchmark | downstream-task
goal: science | evaluation-of-methods
