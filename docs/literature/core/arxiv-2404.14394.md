# A Multimodal Automated Interpretability Agent (MAIA)

- **Key:** arxiv-2404.14394
- **Authors / organisation:** Tamar Rott Shaham, Sarah Schwettmann, Franklin Wang, Achyuta Rajaram, Evan Hernandez, Jacob Andreas, Antonio Torralba; MIT CSAIL
- **Date:** 2024-04
- **Link:** https://arxiv.org/abs/2404.14394
- **Kind:** paper
- **Read from:** abstract and sections (method, evaluation, applications, limitations; exact per-model bar-chart values not available in text)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Manual interpretability (looking at exemplars, designing probe inputs, testing hypotheses) does not scale to the
number of units and behaviours in modern networks. One-shot automated labelling (describe the top exemplars)
cannot test hypotheses. The authors want an agent that does what a human interpretability researcher does: form a
hypothesis about a component, design experiments, run them, and revise. The larger goal is scalable, iterative,
experiment-driven explanation of vision models, applied both to describing units and to practical audits
(spurious features, biases).

## What they studied
Vision models: ResNet-152 (conv.1, res.1 to res.4), DINO ViT (MLP layers 1 to 11), CLIP ResNet (res.1 to res.4),
and ResNet-18 trained on the Spawrious spurious-correlation dataset. Unit of analysis is mostly individual neurons
(100 randomly sampled per model), plus 85 synthetic neurons with known selectivity, plus whole-classifier behaviour
for bias finding.

## How they did it
MAIA is GPT-4V given a Python API. A System class wraps the target unit so the agent can feed it any image and get
back activations and activation-highlighted masks. A Tools class offers: top-activating ImageNet exemplars;
text-to-image generation (Stable Diffusion v1.5, or DALL-E 3 in an ablation); image editing (InstructPix2Pix);
description and summarisation by fresh GPT-4V instances with no experiment history (to limit confirmation bias);
and a log. Given a query ("describe this neuron"), MAIA writes programs, runs them, inspects results and iterates
until it produces a label. To evaluate labels on real neurons, which lack ground truth, they built a predictive
protocol: for each candidate label (MAIA, MILAN, human expert), GPT-4 writes 7 prompts meant to activate the
neuron and 7 neutral ones; a GPT-4 selector picks, per label, the prompts it expects to most and least match; DALL-E
3 renders them; the neuron's real activations on positive vs neutral images are compared. Synthetic neurons were
built from Grounded DINO + SAM to respond to text-specified concepts (monosemantic, disjunctive, conditional), so
labels can be checked against truth. Ablations removed exemplars or image generation. For Spawrious, MAIA picked
neurons robust to the spurious background without balanced data, and a logistic regression was fit on them.

## What counts as an explanation here
A short natural-language description of what a unit is selective for, backed by an experiment log. It is partial
(one unit at a time) and predictive in a limited sense: a good label should let one choose inputs that drive the
unit high versus not.

## How they judged success
Predictive evaluation (mean activation on label-derived positive vs neutral generated images; also a
percentile-normalised variant in the appendix); for synthetic neurons, 2AFC judgments by Mechanical Turk workers
comparing two candidate labels against the ground-truth description, with 95% confidence intervals. Baselines:
MILAN (non-interactive exemplar captioning) and human expert labels (on 25% of units). Ablations of tools. For
Spawrious: test accuracy versus the original model, MILAN-based neuron selection, and an L1-tuned selection on
balanced data.

## What they found
MAIA labels beat MILAN on the predictive measure for all three models and were often comparable to human experts.
On synthetic neurons, judges preferred MAIA over MILAN 0.73 of the time and MAIA over humans 0.53 (humans over MILAN
0.83). Removing either exemplars or synthesis hurt; DALL-E 3 beat Stable Diffusion, so tool quality limits the
agent. On Spawrious, a classifier on 22 MAIA-chosen neurons reached 0.837 test accuracy versus 0.731 for the
original model and 0.786 for MILAN selection (0.865 with balanced data and tuned L1). Bias finding was qualitative.

## Limits and open problems they name
Image tools often fail to follow edit instructions; the agent shows confirmation bias and draws conclusions from
small samples; open-source VLMs lag far behind GPT-4V; synthetic neurons only cover simple segmentable concepts;
failing to find something is not evidence it is absent; human oversight remains needed.

## What we take from it
Two reusable pieces. (1) The predictive evaluation protocol: turn an explanation into inputs it says should and
should not activate the unit, then measure the real network. This is exactly the kind of test our white-box model
should pass, and it works without ground truth. (2) Synthetic units with planted, known selectivity as a ground
truth for validating an explainer. Also the design choice of using history-free model instances for describing
results, to reduce confirmation bias. Warning: explanations are per-unit text, not a model of computation, so they
do not compose into prediction of the whole network.

## Tags
unit: neuron
form: description
method: agent
eval: prediction/simulation | human-rating | ablation | downstream-task
goal: understanding | safety/auditing
