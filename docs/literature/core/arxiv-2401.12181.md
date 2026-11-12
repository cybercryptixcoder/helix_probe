# Universal Neurons in GPT2 Language Models

- **Key:** arxiv-2401.12181
- **Authors / organisation:** Wes Gurnee, Theo Horsley, Zifan Carl Guo, Tara Rezaei Kheirkhah, Qinyi Sun, Will Hathaway, Neel Nanda, Dimitris Bertsimas; MIT (Horsley also Cambridge)
- **Date:** 2024-01
- **Link:** https://arxiv.org/abs/2401.12181
- **Kind:** paper
- **Read from:** abstract and sections (via WebFetch summaries of the arXiv HTML; figures and appendices not viewed)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
If mechanisms are universal across models, interpretability findings transfer and are worth more. The authors test the
weakest version: do the same neurons appear when only the random seed changes? They hypothesise that universal neurons
are more likely to be monosemantic, and use universality as a filter to find interpretable neurons and study their
weight properties and functional roles.

## What they studied
GPT-2 small and GPT-2 medium, five seeds each, with Pythia-160M as support (and larger Pythia models in places). Data:
100M tokens of the Pile test set. Unit: MLP neurons, with weight-level analysis of their input/output vectors and their
composition with the unembedding and attention heads.

## How they did it
Compute Pearson correlation of every neuron's activation with every neuron in the other seeds' models (streaming). A
neuron's excess correlation is its best match correlation minus the best match in a randomly rotated basis of the same
layer (a no-privileged-basis baseline), averaged over models; above 0.5 counts as universal. Compare universal and
non-universal neurons on weight and activation statistics (weight norm, input bias, activation frequency, pre-activation
skew and kurtosis). Label neuron families with several hundred automated binary tests (token properties, spaCy POS and
dependency labels, positions, Pile subsets), scored by variance reduction of activations. Analyse output roles from
weights by projecting w_out onto the unembedding and examining the skew and kurtosis of that vocabulary distribution
(prediction, suppression, partition neurons). Test specific mechanisms by intervention: fixing an "entropy neuron"'s
activation and tracking final layer-norm scale and prediction entropy (against 20 random final-layer neurons); a
weight-based score for neurons that push attention heads to the BOS token, checked with path ablation.

## What counts as an explanation here
A taxonomy of neuron families plus mechanistic stories for individual neurons, partly read from weights (vocabulary
projections, neuron-to-head weight compositions). Partial and largely qualitative.

## How they judged success
Excess correlation across seeds against a rotated-basis baseline; variance reduction for family labels; consistency of
weight statistics; causal checks by activation fixing and path ablation, compared to random neurons.

## What they found
Only about 1-5% of neurons are universal (GPT-2 medium 1.23%, Pythia-160M 1.26%, GPT-2 small 4.16%). Universal neurons have
large weight norms, large negative input bias, sparse activation, and high pre-activation skew and kurtosis; ordinary
neurons look Gaussian. Families: unigram (early layers), alphabet, previous-token, position, syntax and semantic neurons.
From weights, late layers contain prediction, suppression and partition neurons, with suppression more common at the
very end. An entropy neuron (GPT-2 medium L23.945) has almost no direct logit effect but raises the final layer-norm
scale and thus entropy; an anti-entropy partner has output-weight cosine -0.886. Attention-deactivation neurons switch
heads off via BOS attention (e.g. L4.3594 on head L5.H0). Activation frequency relates strongly to the cosine between a
neuron's input and output weights.

## Limits and open problems they name
Small models only; universality tested only across seeds in one family; tokeniser differences block cross-family
comparison; heavy reliance on manual or algorithmic labelling; neuron basis may miss structure that overcomplete
dictionaries would capture. They suggest repeating with SAEs and using LLM auto-explanations.

## What we take from it
Two direct points for reading weights. First, a set of weight-only signatures (vocabulary projection skew/kurtosis,
w_in/w_out cosine, bias, norm, neuron-to-head QK composition) predict a neuron's role without data; these are features a
weight-reading model could compute. Second, most neurons are not canonical across seeds, so a white-box model built on
the neuron basis will mostly describe seed-specific units; the rotated-basis baseline is a good control for any claim
that our units are privileged. Entropy neurons are a warning that a unit with no direct logit effect can matter through
normalisation, so a predictive model must include layer norm.

## Tags
unit: neuron | weights
form: description | dictionary
method: weight-analysis | probing | ablation
eval: ablation | patching
goal: understanding | science
