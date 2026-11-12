# Predicting Neural Network Accuracy from Weights

- **Key:** arxiv-2002.11448
- **Authors / organisation:** Thomas Unterthiner, Daniel Keysers, Sylvain Gelly, Olivier Bousquet, Ilya Tolstikhin; Google Research (Brain Team)
- **Date:** 2020-02
- **Link:** https://arxiv.org/abs/2002.11448
- **Kind:** paper
- **Read from:** full text (HTML version, method, results and appendix summaries)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors ask whether a trained network's test accuracy can be read off its weights alone, without feeding it any
data. If so, weights carry recoverable information about how well training went, which could help understand
generalization and could be used practically (e.g. killing doomed training runs early). They also want to know
whether such a weights-to-accuracy predictor transfers to new datasets and architectures. It is an early,
foundational step in what later became "weight-space learning": treating trained networks as data points.

## What they studied
The "Small CNN Zoo": about 30k small CNNs per dataset (3 conv layers of 16 filters, global average pooling, one dense
layer; 4,970 weights) trained on MNIST, Fashion-MNIST, grayscale CIFAR-10 and grayscale SVHN, with randomly sampled
optimizer, learning rate, L2, dropout, initializer, activation (ReLU/tanh) and training-data fraction. Unit of
analysis: the whole weight vector, single layers, and summary statistics of weights. Transfer tests on ResNet-32
(DEMOGEN set) and on MLPs.

## How they did it
They trained the zoo (one seed per configuration, 86 epochs, no augmentation or batch norm) and recorded test
accuracy. From each network they built several input representations: the flattened weights, single layers, seven
statistics (mean, variance, five percentiles) of the whole vector, the same statistics per layer (56 features), per
layer l1/l2 norms, and, for comparison, the training hyperparameters themselves. They fit three regressors (logit-linear,
LightGBM gradient boosting, a fully connected network) with MSE loss, tuning by 3-fold cross-validation on a
15k-model split and evaluating once on held-out models. They then probed the trained predictor's sensitivity to weight
rescaling and neuron permutations, inspected which statistics mattered, and tested cross-dataset and
cross-architecture transfer by ranking networks from another zoo.

## What counts as an explanation here
Not a mechanistic explanation: a black-box predictor mapping weights (or weight statistics) to a scalar property
(test accuracy). The "understanding" is that certain coarse weight statistics are sufficient to predict outcome;
some hand-noted correlates (bias ranges in first and last layers) are offered, but the authors found no simple
interpretable rules. It does predict, but only one scalar.

## How they judged success
R-squared versus a constant predictor (main metric), mean absolute deviation and MSE, and Kendall's tau for
ranking networks in transfer experiments. Baselines: predicting from hyperparameters alone; comparison across
regressors and input representations. Held-out test split used once.

## What they found
- Per-layer weight statistics with gradient boosting gave R-squared of about 0.98 to 0.99 on all four zoos (e.g.
  0.984 on CIFAR10-GS); the full weight vector was slightly worse (0.970 to 0.989); hyperparameters alone gave
  only 0.918 to 0.935, so weights carry more than the training recipe.
- The final dense layer alone was nearly as good as all weights; conv layers alone were clearly worse.
- The predictor was robust to conv-layer permutations and upscaling, but not to permutations in the final dense
  layer or downscaling (symmetries were not built in).
- Cross-dataset ranking: Kendall's tau 0.60 to 0.80 off-diagonal versus 0.85 to 0.93 in-distribution.
- Transfer to ResNet-32 was weak (tau 0.28 to 0.59 for test accuracy), and correlated more with train accuracy,
  suggesting a shortcut.

## Limits and open problems they name
Tiny, grayscale, far-from-SOTA CNNs; no overfitting in the zoo, so little to say about generalization gaps; one
seed per configuration; only off-the-shelf regressors; no interpretable rules found; possible reliance on
train-accuracy as a shortcut; models not trained to convergence.

## What we take from it
- **Warning/baseline:** cheap per-layer weight statistics are a very strong baseline for predicting scalar model
  properties. Any weights-reading method we propose must beat "statistics + gradient boosting" (later called
  STATNN), or it is not showing anything beyond coarse statistics.
- **Measure:** R-squared and Kendall's tau over held-out models; split by model, not by checkpoint.
- **Framing gap:** predicting one scalar is far from predicting behaviour on inputs; our goal (per-input
  prediction) is a much harder target that this line of work does not address.
- **Symmetry lesson:** predictors not built for permutation symmetry are fragile to it.

## Tags
unit: weights | whole-model
form: probe
method: weight-analysis
eval: prediction/simulation | benchmark
goal: science | evaluation-of-methods
