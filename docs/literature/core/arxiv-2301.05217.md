# Progress Measures for Grokking via Mechanistic Interpretability

- **Key:** arxiv-2301.05217
- **Authors / organisation:** Neel Nanda, Lawrence Chan, Tom Lieberum, Jess Smith, Jacob Steinhardt
- **Date:** 2023-01
- **Link:** https://arxiv.org/abs/2301.05217
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Neural networks sometimes show sudden qualitative changes during training (emergence, grokking). The authors wanted to know whether a full mechanistic understanding of a trained network could yield continuous "progress measures" that reveal the hidden, gradual change underneath an apparently sudden jump. They use grokking on modular addition, where a model first memorises and much later generalises, as a case study. The larger aim is to show that reverse-engineering a network completely is possible and useful for understanding training dynamics.

## What they studied
A one-layer ReLU transformer (d_model 128, 4 attention heads, 512 MLP neurons) trained on a + b mod 113 using 30% of all input pairs, AdamW with learning rate 0.001 and weight decay 1, for 40,000 epochs. Units: embedding and unembedding weights, attention heads, MLP neurons, and their representation in the Fourier basis over inputs; also the whole model across training checkpoints.

## How they did it
They reverse-engineered the trained model, finding that it implements a "Fourier multiplication" algorithm: embeddings map each input to sines and cosines at a few key frequencies (14, 35, 41, 42, 52), attention and MLP compute cos and sin of w_k(a+b) via trigonometric identities, and the unembedding computes cos(w_k(a+b−c)) for each candidate c, which interfere constructively at the correct answer. They supported this with several lines of evidence: periodicity and Fourier sparsity of embeddings, attention, neuron activations and logits; analysis of the neuron-to-logit weight map; fits of individual neurons to low-degree polynomials of one frequency; and ablations in Fourier space. They then defined progress measures based on the mechanism and tracked them over training checkpoints: restricted loss (keep only the key-frequency components), excluded loss (remove only them, on training data), Gini coefficient of the Fourier-basis weights, and total weight norm. They also varied weight decay, dataset fraction and regulariser type, and checked other small algorithmic tasks.

## What counts as an explanation here
A complete, mathematically specified algorithm the network implements, read largely from weights expressed in a well-chosen basis (Fourier), and verified by interventions. It is predictive: it says exactly which components matter and what happens if they are removed, and the derived progress measures track training.

## How they judged success
Fraction of variance explained (logits by five frequency terms; neurons by single-frequency quadratic fits); the rank of the neuron-to-logit map; ablation of key frequencies versus all other frequencies (loss, accuracy); restricted and excluded loss curves versus train and test loss over training; Gini coefficient and weight norm trends; sensitivity to weight decay and data fraction.

## What they found
The neuron-to-logit map is approximately rank 10; five frequencies explain about 95% of logit variance; 433 of 512 neurons are fit at over 85% variance by a single-frequency quadratic. Removing the key frequencies brings performance to chance, while removing the remaining roughly 95% of frequencies slightly improves loss. Training splits into three phases: memorisation (0 to 1.4k epochs), circuit formation (1.4k to 9.4k, where excluded loss rises and restricted loss falls while train and test loss look flat), and cleanup (9.4k to 14k, when test loss drops, weight norm falls and Gini rises as weight decay removes memorising components). So the generalising circuit forms gradually well before the visible jump. Without weight decay or another regulariser grokking does not occur; with 60% or more of the data the model generalises immediately; dropout can induce grokking but L1 did not.

## Limits and open problems they name
One small model on one algorithmic task; heavy manual effort; progress measures are task-specific and need the mechanism to be known first, so automated, task-independent methods are needed to scale; no way to predict in advance when the phase transition happens.

## What we take from it
The clearest existence proof that a complete, weight-level, predictive account of a trained network is possible, and of how it was obtained: find the basis in which the weights become sparse (here Fourier), then read the algorithm there. Reusable measures: "restricted" and "excluded" loss (keep only / remove only the components your explanation names) are a clean, general test of whether an explanation is sufficient and necessary. Variance explained by the mechanistic model and ablation of the residual components are good templates for scoring a white-box reconstruction. Warning: the manual cost was high even for a 1-layer toy, which argues for automating basis discovery.

## Tags
unit: weights | neuron | head | whole-model
form: program | description
method: weight-analysis | ablation | decomposition
eval: ablation | prediction/simulation | faithfulness
goal: understanding | science
