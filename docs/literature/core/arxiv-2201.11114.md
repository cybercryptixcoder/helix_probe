# Natural Language Descriptions of Deep Visual Features (MILAN)

- **Key:** arxiv-2201.11114
- **Authors / organisation:** Evan Hernandez, Sarah Schwettmann, David Bau, Teona Bagashvili, Antonio Torralba, Jacob Andreas; MIT CSAIL, Northeastern University, Allegheny College
- **Date:** 2022-01 (ICLR 2022)
- **Link:** https://arxiv.org/abs/2201.11114
- **Kind:** paper
- **Read from:** full text (main paper; appendices skimmed only)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Earlier automatic neuron labelling (NetDissect, compositional explanations) could only pick labels from a fixed concept
inventory, so it labelled few neurons and could not surface unexpected behaviour. The authors want open-ended,
compositional natural-language descriptions of vision neurons, and to show such descriptions are actionable for
analysis, auditing and editing. It is an early step toward automated, model-agnostic neuron description.

## What they studied
Vision models: AlexNet and ResNet152 (ImageNet and Places365 classifiers), BigGAN (generator), DINO ViT (self-supervised
MLP units); ResNet18 for applications; 12 models trained on face-blurred ImageNet. Unit: neurons (convolutional units and
ViT MLP units).

## How they did it
Each neuron is represented by its exemplar set: the 15 images with the highest activation, masked to regions above the
0.99 activation percentile. They collected MILANNOTATIONS: human descriptions for exemplar sets of 20k units from 7 models,
three annotators each (60k annotations). They train a captioner (Show-Attend-Tell variant) for p(description | exemplars)
and an LSTM language model for p(description), then choose the description maximising weighted pointwise mutual
information (log p(d|E) minus 0.2 log p(d)) among a beam of 50 captions, so labels are specific rather than generic.
Generalisation is tested by holding out neurons, architectures, datasets and tasks. Applications: ablate ResNet18
neurons ordered by properties of their descriptions (parts of speech, length, parse depth, semantic spread) and track
ImageNet accuracy; count face-selective neurons in blurred versus unblurred models; on a synthetic dataset with spurious
text labels, find "text" neurons by description and ablate them to improve adversarial accuracy.

## What counts as an explanation here
A free-form natural-language label per neuron, generated from its top exemplars. Partial: it summarises top activations
only and makes no activation-level predictions.

## How they judged success
BERTScore agreement with held-out human descriptions, against NetDissect, compositional explanations, and plain
captioning (p(d|E) only); accuracy curves under description-guided ablation versus random ablation; adversarial test
accuracy after editing versus an importance-sorted ablation control.

## What they found
MILAN agreed with humans better than baselines on held-out networks (BERTScore around 0.31-0.38 versus 0.21-0.25 for
NetDissect and 0.01-0.03 for compositional explanations), and PMI beat plain captioning. It generalised across
architectures (including CNN to ViT), datasets and tasks, with asymmetric transfer. Neurons described with adjectives or
prepositions (attributes, relations) mattered most to accuracy; neurons with semantically scattered descriptions mattered
less than random. Blurred-data models still had 142 face-selective neurons versus 213 in unblurred ones, some apparently
demographic-specific. In the spurious-text experiment MILAN found 300 text units of 1024; ablating 13 raised adversarial
accuracy by 4.9 points (from 58.8%), versus under 1 point when sorting all neurons by importance.

## Limits and open problems they name
Descriptions are partial and noisy, based on a fixed set of exemplars; exemplar-based explanation has known pitfalls;
human annotations are noisy; the captioner is itself a black box that may misbehave out of domain. Failure modes include
wrong concepts, vague labels, and describing context instead of the highlighted region.

## What we take from it
Background for language-based neuron labelling. Useful ideas: choosing descriptions by PMI (specificity relative to what
is generic across neurons) is a principled fix for overly broad labels, the same failure later seen in LLM explainers;
and "description-guided ablation" is a cheap way to test whether a label class tracks functional importance. Not
predictive in our sense.

## Tags
unit: neuron
form: description
method: other | ablation
eval: human-rating | ablation | downstream-task
goal: understanding | safety/auditing | control/editing
