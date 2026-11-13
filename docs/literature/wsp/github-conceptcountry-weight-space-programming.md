# Gradient-Free Weight Editing Reduces Overthinking in Qwen3.8-27B (a norm-matched controlled replication of weight-space programming)

- **Key:** github-conceptcountry-weight-space-programming
- **Authors / organisation:** Justin Bennington, Nikki Kaelar, Spencer Lee, Mitchell Edwards, Kojin Glick, Cilvia Danks; Concept Country, New York
- **Date:** 2026-11-08 (working paper v1)
- **Link:** https://github.com/conceptcountry/weight-space-programming (paper page: https://concept.country/research/weight-space-programming)
- **Kind:** paper (working paper) with analysis code and result artifacts
- **Read from:** README in full; the paper source `paper/paper.typ` in full with its generated constants `paper/numbers.typ`; `results/seed_stability.txt`. Not read: `results/results.json`, the generator scripts, figures (seen only as captions), the paper web page, the published model weights. Repository obtained by shallow clone (GitHub API blocked for this session).
- **Relevance to us:** 1 (background)

## What they wanted, and why
The authors want to know whether a weight edit that makes a reasoning model think less does so because of the direction written into the weights or merely because any small perturbation of that size happens to help. They port an activation-derived, gradient-free edit to Qwen3.8-27B, pre-register a success criterion, and compare against both the unedited model and a norm-matched random edit on the same matrices. They also report measurement failures (a data-contamination bug, a borderline interval) as lessons for this class of study.

## What they studied
Qwen3.8-27B in thinking mode, served as Q8_0 GGUF. Unit: directions in the residual stream, written into the down-projection matrices of nine alternating layers (32 to 48, even).

## How they did it
1. On the MATH train split only, sample 48 level-5 problems, 6 samples each, under a 4k cap; take one forward pass per trace (288) and record residual activations at every layer for several position sets.
2. Form three contrast directions: short minus long correct traces on the same problem, positions before verification phrases vs others, and the region before end-of-thinking vs others.
3. Compile a direction into weights either projectively (remove it) or additively (a rank-one term that writes along it in proportion to the writer's mean input and output norm).
4. Screen on 64 fresh train problems; select the additive end-of-thinking direction at alpha 0.1 on nine down-projections (relative change about 0.5%).
5. Build a control with a per-layer random unit vector orthogonal to the fitted direction, same norm of change, same matrices.
6. Evaluate base, edit and control with identical sampling, seeds and 32k cap on GPQA Diamond (198 x 2 samples), IFBench (300) and LiveCodeBench v6 (131); paired bootstrap over problems (10,000 replicates).

## What counts as an explanation here
A direction in activation space, read from contrasts of the model's own reasoning traces, whose insertion into weights changes thinking length. It is an intervention, not a description; the claim is that the direction carries the effect.

## How they judged success
Pre-registered: on held-out benchmarks, paired against base, accuracy gain with CI excluding zero, or at least 15% fewer thinking tokens with accuracy non-inferior (lower bound above -2 points); must also beat the norm-matched random edit, show dose-response, and not regress instruction following. Bootstrap seed sweep to check stability of borderline intervals.

## What they found
- Edit vs base: GPQA Diamond +4.3 points [+1.8, +7.1] with thinking tokens -30.0%; LiveCodeBench v6 +13.0 [+6.1, +20.6] at -29.2% tokens; IFBench +3.3 [-1.0, +7.7] at -54.1% tokens (passes on the token clause).
- Control vs base: every accuracy interval includes zero (GPQA -1.0, IFBench -1.3, LCB +3.0) and no token saving (+0.2%, -0.1%, -2.6%).
- Edit vs control: GPQA +5.3 [+2.8, +8.1], LCB +9.9 [+3.8, +16.8]; IFBench +4.7 [+0.3, +9.3] but the lower bound touches zero for 2 of 10 bootstrap seeds, so reported as borderline and not claimed.
- Dose-response between alpha 0.05 and 0.1 on the screen set: tokens fall and accuracy gain rises.
- An appended follow-up sampling run silently contaminated result files read by three separate scripts; each had to be fixed separately.

## Limits and open problems they name
One model, one size, one edit form, one alpha, one engine, three benchmarks; Q8_0 only; 32k cap well below the recommended budget, with truncation present in every arm and the 128k robustness run still in progress; one random direction per layer (no distribution over control seeds); coarse per-problem estimates; the IFBench control clause judged borderline.

## What we take from it
- **Disconnect to flag:** despite the title, there is no LLM reading or writing weights here. The direction comes from forward-pass activations (steering compiled into weights), and the analysis was done by the authors with an AI coding agent. It is not WSP in the Sparks sense and says nothing about K1 reading.
- **Control (reusable):** a norm-matched random edit on the same matrices, orthogonal to the fitted direction, is the right counterfactual for any edit we derive from a white-box model; better still, sample several random seeds and report a distribution.
- **Process warning:** recompute every statistic from one filtered script with a per-arm sample census; append-only result files can silently mix sample counts.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** none. No LLM reads weights; directions are fitted from activations by the authors' code. (An AI coding agent assisted the analysis under the authors' direction; not a reader.)
- **Target networks:** Qwen3.8-27B (thinking mode), a general reasoning LLM; Q8_0 GGUF.
- **How the weights were presented:** not applicable (no reader).
- **Prompt:** not applicable.
- **Access regime:** forward passes on 288 train-split traces to collect activations; no gradients; edits are closed-form rank-one updates.
- **Controls:** norm-matched random orthogonal direction on the same nine matrices; unedited base; dose (alpha 0.05 vs 0.1); held-out confirmation suite; bootstrap seed sweep.
- **Failure modes observed:** contaminated result files (mixed sample counts) affecting three analysis scripts; a stale baseline number copied across documents; a robustness run that exhausted memory because the cap was multiplied by parallelism.
- **Anything about which prompt or format choices helped or hurt:** not applicable. Among edit forms, the additive end-of-thinking direction was selected on the screen; the projective form and other directions were tried but their screen results are not given in the parts read.
