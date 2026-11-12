# Weight Banding

- **Key:** distill-2020-circuits-weight-banding
- **Authors / organisation:** Michael Petrov, Chelsea Voss, Ludwig Schubert, Nick Cammarata, Gabriel Goh, Chris Olah; OpenAI (Distill Circuits thread)
- **Date:** 2021-04-08
- **Link:** https://distill.pub/2020/circuits/weight-banding/
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 1 (background)

## What they wanted, and why
Most circuits work studies individual neurons or small circuits. This article studies a structural phenomenon visible across a whole layer's weights: in the final convolutional layer of many vision models, weights form horizontal bands. The authors want to know what causes it, as an example of how larger-scale weight structure can be explained and could feed a higher-level account of networks.

## What they studied
InceptionV1 (mixed_5b, and mixed_5c 5x5 in retraining), ResNet50 (last 3x3 conv), VGG19 (conv5), AlexNet (no banding), and a simplified ImageNet CNN (six conv groups, L2 pooling, global average pooling to 512 values, then a 1001-way FC layer) that reliably bands at layer 5b. Unit: weights of a whole layer.

## How they did it
They visualised each neuron's incoming spatial weights by reducing them with NMF to three factors shown as RGB, sorting neurons by similarity. They then retrained the simplified network under architectural and data changes: rotating input images 90 degrees; replacing global average pooling with a full fully-connected layer over all positions; pooling only over the x-axis; and variants with learned spatial masks, attention, CoordConv channels, grouped FC layers, and global max pooling. They then retrained InceptionV1, ResNet50 and VGG19 from scratch on ImageNet (90 epochs) with rotation and with GAP removed.

## What counts as an explanation here
A causal account of a weight pattern: which architectural choice (global average pooling) and which data property (vertical position matters in ImageNet) produce it, established by interventions on training. Qualitative, partial.

## How they judged success
Presence, absence or orientation of banding in the visualised weights after each training intervention (qualitative visual inspection; no quantitative banding metric reported).

## What they found
Banding appears consistently in the last conv layer of models with global average pooling. Rotating inputs makes the bands vertical. Removing GAP removes banding (with 49x more FC parameters and overfitting) in the simple net, InceptionV1 and ResNet50, but not VGG19. X-only pooling removes banding from 5b but it reappears in 5a. Banding survives many alternatives (learned masks, attention, CoordConv, max pooling). Hypothesis: banding is a learned way to preserve spatial (vertical) information that pooling would otherwise destroy.

## Limits and open problems they name
Whether banding is good or bad; whether spatial information could flow more efficiently; why VGG19 keeps banding without GAP and why AlexNet lacks it; untested ideas (combining x- and y-pooling, random rotation as regulariser).

## What we take from it
A method template: some weight structure is explained by architecture and data statistics, not by task features, and can be tested by retraining with controlled interventions. When reading weights, we should expect and factor out such layer-wide "bookkeeping" structure (e.g. positional information storage) before interpreting features. Also an example of NMF as a weight visualisation tool.

## Tags
unit: weights | layer
form: description | other (causal account of weight structure)
method: weight-analysis | other (retraining interventions)
eval: ablation (architectural interventions)
goal: science | understanding
