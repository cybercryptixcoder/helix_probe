# Transformer Feed-Forward Layers Are Key-Value Memories

- **Key:** arxiv-2012.14913
- **Authors / organisation:** Mor Geva, Roei Schuster, Jonathan Berant, Omer Levy; Tel-Aviv University, Allen Institute for AI, Cornell Tech
- **Date:** 2020-12 (v2 2021-09; EMNLP 2021)
- **Link:** https://arxiv.org/abs/2012.14913
- **Kind:** paper
- **Read from:** full text (PDF)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Feed-forward (FFN) layers hold about two thirds of a transformer's parameters but were little studied compared with attention. The authors want to know what these layers store and how they contribute to predictions. They propose that an FFN is formally almost a key-value memory, and test whether the keys and values actually behave like interpretable memories. The aim is a basic, weight-level account of a large part of the network.

## What they studied
The 16-layer transformer language model of Baevski and Auli trained on WikiText-103 (d = 1024, 4096 FFN units per layer, 65,536 keys in total). Units: individual FFN "memories", i.e. a row of the first weight matrix (key) paired with the matching row of the second (value), and whole layers.

## How they did it
They write FF(x) = f(x K^T) V and note it differs from a neural memory only by using an unnormalized nonlinearity instead of softmax; activations are "memory coefficients". For keys, they ran the model over training-set sentence prefixes and took, for each sampled key (10 per layer, 160 total), the 25 prefixes with highest coefficient; NLP graduate students annotated recurring patterns as shallow (n-gram/surface) or semantic (topic). They checked which positions matter by removing the first, last or a random token from the top-50 trigger prefixes for 1,600 keys. For values, they projected each value vector onto the output embedding matrix to get a vocabulary distribution and measured agreement between the value's top token and the actual next token of the key's top trigger example, by layer. Finally, on 4,000 validation prefixes, they studied how many memories fire, whether a layer's output prediction matches any single memory's, and how the residual stream's prediction is kept, overridden or compromised across layers.

## What counts as an explanation here
A reading of weights as a lookup structure: each key is described by the input patterns that trigger it (text descriptions from annotators), each value by its projected distribution over next tokens. It is partial (sampled memories, descriptive) but has a predictive element: the value's top token should predict the next token for inputs that trigger the key.

## How they judged success
Human annotation coverage (share of trigger prefixes matching a pattern; shallow vs semantic by layer); change in memory coefficient when tokens are removed; agreement rate between value top token and trigger next token versus a random-token baseline; rank of the true next token in the value distribution; counts of active memories; how often layer output differs from every individual memory; residual-versus-FFN agreement categories.

## What they found
Every sampled key had at least one recognizable pattern (3.6 on average) and 65 to 80% of trigger prefixes matched one; lower layers (1 to 9) skew shallow, upper layers (10 to 16) semantic. Removing the last token disrupts coefficients more than removing the first, less so in upper layers. Value-trigger agreement is near zero in layers 1 to 10 and rises to about 3.5% in upper layers versus about 0.0004% chance; 97 of the 100 most confident values sit in layers 11 to 16. A typical input activates hundreds of memories per layer (10 to 50%), and in at least about 68% of cases the layer's top prediction matches no individual memory, so outputs are compositional. Predictions are refined gradually through the residual stream; when the FFN changes the residual's top choice, it usually lands on a compromise rather than its own top token, hinting at a veto role.

## Limits and open problems they name
Small sample (160 keys, one annotator each), one model; annotations are subjective; projecting values with the output embedding assumes a shared space across layers, which is naive and fits lower layers poorly. FFN-attention interplay is unstudied; automatic pattern identification is future work.

## What we take from it
The founding frame for reading MLP weights directly: rows of W_in as pattern detectors, rows of W_out as vocabulary-space votes. Reusable measures: value-trigger agreement against a random baseline, and the "does the layer output equal any single memory" check, which is a quick test of whether a per-unit reading can predict layer behaviour. Warning for us: at least two thirds of the time the output is a composition of many memories, so a white-box model that reads units one at a time will not predict outputs; it needs a composition rule. Also, lower-layer values do not project cleanly to vocabulary.

## Tags
unit: neuron | weights | layer
form: description | dictionary
method: weight-analysis | other
eval: human-rating | prediction/simulation
goal: understanding | science
