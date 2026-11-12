# LEACE: Perfect Linear Concept Erasure in Closed Form

- **Key:** arxiv-2306.03819
- **Authors / organisation:** Nora Belrose, David Schneider-Joseph, Shauli Ravfogel, Ryan Cotterell, Edward Raff, Stella Biderman; EleutherAI, Bar-Ilan University, ETH Zurich, Booz Allen Hamilton
- **Date:** 2023-06
- **Link:** https://arxiv.org/abs/2306.03819
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Concept erasure removes a specified concept (e.g. gender, part of speech) from a representation so that no classifier of a given family can recover it. This serves fairness (stop a downstream model using gender) and interpretability (remove a concept and see what the model can no longer do, a causal test of concept use). Earlier linear erasure methods (INLP, RLACE) were iterative, did not guarantee erasure, or damaged the representation more than necessary. The authors want a provably complete linear erasure that changes the representation as little as possible, and a way to apply it inside every layer of an LM.

## What they studied
BERT-base-uncased ([CLS] embeddings on Bias in Bios for gender; token embeddings on English Universal Dependencies with 18 coarse POS tags). Autoregressive LMs: Pythia 160M, 1.4B, 6.9B, 12B and LLaMA 7B, 13B, 30B, on Pile validation (Pythia) and a RedPajama replication (LLaMA), 2^22 tokens to fit and 2^22 to evaluate, POS tags from spaCy. Unit: the residual-stream representation (input to each block) and linear directions within it.

## How they did it
They define linear guardedness: X guards Z if no linear predictor (under any convex loss) beats a constant predictor. They prove this is equivalent to all class-conditional means of X equalling the overall mean, i.e. zero cross-covariance between X and Z, and that an affine map erases Z exactly when the columns of the cross-covariance lie in its null space. They then solve for the affine map that guarantees this while minimizing expected squared change (for any positive semidefinite inner product at once): de-mean, whiten, project out the span of the whitened cross-covariance, unwhiten. The result is an oblique rather than orthogonal projection, computed in closed form from covariance statistics. "Concept scrubbing" applies LEACE at every layer sequentially, fitting each layer's eraser on activations already scrubbed upstream. Experiments: erase gender from BERT [CLS] and measure gender-probe accuracy and edit size; measure downstream fairness on Bias in Bios; amnesic probing of POS in BERT; scrub POS from every layer of Pythia and LLaMA and measure the perplexity increase, against random-erasure and SAL controls.

## What counts as an explanation here
Not an explanation of a mechanism but a tool for causal testing: a concept is declared to be "used" by the model if erasing exactly its linearly available information, with minimal collateral damage, degrades behaviour. The explanation is a subspace (rank equals number of classes minus one) plus the counterfactual behaviour once it is removed.

## How they judged success
Probe accuracy on the erased concept vs chance; size of the edit (mean squared change); runtime vs RLACE; for fairness, profession accuracy, TPR-GAP and the correlation between per-profession TPR gap and proportion of women; for amnesic probing, MLM accuracy/loss and number of dimensions removed; for LMs, perplexity in bits per UTF-8 byte against no erasure, random erasure of equal rank, SAL (orthogonal projection) and a unigram baseline. Baselines: INLP, RLACE, SAL, random projection; Mean Projection and Fair PCA discussed.

## What they found
LEACE alone reaches chance-level gender accuracy with a small edit; RLACE gets close, INLP does not; LEACE is about two orders of magnitude faster than RLACE. On Bias in Bios, profession accuracy goes 79.3% -> 77.3% while TPR-GAP falls 0.198 -> 0.084 and the gap-vs-women correlation 0.867 -> 0.392. For POS in BERT, INLP needed 20 iterations, removed 360 dimensions and still left accuracy above majority baseline; LEACE removes 17. Scrubbing POS from LMs raises perplexity a lot while random erasure does nearly nothing: e.g. LLaMA 7B 0.69 -> 1.73 (SAL 3.24), Pythia 12B 0.62 -> 3.20 (SAL 4.69), unigram baselines 2.90 (LLaMA) and 2.66 (Pythia). SAL's larger damage would have overstated how much the model relies on POS.

## Limits and open problems they name
Only linear erasure; nonlinear erasure is conjectured intractable without knowing the data-generating process. Concept scrubbing needs testing on narrower concepts than POS and with behavioural checks. Training could route around the constraint by encoding the concept nonlinearly. Norm divergence at some layers needed a heuristic regularizer. Caching hidden states for sequential fitting costs up to 500GB, or quadratic compute in depth if recomputed.

## What we take from it
A measure, not a model: when we claim our white-box model says a concept is represented in a subspace and used downstream, LEACE gives the principled, minimal-damage counterfactual to test it, with random-subspace erasure of equal rank as the control. The SAL comparison is a warning that a crude ablation inflates estimated causal importance, so our predictions under intervention should be scored against minimal interventions. The closed-form, covariance-only construction is cheap enough to run at every layer. Also a caution that linear unavailability does not mean the information is gone.

## Tags
unit: direction | layer
form: direction
method: ablation | probing | other
eval: ablation | downstream-task | benchmark
goal: control/editing | evaluation-of-methods | science
