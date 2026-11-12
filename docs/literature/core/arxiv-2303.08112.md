# Eliciting Latent Predictions from Transformers with the Tuned Lens

- **Key:** arxiv-2303.08112
- **Authors / organisation:** Nora Belrose, Igor Ostrovsky, Lev McKinney, Zach Furman, Logan Smith, Danny Halawi, Stella Biderman, Jacob Steinhardt; EleutherAI, FAR AI, University of Toronto, Boston University, UC Berkeley
- **Date:** 2023-03 (read v6, updated 2025-11)
- **Link:** https://arxiv.org/abs/2303.08112
- **Kind:** paper
- **Read from:** full text (HTML v6; some appendices skimmed)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors treat each transformer layer as refining a latent next-token prediction ("iterative inference") and
want a reliable way to read that latent prediction at every layer. The logit lens does this with no training but is
biased, unreliable on some model families, and confused by the residual basis drifting across layers. They want a
lens that is accurate, minimally biased, and causally faithful to what the model actually uses, and then to show it
is useful for downstream tasks such as detecting malicious inputs.

## What they studied
GPT-2, GPT-Neo (up to 2.7B), BLOOM 560M, OPT 125M, Pythia (160M, 410M, 12B), GPT-NeoX-20B and Vicuna 13B; up to
20B parameters. Unit: the residual stream at each layer. Data: Pile validation data (or model validation sets),
documents chunked to 2048 tokens; evaluation on about 16.4M tokens.

## How they did it
For each layer, train an affine "translator" (a d×d matrix plus bias, initialised at the identity) applied to the
hidden state before the model's own final norm and unembedding; nothing else is learned. The loss is KL divergence
from the model's final-layer distribution to the lens distribution, i.e. distillation, so the probe is not given
labels it could learn on its own. Training used SGD with Nesterov momentum (250 steps, 2^18 tokens per batch); a
later update reports Muon trains much better and that the SGD lenses were undertrained, but not all experiments
were re-run. They compare with the logit lens on perplexity and on bias (KL between the lens's marginal token
distribution and the model's). They test transfer of a translator to neighbouring layers and to fine-tuned models.
For causal faithfulness they introduce causal basis extraction (CBE): sequentially find orthogonal directions whose
mean-ablation most changes the lens output, then check how much ablating the same directions changes the model's
actual output. They also test "stimulus-response alignment": whether a perturbation changes lens and model outputs
in the same direction (an Aitchison inner product on the probability simplex). Applications: prompt-injection
detection from the trajectory of latent predictions across layers, using isolation forest and local outlier factor
fit only on normal prompts; and "prediction depth" as a measure of example difficulty.

## What counts as an explanation here
A set of per-layer affine readouts that turn any hidden state into a next-token distribution: a decoder of the
model's current best guess. It is partial (only the next-token prediction is read, not why), but it is checked for
causal relevance, and the lens trajectory is used as a predictive feature.

## How they judged success
Perplexity of lens predictions against model outputs; bias as KL between marginal distributions (in bits); transfer
penalty in cross-entropy; Spearman correlation between a CBE feature's influence on the lens and on the model;
stimulus-response alignment; AUROC with bootstrap confidence intervals for prompt-injection detection (baseline:
SRM, plus logit-lens versions of the same detectors); Spearman correlation between prediction depth and training
step at which an example is learned. Baseline throughout: the logit lens.

## What they found
- Tuned-lens predictions have much lower perplexity than logit-lens ones across models and layers. Logit-lens bias for
  GPT-Neo-2.7B is about 4–5 bits at most layers; the tuned lens is far less biased.
- Translators transfer to nearby layers with small penalties, which track covariance similarity (Spearman −0.78), and
  transfer to fine-tuned models with little loss (worst case about 0.3 bits per byte on RedPajama).
- In Pythia 410M layer 18, a feature's influence on the lens correlates with its influence on the model (Spearman
  0.89); no direction was found that mattered to the lens but not the model.
- Prompt injection (Pythia 12B): tuned-lens detectors reach AUROC near 1.0 on BoolQ, MNLI, QNLI, QQP and SST-2, beat
  logit-lens detectors, and are comparable to SRM, which is stronger on some tasks.
- Prediction depth under the tuned lens correlates better with learning order than under the logit lens on 8 of 11
  tasks.

## Limits and open problems they name
One translator per layer must be trained (cheap, under an hour on one 8×A40 node). CBE is expensive because
directions are optimised one at a time and the search is non-convex. Causal tests assume features are directions.
Earlier lenses were undertrained. Transfer is asymmetric and limited by covariance drift. Only language models were
studied.

## What we take from it
- **Method:** a layer-wise readout trained by distillation to the model's own output, with the explicit rule that the
  probe should not learn new information. Useful as a reference decoder for any intermediate state our white-box
  model claims to compute.
- **Measure:** check a readout's causal faithfulness by asking whether the directions it depends on are the ones the
  model depends on (CBE plus correlation of influence). This is a reusable template for checking that a reconstructed
  component reads the same information the real one does.
- **Framing:** a trajectory of per-layer predictions is itself predictive (anomaly detection, difficulty).
- **Warning:** the logit lens is biased; any weight-reading via the unembedding should be checked against a tuned
  alternative.

## Tags
unit: layer
form: probe
method: probing
eval: faithfulness, ablation, downstream-task, prediction/simulation
goal: understanding, safety/auditing
