# Transformer Circuit Exercises

- **Key:** transformer-circuits-pub-2021-exercises-index-html
- **Authors / organisation:** Transformer Circuits Thread (Anthropic); typos reported by Tuomas Oikarinen and Callum Canavan
- **Date:** 2021-12
- **Link:** https://transformer-circuits.pub/2021/exercises/index.html
- **Kind:** tool (teaching problem set; companion to *A Mathematical Framework for Transformer Circuits*)
- **Read from:** full text (prompts and worked solutions; no separate artifact beyond the page)
- **Relevance to us:** 1 (background) — but see "What we take from it": the notation and the two composition identities are directly reusable

## What they wanted, and why

The authors of the transformer-circuits framework wanted a way to check that their mechanistic account of transformers was actually understood down to individual parameters, not merely at the level of diagrams. The stated worry is that a reader can follow the prose while quietly blurring over confusion about which matrix does what. Their remedy is a problem set in which you *write down the weights* of attention heads that implement named algorithms, then compare with published solutions. The larger goal is to make "circuit" claims concrete enough that anyone can construct a working example of one by hand.

## What they studied

No trained models and no data. The objects are attention heads as parameter matrices — W_Q, W_K, W_V, W_out, and the residual stream they read from and write to. The exercises fix concrete dimensions so the matrices can be written out: 4-dimensional query/key/value vectors and a 16-dimensional residual stream for the virtual-head exercise, an 8-dimensional query/key head for the induction exercises. The unit of analysis is the level of a single head and of a head pair, and the target phenomenon is in-context copying.

## How they did it

The set has three parts. A warm-up asks for the architecture, for a single head written in terms of its four matrices, for which matrix decides the read subspace and which the written subspace (and what their product means), for which two matrices control *where* attention goes, and for the rank of the factored matrices. Exercise 1 builds a "virtual attention head": head 1 in layer one attends to the previous token and copies residual dimensions 0–3 to 8–11; head 2 in layer two attends to the previous token and copies three untouched dimensions plus one dimension that head 1 wrote, so the pair behaves as a head attending two tokens back without any single head paying the full cost. Exercise 2 hand-builds an induction head by pointer arithmetic — a content-matching Q/K from the principal components of the content embedding, a self-selecting position Q/K from the sin/cos position basis, a previous-token version of the same by composing a 2-D rotation into the query, a content-plus-position head with a signed scalar to suppress attending to itself, a V/W_out pair that copies the largest position-embedding components out, and finally a head that rotates *forwards* rather than backwards to land on the token after the earlier copy. Exercise 3 rebuilds the same behaviour as a previous-token *K-composition* circuit, because rotary-style positional encodings never reach W_V, so position cannot be copied out by the value path and must instead be delivered into the second head's key through a first head's content copy. Solutions give explicit matrices and note that an arbitrary rotation can be composed into both Q and K with no functional change.

## What counts as an explanation here

A constructive one: a set of weight matrices that provably implement a stated algorithm, plus the two identities that license reading a pair of heads as a single longer-range head. It is not a description of any real trained model and makes no predictions about one; it is the minimal standard of rigour a mechanistic claim should be able to meet — you should be able to write the weights down.

## How they judged success

Correctness of the hand-derived matrices, and whether the composed products produce the intended behaviour. Two quantitative ingredients do the work. First, expanding W_net = W_out·W_V collapses a head to one linear map from the attended position's residual subspace to the writer's subspace, giving h_i(x) = Σ_j A_ij W_net x_j, so a head is a routing matrix times a rank-limited content map. Second, for hierarchical reading, W_V(head 2)·W_out(head 1) is the composition that asks whether the later head consumes what the earlier head wrote, with its singular values as the strength per direction. For the virtual head, the two-token copy is W_net²·W_net¹ and the one-token copy is W_net²·Id + Id·W_net¹, so a mixed-capacity head is a sum of a same-position and a two-back path. There is no benchmark, baseline or metric — success is a checked derivation.

## What they found

The worked answers are mostly the surprising omissions rather than positive results. The virtual-head solution is deliberately non-unique: what matters is only that W_V² has a 1 in a column aligned with a row of W_out¹ and 1s in columns untouched by the first head, and their own accounting is that the pair spent seven eighths of its capacity on the previous token and one eighth on two-back. The pointer-arithmetic induction head falls out of one observation: the sine/cosine pair of the position basis is a 2-D point, and the previous token's point is the current point rotated by minus the frequency, so a *query-side rotation* turns a self-selecting head into a previous-token head and the reverse rotation turns the copied-position head into one that lands on the token after the earlier copy. Once Q/K carry that rotation, W_K stays identical between the two cases. The only tunable in the self-suppressing head is a single scalar beta weighting the "content matches" against "not the present position" components of an 8-D query. The K-composition variant needs no rotate-out-of-V at all: head 1 attends to the previous token and copies its content into v_0…, head 2 uses that subspace in W_K and compares it to the current token's content in W_Q — the same behaviour with the position handled implicitly.

## Limits and open problems they name

Nothing is measured, so there are no results about real networks, and the constructions are existence proofs of mechanisms rather than evidence that a given model uses them. The base framework's own problem — that heads can be analysed only when composition patterns make them legible — carries over. The page also flags that which mechanism a model can use depends on its positional-encoding scheme: with rotary attention the value path is closed to positional information, so only the K-composition route is available, which is an architectural constraint on what circuits are even expressible. The solution notes also repeatedly point out non-uniqueness (arbitrary rotation composed into Q and K), so the written weights are one representative of an equivalence class, not the model's actual parameters.

## What we take from it

- **A method:** W_net = W_out·W_V, and W_V^(later)·W_out^(earlier) with its singular values, are the right primitives for building a *reader of the weights* — the first says what a head writes and how many directions it can carry, the second says whether a downstream head reads that write and with how much gain per direction. This is weight-side, needs no forward pass, and is exactly the low-cost precursor to probing that our project needs.
- **A framing:** the virtual-head identity (two-token path = W_net²·W_net¹, one-token path = the sum with identities) tells us that "which token does this head read" is not a property of any single head's V or output matrix, so any per-head attribution we compute should be reported as a decomposition over paths, with the mixing known rather than assumed.
- **A warning:** solutions are equivalence classes — an arbitrary rotation composed into both Q and K is functionally identical. Any weight-based distance or similarity metric we use (cosine of head vectors, direction alignment) is not invariant to that, so it will rank two implementations of the same algorithm as different. Fix the gauge (e.g. compare W_Q^T·W_K and W_out·W_V, the factored products, rather than the raw matrices) before comparing heads across models or layers.
- **A dataset/harness:** a hand-constructed weight set with known algorithm is a free ground truth for any weight-reading tool — the analogue, at the parameter level, of the toy models used for testing decomposition methods. We can build these heads into a small transformer and check whether our reader recovers the algorithm it was given.

## Tags

unit: head, weights, circuit
form: description, causal-abstraction
method: weight-analysis, other (pedagogical construction)
eval: faithfulness (of a hand-built mechanism, by derivation)
goal: understanding
