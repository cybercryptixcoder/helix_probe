# The Linear Representation Hypothesis and the Geometry of Large Language Models

- **Key:** arxiv-2311.03658
- **Authors / organisation:** Kiho Park, Yo Joong Choe, Victor Veitch; affiliations not stated in the HTML read (ICML 2024)
- **Date:** 2023-11
- **Link:** https://arxiv.org/abs/2311.03658
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
"Concepts are directions" is assumed throughout interpretability, but the phrase is used in three different senses:
a direction in a subspace (word analogies), a linear probe that measures the concept, and a steering vector that
changes it. The authors want a precise definition that unifies these, and they want to know which inner product
makes cosine similarity and projection meaningful, since a language model's representations are only identified up
to an invertible linear transform and the Euclidean inner product has no special status.

## What they studied
LLaMA-2 7B (4096-dim, 32K vocabulary), with Gemma-2B for one comparison. Unit: the model's output (unembedding)
vectors for words and its final-layer context embeddings. 27 binary concepts from BATS 3.0 and related lists (verb
inflections, derivations, male to female, lower to upper case, country to capital, plural, comparative, thing to
part, frequent to infrequent and so on) plus four language pairs, each defined by 4 to 63 counterfactual word pairs
of single tokens.

## How they did it
They define a concept by counterfactual output pairs (e.g. king/queen) and call two concepts causally separable if
they can vary independently. They prove that an unembedding-space concept direction gives a logit-linear probe that
ignores off-target concepts, and that an embedding-space direction, when added to the context, changes the target
concept without changing separable ones. They define a "causal inner product" as one under which separable concepts
are orthogonal, show it maps unembedding directions to embedding (steering) directions, and, under an assumption that
random vocabulary words' concept values are uncorrelated, derive that it can be estimated as the inverse covariance of
the unembedding vectors (one choice among a family). Experiments: compute concept directions from pair differences;
check that held-out pair differences project strongly on them (vs random pairs); compute pairwise inner products
among all concepts under the causal and Euclidean inner products; use a direction to classify the language of
Wikipedia contexts; add the derived embedding direction to the context of prompts and track logits of target and
off-target counterfactual words.

## What counts as an explanation here
A geometry: each concept is a direction in output space and a dual direction in context space, linked by a specific
inner product; probing and steering are two faces of the same object. Partial (binary concepts, input/output spaces
only), but it makes testable predictions: which directions should be orthogonal and how logits move under a given
intervention.

## How they judged success
Projection histograms of counterfactual pair differences against random word pairs; heatmaps of inner products
between concept directions (block structure, near-orthogonality of separable concepts); separation of French vs
Spanish contexts by a probe direction and failure of an unrelated direction; change in target vs off-target logit
differences as the steering coefficient grows; a sanity check that projections of separable concepts are uncorrelated
over the vocabulary while non-separable ones are correlated.

## What they found
- Most concepts are linearly represented in output space; thing to part is a clear exception.
- Under the estimated causal inner product, separable concepts are nearly orthogonal, with block structure by semantic
  group. In LLaMA-2 the Euclidean product also looks mostly fine, but in Gemma-2B it fails while the causal one works.
- The French-Spanish direction separates contexts in the expected way; male-female does not.
- Adding the derived embedding direction raises "queen" over "king" while leaving "King" vs "king" roughly unchanged;
  "queen" becomes top-1 for "Long live the" at a small coefficient.

## Limits and open problems they name
Concepts must be binary and readable from output tokens; separability and the uncorrelatedness assumption are
idealisations; the inner product is only determined up to a scaling with no principled choice; tokenisation and
machine-generated pairs add noise; only the input/output spaces were studied, not intermediate layers or parameters;
mostly one model; some concepts are not linear.

## What we take from it
- **Method, weight-based:** concept directions and a meaningful inner product can be computed from the unembedding
  matrix alone (inverse covariance of unembeddings), with no activations. This is a direct example of reading
  structure out of weights.
- **Warning:** cosine similarity in raw coordinates can be meaningless; any weight-space geometry we use should
  justify its inner product, or test it by intervention.
- **Measure:** "steering along the derived direction moves the target and leaves separable concepts unchanged" is a
  concrete prediction-under-intervention test.
- **Framing:** the probe/steer duality says a correct variable should both read and write; this matches what a
  predictive white-box model needs.

## Tags
unit: direction, weights
form: direction, probe, steering
method: weight-analysis, probing, steering
eval: prediction/simulation, faithfulness
goal: science, understanding
