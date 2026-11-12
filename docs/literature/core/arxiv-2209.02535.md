# Analyzing Transformers in Embedding Space

- **Key:** arxiv-2209.02535
- **Authors / organisation:** Guy Dar, Mor Geva, Ankit Gupta, Jonathan Berant; Tel-Aviv University, Allen Institute for AI
- **Date:** 2022-09
- **Link:** https://arxiv.org/abs/2209.02535
- **Kind:** paper
- **Read from:** full text (HTML, first ~100k of ~164k characters; appendices partly unread)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Most interpretation methods need forward passes over inputs. The authors want an input-independent ("zero-pass") way to interpret all parameters of a trained transformer by projecting them into the space of vocabulary tokens. If this works, parameters can be read directly, and because the vocabulary space is fixed by the tokenizer, parameters of different models sharing a vocabulary can be compared or aligned without any data.

## What they studied
GPT-2 medium (345M, 24 layers, 384 heads) mainly, with GPT-2 base and large as checks, and BERT-base (MultiBERTs, 25 seeds) for alignment. Units: all weight matrices: FFN keys and values, and attention heads via the query-key interaction matrix W_QK and the value-output matrix W_VO, further split into rank-one "subheads".

## How they did it
Every parameter is multiplied by the embedding matrix E (using E transpose in place of a true right-inverse; they report the pseudo-inverse works badly under top-k reading). FFN values and keys become vocabulary scores; W_QK becomes a token-by-token interaction matrix and W_VO a token-to-token transition matrix, read via top-k token pairs. LayerNorm and biases are ignored. Experiments: (1) qualitative reading of heads and FFN units; (2) a check against activations: on 60 IMDB examples, overlap between top-k tokens of a hidden state and the top tokens of its most active parameter vectors, compared with a random hidden state; (3) fine-tune the top three layers of GPT-2 base for IMDB sentiment and project the weight differences; (4) align layers of independently trained MultiBERTs by correlating their embedding-space projections and matching with the Hungarian algorithm, versus matching raw weights; (5) zero-shot stitching: map GPT-2 medium hidden states into GPT-2 base's space via the two embedding matrices and feed them to GPT-2 base's fine-tuned classifier layers.

## What counts as an explanation here
A static, data-free description of each weight matrix as relations among vocabulary items (what token a unit promotes; which token pairs a head links). Partial and approximate (linear, ignores LayerNorm, depends on the transpose heuristic), but it is a reading of weights alone, and the stitching experiment makes a prediction about cross-model compatibility.

## How they judged success
Qualitative examples; overlap score R_k (k = 100) between parameter-derived and activation-derived tokens versus random hidden states; a top-k reconstruction score comparing E transpose (0.83) with pseudo-inverse (0.10); Hungarian layer matching across seeds, with raw-weight matching as a control; IMDB accuracy of stitched models over 11 seeds.

## What they found
Projected heads and FFN units show recognizable themes (word pieces, gender, geography, spelling, topics). Parameter-derived tokens overlap more with the actual hidden state than with a random one, though the effect is partial. Fine-tuning weight deltas for sentiment project onto sentiment words for W_Q, W_K, W_V and FFN keys, but not for FFN values or W_O. Same-index layers align across MultiBERT seeds after projection, while raw weights give random-looking matches. Stitching works only sometimes: 3 of 11 seeds reach about 70% IMDB accuracy.

## Limits and open problems they name
Only the vocabulary lens; E transpose is a heuristic; requires a linear LM head (hence mostly GPT-2), though BERT alignment still worked; ignores LayerNorm and biases; parameters may encode corpus stereotypes.

## What we take from it
The most direct precedent for reading a whole transformer from weights without inputs, and a set of concrete building blocks: W_QK and W_VO as token-space matrices, subhead decomposition, projecting fine-tuning deltas (connects to task vectors, arxiv-2212.04089), and embedding-space alignment of models as a data-free comparison. Reusable checks: compare weight-derived readings with activation-derived ones on real inputs (R_k overlap) and against a random baseline. Warning: the weight-only reading only partially matches what the network actually does on inputs, and the stitching success rate is low, so weight projections alone will not predict behaviour without accounting for nonlinearity and composition.

## Tags
unit: weights | head | neuron | layer
form: description | dictionary
method: weight-analysis | decomposition
eval: prediction/simulation | downstream-task
goal: understanding | science
