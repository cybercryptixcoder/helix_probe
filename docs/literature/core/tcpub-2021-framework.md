# A Mathematical Framework for Transformer Circuits

- **Key:** tcpub-2021-framework
- **Authors / organisation:** Nelson Elhage, Neel Nanda, Catherine Olsson, et al.; Anthropic
- **Date:** 2021-12
- **Link:** https://transformer-circuits.pub/2021/framework/index.html
- **Kind:** paper
- **Read from:** full text (main body and appendices, via page fetch in two parts)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors want to reverse-engineer transformers the way one decompiles a binary into readable source, as a basis
for spotting current and future safety problems. Earlier circuits work covered vision CNNs, not transformers. Their
strategy is to start with the simplest transformers (zero, one and two layers, attention only), work out their
computation exactly from the weights, and find algorithmic motifs that might carry over to large models. The paper
mainly supplies a mathematical vocabulary for doing this.

## What they studied
Small decoder-only, attention-only transformers with 0, 1 and 2 layers (no MLPs; biases and layer norm folded in),
about 50k-token vocabulary, 2048-token context, typically 12 heads of dimension 64 (one variant 32 heads of
dimension 128). Units of analysis: the residual stream, individual attention heads split into QK and OV circuits,
and end-to-end paths through the weights.

## How they did it
They rewrite the transformer algebraically. The residual stream is treated as a shared linear channel that every
layer reads from and writes into, so products of weight matrices across layers ("virtual weights") say how much a
later component reads what an earlier one wrote. Multi-head attention is shown to equal a sum of independent heads.
Each head is factored into a QK circuit (W_E^T W_QK W_E, which tokens attend to which) and an OV circuit
(W_U W_OV W_E, what an attended token does to output logits). Freezing attention patterns makes the model linear
in tokens, and multiplying out the layers gives a "path expansion": a sum of direct, single-head and multi-head
(virtual head) terms, each inspectable as a token-by-token matrix. They summarise OV matrices by their eigenvalues
(positive real eigenvalues as a signature of copying, compared against random Ginibre matrices) and measure Q-, K-
and V-composition between heads with normalised Frobenius-norm scores minus a random-matrix baseline. To test
whether higher-order paths matter, they freeze attention and replace head outputs with saved values, isolating the
marginal effect of paths with a given number of V-composition steps. Behaviour is checked on natural text and on
repeated random token sequences. Matrices are kept in factored low-rank form so eigen/SVD analysis runs on the
small head dimension.

## What counts as an explanation here
A closed-form, weight-derived description: the model is literally rewritten as a sum of interpretable paths, each a
small table (bigram table, skip-trigram tables, composed induction circuit). For attention-only models this is
close to a complete, exact account computed from weights alone and it predicts logit effects directly. For MLPs no
such account was found.

## How they judged success
Mostly qualitative agreement between weight-derived tables and observed behaviour (attention patterns on text,
value-weighted attention, behaviour on random repeated tokens), eigenvalue statistics against a random baseline,
composition scores against a random baseline, and ablation of higher-order path terms. No benchmark or aggregate
faithfulness metric.

## What they found
A zero-layer model is just a bigram table (W_U W_E). A one-layer attention-only model is a bigram model plus an
ensemble of "skip-trigram" rules of the form A ... B -> C, mostly copying; some heads are positional; factorisation
causes predictable "bugs" (a head that boosts both "keep ... in mind" and "keep ... at bay" also boosts
"keep ... in bay"). Eigenvalue analysis flagged 10 of 12 heads as copying, matching manual inspection. Two-layer
models use K-composition with a previous-token head to build induction heads ([a][b] ... [a] -> [b]), which work on
random repeated sequences. In the two-layer model, only K-composition was significant and V-composition (virtual
heads) had a small marginal effect. A post-publication bug fix showed somewhat more composition than first reported.

## Limitations and open problems they name
MLP layers (about two-thirds of parameters) remained unexplained; superposition in bottleneck activations (residual
stream, keys, values) blocks direct reading; only tiny models; "copying" lacks a formal definition and positive
eigenvalues are an imperfect proxy; layer norm turns paths into rescaled terms that are hard to compare; examples
can be cherry-picked; importance of virtual heads at scale unknown.

## What we take from it
The clearest precedent for our goal: an exact, predictive white-box account read from weights alone, for a
restricted architecture. Reusable tools: path expansion, QK/OV factorisation, virtual weights, composition scores
with random-matrix baselines, eigenvalue summaries, and the privileged-vs-non-privileged and bottleneck
classification of activations. Warning: the method breaks at nonlinear MLPs and superposed bottlenecks, which is
exactly where a weight-reading approach needs new ideas. Random-repeated-token tests are a cheap behavioural control.

## Tags
unit: head, circuit, weights
form: program, graph
method: weight-analysis, decomposition, ablation
eval: ablation, prediction/simulation
goal: understanding, science
