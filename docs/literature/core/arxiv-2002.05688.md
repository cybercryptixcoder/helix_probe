# Classifying the Classifier: Dissecting the Weight Space of Neural Networks

- **Key:** arxiv-2002.05688
- **Authors / organisation:** Gabriel Eilertsen, Daniel Jönsson, Timo Ropinski, Jonas Unger, Anders Ynnerman; Linköping University and Ulm University
- **Date:** 2020-02
- **Link:** https://arxiv.org/abs/2002.05688
- **Kind:** paper
- **Read from:** full text (PDF, via a summarising fetch; exact accuracy values are only in figures and were not extracted)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors ask how much of a network's training history is recoverable from its trained weights alone. They treat each trained model as a point in a "neural weight space" and train meta-classifiers to map weights back to the training choices (dataset, optimiser, activation, initialisation, architecture settings). The aim is to quantify how much, where (which layers / weight types) and when (which point in training) these choices leave traces. They frame this as a complementary route to explainable AI, and note privacy consequences: training details may leak from released weights.

## What they studied
Small vanilla image CNNs (6 to 10 layers, 3 max-pool layers, batch norm, dropout after FC layers; roughly 20K to 390K weights). Training sets: MNIST, CIFAR-10, SVHN, STL-10, Fashion-MNIST. The Neural Weight Space (NWS) dataset: about 16K trained CNNs and about 320K weight snapshots (20 per run), split into a 13K random-architecture part and a 3K fixed-architecture part (92,868 weights each). Unit of analysis: weights (whole model, and random contiguous slices).

## How they did it
They sampled training configurations from a grid: learning rate, batch size (32 to 256), augmentation on/off, optimiser (Adam, RMSProp, momentum SGD), activation (ReLU, ELU, sigmoid, tanh), initialisation (constant, random normal, Glorot uniform/normal), filter size, number and width of conv and FC layers. Each configuration was trained to early stopping, saving snapshots. Models that failed to learn were removed. A "global" meta-classifier (1D CNN over the flattened weights of fixed-architecture models) predicts each hyperparameter. A "local" meta-classifier sees only a random run of about 5,000 consecutive weights (about 5% of a model), drawn from all weights, conv-only, or FC-only, which lets them map where information sits. Baselines were linear and RBF SVMs on summary statistics (mean, variance, skewness, percentiles) of weights and gradients, including layer-wise variants (480 features). They also regressed test accuracy on hyperparameters with a linear model.

## What counts as an explanation here
A map of where in the weights (layer type, weight type, training time) each training property is decodable, read through probes (meta-classifiers). It is a partial, correlational account of what weights encode about their origin; it does not predict network behaviour on inputs.

## How they judged success
Classification accuracy of the meta-classifier per hyperparameter, compared with chance and with SVMs on weight statistics; "performance maps" of local-classifier accuracy across weight positions and training snapshots; accuracy as a function of the number of weights given.

## What they found
The global deep meta-classifier predicts most properties with fairly high accuracy; batch size is the hard exception (reported accuracies span roughly 20% to 90% depending on property and region, in figures). Initialisation is the most distinguishable property and dominates locally. Dataset identity is clearest in conv layers; optimiser is concentrated in conv biases; activation shows up in batch-norm running statistics of FC layers. Weights near input and output move away from initialisation faster than middle layers. Filter size is partly readable from FC weights. Accuracy grows roughly logarithmically with the number of weights given. Linear SVMs on statistics do well globally but degrade on local slices.

## Limits and open problems they name
Only small vanilla CNNs. The flat vector representation ignores permutation symmetry and the 2D structure of filters. The meta-classifier design was not tuned much. Future work: larger architectures, meta-classifiers used during training, learned initialisation.

## What we take from it
A baseline and a warning. The "DMC" (1D CNN on flat weights) and weight-statistics SVMs became standard baselines in later weight-space work (see arxiv-2110.15288, arxiv-2312.04501), so we should report against them. The finding that initialisation and optimiser leave strong signatures means a weight reader can succeed by detecting training artefacts rather than function: our evaluations need controls that vary seed and training recipe, or the reader may predict "how it was trained", not "what it computes". The localisation method (classifier on random contiguous slices, mapped across layers and checkpoints) is a cheap way to ask where a property lives in weights.

## Tags
unit: weights
form: probe
method: weight-analysis, probing
eval: downstream-task, benchmark
goal: science, understanding
