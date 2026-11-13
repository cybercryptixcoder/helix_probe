# Reasoning Theater: Probing for Performative Chain-of-Thought

- **Key:** goodfire-com-research-reasoning-theater
- **Authors / organisation:** Siddharth Boppana, Annabel Ma (equal contribution), Max Loeffler, Raphael Sarfati, Eric Bigelow, Atticus Geiger, Owen Lewis, Jack Merullo; Goodfire AI, with Harvard University. Began as a SPAR fellowship project.
- **Date:** 2026-03-12
- **Link:** https://www.goodfire.com/research/reasoning-theater
- **Kind:** blog/research post (summary of an arXiv paper)
- **Read from:** full text of the research post (summary page; the linked arXiv paper was not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why

RL-trained reasoning models produce long verbal chains of thought, and the obvious monitoring strategy is to read them: assume the written trace tracks what actually drove the answer. Prior work already showed traces are often unfaithful, but that evidence is mostly behavioural — perturb the prompt, see whether the text changes accordingly. The authors want a *state-based* version of the faithfulness question: instead of asking whether the text explains a decision, track how the model's internal distribution over the final answer evolves token by token and compare it with what the trace communicates. When the internals already commit to an answer that the trace has not yet (or never) disclosed, they call the reasoning performative — the trace looks like deliberation but is not where the answer is being decided. The larger goal is monitorability: if a fixed readout can stand in for the trace, external monitors stop depending on the model's willingness to narrate itself. A side effect they pursue deliberately is inference efficiency, since the same readout doubles as a stopping rule.

## What they studied

Two large open-weight reasoning models — DeepSeek-R1-0528-671B and GPT-OSS-120B — plus the DeepSeek-R1 distilled model family, which supplies the size axis. Benchmarks: MMLU-Redux (multiple choice, largely recall-shaped) and GPQA-Diamond (graduate-level, multi-step). Unit of analysis: the model's evolving probability distribution over answer letters, read from internal activations with a trained probe, at every token position of the reasoning trace, and compared against the same distribution recovered from the text alone.

## How they did it

Three independent estimators of "what would the model answer right now" are computed at each intermediate point in a trace:

1. **Attention probe.** A context-pooling probe (attention over positions rather than a single-token classifier) is trained on internal activations to output a distribution over the answer choices. Trained once per model, then applied at every position, so the estimate is a trajectory over the course of generation.
2. **Forced answering.** The reasoning is cut at position *t* and the model is instructed to commit to an answer immediately. This is a behavioural ground truth for the counterfactual "answer if asked now" and does not rely on the probe at all.
3. **CoT monitor.** A separate LLM is shown the trace text up to position *t* and asked which answer the original model is converging on. This is the ceiling of what an outside reader of the trace can infer.

Performativity is then defined as the gap between the CoT monitor and the probe/forced-answer estimates at the same position — a text-versus-state difference, not an absolute accuracy number. They also classify verbalized inflection points in the traces ("Wait", "Aha") with the monitor and test whether these coincide with jumps in probe confidence, at both the per-response and per-token level. Finally, the calibrated probe is used as an early-exit rule: stop generating when probe confidence crosses a threshold, and measure tokens saved against retained benchmark accuracy.

## What counts as an explanation here

A **probe trajectory**: a time series of answer distributions over the reasoning trace, plus a scalar gap to the verbalized trace. It is not a mechanistic account of *why* the model's internals commit early — nothing here localises a circuit or a feature set. It is a readout that is meant to be predictive (it forecasts the final answer long before the model writes it) and causally validated by agreement with forced answering, which is a real intervention on the computation rather than another readout.

## How they judged success

- Probe accuracy averaged over all token positions per question, then averaged over a held-out test set (their stated protocol), on MMLU and GPQA-Diamond.
- Single-token linear probes as the obvious cheap baseline, against a 25% chance rate for four-way multiple choice.
- The **forced-answering** arm as an external, non-probe check on the probe's trajectory — the key control, since a probe could in principle be scoring surface features of the prompt rather than the model's leaning.
- The CoT-monitor arm as the "what an outside observer can see" ceiling.
- Calibration of the probe, which is the precondition for using its score as a stopping threshold rather than just a ranking.
- Early exit judged as a two-sided trade: tokens saved versus accuracy retained as a percentage of full-trace baseline.

## What they found

- **Attention-pooling probes work where single-token probes do not.** Best attention probes reach about 88% accuracy on MMLU, while single-token linear probes stay near 32% — barely above the 25% chance line. The pooling rule, not the linearity of the readout, is what carries the signal, mirroring the segment-pooling result the loop already recorded.
- **Performativity is difficulty-dependent.** On recall-heavy MMLU questions the probe and forced answering are well above chance from the very start of the trace while the CoT monitor lags: the answer was effectively known before reasoning began, and the trace is narrative rather than deliberation. On GPQA-Diamond all three estimators start near chance and rise together, i.e. the text tracks the state.
- **Model size moves the gap in the predicted direction.** Larger models commit earlier on MMLU, consistent with the answer being retrievable from memory; the smaller distilled models spend more of the trace actually working, and correspondingly look more genuine. Same tasks, more genuine reasoning simply because they are harder for that model.
- **Verbalized inflection points track uncertainty at the response level but not locally.** Confident responses contain roughly half as many "Wait"/"Aha" markers as unconfident ones, across both model families — but an individual marker does not reliably align with a shift in probe confidence at that token.
- **Calibrated probes work as a controller.** Exiting at 95% probe confidence saves 67.7% of tokens on MMLU for DeepSeek-R1 while retaining 96.7% of baseline accuracy, and 33.4% on GPQA-Diamond with accuracy actually at baseline (100.8%); GPT-OSS-120B gives 61.3%/94.9% and 26.1%/98.2% on the same pair.
- Their framing is explicit that "performative" is not an accusation of deception: RL rewards traces that are useful to the model, so superfluous trace on an easy item is the expected optimum, and a CoT monitor can never exceed the quality of the trace it reads.

## Limits and open problems they name

The mechanism behind the internals/text gap is left open — they identify *that* the divergence exists and that it scales with difficulty, not why a model bothers to narrate decisions it has already made. Local timing of inflection points remains unexplained: the aggregate correlation with uncertainty holds while the point-level correlation does not. The work is all multiple-choice, where "final answer" is a small discrete set and a probe can be trained against it; whether the same trajectory comparison survives free-form answers with no letter distribution is not addressed. Everything is measured on open-weight models, so the readout is only available where activations are. Two of the three estimators (probe, CoT monitor) require models or trained components beyond the target, and the blog post defers detail of probe training, layer choice and calibration to the arXiv paper.

## What we take from it

- **Use agreement with a forced-choice intervention as the validator for a temporal readout.** If a probe claims the model "already knows" at position *t*, cutting the generation there and asking for an answer is a cheap, independent causal test of the same claim. This is the temporal counterpart of the loop's recurring rule that every readout needs a null it could plausibly pass by being wrong.
- **A pooling rule again beats a per-token classifier by a wide margin** (88% vs 32% here). When building any trajectory readout, treat "how do I pool across positions" as a first-class design parameter and report the per-token baseline alongside.
- **Define the quantity of interest as a difference between two readouts, not as an accuracy.** Performativity is monitor-minus-state, so it is robust to both being wrong in the same direction on hard items — a generally reusable shape for "does the surface report track the internal variable" questions.
- **Calibration is what turns a probe into a control knob.** The early-exit result only exists because the probe's score could be compared to a threshold; this is the same licence the loop already noted for reward probes, now in the inference-time setting.
- **Difficulty is a confound when interpreting faithfulness.** Any "the model reasons genuinely" or "the model is performing" claim needs the task-difficulty axis held fixed, since the same model shifts from performative to genuine purely as items get harder.
- Watch for the trap when adapting this for our own model: the target distribution must be learnable from the readout at all. Multiple-choice letters are a favourable case; a free-form next-token objective will need a different definition of "the answer it is leaning toward".

## Tags

unit: layer
form: probe
method: probing
eval: patching | downstream-task | benchmark
goal: safety/auditing | evaluation-of-methods
