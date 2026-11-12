# Compact Proofs of Model Performance via Mechanistic Interpretability

- **Key:** arxiv-2406.11779
- **Authors / organisation:** Jason Gross, Rajashree Agrawal, Thomas Kwa, Euan Ong, Chun Hei Yip, Alex Gibson, Soufiane Noubir, Lawrence Chan; funded by the Alignment Research Center, with MARS (Cambridge AI Safety Hub), Constellation and FAR Labs support (affiliations not listed on the page read)
- **Date:** 2024-06
- **Link:** https://arxiv.org/abs/2406.11779
- **Kind:** paper
- **Read from:** full text (HTML, first ~100k of ~226k characters; main body, appendices only partly)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors want a way to turn mechanistic understanding into something checkable: a formal proof, computed from a
model's weights, that its accuracy on a task is at least some bound. Their thesis is that real understanding of a
model's algorithm should let you write a proof that is both short (cheap to verify) and tight (bound close to true
accuracy), while black-box verification must enumerate inputs. If that holds, proof length and tightness become a
quantitative measure of how good an interpretation is. The larger goal is safety-relevant global guarantees about
model behaviour, rather than local robustness certificates.

## What they studied
One-layer, one-head, attention-only transformers (no biases, no MLP, no layernorm, learned positional embeddings),
d_model 32, vocabulary 64, trained on Max-of-K (output the largest of K=4 tokens). 151 seeds were trained (mean
accuracy 0.9992 +/- 0.0015); extra models for K = 5, 10, 20 and vocabulary 128 were used as checks. Unit: weights,
decomposed into QK circuit, OV circuit and direct path.

## How they did it
First they interpret the model: it attends more to larger tokens and copies what it attends to; position effects are
negligible and the QK product (EQKE) is close to rank 1. They then write a family of verifier programs that take the
weights and output a certified accuracy lower bound. The brute-force baseline runs the model on every one of the
64^4 inputs. The "cubic" proof uses the path decomposition and a convexity argument so that only sequences with few
distinct tokens need checking, pessimising over order. "Sub-cubic" proofs avoid even that by bounding over groups of
small tokens, replacing matrices with low-rank SVD approximations plus a worst-case bound on the leftover, and tricks
(mean+diff, max row-diff) for bounding error terms without full matrix products. In total 102 proof strategies are
compared. Proof length is measured as asymptotic cost and as estimated FLOPs (instrumenting the code), and each
proof's bound is compared with the true accuracy.

## What counts as an explanation here
A proof: a program over the weights whose correctness argument encodes which structure (paths, rank-1 attention,
monotonic token preference) the model uses. An explanation is good if it compresses the verification (shorter proof)
without loosening the guarantee. It is meant to be a complete account of worst-case performance, and it yields a
certified prediction (a lower bound on accuracy) without running the model on the full input space.

## How they judged success
Two axes: proof length (asymptotic complexity, estimated FLOPs) and tightness (certified bound divided by true
accuracy). A third proxy, "unexplained dimensionality" (log-size of the function space the proof leaves unexplained),
stands for how much mechanistic understanding the proof uses. Baselines: brute force (exact but expensive) and a null
proof (vacuous). Results are reported as means over 151 models, with trend fits of bound against understanding.

## What they found
Brute force gives the exact bound at about 2^47 FLOPs; the cubic proof certifies about 0.95 of accuracy at about 2^25
FLOPs; sub-cubic proofs get about 0.70 at about 2^21; a quadratic-QK variant only about 0.32. Some SVD-only variants
collapse to near-zero bounds. At K=20 brute force would need around 2^148 FLOPs, while the cubic proof certifies
88.4% in under two minutes. More understanding buys shorter proofs, but the length/tightness trade-off is weak
(R^2 roughly 0.2 to 0.4), and there is a Simpson's-paradox pattern: within a proof class more understanding gives a
tighter bound, across classes it does not. Closeness of EQKE to true rank 1 predicts tighter bounds within a class.

## Limits and open problems they name
Only a toy one-layer attention-only model on an algorithmic task. The OV circuit could not be compressed without
multiplying matrices out. The proofs gave no new insight about the model. The central obstacle is compounding
structureless noise: small, unstructured residual errors must be bounded worst-case, and these bounds add up across
components until the guarantee becomes vacuous. Floating-point versus real arithmetic is left open. They suggest
typical-case (heuristic) rather than worst-case arguments as a way forward.

## What we take from it
A measure: an explanation read from weights can be scored by how cheaply it lets you predict performance and how
close the prediction is, against brute-force evaluation as the reference. That is a ready-made "compression versus
accuracy" frame for a predictive white-box model. A warning: residual error from low-rank or simplified weight
readings is the bottleneck; we must model or bound the unexplained part, not drop it. A method: decompose into QK/OV/
direct paths and use SVD with explicit error terms.

## Tags
unit: weights | circuit
form: program | other (formal proof)
method: weight-analysis | decomposition
eval: prediction/simulation | completeness | faithfulness
goal: understanding | safety/auditing | evaluation-of-methods
