# Inducing Causal Structure for Interpretable Neural Networks

- **Key:** arxiv-2112.00826
- **Authors / organisation:** Atticus Geiger, Zhengxuan Wu, Hanson Lu, Josh Rozner, Elisa Kreiss, Thomas Icard, Noah D. Goodman, Christopher Potts; Stanford University
- **Date:** 2021-12 (ICML 2022)
- **Link:** https://arxiv.org/abs/2112.00826
- **Kind:** paper
- **Read from:** full text (PDF v2)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Rather than discover a network's causal structure after training, the authors want to impose a known high-level
causal model (a program or Bayesian network) on a network during training, so that the network provably implements
that structure. This should both improve systematic generalisation and give interpretability by construction. It is
a step toward causal abstraction as the standard for when a high-level algorithm faithfully describes a network.

## What they studied
Three tasks: MNIST-PVR (pointer-value retrieval over four MNIST quadrants) with a ResNet18; ReaSCAN grounded
navigation with the original CNN-LSTM baseline; and MQNLI (multiply quantified NLI) with fine-tuned BERT-base. Unit:
chosen sets of neurons (quadrant regions of a pooling layer, chunks of LSTM encodings, token positions at a BERT
layer) aligned to causal-model variables.

## How they did it
Pick a causal model and an alignment from its intermediate variables to groups of neurons. For a base input and a
source input, run an interchange intervention: copy the aligned neurons' values from the source run into the base run.
The causal model says what the output should be under the matching intervention; the IIT loss trains the network's
intervened output toward that counterfactual label, with gradients through both runs, alongside the normal task loss.
In MNIST-PVR the four quadrant variables share a type, so swaps across quadrants are allowed ("typed" IIT). ReaSCAN
splits a 75-d command encoding into size/colour/shape chunks and a 100-d decoder state into row/column chunks. MQNLI
aligns one intermediate variable to positions above the verb at layers 0 to 10. Baselines: standard training,
multi-task training (linear probes predicting intermediate variables from the aligned neurons), and data augmentation
by recombining input parts. Evaluation uses held-out systematic generalisation splits.

## What counts as an explanation here
A causal abstraction: a high-level causal model plus an alignment of its variables to neurons, such that intervening
on the neurons does what intervening on the variable does. Zero IIT loss guarantees the causal model abstracts the
network (sufficient, not necessary). It is predictive of counterfactual behaviour under interventions.

## How they judged success
Task accuracy (exact match for ReaSCAN) on systematic generalisation splits, and interchange intervention accuracy
(IIA): the share of base-source pairs where the intervened network output matches the causal model's counterfactual
output. Ablations of typing and of which layer is aligned.

## What they found
MNIST-PVR test: standard and multi-task training get 0% behavioural accuracy and about 20% IIA; augmentation about
91% / 92%; IIT about 94% / 95%; IIT plus multi-task about 96% / 97%; removing typing collapses to near 0%. ReaSCAN:
IIT plus multi-task gives the best exact match on every split (e.g. about 75% vs 42% standard on novel size, 26% vs
6% on novel length), though novel direction stays hard. MQNLI: IIT reaches near-perfect accuracy and IIA when aligned
at layer 6 or later; data augmentation reaches perfect accuracy but very low IIA, i.e. right answers without the
intended mechanism.

## Limits and open problems they name
Results depend on the chosen causal model, alignment and input pairing; the alignment is not unique. Perfect IIA is
rare, so the causal model is often only approximate. Zero loss is sufficient but not necessary for abstraction.
Aligning near the output head failed for MNIST-PVR. Tasks are simplified versions of the benchmarks.

## What we take from it
A measure: IIA is the standard test for whether a claimed high-level algorithm predicts a network under
intervention, and we should report it for any white-box model we propose. A warning: behavioural accuracy alone (the
augmentation result) does not show the network uses the intended mechanism. A possible tool: IIT-trained networks give
models with a known, imposed algorithm, useful as ground-truth targets for testing a weights-to-model reader.

## Tags
unit: neuron | direction
form: causal-abstraction
method: training-interpretable | patching
eval: patching | downstream-task | faithfulness
goal: understanding | evaluation-of-methods
