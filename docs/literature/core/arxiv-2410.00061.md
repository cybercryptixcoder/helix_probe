# Neural Decompiling of Tracr Transformers

- **Key:** arxiv-2410.00061
- **Authors / organisation:** Hannes Thurnherr, Kaspar Riesen; Institute of Computer Science, University of Bern
- **Date:** 2024-10
- **Link:** https://arxiv.org/abs/2410.00061
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Manual reverse engineering of transformers does not scale, so the authors try to learn a decompiler: a model that
reads all of a transformer's weights and writes out the program it implements, in RASP, a language designed to map
onto transformer computation. The obstacle to learning such a mapping is the lack of (weights, description) pairs;
they get these by compiling random RASP programs to weights with Tracr. This is a proof of concept for automatic,
end-to-end weights-to-program interpretation.

## What they studied
About 533,000 randomly generated RASP programs (5 to 12 lines) and their Tracr-compiled transformers (8 to 42 weight
matrices each). Programs are built from Select, Aggregate, SelectorWidth, Map and SequenceMap, sampled in proportion
to their use in hand-written RASP, with rejection filters (compile errors, too many SequenceMaps, over 15 lines,
invalid aggregations). Unit: weights of the whole model, as input; program lines as output. No trained (gradient
descent) models were studied.

## How they did it
Each weight matrix is flattened into one input token, tagged with a descriptor (shape, layer, head, type: embedding,
MLP, query, key or value) and zero-padded; this matrix-level tokenisation beat layer-level and naive flattening.
Each program line is encoded as four one-hot slots (function plus three arguments). The decompiler ("TraDe") is a
Whisper-style encoder-decoder transformer (4 encoder and 4 decoder layers, width 512, 16 heads, feed-forward 2048,
dropout 0.2), tuned on token accuracy over a 28K validation set on one GPU. It is evaluated on 1,000 held-out
programs, both teacher-forced and fully autoregressive. A side analysis of 10,000 programs (1,000 random inputs
each) checks how often distinct programs compute the same function.

## What counts as an explanation here
A program: RASP source code that should compute the same function as the network. It is meant to be complete for the
whole model and, if correct, fully predictive (it can be executed on any input).

## How they judged success
Token accuracy; exact sequence match; share of outputs with at least 90% token accuracy; whether the output compiles;
and functional equivalence with the ground-truth program (same outputs on sampled inputs). Teacher-forced and
autoregressive decoding are compared. No external baselines.

## What they found
Teacher-forced: about 30% exact match, about 85% of programs at 90%+ token accuracy, about 60% compilable, about 41%
functionally equivalent. Autoregressive: exact match falls to 26% but compilable rises to 91% and functional
equivalence to 73%; the authors think self-consistency with its own earlier lines helps. Many "errors" are
equivalent rewrites. About 60% of sampled programs were functionally identical to some other program while only about
5% were string duplicates, so the target is ambiguous: different programs can compile to identical weights.

## Limits and open problems they name
Tracr weights are sparse and structured, unlike trained weights, so transfer is unclear. The decompiler is about three
orders of magnitude larger than the models it reads. RASP is still hard for humans to read. Token accuracy may not
reflect interpretive value. Only in-distribution test programs are used. Future work: compressed Tracr models with
trained matrices, detecting targeted properties (e.g. backdoors) rather than whole programs, and attribution over
which weight matrices drive each output line.

## What we take from it
A framing and a measure: "explanation = executable program read from weights", scored by functional equivalence (run
both on inputs) rather than string match, which is exactly a predictive check. A dataset trick: compile known
programs to get ground-truth weights for training and validating weight readers. Warnings: equivalent programs make
exact-match metrics misleading; and compiled weights are far from trained ones, so any weight reader validated on
Tracr needs a trained-model test before we rely on it.

## Tags
unit: weights | whole-model
form: program
method: weight-analysis | other (learned decompiler)
eval: prediction/simulation | benchmark
goal: understanding | evaluation-of-methods
