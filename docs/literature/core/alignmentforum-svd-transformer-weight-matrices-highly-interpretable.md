# The Singular Value Decompositions of Transformer Weight Matrices are Highly Interpretable

- **Key:** alignmentforum-svd-transformer-weight-matrices-highly-interpretable
- **Authors / organisation:** beren (Beren Millidge), Sid Black; Conjecture
- **Date:** 2022-11-28
- **Link:** https://www.alignmentforum.org/posts/mkbGjzxD8d8XqKHzA/the-singular-value-decompositions-of-transformer-weight
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Neurons are often polysemantic, so the authors look for meaningful directions instead, directly in the weights. Their hypothesis: the top singular vectors of a weight matrix are where it acts most strongly, and so may correspond to the features it reads or writes. They also want a form of static analysis: understanding the network from parameters alone, without running data through it.

## What they studied
GPT-2 small, medium and large, with most detail on GPT-2 medium (24 blocks, 16 heads, head dimension 64). Matrices: attention OV circuits, MLP input and output weights; QK circuits briefly. Unit: singular directions of weight matrices.

## How they did it
Take the SVD of each weight matrix; take the singular vectors that live in the residual stream; project each into vocabulary space through the unembedding and read off its top-k tokens. Label each direction as interpretable if most top tokens share a concept. Manual labelling: about 40 directions per block across GPT-2 medium MLP input weights (960 in total). Automated labelling: GPT-3 (text-davinci-002) with few-shot prompts plus a separate verifier prompt, both must agree, over the first 30 directions of every MLP layer in three model sizes. Random Gaussian matrices served as a no-structure control. Editing: remove a single rank-one component from a head's OV matrix and measure the change in log-probability of a related token. "SVD tracing": embed a natural-language query and find singular vectors with cosine similarity above 0.15.

## What counts as an explanation here
A labelled list of weight directions: each singular direction of a head or MLP is described by a token cluster/concept. It is a static, partial dictionary of what each component reads and writes, not an input-specific account. Predictions are limited to closed-form rank-one edits.

## How they judged success
Fraction of singular directions judged interpretable (human and GPT-3-with-verifier labels), as a function of layer and singular index; comparison to random matrices; edit effect on target-token log-probability relative to removing other directions.

## What they found
- Automated labels: per-block interpretable fraction rose from roughly 40-50% in early layers to 80-90% late; overall about 70-80%, stable through 30 directions. The labeller was biased toward "interpretable".
- Manual labels: interpretability rose with depth; roughly U-shaped across singular index (first and very late directions less clean). The first direction is often just frequent words.
- OV heads tend to cover a broad topic with directions as subtopics; positive and negative ends of a direction can carry opposed concepts (e.g. fire vs ice). MLP directions stay interpretable deeper into the spectrum than OV ones; output weights less interpretable than input weights (unexplained).
- QK directions much less interpretable.
- Removing the "fire" direction from one head lowered "fire" log-probability more than removing other directions; but single-component edits rarely change global behaviour because processing is distributed.

## Limits and open problems they name
Subjective, noisy labels with no ground truth; GPT-3 labeller positive bias; weight-only analysis cannot explain particular inputs; nonlinear structure missed; edits too weak. Commenters add: near-equal singular values make individual vectors unstable (only their span is defined), and SVD cannot recover overcomplete/superposed features.

## What we take from it
A cheap baseline for reading weights: SVD plus unembedding projection gives a static, data-free dictionary of what each component reads and writes, which our weight-reading method should beat. Use random-matrix controls and automated labelling with a verifier, but correct for labeller bias. Warnings: individual singular vectors are not identifiable when singular values are close, SVD is orthogonal so it cannot express superposition, and per-component edits are not predictive of whole-model behaviour.

## Tags
unit: weights | head | direction
form: direction | description
method: weight-analysis | decomposition | agent (LLM labelling)
eval: human-rating | ablation
goal: understanding | control/editing
