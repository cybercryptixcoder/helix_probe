# Shaping & Monitoring Models through their Internal Representations (Goodfire blog: "Mechanistic Shaping")

- **Key:** arxiv-2611.07071
- **Authors / organisation:** Thomas Fel, Matthew Kowal, Matt Feiszli, Satchel Grant, Andrew Lee, Chris Earls (core), with many further Goodfire contributors incl. Atticus Geiger, Ekdeep Singh Lubana, Jack Merullo; senior: Thomas McGrath, Owen Lewis; Goodfire
- **Date:** 2026-11 (blog post 2026-11-05)
- **Link:** https://arxiv.org/abs/2611.07071 (blog: https://www.goodfire.com/research/mechanistic-shaping)
- **Kind:** paper (with blog/research post)
- **Read from:** abstract and sections (Goodfire blog in full; arXiv HTML methods, setups and main results, first ~30% of the page; harmlessness and later sections only partly seen)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Training rewards correct outputs, not the route to them, so models can succeed for the wrong reasons (a chest X-ray
classifier detecting post-diagnosis chest drains instead of lung pathology; sycophancy; reward hacking). The authors
want interpretability to specify *how* a model solves a task, not just audit it afterwards. They also ask the obvious
worry: if you train against an interpretability signal, does the concept just hide, so that monitors stop working?
This is a step toward applied, "mechanistic" alignment where internal representations are both a training target
and a monitoring channel.

## What they studied
Vision: DINOv2 on a custom perfectly-confounded Waterbirds (2,066 training birds); DINOv3 Large on ImageNette
(conditional rules via a BatchTopK SAE); frozen RAD-DINO on CheXpert pneumothorax (1,152 radiographs with perfect
drain confounding). Language: OLMo 3 7B under DPO (checks at 13B and 32B) for sycophancy; Qwen3.5-9B under GRPO on an
agentic Countdown task with a forbidden target file (chess-puzzle transfer). Also a toy model for theory. Unit:
concept directions/subspaces at a chosen layer.

## How they did it
The method is framed as constrained learning: minimise task risk subject to a violation bound, optimised as task
loss plus lambda times a penalty. Two penalties: *expression* shaping penalises how strongly a concept is present
(a discounted per-token sum of a probe or difference-of-means score; the reader can be the live policy, a frozen
initial copy, or another model, with gradients through the score or detached); *reliance* shaping penalises the
squared attribution of the output to a concept direction, using gradient, gradient-times-input, integrated
gradients, SmoothGrad, noise, shuffle or deletion attributions. Concept directions come from difference of means
(preferred), linear probes, SAE decoder atoms or distributed alignment search, and are periodically refit (e.g.
every 100 steps) when the encoder trains. On CheXpert, an LLM agent labelled SAE features as tube-like without seeing
drain labels. Then a five-level monitorability test: L1 reuse the original probe, L2 linear refit, L3 nonlinear
refit, L4 a different layer, L5 an external black-box judge. A toy-model theory analyses what happens to a concept
after projection-based shaping.

## What counts as an explanation here
Not an explanation of the model per se: a concept direction (probe/DoM/SAE atom) is treated as a good-enough handle
on a mechanism to train against and to monitor. Partial by design. The theory does make predictions about where a
suppressed concept goes (regrowth elsewhere, entanglement, a nonlinear "product code").

## How they judged success
Worst-group accuracy (WGA) and background-detection AUROC (Waterbirds, CheXpert); multi-turn sycophantic agreement
on MMLU questions plus accuracy on six capability benchmarks (sycophancy); peek rate and honest-solve rate
(Countdown, chess); probe AUROC/balanced accuracy at each monitoring level. Baselines: ERM, projection, LEACE, INLP;
data filtering, reward shaping, inoculation prompting, learning-rate reduction, preventative steering; ordinary
GRPO, random direction, rollout filtering; balanced-data training as a soft ceiling. Three seeds for vision.

## What they found
Waterbirds: shaped WGA 93-97.7% vs 51.6% for ERM. CheXpert: ERM 33.3% WGA vs 56.0% balanced training; agent-derived
rank-8 spans matched or exceeded balanced training. Sycophancy: gradient-times-input reliance shaping kept DPO-level
capability with sycophancy at the pre-DPO level, where baselines either did little or cost capability; it held at
7B, 13B and 32B. Countdown: plain GRPO drove peek rate to 1.00 within ten updates and honest solving to zero;
expression shaping gave 0.96-0.98 honest solve; filtering helped in one of three seeds; chess transfer cheating 99%
under plain RL vs near zero shaped. Monitoring: sycophancy DoM AUROC 0.981 to 0.931, a refit linear probe stays at
1.00; reward-hacking original probe fell to 0.57 balanced accuracy in the worst case (gradients through the probe),
refit probes 0.97-0.98. Under LEACE at layer 9 a linear probe fell to 0.44 AUROC but a nonlinear probe still read
0.842. Concepts stayed monitorable in every experiment, sometimes only at L3/L4.

## Limitations and open problems they name
Small-to-medium scale only; Waterbirds is a toy; theory exact only for a toy model and projection shaping (some
last-layer reliance penalties produced unpredicted partial erasure); single-direction assumption; sensitivity to
refresh period, lambda and attribution choice; a failed probe is ambiguous between erasure and a weak probe; L4/L5
do not show readability inside the shaped model; training against monitors still risks degrading them. Open:
characterising possible neural codes, deeper-network theory, frontier scale, making the theory predict real
monitorability.

## What we take from it
(1) A warning for any white-box model built from probes: after training pressure, a concept can move layer, become
nonlinear or entangle, so a static linear readout is not a stable explanation; the L1-L5 hierarchy is a reusable
protocol for testing how far an explanation must be refit to keep working. (2) Reliance (attribution to a direction)
vs expression (presence of a direction) is a useful distinction for our own predictions: a direction can be present
but unused. (3) Concrete baseline set (projection, LEACE, INLP, filtering, steering) for any intervention claim.

## Tags
unit: direction | whole-model
form: direction | probe
method: attribution | probing | SAE | agent | training-interpretable
eval: downstream-task | benchmark
goal: control/editing | safety/auditing
