# Converting MLPs into Polynomials in Closed Form

- **Key:** arxiv-2502.01032
- **Authors / organisation:** Nora Belrose, Alice Rigg; EleutherAI
- **Date:** 2025-02
- **Link:** https://arxiv.org/abs/2502.01032
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Polynomial models (linear, quadratic) can be read off their coefficients, but ordinary MLPs cannot. The authors derive
the least-squares-best linear and quadratic polynomial approximations of an MLP or GLU directly from its weights, in
closed form, given a simple model of the input distribution. This gives a weights-to-interpretable-surrogate map, and
lets them watch how much of the network's behaviour is low-order across training.

## What they studied
A single-hidden-layer ReLU MLP trained on MNIST (width not given in what we read), checkpointed at log-spaced steps.
Theory covers ReLU and GELU MLPs and GLUs including bilinear layers. Unit: whole layer / weights.

## How they did it
Model the inputs as a Gaussian (or a Gaussian mixture, e.g. one component per class), the maximum-entropy choice given
mean and covariance. For the linear approximant, the optimal coefficients reduce to ordinary least squares whose
expectations are computed analytically (Stein's lemma, closed-form Gaussian moments of ReLU/GELU). For quadratic and
higher degrees, a change of variables turns quadratic features into a linear problem, and a general theorem reduces the
needed expectations to one-dimensional integrals. Mixtures are handled by the law of total covariance. On MNIST the
exact mixture quadratic was intractable, so the quadratic was initialised from the N(0,1) solution and fine-tuned by
SGD. They then track fit across training, eigendecompose quadratic coefficients for feature visualisation, and attack
the MLP by projecting inputs off the top singular directions of the linear coefficients.

## What counts as an explanation here
A closed-form polynomial surrogate of the network (linear plus quadratic coefficients), interpreted through its
coefficients and eigenvectors. Partial: it explains as much variance as a low-degree polynomial can, and it predicts
outputs directly.

## How they judged success
Fraction of variance unexplained (FVU) / R^2 of the approximants on network outputs; KL divergence between network and
approximant; test accuracy of both network and approximants under SVD-based input ablations (whether they drop
together).

## What they found
Quadratic approximants explain over 95% of output variance even at the end of training. Between about 500 and 4K steps
the linear approximant's FVU and KL rise sharply while the quadratic's stays flat, read as a shift from linear to
quadratic feature use (consistent with a distributional simplicity bias). Early in training both FVUs fall (not seen in
KL). Most interpretable features appear around steps 2^12 to 2^14, before overfitting. Ablating the top four
directions of the linear coefficients drops MLP accuracy below 50%, all ten brings it to near chance while images stay
recognisable, and accuracy falls in lockstep for the network and both approximants.

## Limitations and open problems they name
Depends on the Gaussian / mixture input assumption (suggested fix: use the analytic solution as an initialisation, then
fine-tune on real data). Degree-n approximants need about d*k^n parameters, so degree 2 is the practical ceiling. If
the best quadratic fit is poor, little is explained. Only a single MNIST MLP tested; transformers and tensor
decompositions for overcomplete bases left to future work.

## What we take from it
A direct weights-to-surrogate method with a principled fit metric: FVU / KL of a closed-form polynomial tells you how
much of a module's behaviour a simple, readable model captures, without any training data beyond moment estimates.
The lockstep-accuracy-under-ablation test is a nice check that a surrogate shares the network's causal features, which is
our "prediction under intervention" criterion. Warning: tested only on a tiny MNIST MLP.

## Tags
unit: layer | weights
form: replacement-model
method: weight-analysis | other
eval: prediction/simulation | faithfulness | ablation
goal: understanding | science
