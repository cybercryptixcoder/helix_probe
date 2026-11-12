# Editing Models with Task Arithmetic

- **Key:** arxiv-2212.04089
- **Authors / organisation:** Gabriel Ilharco, Marco Tulio Ribeiro, Mitchell Wortsman, Suchin Gururangan, Ludwig Schmidt, Hannaneh Hajishirzi, Ali Farhadi; University of Washington, Microsoft Research, Allen Institute for AI
- **Date:** 2022-12
- **Link:** https://arxiv.org/abs/2212.04089
- **Kind:** paper
- **Read from:** full text (HTML, first ~100k of ~104k characters)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors want a cheap, training-free way to steer what a pretrained model can do after the fact: remove a behaviour, add capabilities, or transfer a skill to a domain with little data. Their proposal is that the weight change produced by fine-tuning on a task is itself a reusable object, a "task vector", that can be scaled, negated and added like a vector. The larger goal is modular model editing where skills are composed in weight space rather than by retraining. It is not an interpretability paper in the mechanistic sense, but it makes a strong empirical claim that weight differences carry composable, task-level meaning.

## What they studied
CLIP image encoders (ViT-B/32, ViT-B/16, ViT-L/14) on eight classification tasks (Cars, DTD, EuroSAT, GTSRB, MNIST, RESISC45, SUN397, SVHN) with ImageNet as control, plus OCR and celebrity identification; GPT-2 Small/Medium/Large fine-tuned on toxic Civil Comments, with WikiText-103 perplexity as control; T5 small/base/large on GLUE (MRPC, RTE, CoLA, SST-2) and Yelp/Amazon sentiment. Unit: the full parameter vector (difference between fine-tuned and pretrained weights).

## How they did it
A task vector is defined as fine-tuned weights minus pretrained weights. A model is edited by adding lambda times a task vector (or a sum of them) to the pretrained weights, with lambda chosen on held-out validation data. Three operations are tested. Negation subtracts a task vector to make the model forget a task (e.g. a classification task, or toxic generation), and is compared with gradient-ascent fine-tuning and with a random vector of matched per-layer norm. Addition sums several task vectors to build a multi-task model, compared with individually fine-tuned models and joint multi-task training; they also use task vectors downloaded from the Hugging Face Hub. Analogies combine vectors as tau_C + (tau_B - tau_A) to improve a target task D with little or no labelled data (e.g. sentiment on Yelp from Amazon; "sketch lion" subpopulations; king/queen). They then analyse cosine similarity between task vectors, how quickly the direction of intermediate-checkpoint task vectors converges, sensitivity to learning rate and seed, and the link between adding two vectors and output ensembling.

## What counts as an explanation here
Not an explanation of mechanism. The object is a direction in weight space that stands for a task; its "meaning" is defined operationally by what happens to behaviour when it is added or subtracted. It does predict, coarsely: the sign and scale of a task vector predict gain or loss on that task with small collateral change.

## How they judged success
Accuracy on target and control tasks (ImageNet), normalized accuracy relative to individually fine-tuned models, percent toxic generations and mean Detoxify score with WikiText-103 perplexity as control, GLUE metrics, ROUGE-2/exact match. Baselines: gradient ascent, random matched-norm vector, fine-tuning on non-toxic data, joint multi-task training. Pearson correlation between task-vector addition and ensembling accuracy.

## What they found
Negation on ViT-L/14 drops average target accuracy from 64.8% to 19.0% while ImageNet falls only from 75.5% to 72.9%; gradient ascent reaches similar forgetting but drops ImageNet to 16.3%; random vectors barely change anything. For GPT-2 Large, negating the toxic vector cuts toxic generations from 4.8% to 0.8% with perplexity rising from 16.4 to 16.9 (gradient ascent destroys perplexity). Adding all eight image task vectors gives 91.2% normalized accuracy versus 99.4% for joint training; pairs reach 98.9%. Analogies help: e.g. ViT-L/14 reaches 100% on a queen-recognition target with no data for it, and subpopulation analogies add about 3.4 points. Task vectors are close to orthogonal, with higher similarity between related tasks (digit tasks; satellite tasks); intermediate-checkpoint vectors point in nearly the final direction early. Addition of two vectors tracks ensembling with correlation 0.99.

## Limits and open problems they name
Requires identical architecture and pretrained initialization; new heads are out of scope. Negation is weaker when fine-tuning gave little gain or the behaviour is already strong. Scaling coefficients must be tuned on validation data and one shared coefficient is a simplification. Higher fine-tuning learning rates hurt composability. Overlap between target and control semantics limits clean forgetting.

## What we take from it
A framing and a baseline: weight differences between related checkpoints are a usable, roughly linear, roughly orthogonal unit of meaning, so "reading" a fine-tune can start from its delta. The near-orthogonality and the strong ensembling correlation suggest that a white-box model could predict the effect of combined edits from separate ones. Reusable controls: a random matched-norm vector as a null edit, and a held-out control task to measure collateral damage. Warning: the semantics is purely behavioural; nothing here says which parts of the delta do what.

## Tags
unit: weights | whole-model
form: direction
method: weight-analysis | other
eval: downstream-task | ablation
goal: control/editing
