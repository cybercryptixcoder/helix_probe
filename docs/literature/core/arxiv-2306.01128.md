# Learning Transformer Programs

- **Key:** arxiv-2306.01128
- **Authors / organisation:** Dan Friedman, Alexander Wettig, Danqi Chen; Princeton University
- **Date:** 2023-06
- **Link:** https://arxiv.org/abs/2306.01128
- **Kind:** paper
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Tracr compiles human-written programs into transformers, but that only covers algorithms people already know. The
authors want the reverse: train a transformer by gradient descent under constraints that guarantee it can be
converted exactly into a readable Python program. This makes interpretability a property of the architecture
rather than something recovered after the fact, and lets the learned program be inspected with ordinary software
tools.

## What they studied
"Transformer Programs": constrained transformers trained from scratch on a toy in-context-learning task, seven RASP
algorithmic tasks (histogram, sort, reverse, Dyck, most-frequent, double histogram, etc.), CoNLL-2003 named entity
recognition, and text classification (TREC, MR, Subj, AG News). Unit of analysis: named variables in a disentangled
residual stream, categorical/numerical heads, and lookup-table MLPs.

## How they did it
The residual stream is split into named categorical variables; each module reads a fixed set of variables chosen
by one-hot gates and writes to its own new subspace. Categorical attention heads use a one-to-one predicate between
query and key values with hard attention (attend to BOS if nothing matches, the nearest match if several do);
numerical heads sum bounded integers for counting. MLPs are small lookup tables over two input variables. The
discrete choices are relaxed with Gumbel-softmax and the temperature annealed during training. After training, the
most likely discrete weights are taken and each module is written out as Python (predicate functions plus calls
like select-closest and aggregate). They compare accuracy with standard unconstrained transformers and a unigram
baseline, then analyse the programs with debuggers, static analysis and pruning.

## What counts as an explanation here
The network is its own explanation: an executable Python program that is exactly equivalent to the trained model,
not an approximation. Complete by construction, and it predicts every output.

## How they judged success
Held-out accuracy (or F1 for NER) of the program versus standard transformers of comparable size and a unigram
baseline; qualitative analysis of the extracted code (does it reveal interpretable mechanisms); code length before
and after pruning.

## What they found
The in-context learning task was solved perfectly with an induction-head-like program. On short-input RASP tasks,
five of seven exceeded 99% accuracy; double histogram reached 98.4% and most-frequent 75.69%. Standard transformers
were generally better except on histogram-type tasks, and on the hardest setting (longer inputs, bigger vocabulary)
programs trailed by more than 50 points. On CoNLL-2003 NER the program scored F1 76.1 versus 70.5 for a standard
transformer and 66.2 for unigram. On classification, standard vs program: TREC 88.6 vs 85.6, MR 77.2 vs 77.9, Subj
92.3 vs 93.0, AG News 91.7 vs 90.8. Programs could be stepped through in a debugger; the NER program, for example,
boosts a location tag after prepositions like "at". Static pruning shrank the Dyck-1 program from 9,975 to 892 lines.

## Limitations and open problems they name
Optimisation is the main obstacle: programs struggle on longer inputs, and a Reverse case study points to attention
layers being hard to train. Learned programs use more layers and heads than human solutions and can still be long
and convoluted. The constraints that make programs readable also reduce expressivity.

## What we take from it
An existence proof that an exact network-to-program mapping is possible when the architecture is constrained, and a
concrete format (Python with select/aggregate primitives) for a predictive white-box model. A warning: even exact
programs can be thousands of lines, so "it is a program" is not the same as "it is understood"; pruning and static
analysis are needed. A possible bridge: distil a black-box network into a Transformer Program and score agreement,
which would make the program a replacement model whose fidelity can be measured.

## Tags
unit: head, layer, whole-model
form: program
method: training-interpretable
eval: downstream-task, benchmark
goal: understanding, debugging
