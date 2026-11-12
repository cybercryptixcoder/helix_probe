# Notes: programs as explanations (batch 13a)

**What an explanation is.** All four papers treat an explanation as an executable program that reproduces the
network's input-output map: RASP (arxiv-2106.06981) as a hand-written hypothesis, Tracr (arxiv-2301.05062) as the
source of compiled weights, Transformer Programs (arxiv-2306.01128) as an exact decompilation of a constrained
network, and MIPS (arxiv-2402.05110) as code extracted from an unconstrained RNN's weights. Explanations here are
complete and predictive by design, the opposite of partial feature/circuit stories.

**How success is measured.** Mostly behavioural: task accuracy of the program (MIPS demands 100%), accuracy of
models trained at a predicted size, and shrink-the-model tightness tests (RASP). Only Tracr also checks internal
agreement (per-layer cosine similarity), and it shows why that matters: a compressed sort model kept near-perfect
accuracy while changing its encoding (similarity about 0.8). Baselines: standard unconstrained transformers
(Transformer Programs), GPT-4 program synthesis from examples (MIPS), PCA (Tracr compression).

**Recurring methods.** A shared primitive vocabulary (select / aggregate / elementwise, lookup-table MLPs);
discretisation (categorical variables, hard attention, Boolean/integer autoencoders); one subspace per variable;
shrinking the network to its minimal sufficient size; removing weight symmetries before reading (MIPS).

**Open problems.** (1) Learned networks often do not use the "obvious" program even at the right size (RASP).
(2) Exact programs can be huge (Dyck-1: 9,975 lines before pruning). (3) Everything breaks on continuous or noisy
representations and superposition (MIPS failures; Tracr's basis-aligned weights are unrealistically easy).
(4) Optimisation of interpretable-by-construction models is hard and they lag on long inputs. (5) Nothing here
scales past toy tasks or small text classifiers.

**For a predictive white-box model from weights.** MIPS is the nearest template: minimise, canonicalise, discretise,
symbolically regress, then demand exact output agreement. Tracr supplies a ground-truth testbed (compile a program,
optionally compress to induce superposition, check whether our reader recovers it). RASP/Transformer-Program Python
is a ready target format. We should score both output agreement and internal-state agreement, since behaviour
matching alone can hide a different mechanism (Tracr), and report program size alongside accuracy.
