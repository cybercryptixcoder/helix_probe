# Tracing Attention Computation Through Feature Interactions

- **Key:** tcpub-2025-attention-qk
- **Authors / organisation:** Harish Kamath, Emmanuel Ameisen, Isaac Kauvar, Rodrigo Luger, Wes Gurnee, Adam Pearce, Sam Zimmerman, Joshua Batson, Thomas Conerly, Chris Olah, Jack Lindsey; Anthropic
- **Date:** 2025-07-31
- **Link:** https://transformer-circuits.pub/2025/attention-qk/index.html
- **Kind:** paper (Transformer Circuits Thread)
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Attribution graphs (tcpub-2025-attribution-graphs-methods) freeze attention, so they cannot say which heads carry an
edge or why a head attends where it does, and in many prompts that is the heart of the computation (induction,
multiple choice, checking an answer). The authors extend attribution graphs to explain attention scores in terms of
interacting features on the query and key sides.

## What they studied
Claude 3.5 Haiku. Units: pre-softmax attention scores, attention heads, and residual-stream SAE or weakly causal
crosscoder features at query and key positions.

## How they did it
A pre-softmax attention score is bilinear in the query-position and key-position residual streams, so if both are
written as sums of features, the score splits exactly into query-feature x key-feature terms (with corrections for
normalisation; rotary embeddings handled in principle). These terms are ranked and shown in the graph UI. Separately,
each graph edge is split into attention-, MLP- and residual-mediated parts, with the attention part broken down per
head ("head loadings"). Because head paths through transcoder-only graphs multiply exponentially with depth, they
"checkpoint" with residual-stream SAEs or weakly causal crosscoders so each edge passes through only single-layer
head paths, at the cost of nonlinear MLP attributions. Case studies: name induction (Aunt/Uncle), a two-name variant,
French antonyms, multiple choice, and correctness checking (banana colour, arithmetic like 18+5=23). Each mechanism is
checked by steering query- or key-side features or scaling head outputs and observing changes in attention and
output.

## What counts as an explanation here
An attribution graph augmented with per-head edge decompositions and, for each important attention score, a ranked
list of query-key feature pairs: a feature-level account of why attention goes where it does. Partial, per-prompt.

## How they judged success
Causal interventions only: steering query/key features and checking whether attention and the predicted token move
as the explanation predicts; number of heads that must be steered; asymmetry of steering strength between directions.
No aggregate metrics or benchmarks are reported.

## What they found
Induction is driven by query-side "Aunt/Uncle" features matching key-side name and "name of Aunt/Uncle" features, fed
by a previous-token mechanism; the two-name variant shows independent interaction terms (rank at least 2) and a
general bias to attend to names. Antonyms mix a mechanism tagging the target word with one searching for any suitable
adjective. Multiple-choice heads match correct-answer key features with answer-request query features, and
false-statement features suppress attention to wrong options. Correctness checks use "concordance" and "discordance"
heads (W_QK eigenvalues skew positive vs negative), suggesting the model validates a stated property rather than
recomputing. Steering about 3-10% of heads was needed to break induction, fewer than half that when other heads were
frozen, showing compensating heads ("hydra" effect). Flipping No to Yes needed stronger steering than Yes to No.

## Limits and open problems they name
Softmax competition means important negative terms at other positions are not surfaced automatically; quadratic cost
in context length; error nodes hide some cross-token inputs; positional effects largely omitted; checkpointing
sacrifices MLP linearity; head roles shown only on specific prompts. Open: distilling QK attributions (low rank per
head), finding inhibitory terms automatically, long-context scaling, testing whether heads are polysemantic,
decomposing functional units spread across heads, and applying to binding, state tracking and in-context learning.

## What we take from it
(1) Method: the bilinear QK decomposition is exact and reads directly off W_Q, W_K and feature directions, so it is a
natural weights-plus-features component for a white-box model that must predict attention patterns. (2) W_QK
eigenvalue sign as a weight-level signature of head type (concordance vs discordance) is a direct weight-reading
handle. (3) Warning: redundancy and self-repair across heads mean single-head ablations underestimate importance; our
intervention tests should freeze or account for compensating heads.

## Tags
unit: head, feature, circuit
form: graph
method: attribution, SAE, steering, weight-analysis
eval: ablation, patching
goal: understanding, science
