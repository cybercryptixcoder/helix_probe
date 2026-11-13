# Covariance-based Sequence Pooling

- **Key:** goodfire-com-research-covariance-pooling
- **Authors / organisation:** Thomas Dooms, Nicholas K. Wang, Michael T. Pearce; Goodfire (life-sciences team)
- **Date:** 2026-04-10
- **Link:** https://www.goodfire.com/research/covariance-pooling
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Genomic foundation models emit one vector per nucleotide, but the biological unit anyone cares about is the
gene — so thousands of token vectors must be collapsed into one embedding before a probe can be trained. The field
default is mean pooling, which is stable and a good regulariser but only records *which* features are present in
the sequence, never *whether they occur together at the same position*. The authors want a pooling operation that
keeps co-occurrence structure and still works in the low-data, very-long-input regime that genomic probes live in.
This is a small methods step toward the larger goal of extracting knowledge from foundation-model internals rather
than from raw sequence, which they frame as interpretability as a scientific-discovery engine.

## What they studied
NTv3, a genomic foundation model, on DNA sequences (genes, spanning hundreds to millions of nucleotides). The unit
of analysis is neither a neuron nor a token but a *sequence-level statistic of the activation cloud*: the truncated
second moment of per-token hidden states, plus learned linear projections of those states. Downstream, a linear
probe sits on the pooled matrix.

## How they did it
Per sequence, take the activation matrix X ∈ R^{T×d}. Mean pooling is the 1×d centroid; their covariance pooling is
the d×d matrix formed from XᵀX scaled by one over the sequence length, whose (i,j) entry is large exactly when
dimensions i and j are simultaneously active in the same token. To make this tractable they push X through two
untied linear projections L and R into a compressed dimension and form M = (XL)ᵀ(XR)/T, so the pooling step itself
becomes trainable and selects which feature pairs survive. Two training modes: (a) supervised, with a probe on the
flattened M and gradients flowing back into L and R; (b) unsupervised, treating L and R as a sequence autoencoder
whose target is the full d×d second moment and whose loss is the Frobenius norm of the reconstruction L M Rᵀ — they
note the Frobenius norm identity makes this optimisable in linear time without ever materialising the sequence-by-
sequence similarity matrix, and without positional embeddings or an explicit token decoder. They deliberately do not
centre the matrix (no mean subtraction, which they say gave no gain), and they concede "second-order pooling" would
be the more accurate name since L and R are untied and M need not be symmetric. Two evaluations: predicting 39
functional genomic track signals, and Gene Ontology classification over 763 filtered terms.

## What counts as an explanation here
Not an explanation in the usual sense — no circuit, no feature dictionary, no text description. The deliverable is
a *replacement pooling operator plus a learned compression*, i.e. a representation-level claim: the second moment of
the activation cloud carries structure that the first moment provably cannot, and a low-rank factorization of it is
a sufficient statistic for the downstream label. It is partial by construction: token identity and absolute position
are explicitly discarded (the U factor of the SVD cancels), so what is preserved is the *shape* of the token cloud,
not the trajectory through it. It does predict, but only the sequence-level label, not any per-token quantity.

## How they judged success
Two backbones-frozen downstream tasks, both against mean pooling as the baseline: R² on 39-track genomic signal
prediction, and AUC on 763 Gene Ontology terms, using the unsupervised autoencoder embeddings (i.e. the harder,
label-free condition). The authors describe these as small-scale sanity checks and state that larger-scale results
are still forthcoming; there is no ablation over compression dimension, no comparison to attention pooling beyond a
qualitative claim that it overfits in low-data regimes, and no statistics over seeds.

## What they found
The learned covariance bottleneck improved track-prediction R² by 52.9% over mean pooling, and the frozen
unsupervised embeddings lifted Gene Ontology AUC by 8.4%. Worked example motivating the mechanism: two RNA
sequences with the same motif and the same hairpin loop in different relative positions produce an identical mean
vector but different covariances, because the motif-dimension × loop-dimension product is high only when they fire
in the same token. They argue this applies to any pair of linearly accessible feature directions, not just residual
stream coordinates.

## Limits and open problems they name
Experiments are described as small-scale sanity checks, with scaling deferred. Covariance pooling is bounded by what
the foundation model already encodes — it cannot recover combinatorial structure the model never represented. It
does not replace established bioinformatics annotation pipelines. It also throws away position and token identity,
which is the flip side of the property they are selling.

## What we take from it
- **Method to copy:** a *second-moment readout* as an option alongside mean/top-K pooling. Any time our target is a
  property of a whole sequence (a trait, a persona, a task state) and the candidate mechanism is co-occurrence of
  two features at one position, the centroid is information-theoretically blind to it while the covariance is not —
  and the failure is silent, since both sequences get identical mean embeddings.
- **Measure:** report the co-occurrence case explicitly. Construct a matched pair of inputs that share per-feature
  marginal counts but differ in joint occurrence, and check whether the readout separates them. This is the pooling-
  level analogue of the minimal-pair tests already standard for head circuits.
- **Warning for our own work:** all pooling is lossy in a *specific* direction, and the losses differ — mean loses
  co-occurrence, top-K loses coverage, attention pooling loses low-data stability, covariance loses position. Which
  one is acceptable is a claim about the mechanism we are predicting, so the pooling choice must be justified against
  the hypothesised mechanism rather than tuned on validation.
- Third sighting in this reader's notes that **aggregation is a first-class design choice** (after top-K segment
  pooling and attention-pooled probes); here it is the *only* change made, and it bought tens of percent on one
  metric — a reminder that our reader's headline number may be dominated by its pooling rule, not its classifier.

## Tags
unit: layer
form: direction
method: probing | decomposition | other
eval: downstream-task | ablation
goal: science | understanding
