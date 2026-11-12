# Sparse mixtures of linear transforms

- **Key:** tcpub-2025-bulk-update-molt
- **Authors / organisation:** Jack Lindsey, Brian Chen, Adam Pearce, Sasha Hydrie, Thomas Conerly (edited by Jeff Wu); Anthropic
- **Date:** 2025-07
- **Link:** https://transformer-circuits.pub/2025/bulk-update/index.html
- **Kind:** blog/research post
- **Read from:** full text (via a page-summarising fetch; plots not inspected directly)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Transcoders, used to build replacement models for attribution graphs, break MLP computation into very many narrow
features. This causes feature splitting and absorption and is inefficient: addition, for example, gets implemented
with lookup-table features for individual digit sums. Matching a large model this way may need impractically many
features. The authors propose replacing each MLP with a sparse set of low-rank linear transforms, so that the
replacement captures computation (maps between representations) rather than only representations. It is a
preliminary update toward a more faithful, more efficient replacement model for circuit tracing.

## What they studied
A middle-layer MLP of Claude 3.5 Haiku for reconstruction/scaling experiments, and the 18-layer model from the
circuit-tracing methods paper for Jacobian-faithfulness analysis. Training data not stated. Unit: low-rank
transforms (and the SAE/transcoder features they connect).

## How they did it
A MOLT predicts the MLP output as a sum over transforms; each transform t has an encoder (vector e_t and bias b_t,
passed through ReLU/JumpReLU) that gates it, and a low-rank map U_t V_t of rank k_t applied to the residual stream.
It is trained to reproduce MLP outputs with a sparsity penalty weighted by the Frobenius norm of each transform. They
swept the allocation of ranks across transforms, then compared MOLTs with parameter-matched transcoders across a
compute range (each 4x FLOPs step = 2x parameters and 2x steps; the largest transcoder has about 10 million
features). They measured reconstruction at fixed sparsity and Jacobian agreement with the true MLP. They inspected
what activates transforms, and integrated MOLTs into attribution graphs by splitting edges into transform-mediated
and attention-mediated parts, annotating edges with the transform that carried them.

## What counts as an explanation here
A replacement model in which a layer's computation is a sparse mixture of interpretable, conditionally active linear
maps; combined with features, it yields attribution graphs whose edges are labelled by which transform carried them
(e.g. a "plus 3" rotation on a digit circle). Partial: it explains per-prompt computation, not a global program.

## How they judged success
MSE versus L0 Pareto frontiers against parameter-matched transcoders; scaling with FLOPs; faithfulness as
correlation/cosine similarity between replacement and true MLP Jacobians; Jacobian rank; qualitative
interpretability of transform activations; qualitative case studies in attribution graphs.

## What they found
Best Pareto performance came from mixed ranks (N transforms of rank 512, 2N of 256, 4N of 128, 8N of 64, 16N of 32),
beating uniform ranks at equal parameters. MOLTs had much lower MSE at a given L0; the smallest MOLT Pareto-dominated
transcoders using 1024x the FLOPs, and transcoders appeared to saturate while MOLTs did not. Jacobian faithfulness was
substantially higher and stable with scale, while transcoder faithfulness fell with scale (transcoder Jacobian rank
is bounded by L0). Transforms activate in interpretable patterns (token-level early, contextual later). In graphs,
examples include a Spanish-context transform routing "hot" to a "cal..." output feature, and a transform active
after "5" routing "plus 3" to "say 8". Some transforms are uninterpretable or redundant.

## Limits and open problems they name
Preliminary; rank allocation under-explored; Jacobian results use a different model from scaling results; graphs
with transforms are harder to read; reading what transforms do (feature-to-feature interaction strengths) is hard;
no comparison yet with the closely related Mixture of Decoders; not claimed strictly better than transcoders.

## What we take from it
Strong candidate component for a predictive white-box model: a layer described as gated low-rank linear maps is
closer to a program than a feature list, and the reported Jacobian-faithfulness measure is a good test for whether a
surrogate predicts the true layer's local behaviour. The finding that transcoder faithfulness degrades with scale is
a warning for any feature-only replacement. The rank-allocation result is a concrete design hint.

## Tags
unit: layer
form: replacement-model
method: transcoder
eval: faithfulness
goal: understanding
