# Compositional Explanations of Neurons

- **Key:** arxiv-2006.14032
- **Authors / organisation:** Jesse Mu, Jacob Andreas; Stanford University, MIT CSAIL
- **Date:** 2020-06 (NeurIPS 2020)
- **Link:** https://arxiv.org/abs/2006.14032
- **Kind:** paper
- **Read from:** full text (main paper; appendices not read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
NetDissect labelled each neuron with the single best-matching concept from a labelled probing dataset, but neurons often
respond to combinations of concepts or to unrelated concepts. The authors extend this to logical formulas over concepts,
to describe neurons more precisely and to ask: what abstractions do neurons learn, does neuron interpretability relate to
model accuracy, and can explanations be used to predictably manipulate model behaviour?

## What they studied
Vision: the final 512-unit convolutional layer of a ResNet-18 trained on Places365, probed with 1,105 Broden/ADE20k
concepts (scenes, objects, parts, colours) using pixel masks. NLP: a BiLSTM NLI model trained on SNLI, probing the 1,024
neurons of the penultimate MLP layer on 10K validation pairs, with concepts for the 2,000 most common words and POS tags in
premise or hypothesis plus lexical-overlap levels. Unit: neurons.

## How they did it
Each neuron's activations are binarised (top 0.5% per neuron in vision; above zero for post-ReLU NLI units, restricted to
neurons active at least 5% of the time). Primitive concepts are binary masks over inputs. Candidate explanations are
logical forms built with AND, OR, NOT (and, for NLI, a NEIGHBORS operator that ORs the 5 nearest GloVe words). Beam search
(beam 10) grows formulas up to a maximum length, keeping those with the highest intersection-over-union between neuron
mask and formula mask. They then (a) manually categorise 128 vision neurons' length-10 explanations, (b) correlate each
neuron's IoU with model accuracy on inputs where it fires, and (c) use explanations of neurons with large final-layer
weights to hand-craft "copy-paste" adversarial inputs (pasting an image patch or inserting a word) and check that
predictions shift as predicted, including across other architectures.

## What counts as an explanation here
A logical formula over labelled primitive concepts that approximates the set of inputs where a neuron is active. It is
explicit and checkable, a small program, but it predicts only binary firing and only within the concept vocabulary.

## How they judged success
IoU between neuron mask and formula as a function of formula length (length 1 equals NetDissect); significance testing of
IoU gains; manual categorisation; Pearson correlation of IoU with conditional model accuracy; success of copy-paste
adversarial examples in changing predictions.

## What they found
Vision mean IoU rose from 0.059 at length 1 to 0.099 at length 10 (a 68% increase, p = 2e-9), with diminishing returns
after; NLI IoU kept rising past length 30. Of 128 sampled vision neurons, 69% learned meaningful combinations
(abstractions or specialisations such as water OR river AND NOT blue), 31% were polysemantic. NLI neurons encoded
shallow heuristics (gender words, "nobody", "sitting", lexical overlap). IoU correlated positively with accuracy in vision
(r = 0.31) but negatively in NLI (r = -0.60): well-explained NLI neurons implement spurious rules. Explanations enabled
copy-paste adversarial examples, some transferring to AlexNet, ResNet-50 and DenseNet-161.

## Limits and open problems they name
Explanations are bounded by the concept inventory and much behaviour remains unexplained; only penultimate layers were
studied; neuron-level analysis misses distributed concepts. Open questions: can the formulas serve as drop-in
replacements for neurons (distilling the model into a classifier over concept detectors), how concepts compose across
layers, and whether interpretability can be used as a training regulariser.

## What we take from it
A clean, checkable explanation format (a symbolic program over concepts, scored by IoU) and an explicit statement of the
drop-in-replacement question we care about. Warns that high explanation quality can signal a spurious heuristic, not good
computation. The copy-paste test is a simple form of intervention-based validation: an explanation is useful if it lets
you predict the effect of an input edit.

## Tags
unit: neuron
form: program | description
method: probing | other
eval: faithfulness | downstream-task | human-rating
goal: understanding | debugging
