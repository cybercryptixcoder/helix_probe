# Weight-Space Programming for Improving Image-Restoration Diffusion Models: Technical Conjectures and a Recursive Improvement Loop

- **Key:** arxiv-2611.04268
- **Authors / organisation:** Zhuoran Zheng (affiliation listed as "Doubao"; contact address at njust.edu.cn)
- **Date:** 2026-11-03
- **Link:** https://arxiv.org/abs/2611.04268
- **Kind:** essay (position / conjecture paper; no experiments)
- **Read from:** full text (arXiv HTML v1). The arXiv comment states the manuscript is purely conjectural.
- **Relevance to us:** 1 (background)

## What they wanted, and why
The author asks whether WSP can move from fixing bugs to improving quality, using diffusion-based image restoration (deblurring, super-resolution, denoising, inpainting) as the setting. The motivation is that fixing restoration failures today needs paired data and fine-tuning. The paper frames restoration UNets as a middle ground: low-level and output layers may be concentrated enough for sparse edits, while bottleneck (semantic) layers are distributed. It also frames an iterative diagnose-edit-evaluate loop as a minimal form of recursive self-improvement.

## What they studied
Nothing empirically. The object of discussion is a hypothetical restoration diffusion UNet run along a denoising chain. The paper builds on its reading of the Takehi et al. WSP blog post (a Qwen3.5-0.8B reasoning-loop fix touching 0.016% of parameters, and a failed attempt to add math ability to Gemma3 270M).

## How they did it
The paper states three conjectures, each with input, edit target, expected effect, failure boundary and a falsification criterion. C1: an LLM can localise which layer causes a described quality gap (over-smoothing, colour shift, hallucinated texture) within a forward-pass budget, seeing per-layer chunks of summary statistics (layer name, type, channel counts, kernel size, weight histogram statistics, top-k largest entries, mean activation magnitude) and requesting targeted ablations. C2: on a diagnosed layer, a small weight delta (output-bias shift for colour cast, scaling high-frequency filter norms for sharpness, scaling skip connections against halos) improves PSNR while touching under 0.1% of parameters. C3: repeating diagnose-edit-evaluate compounds gains over rounds until only distributed defects remain. It gives PyTorch-style pseudocode for a sandbox (chunked weight access, forward-pass budget, edit-ratio cap, feedback/test split, an acceptance rule on PSNR gain) and an outer loop, a taxonomy of which defects are concentrated vs distributed, and an outline benchmark with injected concentrated defects as positives and natural distributed defects as negative controls.

## What counts as an explanation here
A localisation of a quality gap to a layer or small set of layers, plus a structured weight direction (bias shift, filter-norm scaling) that fixes it. Explicitly partial.

## How they judged success
Proposed only: PSNR (plus SSIM/LPIPS and visual inspection) on a held-out set; falsification thresholds per conjecture (e.g., failing to localise the correct layer within a pass budget on more than half of a proposed 20-model benchmark). No results.

## What they found
No empirical findings. All numeric "expected gains" are stated by the author as hypotheses.

## Limits and open problems they name
A 100M-parameter UNet cannot fit in context, so the LLM would see summaries, not raw weights; distributed defects cannot be fixed sparsely; channel permutation symmetry makes weight interpretation ambiguous; edits may hurt out-of-distribution images; diffusion sampling noise makes small PSNR deltas hard to detect within a small budget; PSNR correlates poorly with perception; an LLM may be biased toward editing late layers (suggests randomising chunk order).

## What we take from it
- **A framing (weak):** the concentrated vs distributed defect distinction as a predictor of what weight edits can fix, which other WSP papers also observe empirically.
- **A design idea:** presenting a large network to a reader as chunked per-layer summary statistics rather than raw weights, with randomised chunk order to counter positional bias. Untested.
- **A caution:** this is not evidence; it should not be cited as showing WSP works on diffusion models. Its description of the Takehi results is second-hand.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** none run. The paper speaks of a "GPT-6-class LLM" hypothetically. No scores.
- **Target networks:** hypothetical restoration diffusion UNets (the paper mentions a 100M-parameter UNet and a 10M-parameter conv net as examples); none trained or tested.
- **How the weights were presented:** proposed only: per-layer chunks of 5 to 10 layers at a time, with layer name, type, channel counts, kernel size, weight histogram statistics (mean, std, sparsity), top-k largest-magnitude entries, and mean activation magnitude on a feedback set. Raw weights are explicitly not shown. Number format and precision: not stated. Tokens: not stated.
- **Prompt:** not given; the pseudocode builds a prompt from a quality-gap description, layer statistics and round number and expects a JSON edit proposal (type, layer, slice, delta). No prompt files.
- **Access regime:** proposed: 30 to 50 forward-pass evaluations per session (C1 mentions 200 and also 30 to 50), edit-ratio cap below 0.1% of parameters, 32 to 64 feedback image pairs, an automatic accept rule on PSNR gain of at least 0.1 dB.
- **Controls:** proposed only: distributed defects as negative controls in a benchmark. Not run.
- **Failure modes observed:** none observed (no experiments); anticipated ones are permutation-symmetry confusion, late-layer search bias, noise in PSNR feedback, OOD side effects.
- **Prompt or format choices that helped or hurt:** not stated (no experiments). Suggests randomising chunk order to counter late-layer bias and adding before/after images as visual feedback at token cost.
