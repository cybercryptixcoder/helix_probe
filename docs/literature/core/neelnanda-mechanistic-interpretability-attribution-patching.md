# Attribution Patching: Activation Patching at Industrial Scale

- **Key:** neelnanda-mechanistic-interpretability-attribution-patching
- **Authors / organisation:** Neel Nanda (work begun at Anthropic, Feb-Mar 2022; finished independently)
- **Date:** 2023-02 (per scout; the page itself shows no date)
- **Link:** https://www.neelnanda.io/mechanistic-interpretability/attribution-patching
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Activation patching needs one forward pass per patched activation, which is too expensive for sweeping every head,
neuron and position in a large model. Nanda wants a cheap approximation that ranks all candidate components at once,
so patching can be used for exploration at scale, with real patching kept for confirmation.

## What they studied
GPT-2 Small on Indirect Object Identification (IOI), with clean and corrupted prompts differing in one name. Units:
residual stream, attention and MLP outputs, MLP0, individual heads and their queries, keys, values and attention
patterns, per position; head-to-head paths.

## How they did it
1. Forward pass on the clean prompt and the corrupted prompt, caching activations.
2. Backward pass on the corrupted run, caching gradients of the metric with respect to activations.
3. Estimate each patch's effect as the dot product of (clean activation minus corrupted activation) with the
   corrupted-run gradient: a first-order Taylor approximation of patching.
4. Because it is linear, attributions of sub-components sum to the component's attribution.
5. Extend to direct path patching between pairs of components and to attention-pattern attribution.
6. Compare attribution results with real activation patching plots for the same components.
Metric: logit difference between correct and incorrect name.

## What counts as an explanation here
A ranked map of which components (and edges) carry the clean-vs-corrupted difference in a metric; a candidate
circuit to be confirmed by other methods. Explicitly exploratory, not an explanation in itself.

## How they judged success
Visual, qualitative agreement between attribution and activation patching across component types; recovery of the
known IOI circuit. No correlation numbers are reported.

## What they found
Good agreement for head outputs, layer outputs and finer head activations; poor for large activations such as the
residual stream and for MLP0/embeddings. It recovers the broad IOI circuit; head-to-head path attribution is sparse
and finds some known edges but is messy. Cost is two forward passes and one backward pass regardless of the number
of patches, estimated at roughly 30,000x faster than patching every head at every position in GPT-2 XL on a 100-token
prompt.

## Limits and open problems they name
Fails where nonlinearities matter: LayerNorm (residual stream patches), discrete embeddings, saturating softmax and
GELU, multi-feature interactions, and deep composition between patch site and metric. Backup heads create false
positives. Metric choice matters: probabilities mislead, logit differences mislead when the corrupted prompt is
confidently wrong. True accuracy is still unclear and more empirical study is needed.

## What we take from it
A shortcut: gradient-times-difference attribution can screen thousands of candidate locations for our predictive
model cheaply, with real patching used only to confirm. A warning that any linearised prediction of intervention
effects (including one read from weights) will break at LayerNorm, saturating nonlinearities and large patches, so
we should report where our predictions are first-order and test them against real interventions. Guidance on
metrics: use logit difference and watch for confidently wrong corrupted baselines.

## Tags
unit: head, layer, neuron
form: graph
method: attribution, patching
eval: patching
goal: understanding, debugging
