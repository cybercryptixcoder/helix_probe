# AxBench: Steering LLMs? Even Simple Baselines Outperform Sparse Autoencoders

- **Key:** arxiv-2501.17148
- **Authors / organisation:** Zhengxuan Wu, Aryaman Arora, Atticus Geiger, Zheng Wang, Jing Huang, Dan Jurafsky, Christopher D. Manning, Christopher Potts; Stanford University (Geiger: Pr(AI)²R Group)
- **Date:** 2025-01
- **Link:** https://arxiv.org/abs/2501.17148
- **Kind:** benchmark
- **Read from:** full text (HTML version, v3; read in parts)
- **Relevance to us:** 3 (central)

## What they wanted, and why
SAEs are often justified by their usefulness for control and monitoring, but nobody had compared them directly with
plain prompting, finetuning, or simple supervised directions on the same tasks. The authors built a large benchmark
for two uses of concept representations, detecting a concept in text and steering generation toward it, to check
whether interpretability-derived methods actually beat cheap baselines. The broader goal is to hold interpretability
tools to downstream-utility standards.

## What they studied
Instruction-tuned Gemma 2 2B (layers 10, 20) and Gemma 2 9B (layers 20, 31), giving eight task settings. Concepts:
500 taken from Gemma Scope SAE feature labels (Concept500). Unit: one direction or intervention per concept.

## How they did it
For each concept, gpt-4o-mini generated 144 synthetic training examples and about 72 evaluation examples (with hard
negatives only in evaluation). Detection: each method scores tokens, max-pooled to a sequence score, judged by
AUROC (plus F1 under balanced and roughly 1%-positive settings). Steering: each method intervenes while the model
answers Alpaca-Eval instructions (10 per concept, 14 steering strengths); an LLM judge rates concept presence,
instruction relevance and fluency from 0 to 2, combined by harmonic mean so failure on any axis is penalised.
Methods: prompting, full finetuning, LoRA, LoReFT, linear probes, difference-in-means (DiffMean), PCA, linear
artificial tomography (LAT), supervised steering vectors, raw SAE features, SAEs with feature chosen by AUROC
(SAE-A), bag-of-words, and gradient attribution. They also proposed ReFT-r1, a weakly supervised rank-1 method that
jointly learns detection and steering, and released ReFT-r1 and DiffMean dictionaries at SAE scale.

## What counts as an explanation here
Not explanation per se: a concept direction is judged by whether it detects and controls the concept. The paper
treats "this feature means X" as a claim that should cash out in detection and steering performance.

## How they judged success
Detection AUROC (with paired t-tests), F1; steering harmonic-mean LLM-judge score and pairwise win rates; baselines
spanning prompting, finetuning and supervised linear methods.

## What they found
Detection (mean AUROC): DiffMean 0.942, probe 0.940, ReFT-r1 0.938, prompting 0.929, SAE-A 0.917, bag-of-words
0.914, raw SAE 0.695, PCA 0.652; the top three are not significantly different. Steering (mean score): prompting
0.894, LoReFT 0.741, SFT 0.676, LoRA 0.615, ReFT-r1 0.543, DiffMean 0.239, SAE 0.165, SAE-A 0.157, probe 0.098.
ReFT-r1 beats SAEs 88% of the time and is near prompting on 2B but not on 9B. Picking SAE features by detection
quality (SAE-A) does not improve steering, so good detection does not imply good control. Larger steering factors
monotonically hurt instruction following. Part of the SAE deficit is blamed on auto-interpretation labels that skew
to token-level concepts.

## Limitations and open problems they name
Supervised dictionary methods need the concept list in advance and depend on a good data generator; SAEs depend on
good concept labels. Steering by representation remains far behind prompting and finetuning; joint learning of
detection and steering looks like the way forward.

## What we take from it
A hard-nosed evaluation lesson: any claimed unit of a white-box model must be compared against cheap supervised
baselines (DiffMean, linear probes) and against prompting, or a reviewer will ask why we did not. Detection and
control come apart, which supports judging our model on prediction under intervention, not on correlational
labels. Concept500 and the harmonic-mean steering score are reusable benchmark components.

## Tags
unit: direction | feature
form: direction | steering | probe
method: SAE | steering | probing
eval: benchmark | downstream-task
goal: evaluation-of-methods | control/editing
