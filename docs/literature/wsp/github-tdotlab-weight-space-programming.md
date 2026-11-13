# WeightSpaceProgramming: home replication of the Qwen3.5 reasoning-loop edit with Claude as editor

- **Key:** github-tdotlab-weight-space-programming
- **Authors / organisation:** tdotlab (GitHub); independent, single desktop with a GTX 1070
- **Date:** 2026-11 (STATUS.md last updated 2026-11-04)
- **Link:** https://github.com/tdotlab/weight-space-programming
- **Kind:** tool / replication repository with run logs
- **Read from:** README, `docs/STATUS.md` in full, `runs/INDEX.md` in full, and the opening sections of `logs/edit_session.md` (deviations, architecture facts, steps a01-a05) plus its section headings. Not read: the rest of `edit_session.md` (a06-a12, t01-t03, predictions in full), the analysis scripts in `src/`, per-problem transcripts, the 2B logs. Repository obtained by shallow clone (GitHub API blocked for this session).
- **Relevance to us:** 2 (useful)

## What they wanted, and why
To replicate at home the Sparks Experiment 8 claim that a frontier LLM can edit Qwen3.5-0.8B's weights, without gradients or forward passes during the edit, so that its math reasoning stops looping and accuracy rises. Here the editor is Claude (Opus) rather than GPT-6 Astra. The work then extends to Qwen3.5-2B and to a second round aimed at the decision to stop thinking, testing pre-written predictions about what each edit will do.

## What they studied
Edited models: Qwen3.5-0.8B (24 layers, hidden 1024, SwiGLU MLP of 3584, tied embeddings, mixed full and linear attention) and Qwen3.5-2B, plus their -Base checkpoints for weight diffs. Units: MLP neurons (down_proj columns), singular directions of post-training weight deltas, and logit-lens readouts of write vectors. Evaluation on a 100-problem MATH-500 sample via llama.cpp Q8_0 GGUF.

## How they did it
1. Baseline evals (accuracy, truncation at the token cap, rate of "Wait" per thousand characters).
2. Blind analysis by Claude using only tensor math (no forward passes through Qwen), every step logged: a logit lens over every MLP neuron's write vector; a two-hop path trace (found noise); a base-vs-instruct weight diff (declared deviation); the top singular direction u of layer 22's down_proj delta, which writes "Wait".
3. Build edits on copies: project u out of the 64 most aligned layer-22 columns (MIT-shaped, P64), a same-size random-direction control (R64), reverting u across all of layer 22 (D_full), and amplifying u in those columns by x1.5 to x5 (A64h, A64, A64x3, A64x5).
4. After P64 backfired, iterate using eval feedback (declared deviation from MIT's blind setup); later derive a weight-only "self-gain" readout that predicts the sign of an edit, find single "brake" neurons per discourse token, and write predictions before each eval round.
5. Port the recipe blind to Qwen3.5-2B; in round 2, edit the "Final" brake neuron with a "Therefore" control.
6. Compare edits by paired sign tests on the same problems and a held-out subset of 60 problems never used to judge an edit.

## What counts as an explanation here
A direction or a single neuron identified from weights (logit-lens z-scores of its write vector, alignment of gate/up/down weights), plus a predicted behavioural effect (rate of a token, accuracy) that is then tested. Partial, mechanistic, and partly predictive (written predictions with clauses).

## How they judged success
MATH-500 accuracy on 100 problems (and first-40 screens), truncation rate at 16k/32k (0.8B) or 8k (2B) caps, "Wait"/"No,"/"Final" rates per thousand characters, paired sign tests vs baseline and between edits, held-out 60-problem subset, a random-direction control and a dose curve, and pass/fail of pre-written prediction clauses.

## What they found
- MIT-shaped removal of the "Wait" direction (P64) backfired: 0/40, all truncated, "Wait" exploded; the random-direction control matched baseline, so the effect was specific to u.
- Amplifying u in the same 64 columns helped with a graded dose response: A64x3 took 0.8B from 5/100 to 30/100 at a 16k cap (25 gained, none lost; held-out 1/60 to 17/60), and to 41/100 at 32k; tripling one neuron alone (layer 22, column 573) gave most of the gain.
- MIT's layers 15 and 19 did nothing here in either sign on top of A64.
- The recipe moved blind to the 2B: 26/100 to 46/100 at 8k; one neuron alone gave 42/100. Weight-only analysis found the same structure: a pretraining "brake" neuron per discourse token.
- Round 2 ("Final" brake) moved the word's rate but not accuracy; several pre-written predictions failed.
- About 55-60% of problems still hit the cap; removing hesitation words does not end loops that continue in other phrasing.
- A hardware fault (RAM corrupting data) produced single-bit flips in some builds; all evaluated GGUFs were verified against their builds.

## Limits and open problems they name
The editor saw baseline transcripts and knew MIT's edit from press coverage (declared deviations); after P64 the work used eval feedback, unlike MIT's blind setup; Q8_0 quantised evals; one 100-problem sample; no greedy baseline or non-math regression set yet; RAM corruption on the eval machine; stopping is not a single lever.

## What we take from it
- **Method (weight-only reading of an LLM):** logit lens on write vectors, singular directions of base-vs-instruct deltas, and a gate/up/down alignment "self-gain" readout are practical tools a reader can use without forward passes; the self-gain readout was checked against edit outcomes, which is the kind of predictive test we want.
- **Warning:** a weight-only reading got the sign of the needed edit wrong at first (P64); weights told where, not which way, until a later readout. Prediction under intervention must be tested, not assumed.
- **Control:** same-size random-direction edits and dose curves cleanly separate direction from magnitude.
- **Disconnect to flag:** this is an editing study; there is no LLM-reads-weights-and-names-function task, so K1 detail below is mostly about the editor's weight analysis.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** Claude (Opus; exact version not stated in the parts read) as editor/analyst. No reading score in the K1 sense; edit outcomes: A64x3 30/100 vs baseline 5/100 on 0.8B at 16k; 2B_A64x3 46/100 vs 26/100 at 8k.
- **Target networks:** Qwen3.5-0.8B and Qwen3.5-2B (instruct, thinking mode) and their Base checkpoints; trained by Alibaba for general language and reasoning.
- **How the weights were presented:** as tensors loaded with numpy/torch (CPU) in scripts the editor ran; not as text in a prompt. Number format: bf16 originals. Total tokens not applicable.
- **Prompt:** the task framing given in README and AGENTS.md: stop math reasoning loops by editing weights, with weight-tensor math only and no forward passes through the model during the edit phase, logging every step; edits only to copies. No candidate answers. The editor also saw baseline transcripts (declared). No separate prompt file was found in the parts read.
- **Access regime:** Python with numpy/torch on the weights; no forward passes during analysis; the experimenter ran evals (llama.cpp) and, from P64 on, results were fed back into the editing loop. Budgets not stated.
- **Controls:** same-size random-direction edit (R64), full-layer revert (D_full), dose series (x1.5, x2, x3, x5), MIT-layer edits in both signs, a "Therefore"-brake control in round 2, held-out problem subset, paired sign tests.
- **Failure modes observed:** wrong edit sign from weights alone (P64 runaway); weak or noise-like signals from two-hop path tracing; directions found by press-informed priors not standing out under the editor's own lenses; edits that remove a word without removing the underlying loop.
- **Anything about which prompt or format choices helped or hurt:** the base-vs-instruct diff (an extra model, a declared deviation) gave the decisive direction where single-model analyses did not; knowing MIT's answer in advance was declared as a strong prior; using eval transcripts informed which tokens to target.
