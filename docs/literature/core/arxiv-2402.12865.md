# Backward Lens: Projecting Language Model Gradients into the Vocabulary Space

- **Key:** arxiv-2402.12865
- **Authors / organisation:** Shahar Katz, Yonatan Belinkov, Mor Geva, Lior Wolf; Technion, Tel Aviv University
- **Date:** 2024-02
- **Link:** https://arxiv.org/abs/2402.12865
- **Kind:** paper
- **Read from:** abstract and sections (arXiv HTML main text; proofs not checked)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Vocabulary projection (the logit lens) has been used to read hidden states and neurons as tokens, but never gradients. The authors want to read the backward pass: what a single gradient step writes into a model's weights, expressed in tokens. The larger aim is to explain how language models absorb and store new knowledge, especially in MLP layers, and to connect weight updates to interpretable quantities.

## What they studied
GPT-2 (small, medium, XL) and Llama-2-7B. 100 random CounterFact prompts, one SGD step each (no Adam, no batching). Unit: weight matrices of MLP layers (first layer FF1 and second layer FF2) and their gradients, decomposed into per-token vectors.

## How they did it
They note that a linear layer's gradient is a sum of outer products of each token's forward input x and its backward vector-Jacobian product delta, so an MLP matrix's gradient has rank at most the prompt length (rank 1 at the last layer). The gradient can therefore be written in terms of a few vectors, each of which can be projected through the unembedding (logit lens). They show the top-layer VJP is dominated by the target token's embedding with a negative coefficient, so in projection the target appears among the least likely tokens. From this they describe a two-part mechanism: "imprint" (the FF1 update adds or subtracts the forward inputs, so neurons become keyed to the current context) and "shift" (the FF2 update moves neuron outputs toward the target token embedding). They check rank empirically, project gradients and VJPs per layer and per token, and map where large updates occur. As a case study they build "forward pass shifting": edit one FF2 matrix by adding learning rate times the outer product of the last token's input and the target token's embedding, needing only a forward pass, and compare it with MEND, ROME and MEMIT on CounterFact (GPT-2 XL, layer 35, chosen from 30 to 40).

## What counts as an explanation here
An analytic description of a weight update as a low-rank sum of token-readable vectors, plus a mechanistic story (imprint then shift) of how one step stores a fact in an MLP. It is meant to be exact for one SGD step under simplifying assumptions, and it predicts the form of the update and allows a closed-form edit.

## How they judged success
Empirical gradient rank vs prompt length; logit-lens rank of the target token in projected VJPs; for editing, the standard CounterFact metrics: efficacy, paraphrase (generalisation), neighbourhood (specificity), and fluency by n-gram entropy.

## What they found
Gradient rank equals prompt length in over 98.5% of cases (rank 1 at the last layer). Upper-layer gradients project onto the target token; early layers are harder to read. In GPT-2 XL, large updates sit on subject tokens in early layers and on the last token around the second quarter of layers. Forward pass shifting: efficacy 99.4 (ROME 99.4, MEMIT 79.4, MEND 71.4), paraphrase 41.55 (ROME 71.9, MEMIT 40.7), neighbourhood 6.02 (lowest of all), fluency about unchanged (622.45 vs 626.94), at far lower cost.

## Limits and open problems they name
Logit lens is unreliable in early layers; unclear if gradients share an embedding space across layers. SGD only (Adam changes the picture). Theory ignores dropout, layer norm, positional embeddings, biases. Single edits only, not real fine-tuning. Attention not covered. Decoder-only models only. The editing method is a case study with weak specificity.

## What we take from it
(1) A weight-reading tool: weight changes from training on a few tokens are low rank and decomposable into input-side and output-side vectors that can be named through the embedding/unembedding. This is directly useful for explaining fine-tuning diffs or for predicting what a training step will change, a weights-first route to prediction. (2) The imprint/shift picture gives a concrete key-value reading of MLP weights we can test against. (3) Warning: vocabulary projection only works well near the output; early-layer weights need another basis. (4) Benchmark: CounterFact efficacy/paraphrase/neighbourhood, a standard way to score whether a weight-level story supports precise edits.

## Tags
unit: weights, layer
form: description, direction
method: weight-analysis, decomposition, other
eval: downstream-task, benchmark
goal: understanding, control/editing, science
