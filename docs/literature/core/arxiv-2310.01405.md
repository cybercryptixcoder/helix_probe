# Representation Engineering: A Top-Down Approach to AI Transparency

- **Key:** arxiv-2310.01405
- **Authors / organisation:** Andy Zou et al. (21 authors incl. Matt Fredrikson, Zico Kolter, Dawn Song, Sanmi Koyejo, Dan Hendrycks); Center for AI Safety, CMU, Stanford, UC Berkeley, Cornell, UMD, UPenn, UIUC, EleutherAI
- **Date:** 2023-10
- **Link:** https://arxiv.org/abs/2310.01405
- **Kind:** paper
- **Read from:** abstract and sections (main text and results; later appendices not read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors argue for a "top-down" alternative to mechanistic interpretability: instead of neurons and circuits,
take population-level representations of high-level concepts (truthfulness, utility, power-seeking, emotion) as the
unit, borrowing the Hopfieldian view from cognitive neuroscience. The goal is safety-relevant transparency and
control: read whether a model is being honest or harmful, and steer it, without understanding the full mechanism.

## What they studied
Mainly LLaMA-2-Chat 7B, 13B and 70B (base vs chat compared in an appendix); DeBERTa for comparison with CCS. Unit:
residual-stream activations at chosen layers and token positions, summarised as directions.

## How they did it
Linear Artificial Tomography (LAT), the reading baseline: (1) design stimuli, either prompts asking the model to
consider how much of a concept a statement contains, or paired instructions for doing vs not doing a function (e.g.
be honest vs lie); (2) collect activations at the last token (concepts) or across response tokens (functions);
(3) run PCA on differences between paired activations and take the first component as a "reading vector"; score new
inputs by dot product. Stimulus sets are small (5 to 128). Control methods: add or subtract the reading vector; a
"contrast vector" computed per input from the difference between activations under contrasting prompts; and LoRRA,
low-rank adapters trained so the representation moves by the contrast vector, which can be merged into weights.
Operators: linear combination, piecewise (conditional) addition, projection out. They frame evaluation as four
neuroscience-style tests: correlation, manipulation, termination (removal), recovery. Applications span honesty and
lie detection, utility, morality and power (MACHIAVELLI), emotion, harmlessness under jailbreaks, bias, fact
editing and memorisation.

## What counts as an explanation here
A direction (reading vector) for a named concept or function, found from contrastive stimuli, with the claim that
projecting onto it measures the concept and moving along it changes behaviour. Partial and concept-specific; no
mechanism. It predicts, in a coarse way, how behaviour shifts under control.

## How they judged success
TruthfulQA MC1 accuracy (against zero-shot likelihood, a verbalised-confidence heuristic, few-shot, CCS and linear
probes); accuracy on OpenbookQA, CommonsenseQA, RACE, ARC; classification accuracy of a lie detector on held-out
examples; MACHIAVELLI immorality and power scores with reward; jailbreak refusal rates; rates of demographic mentions
in generated medical cases; exact-match on memorised quotes; and the correlation/manipulation/termination/recovery
framework for comparing reading methods.

## What they found
- TruthfulQA MC1 (reading): LAT averages 56.8–60.7 versus 32.3 standard zero-shot. Control: LLaMA-2-Chat-7B goes from
  31.0 to 47.9 with contrast vectors and 42.3 with LoRRA; 13B from 35.9 to 54.0 (contrast) and 47.5 (LoRRA).
- An honesty direction separates held-out honest and dishonest examples with over 90% accuracy, but also fires on
  talk about lying.
- Comparing reading methods, logistic regression correlated best but steered least; PCA, K-means and mean difference
  were robust across correlation, manipulation and termination.
- Steering on MACHIAVELLI moves immorality and power scores in the intended direction with little reward change.
- A piecewise operator raised the helpful-and-harmless average under jailbreaks from 81.4 to 90.2 (manual) and from
  56.6 to 87.2 (adversarial).
- Subtracting a memorisation direction cut quote exact-match from 89.3 to 47.6 while leaving historical-year accuracy
  nearly unchanged (97.2% to 96.2%).

## Limits and open problems they name
Methods good for reading may be poor for control; correlation is not causation; LAT is a simple baseline that may not
suffice for complex or multi-step functions; contrast vectors cost extra inference and cascade across layers; some
directions had weak manipulation or removal effects; the immorality detector fired on benign text; the lie detector
needs more careful evaluation. Future work: trajectories, manifolds and state spaces rather than subspaces.

## What we take from it
- **Measure/framework:** correlation, manipulation, termination, recovery is a compact checklist for whether a found
  variable is real; "reads well" and "steers well" must be tested separately.
- **Warning:** the probe that best predicts a label is not the direction the model uses; supervised probes can
  mislead a white-box reconstruction.
- **Method:** contrastive stimulus pairs plus PCA on differences is a cheap way to get candidate directions to check
  against weight-derived ones.
- Less directly useful for reading weights: no mechanism, concepts are human-chosen.

## Tags
unit: direction
form: direction, steering, probe
method: probing, steering
eval: ablation, downstream-task, benchmark
goal: safety/auditing, control/editing
