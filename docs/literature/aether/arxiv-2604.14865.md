# Segment-Level Coherence for Robust Harmful Intent Probing in LLMs

- **Key:** arxiv-2604.14865
- **Authors / organisation:** Xuanli He; Bilgehan Sel; Faizan Ali; Jenny Bao; Hoagy Cunningham; Jerry Wei — University College London; Virginia Tech; Anthropic
- **Date:** 2026-04-16
- **Link:** https://arxiv.org/abs/2604.14865
- **Kind:** paper
- **Read from:** full text (HTML body through conclusion; appendices referenced but not read in full)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Streaming probes that watch a model's internal activations while it generates are the cheap alternative to running a
separate classifier model for safety, but they make a specific class of mistake: a benign expert conversation about
dangerous chemistry or biology contains the same vocabulary as a genuinely harmful request, so a probe that keys on
one or two surprising tokens fires constantly on legitimate text. The authors argue this is not a data problem (prior
work already trained on plenty of benign in-domain text) but a problem with *how token-level evidence is pooled into
a sequence-level verdict*. Their goal is to change the aggregation rule so that a positive prediction requires
several parts of the exchange to agree, and to measure whether that holds up on the hard low-false-positive regime
that deployment actually cares about.

## What they studied
Three open instruction-tuned families as probe backbones — Llama-3.1-8B-Instruct, Qwen3-8B, gemma-2-9b-it, plus
Qwen3-14B/32B in an appendix — and five data settings: two CBRN cases (a bio-domain reconstruction/obfuscation attack
set with a WildChat-harmless negative pool and an in-house biology conversation set; a chemical-warfare-agent suite
with synthetic positives and negatives drawn from chemistry and general benchmarks) and a set of generic
high-stakes datasets from prior work. The unit of analysis is a linear probe over per-token, all-layer *concatenated*
activations, with residual stream vs. attention output vs. MLP output varied as the representation choice. Labels exist
only at exchange level; predictions are required token-by-token.

## How they did it
They keep the sliding-window mean over the last 16 token logits from a production streaming-probe baseline, then
replace the softmax-weighted pooling that sits on top of it. The first change takes the average of the K highest
window scores instead of a confidence-weighted sum — so a positive requires K separate windows to be high, and a
sequence can only be called benign when even its K most suspicious windows are jointly low. The second change adds a
soft variance penalty over the probe's own evidence: weights derived from the window scores give a weighted mean and
variance of the logits, and penalising that variance pushes neighbouring evidence the probe selected toward similar
values, discouraging a single sharp spike. Crucially the variance term is applied only to benign exchanges, on the
argument that real harmful exchanges can legitimately present evidence in two disjoint regions (request, then
elaboration) and smoothing those away destroys the signal. They ablate this choice explicitly, applying it to all
instances as a comparison. Training is ordinary sequence-level binary cross-entropy; inference adds an exponential
moving average over the streaming scores. Headline comparison is against mean, softmax, attention, rolling-mean-
attention and the sliding-window-mean probes, plus a LoRA-fine-tuned classifier as a high-capacity reference.

## What counts as an explanation here
Nothing mechanistic — the probe is a detector, not an account of the behaviour. What it *does* contribute is a claim
about the shape of the internal evidence for harmfulness: it is carried by several coherent, contiguous stretches of
the exchange rather than by single tokens, and the authors try to build that shape into the training objective
rather than read it out afterwards. The falsifiable content is the ablation table: if the pooling rule matters, the
Top-K and variance-regularised variants must beat confidence-weighted max-like pooling, and the residual stream must
not already contain everything.

## How they judged success
AUROC, TPR at a fixed 1% false-positive rate, and log-space AUROC (ROC area with the false-positive axis on a log
scale), the last chosen as the default because it concentrates on the operating range a deployed monitor uses. Mean
± standard deviation over repeats. Ablations: aggregation rule × variance-regularisation on/off × variants applied to
negatives only vs. all instances, across three backbones. Representation ablation: residual vs. attention vs. MLP
outputs. Parameter-count comparison against the LoRA classifier. Robustness test: probes frozen, backbone fine-tuned
on five character-level ciphers, performance measured on the obfuscated inputs.

## What they found
At 1% FPR the new objective raises true-positive rate by 35.55% relative to the strongest streaming baselines, and on
a baseline already at 97.40% AUROC it removes 31.2% of the remaining error margin, with 16.80% gain in log-space
AUROC. The chemical domain is where the margin is biggest (log-space AUROC gains of 4.0%, 7.9% and 1.6% over the
prior streaming objective on Llama-3.1, Qwen3 and Gemma2); on generic high-stakes data the gains shrink to a fraction
of a point and the method trails the strongest baseline slightly, which the authors attribute to the generic
constitutions being broad and the examples being roughly ten times shorter, giving streaming little to accumulate.
Ablations show Top-K pooling alone beats confidence-weighted pooling on every backbone, variance regularisation helps
when applied to negatives only and *hurts* when applied to positives. Residual-stream probes are consistently the
weakest representation: attention wins on bio for Llama and Gemma, MLP wins on Qwen3 bio and on chemical for all
three backbones, with chemical gains over residual of 12%, 6.6% and 10.9%. The probe (262K parameters, one linear
layer) matches a LoRA classifier on bio and beats it on chemical while being over 300× smaller. With the backbone
frozen the probes are at chance on ciphered input; after cipher-tuning the backbone, the *same* probes reach 98.85%
AUROC against a 99.90% plain-text ceiling, without retraining.

## Limits and open problems they name
The threat model is static: no adversary optimises against the streaming objective itself, and they expect
segment-coherence to be attackable by diluting it with benign scaffolding or by slowly attenuating activations.
Long, terminology-dense professional dialogue still degrades performance — coherent technical discussion can look
like coherent planning — and they call for hierarchical discourse-level modelling with uncertainty-aware smoothing.
Prompt injection across retrieved documents or multiple tool inputs is flagged as an untested generalisation where no
single segment carries the harm.

## What we take from it
- **Warning:** an input-free readout of "how suspicious is this text" is only as good as its pooling rule; a
  confidence-weighted maximum over tokens is a keyword detector in disguise. Any probe we train should be evaluated
  at a fixed low false-positive rate and with an explicit alternative pooling rule.
- **Measure:** log-space AUROC and TPR@1%FPR as the primary numbers, standard AUROC as the secondary. This is the
  right shape for our evaluation section: a monitor that looks great at 97% AUROC can be useless at deployment
  precision, and the log-scale metric exposes that.
- **Method (as a design constraint on our white-box model):** "harmful" is not a point property of a token but a
  property of an extended span, so a mechanism that claims to explain the verdict should name *where* in the
  sequence the evidence sits. That is a directly testable prediction — patch or ablate a candidate evidence region and
  the verdict should move; patch an equally suspicious keyword elsewhere and it should not.
- **Finding worth reusing:** attention and MLP outputs beat the residual stream for probing, and the winner varies by
  domain and architecture. Residual-only probing is a recurring convenience that costs real accuracy; our own probes
  should sweep representation site, not just layer.
- **Positive result on read-out stability:** the latent signal survives a distribution shift (cipher fine-tuning) that
  makes the *surface* unreadable, and the readout needs no retraining once the backbone has learned to decode. This is
  a clean demonstration that probes track something content-like rather than surface form — and, with the frozen-
  backbone control, a good template for separating "the model can't represent it" from "our reader can't read it".

## Tags
unit: feature | layer
form: probe
method: probing | other
eval: benchmark | downstream-task
goal: safety/auditing
