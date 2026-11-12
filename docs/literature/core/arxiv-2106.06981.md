# Thinking Like Transformers (RASP)

- **Key:** arxiv-2106.06981
- **Authors / organisation:** Gail Weiss, Yoav Goldberg, Eran Yahav; Technion, Bar-Ilan University, Allen Institute for AI
- **Date:** 2021-06 (ICML 2021)
- **Link:** https://arxiv.org/abs/2106.06981
- **Kind:** paper
- **Read from:** full text (PDF)
- **Relevance to us:** 3 (central)

## What they wanted, and why
RNNs have finite automata as a mental model; transformers had no comparable abstraction. The authors want a
programming language whose operations map onto what a transformer encoder can compute, so that people can reason
about transformer solutions as programs instead of as weights. The language should both help write down how a
transformer could solve a task and bound the resources (layers, heads) it needs. The larger goal is a symbolic
vocabulary for "what the network is doing", which later work (Tracr, Transformer Programs) uses as the target
language for compiling to and decompiling from weights.

## What they studied
The transformer encoder as an abstract machine. Concrete check models: small transformers (embedding width 256, FFN
width 512), trained per task on synthetic sequence tasks: reverse, histogram (with and without a BOS token), double
histogram, sort, most-frequent, Dyck-1 and Dyck-2 prefix classification, plus symbolic set-containment examples.
Unit of analysis: attention heads (as select/aggregate) and MLP sublayers (as elementwise maps).

## How they did it
They define RASP: built-in sequence operations (tokens, indices, length), elementwise operations (stand-ins for
MLPs), `select` (a key/query/predicate selection matrix, standing for attention scores), `aggregate` (averaging the
selected values, standing for a head's output) and `selector_width` (counting selected positions). They write RASP
programs for each task by hand. A simple placement procedure (each aggregate becomes a head after its inputs,
elementwise ops placed at the earliest possible layer, heads sharing a selector merged) yields a predicted number
of layers and heads per task; they do not compile to concrete weights. They then train transformers of exactly that
size (four per task, 50,000 training examples, sequences up to length 100, Adam, 100 epochs) and compare learned
attention patterns with the RASP selectors. To test tightness of the bound they also train models with one fewer
layer or head (sometimes with doubled heads). Finally, they train models with an extra loss that supervises
attention toward the RASP patterns, to check that the RASP solution is actually realisable.

## What counts as an explanation here
A human-written program in a restricted sequence language, whose structure (number of select/aggregate stages)
corresponds to transformer layers and heads. It is a complete, executable description of an algorithm the network
could implement, not a reading of what a particular trained network does.

## How they judged success
Test accuracy of transformers trained at the RASP-predicted size; accuracy drop when the model is made smaller than
predicted (tightness of the layer/head bound); qualitative match between learned attention maps and RASP selector
patterns; feasibility under attention supervision.

## What they found
At the predicted size, trained models reached high accuracy: reverse 99.99%, histogram with BOS 100%, double
histogram 99.58%, sort 99.96%, most-frequent 95.99%, Dyck-1 99.67%, Dyck-2 99.85%. Shrinking below the prediction
often hurt badly (reverse fell to 23.1% with one fewer layer; double histogram to 40.5%), but not always (sort
barely dropped, to 99.0%, because a bounded alphabet allows a counting shortcut). Learned attention matched the RASP
pattern fully for histogram with BOS, partially for several tasks, and not at all for sort, most-frequent and
Dyck-2: networks often found other solutions. With attention supervision, models reached over 99% on double
histogram, sort and most-frequent with RASP-like attention. Side results: restricted-attention variants that use
fewer than n log n operations cannot sort; a BOS token enables one-head counting; Dyck-k is solvable in a fixed
number of layers.

## Limitations and open problems they name
RASP says nothing about the embedding width needed. Conversion to actual weights is left out. The optimal Dyck-2
solution needs an extra theoretical operation (`select_best`). Only tasks a human can program are covered, so
language-model-scale behaviour is out of reach.

## What we take from it
A target language: RASP gives a vocabulary (select/aggregate/elementwise) in which a white-box reconstruction of a
small transformer could be written and executed to predict outputs. A warning: a network trained at the "right"
size frequently does not use the human program, so a hand-written program is a hypothesis, not a reading of the
weights. A measure: tightness tests (shrink the model, watch accuracy) are a cheap check on whether a claimed
algorithm's depth is really needed.

## Tags
unit: head, layer, whole-model
form: program
method: other
eval: downstream-task, ablation
goal: understanding, science
