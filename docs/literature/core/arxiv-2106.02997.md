# Causal Abstractions of Neural Networks

- **Key:** arxiv-2106.02997
- **Authors / organisation:** Atticus Geiger, Hanson Lu, Thomas Icard, Christopher Potts; Stanford University
- **Date:** 2021-06
- **Link:** https://arxiv.org/abs/2106.02997
- **Kind:** paper
- **Read from:** full text (arXiv HTML; the tail of the supplementary appendices was not covered)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors want to show that a neural network implements a specific, human-readable algorithm, not just that its
activations contain decodable information. They argue probes and attribution methods cannot establish causal role,
and propose instead to write the hypothesised algorithm as a high-level causal model, align its variables with
locations in the network, and test the alignment by intervening on both. This is a step toward explanations that
are themselves executable models, checkable by experiment.

## What they studied
Multiply Quantified NLI (MQNLI), a templated NLI dataset with quantifiers, negation and modifiers whose labels are
computed by a natural-logic algorithm (used as the high-level causal model, with 14 intermediate nodes). Splits:
500K train, 60K dev, 10K test on the hardest "fair" generalisation split. Models: BERT-base fine-tuned on MQNLI
(reading from [CLS]), a multilayer BiLSTM, and non-fine-tuned BERT as a baseline. Unit of analysis: hidden states
at specific (layer, token position) locations.

## How they did it
1. Write the task algorithm (natural logic) as a causal model with intermediate variables.
2. For each intermediate variable, list candidate network locations (hidden states above the relevant tokens, at
   each BERT layer), 14 x 11 = 154 alignment experiments.
3. Interchange intervention: take a base input and a source input; in the causal model, set the variable to its
   value under the source; in the network, replace the aligned hidden state with its value under the source.
4. The alignment succeeds on a pair if both models give the same output. Pairs where the intervention changes the
   label ("impactful") are the informative ones.
5. Sample 1,000 correctly classified examples (1M ordered pairs); build a graph where examples are connected when
   interventions succeed in both directions; the largest clique containing an impactful edge measures the subset on
   which the abstraction holds.
6. Compare with probes (accuracy and selectivity against a random-label control task) and integrated gradients.
A toy N+ network computing x + y + z illustrates the test on a known algorithm.

## What counts as an explanation here
A causal abstraction: a symbolic algorithm whose intermediate variables are mapped to network locations such that
intervening on a location has the same effect on output as intervening on the variable. It is meant to be a
complete algorithmic account but in practice holds only on subsets of inputs. It predicts the network's output under
counterfactual internal interventions.

## How they judged success
Task accuracy on MQNLI (vs. CBoW, TreeNN, BiLSTM, and the task-specific CompTreeNN as an upper bound); interchange
intervention success over example pairs; size of the largest consistent clique per aligned location; probe accuracy
and selectivity; integrated-gradients attributions with a Wilcoxon signed-rank test.

## What they found
Fine-tuned BERT reaches 88.25 dev / 88.50 test on MQNLI, above CompTreeNN (80.17 / 80.21) and far above BiLSTM
(46.4); without augmented subphrase training data it drops to about 55. For almost all nodes the natural-logic
model is an abstraction of BERT on a substantial subset of examples, much smaller subsets for the BiLSTM. One case
study localises the object noun-phrase relation to layer 4 above the object adjective token. Probes find the
information almost everywhere, while interventions single out few locations, so interventions are much more
discriminating than probes.

## Limits and open problems they name
Abstraction holds only on example subsets; intervention cost grows quadratically with the number of inputs; probe
control tasks break down for long subphrases and closed-class words; one dataset and two architectures; formal
treatment is deterministic.

## What we take from it
Central method: interchange interventions are a direct test of whether a proposed white-box model predicts the real
network's behaviour under internal intervention, which is exactly our success criterion. Measure: per-variable
intervention success over input pairs (later named interchange intervention accuracy). Warning: decodability by a
probe is nearly uninformative about causal role. Practical detail: restrict to impactful pairs, or a trivially
correct explanation looks good.

## Tags
unit: layer, direction
form: causal-abstraction
method: patching, probing, attribution
eval: patching, faithfulness
goal: understanding, evaluation-of-methods
