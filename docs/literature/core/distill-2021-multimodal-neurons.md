# Multimodal Neurons in Artificial Neural Networks

- **Key:** distill-2021-multimodal-neurons
- **Authors / organisation:** Gabriel Goh, Nick Cammarata, Chelsea Voss, Shan Carter, Michael Petrov, Ludwig Schubert, Alec Radford, Chris Olah; OpenAI (Carter: Observable)
- **Date:** 2021-03-04
- **Link:** https://distill.pub/2021/multimodal-neurons/
- **Kind:** blog/research post
- **Read from:** full text (article prose extracted from the page's script bundle; interactive figures not inspected)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Neuroscience found single human neurons that respond to one person or concept across photos, drawings and written names. The authors ask whether CLIP's vision side has comparable abstract, multimodal units, how they combine to support zero-shot tasks, and what this implies for robustness and bias. It extends the circuits-style neuron study from early vision to the highest, most abstract layers of a large multimodal model.

## What they studied
CLIP ResNet vision encoders, chiefly RN50-x4 (with other CLIP variants for comparison), focusing on neurons in the last layers before the attention pooling. Units: individual neurons, linear combinations of neurons, and attribution vectors from text embeddings to vision neurons.

## How they did it
They label neurons with feature visualisation, including a new "faceted" variant that steers the visualisation toward a theme (text, faces, logos) using a linear probe trained on lower layers, plus text feature visualisation and dataset examples. For key neurons they build conditional probability plots: uniformly spaced activation buckets from most inhibitory to most excitatory, a fixed number of validation stimuli per bucket (requiring millions of passes for the tails), labelled into categories by a human blinded to activation. Region neurons are estimated by rendering words as images and checking how many of each neuron's top-five words are geographic. To connect neurons to tasks, they fit a sparse linear probe for ImageNet classes and approximate the final logit as a bilinear form between penultimate vision neurons and the text embedding, which yields attribution vectors from any word (e.g. emotion words) to vision neurons; they check these by boosting the top neuron on a blank image and confirming the matching word's logit rises. They then build typographic attacks (pasting text on images) and measure success on ImageNet validation images, and run a Stroop-style colour/word test with zero-shot classification.

## What counts as an explanation here
Neuron-level descriptions ("person", "emotion", "region" neurons) backed by activation-conditioned human labels, and, at the task level, sparse linear combinations of neurons (e.g. an emotion word as a sum of a few emotion neurons). The bilinear approximation is a simple surrogate for the vision-text interface that is partly verified by intervention.

## How they judged success
Blinded human labelling across activation buckets (more than 1,500 images labelled overall; over 400 for one neuron); precision-style conditional probability plots, with category-conditioned activation plots to address recall; sparse linear probe top-5 accuracy; activation-boost interventions confirming attribution vectors; typographic attack success rate (attack class becomes top-1, excluding images already in that class) versus the fraction of pixels changed.

## What they found
CLIP has neurons for specific people, emotions, regions, brands, holidays, art styles and more that fire for photos, drawings and rendered text alike. Roughly 4% of RN50-x4 neurons are regional by a conservative definition (2.5%, 64 neurons, have all five top words geographic). A sparse ImageNet probe using about 3 neurons per class reaches 56.4% top-5 and its neurons form a rough class hierarchy. Emotion-word attributions are sparse sums of emotion neurons; NMF of them recovers valence/arousal with two factors. The best typographic attacks reach 97% success while changing about 7% of pixels. They report biased associations (e.g. an image-based word embedding similarity of 0.52 between "Terrorist" and "Muslims") and "conjoined" polysemantic neurons. One East Africa neuron changes meaning between medium and strong activations.

## Limits and open problems they name
Feature visualisation was hard to make work on the largest CLIP models. Conditional probability plots show precision, not recall, and the labelling is subjective. The bilinear form is a strong approximation. Single neurons do not necessarily reflect overall model behaviour; many concepts live in combinations. Whether conjoined features are real or coincidental is open.

## What we take from it
Blinded, activation-bucketed labelling is a stronger feature test than top-k examples and should be our default for validating unit labels. The bilinear surrogate shows how a final layer can be read off as a weight matrix and then checked by a targeted intervention; we can reuse that pattern. Typographic attacks are a case where a mechanistic finding predicted a new failure mode, which is the kind of prediction our white-box model should make.

## Tags
unit: neuron | direction
form: description | dictionary
method: probing | attribution | other (feature visualisation, human labelling)
eval: human-rating | prediction/simulation | downstream-task
goal: understanding | safety/auditing
