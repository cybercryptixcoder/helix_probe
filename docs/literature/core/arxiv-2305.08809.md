# Interpretability at Scale: Identifying Causal Mechanisms in Alpaca

- **Key:** arxiv-2305.08809
- **Authors / organisation:** Zhengxuan Wu, Atticus Geiger, Thomas Icard, Christopher Potts, Noah D. Goodman; Stanford University
- **Date:** 2023-05
- **Link:** https://arxiv.org/abs/2305.08809
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Causal abstraction lets one test whether a human-readable algorithm is actually implemented by a network, but its
existing tool, Distributed Alignment Search (DAS), needed a brute-force search over how many dimensions encode each
variable and had only been run on small models. The authors want to test interpretable algorithmic hypotheses on a
7B instruction-tuned LLM. The larger goal is faithful, causally verified explanations of large models, with
alignments robust enough to trust across input variations.

## What they studied
Alpaca 7B (instruction-tuned LLaMA; 32 layers, hidden size 4096). Task "Price Tagging": answer yes/no whether a
dollar amount falls in a bracket, amounts and bounds in [0.00, 9.99], bracket width in [2.50, 7.50]; Alpaca gets
about 85% right. Unit: learned non-basis-aligned subspaces of the residual stream at a given layer and token
position.

## How they did it
Four candidate high-level causal models were written: Left Boundary (one boolean, above the lower bound), Left and
Right Boundary (two booleans combined by AND), Mid-point Distance, and Bracket Identity. For a chosen layer and
token position, Boundless DAS learns an orthogonal rotation of the 4096-d representation plus a learned soft
boundary per causal variable selecting which rotated dimensions encode it; the mask is sharpened to binary at
evaluation. Training uses interchange interventions: run a base and a source input, swap the rotated subspace for a
variable from source into base, and train (model frozen, only rotation and boundaries updated) with cross-entropy
against what the causal model predicts under the same swap. This cuts search cost from O(n*m) to O(m). Data: 20K
training pairs, 1K held-out test; Adam, 3 epochs, 3 seeds (best reported); about 1.5 h per run on one A100. They
swept layers and positions, then tested alignments under distribution shift.

## What counts as an explanation here
A causal abstraction: a small symbolic program (two boolean comparisons then AND) plus an alignment map from each
program variable to a learned subspace of the network. It is predictive: it says what the network will output
after any swap of those variables between inputs. Partial, covering one task.

## How they judged success
Interchange intervention accuracy (IIA): fraction of held-out interventions where the network's output matches the
causal model's counterfactual output. Controls: random rotations (IIA about 0.50 for boundary models, about 0.60
otherwise); Boundless DAS run on a randomly initialised LLaMA-7B (IIA 0 to 69%, near a majority-label baseline,
dropping to 0 on robustness checks). Structure of IIA across layers and positions as a sanity signal. Robustness:
unseen brackets, irrelevant GPT-4-generated prefixes, changing the output vocabulary from yes/no to True/False,
correct-only versus incorrect-only inputs, reported as IIA and correlation with the main heat maps.

## What they found
Left Boundary and Left-and-Right Boundary hypotheses reached max IIA of about 0.90 and 0.86, at or above task
accuracy, with clean structure (strongest near layer 10 at the last input token); Mid-point Distance and Bracket
Identity peaked around 0.72 with unstructured patterns, so were rejected. At the best site, the Left-and-Right model
drops from 0.83 to 0.53 with a random rotation. Successful alignments used only about 5 to 10% of dimensions.
Alignments generalised: unseen bracket 0.95, irrelevant context about 2 points lower (correlation 0.99), True/False
outputs 0.83, incorrect-only inputs 0.71.

## Limits and open problems they name
Failing to find an alignment does not prove absence (search is not exhaustive; non-linear encodings missed). Only
hypotheses the authors thought of were tested. IIA cannot reach 100% when task accuracy is below 100% unless the
causal model also explains errors. Full-layer alignments are infeasible (rotation matrix too large). Weak multi-step
reasoning in 7B to 30B models limited task choice.

## What we take from it
The clearest template for a predictive white-box claim: write a program, align its variables to network subspaces,
and score with IIA on held-out counterfactual pairs, with random-rotation and random-init controls (these controls
matter: learned rotations can fit something even in an untrained model). Our weight-derived model can be scored the
same way, and competing hypotheses compared by IIA. Warning: learned alignments are expressive enough to overfit, so
held-out and robustness splits are required.

## Tags
unit: direction | layer
form: causal-abstraction | program
method: patching | decomposition | other
eval: patching | prediction/simulation | faithfulness
goal: understanding | science
