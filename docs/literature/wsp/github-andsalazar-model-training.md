# Weight-Space Programming experiments: Qwen3.5-0.8B and Ovi (replication incl. weight reading with five readers)

- **Key:** github-andsalazar-model-training
- **Authors / organisation:** GitHub user andsalazar (independent; no organisation stated)
- **Date:** 2026-11 (Stage 8 replies collected 2026-11-09; repo creation date not retrievable)
- **Link:** https://github.com/andsalazar/model-training
- **Kind:** tool (replication repository with write-ups)
- **Read from:** README in full; `docs/stage8-reading-weights.md` in full; `src/wsp/reading.py` (prompt text, weight serialisation, scorer, control); section 5 of `docs/stage0-findings.md` (static-slice ablation). Not read: the per-reply JSON in `artifacts/stage8_reading/`, `docs/WRITEUP.md`, the Stage 1–7 documents other than as summarised in the README. GitHub API and tarball access were blocked in this session, so files were fetched individually by raw URL; no directory listing was available.
- **Relevance to us:** 3 (central)

## What they wanted, and why
The author set out to test whether the WSP result of Takehi et al. (MIT, Nov 2026) depends on the editor/reader being a frontier model, i.e. whether cheaper open-weight models could read and edit another network's weights. Part 1 reproduces the paper's Qwen3.5-0.8B loop-repair edit and tries to derive edits with a cheap editor; Part 2 tries a TBC-sized adapter on the Ovi video model; Part 3 (Stage 8) repeats the paper's Experiment 2, reading a tiny diffusion model's function from raw weights, with fresh networks, a new shape and a shuffled control. The repository frames itself as a replication plus negative results, not a method.

## What they studied
- Readers (Stage 8): GPT-6 Astra (the paper's reader), Kimi (`moonshotai/kimi-k3.1-pro`), GLM, DeepSeek (`deepseek-v4.1-flash-1017`), Qwen; all via OpenRouter. `muse` excluded for context size.
- Targets (Stage 8): nine tiny DDPMs, MLP 160 → 64 → 64 → 144 (23,824 weights), generating 12 × 12 grayscale images. Three are the paper's released networks (circle, square, triangle); three fresh networks of the same shapes; two fresh networks trained on a plus-shaped cross (a shape the paper never used); one control (fresh circle with entries shuffled within each tensor).
- Parts 1–2: Qwen3.5-0.8B (MLP layer 15/19 down-projection columns; LoRA adapters) and Ovi (11.66B joint video+audio DiT). Unit: whole-network weights (Stage 8), weight columns/directions and adapters (Parts 1–2).

## How they did it
1. Rebuilt the paper's Experiment 2 prompts byte for byte from the released weights (RikiyaT/lm_understand-logs, `exp2_diffusion`) and checked the scorer gives the paper's own replies the paper's verdicts.
2. Trained fresh DDPMs with the paper's stated recipe (40,000 steps, batch 512), choosing unstated settings themselves (learning rate, dataset of 20,000 images per shape, shape size ranges); validated each by generating 1,000 images and classifying them with a separately trained shape classifier.
3. Built the control by shuffling values inside each tensor (keeps values, distributions, shapes, format; destroys connectivity); it generates one fixed speckled image.
4. Sent each of the 9 networks to each of 5 readers once, fresh conversation, paper's prompt and one-line system instruction, reasoning effort high, 16,000-token output limit, no tools offered.
5. Before scoring, added a rule (after a DeepSeek plumbing check returned empty): replies cut off before their `Images:` section get one retry at 64,000 tokens; still cut off counts as missing/incorrect.
6. Committed the design, scoring rule and interpretation criteria before any scored reply.
7. Scored with a fixed whole-word keyword rule on the `Images:` section (circle/square/triangle/cross classes); ambiguous, none and missing count as incorrect.
8. After the run, checked whether runs of four or more quoted weights actually occur in the network (rows, columns, strides, corners).
9. Separately (Stage 0), gave five editors a static slice of the Qwen matrix the paper edited, with and without the slice, and asked them to name columns to change.

## What counts as an explanation here
A free-text answer from the reader: observations with quoted weights, reasoning, a description of the generated images, an ASCII 12 × 12 example, and a confidence. It is partial and non-mechanistic; it is scored only on the named shape. For the Qwen editing work, the "explanation" is an activation-derived direction or adapter, judged by re-measured behaviour.

## How they judged success
Stage 8: correct shape under the pre-committed keyword rule; four pre-registered readings (paper result repeats; holds on fresh networks; names the unseen cross; declines on the shuffled control or gives clearly lower confidence). Chance baseline for picking among three shapes stated (1 in 27 for three, 1 in 729 for six). Post-hoc check of quoted weights against the real tensors. For editing: `wsp.verify` rule (validated / partial / no-effect / harmful) with token-count thresholds and held-out guard probes; cross-hardware reproduction.

## What they found
- Astra: 3/3 on the paper's networks, 3/3 on fresh same-shape networks, crosses 1/2 by the keyword rule (one reply wrote "+" which the rule lacked; 2/2 on a plain reading), and on the shuffled control it named nothing with 0% confidence, against 68–87% on real networks.
- Kimi 3/3 on paper networks but 1/3 fresh, 0/2 cross, and described the shuffled network as digit-4-like at 76%. GLM 1/3, 1/3, 0/2, control "no large coherent shape" at 25%. DeepSeek 0 throughout, control "a vertical stroke" at 74%, and no answer on 5 networks even at 64,000 tokens. Qwen 0 throughout, empty answers on 7 of 9.
- 21 of 45 replies needed the 64,000-token retry; Astra spent 4,700–15,400 reasoning tokens per reply versus 1,000–2,600 in the paper's logs. Total spend $21.09.
- Quoted-weight check: Astra 18/18 and Kimi 17/17 runs found in the real weights; GLM 9/14. Kimi's errors come from misreading real weights, not inventing them.
- A scorer bug (Markdown `## Images` headings) was found after the run and fixed; it changed three verdicts, including one Astra triangle.
- Stage 0: with only a static slice of Qwen's weights, all five editors (Astra included) declined to name columns, saying it would be guesswork; the paper's edit itself reproduced on its 25-problem practice subset (4.0% → 64.0%).
- Parts 1–2: a cheap editor could derive an activation-based edit, but it did not reproduce across hardware (tie of 0.0012 at the cut), editors reported numbers they had not measured, and the Ovi adapter gave no speed-up at equal quality.

## Limits and open problems they name
One reply per network, nine networks, one run: counts, not rates. Compliance with "no forward pass" cannot be checked (only reasoning summaries returned). The task is narrow: the output layer W3 is laid out on the same 12 × 12 grid as the image and Astra's observations mostly quote that layer; this says nothing about reading language-model weights. The paper's networks were public since 2026-10-29 and could have been seen. Cheaper readers' failures may reflect prompt/budget, not capability. Experiments 1, 3 and 7 not attempted.

## What we take from it
- **Design template for K1 reading tests:** pre-committed scoring rule; fresh networks never published; a novel class outside the obvious list (the cross); a within-tensor shuffle control that preserves value statistics; per-reply quote verification against the real weights. All directly reusable.
- **Warning:** the success case is the easiest possible layout (output weights map to image pixels). Any claim we make needs targets where function is not spatially readable from one layer.
- **Warning:** non-frontier readers mostly fail by spending the output budget copying weight rows; budget and retry policy must be fixed in advance and reported.
- **Measure:** "declines with low confidence on shuffled weights" is a cheap calibration control worth adding to every reading run.
- **Shortcut:** `src/wsp/reading.py` reproduces the paper's Experiment 2 prompt and weight format byte for byte.

## K1 detail (reading setup)
- **Reader model(s), and the score for each** (correct under keyword rule; paper 3 / fresh same-shape 3 / cross 2 / control): GPT-6 Astra 3/3, 3/3, 1/2 (2/2 plain reading), names nothing at 0%. Kimi 3/3, 1/3, 0/2, names a figure at 76%. GLM 1/3, 1/3, 0/2, "no coherent shape" at 25%. DeepSeek 0/3, 0/3, 0/2, names a stroke at 74%. Qwen 0/3, 0/3, 0/2, no shape at 62%. Exact model versions for GLM and Qwen not stated in what was read.
- **Target networks:** DDPM denoiser MLP 160 → 64 → 64 → 144, ReLU hidden layers, 23,824 weights; x0-prediction, linear betas 1e-4 to 0.02 over 1,000 steps; inputs are 144 noisy pixels plus 16 sinusoidal step features. Trained to generate 12 × 12 filled circles, squares, triangles (paper) or crosses (new). Generated images classified as the target shape 95.2–100%.
- **How the weights were presented:** plain text, all six tensors in order W1, b1, W2, b2, W3, b3; each with a header giving name, shape and row/column meaning (row i = input i; for W3 column j = pixel j); one line per matrix row, space-separated values rounded to 3 decimals; no per-value labels. About 100,000 tokens in total (as stated).
- **Prompt:** system line "Answer the user's request." User message = (1) description of the DDPM: pixel range and indexing, training objective and noise schedule, generation procedure; (2) network equations and input layout; (3) question: what images does it generate, work from the weights, no tools, no forward-pass calculation or simulation of sampling, single response; (4) required answer format: Observations (quote weights) / Reasoning / Images / Example as 12 lines of 12 characters / Confidence 0–100%; (5) the weights. No candidate answers are given. Prompt text is in `src/wsp/reading.py` (DESCRIPTION, QUESTION, SYSTEM), copied from RikiyaT/lm_understand-logs `exp2_diffusion`.
- **Access regime:** no tools, single reply; via OpenRouter chat completions; reasoning effort high; no temperature set; 16,000 output tokens, one retry at 64,000 if cut off before `Images:`. No Python, no forward passes. (Stage 0 static-slice ablation: also no tools. Stage 1 editing: tools to run the model and measure activations, but the editor never saw a weight value.)
- **Controls:** within-tensor shuffle of a real network; fresh unpublished networks (contamination control); unseen shape class (short-list-guessing control); chance baselines stated; post-hoc quoted-weight verification. No label-order or prompt-only control in Stage 8. Stage 0 had a with-slice vs without-slice (blind) arm.
- **Failure modes observed:** spending the whole output budget on reasoning, often copying weight rows, and returning no answer (DeepSeek 5/9, Qwen 7/9, GLM 3/9 with no `Images` section); confident naming of a figure for the shuffled network (Kimi, DeepSeek); defaulting to one shape (Kimi said circle for five of eight real networks); misreading real weights; describing filled shapes as outlines (Astra, as in the paper); answering with digit shapes (DeepSeek); provider-side truncation that looks like a normal stop (Qwen). Scorer fragility to heading style and to "+" vs "plus".
- **Prompt/format choices that helped or hurt:** the 64,000-token retry was needed for 21/45 replies; Astra used far more reasoning tokens via OpenRouter than in the paper's Codex CLI logs. The author notes the image-aligned W3 layout makes this a narrow kind of reading. No prompt variants were compared.
