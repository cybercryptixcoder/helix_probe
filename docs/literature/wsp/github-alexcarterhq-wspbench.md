# WSPBench: does weight access help an agent diagnose and selectively repair a model?

- **Key:** github-alexcarterhq-wspbench
- **Authors / organisation:** Alex Carter (GitHub alexcarterhq; X @NotAlexCarter); independent of the MIT WSP authors
- **Date:** 2026-11 (v0.2.1 Read/Write preview 2026-11-03; current v0.2.2 selective-repair benchmark later in November, exact date not stated)
- **Link:** https://github.com/alexcarterhq/wspbench (site: https://wspbench.com)
- **Kind:** benchmark
- **Read from:** README, `CHANGELOG.md`, `ERRATA.md`, `docs/LIMITATIONS.md`, `experiments/README.md`, and reports `reports/selective-repair-gpt-full/README.md`, `reports/selective-repair-sol-full/README.md`, `reports/selective-repair-hard/README.md`, `reports/selective-repair-hard/budget-check.md`, `reports/paired-read-v2/README.md`, all in full; wspbench.com landing page via a summarising fetch. Not read: source code, prompt templates, data bundles, the v0.2.1 Read/Write pilot report itself (only described in CHANGELOG/LIMITATIONS); no prompt files were locatable without a directory listing (GitHub API blocked in this session).
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The benchmark asks whether giving an agent a network's weights actually helps it find and fix a fault, compared with behaviour probes alone, and whether it can forecast the effect of candidate edits before testing them. It began (v0.2.1) as a Read/Write benchmark: infer the rule implemented by small circuits, or write weights for a task. Following Matthew Honnibal's critique distinguishing direct weight reading from repair with code and feedback, it was reframed into matched-access diagnosis-and-repair, with a scripted solver as baseline. The larger goal is a controlled measure of the value of weight access.

## What they studied
- Agents: OpenAI API aliases GPT-6 Astra, GPT-6 Luna, GPT-6.1 Terra, GPT-6.1 Sol at high reasoning effort; plus a scripted solver.
- Targets (repair): small fitted neural controllers with a planted fault of one of four mechanisms (coupled gates, sensor routing, readout redistribution, cross-layer drift) or a clean control; sizes not stated in what was read. Targets (Read preview): constructed four-stage Boolean ReLU microcircuits with 4,049 float32 scalars and ten binary inputs. Paired Read v2: three synthetic 42-scalar ReLU checkpoint pairs.
- Unit: whole network; edits at the level of individual weights/biases.

## How they did it
1. Generate fault cases from seeds; each case has 14 candidate interventions (localised fixes, partial edits, a global threshold-shift decoy, compound edits, and no edit), exactly one passing, plus a target-fixing decoy that breaks retention.
2. Run each agent twice per case: behaviour probes only, and the same probes plus weights (some runs add weights-only and weights+activations arms).
3. Before testing any edit, the agent may use up to 2 practice probes on the unchanged controller, then commits forecasts of each intervention's effect; after committing, up to 4 more probes; then submits one intervention.
4. One structured function call per turn; per-session limits (full run): 5 turns, 48,000 input tokens, 24,000 output tokens.
5. A hidden grader scores the chosen patch on a hidden target bank (pass at ≥ 95% target accuracy) and a retention bank (≤ 2 pp loss); clean controllers must be left unedited; forecasts scored by MAE against held-out outcomes.
6. Full experiment: 8 seed blocks × (4 faults + 1 clean) = 40 cases per arm; paired comparison per case; 10,000 seed-block bootstrap draws for intervals; invalid submissions count as failures.
7. Paired Read v2 (earlier): for each checkpoint pair, show the true checkpoint, a donor checkpoint ("matched_wrong"), or metadata only ("masked"), and check whether answers follow the weights; access A vs B, where B exposes a tensor tool with handles.

## What counts as an explanation here
Mostly implicit: a committed forecast of each candidate edit's effect plus the chosen patch. Diagnosis is judged by whether the right intervention is chosen and how accurate the forecasts are, not by a stated mechanism.

## How they judged success
Repair success (target ≥ 95%, retention loss ≤ 2 pp), clean controls preserved, forecast MAE, paired gain/loss/tie counts with bootstrap 95% intervals over seed blocks, coverage and invalid-submission counts, metered API cost. Read pilots: accuracy on target/donor disagreement inputs, true-minus-donor and true-minus-metadata contrasts, donor-following rate.

## What they found
- Full comparison (32 faults, 8 clean): with weights vs behaviour only, repairs rose for Sol 14 → 30, Terra 14 → 29, Astra 17 → 32, Luna 8 → 20; scripted baseline 5/32. Paired gains: Sol +50.0 pp (95% interval +28.1 to +71.9), Terra +46.9, Astra +46.9, Luna +37.5. Forecast MAE fell with weights for all four. Sol, Terra and Astra preserved 8/8 clean controls in both arms; Luna preserved 1/8 without weights and 0/8 with.
- Biggest weight effect on coupled gates, cross-layer drift and readout redistribution; small for sensor routing (behaviour alone already 7/8 for Sol).
- Calibration (5,000-token output cap): weight arms mostly failed by running out of output budget; Sol exhausted the cap in all 15 weight-bearing sessions and scored 0/5 there, versus 4/5 with behaviour only. At 12,000 tokens, Sol with weights fixed 2 faults it submitted for and still exhausted the cap on 2.
- Paired Read v2: all three models reached 100% with the true checkpoint and 0–8.3% when shown a donor (i.e. answers followed the weights); metadata-only gave 50%. The tool path (B) cut estimated cost by 52.6% with fewer output tokens. Ceiling accuracy left the tool effect on hard tasks open.
- v0.2.1 Read preview: Luna, Terra and Sol each 0/4 exact on Read; Write 0/2, 1/2, 1/2; a no-edit control already scores 70.1% on Write because outputs are imbalanced.

## Limits and open problems they name
Small development cases, one attempt per cell in calibrations; repeated seeds do not add independent tasks; provider aliases are not immutable snapshots; a trace cannot show the absence of mental simulation; held-out material is API-exposed so leakage cannot be excluded; original cases and traces for the full runs are private; costs include incomplete usage records. Read and Write are reported separately; exact success and partial agreement answer different questions.

## What we take from it
- **Method:** matched access arms (behaviour vs behaviour + weights, same probe and token budgets) with a scripted baseline is the right design for measuring what weights add; reuse for K1 if we test reading with tools.
- **Measure:** forecast-before-test (commit predicted effects of candidate edits, score by MAE) is a direct "prediction under intervention" metric, which is our goal.
- **Control:** paired Read with a donor checkpoint (do answers follow the weights?) and a metadata-only view is a cheap, strong control for reading claims.
- **Warning:** weight access can lower scores when output budgets are tight; budget must be matched and generous, and output-cap failures reported separately.
- **Warning:** with imbalanced outputs, raw accuracy flatters; report exact success and no-edit baselines.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** Repair (with weights / behaviour only, of 32): GPT-6 Astra 32 / 17; GPT-6.1 Sol 30 / 14; GPT-6.1 Terra 29 / 14; GPT-6 Luna 20 / 8; scripted 5 (behaviour only). Paired Read v2: Luna, Terra, Sol all 100% on true checkpoints in both access modes. v0.2.1 Read: Luna, Terra, Sol each 0/4 exact.
- **Target networks:** repair: fitted neural controllers with a planted fault (architecture and size not stated in what was read; the site's worked example is a 2 × 2 linear map). Read preview: constructed four-stage Boolean ReLU microcircuits, 4,049 float32 scalars, ten binary inputs, not trained transformers. Paired Read v2: synthetic ReLU networks with 42 scalars.
- **How the weights were presented:** not stated in what was read. Paired Read v2 says access B gave a tensor tool with exact handles to the arrays; access A is described in LIMITATIONS as no external tools (presumably weights in the prompt as text, but format and precision not stated). The site shows weights as a signed-integer grid only for its toy example.
- **Prompt:** not available in what was read. Protocol elements stated: public task description, shared intervention menu, forecast schema, one structured function call per turn, practice probes before and after committing forecasts. Prompt file paths not found.
- **Access regime:** repair: 5 turns, 48,000 input / 24,000 output tokens (5,000 and 12,000 in calibrations), 2 pre-commit + 4 post-commit behaviour probes; arms: behaviour, weights + behaviour, weights only, weights + activations. Paired Read v2: up to 4 turns and 4,096 total output tokens; A no tools vs B tensor-analysis tool. LIMITATIONS lists three conditions: A no tools, B bounded computational weight analysis, C instrumented diagnosis/repair.
- **Controls:** clean controllers (no edit is correct); target-fixing decoy that breaks retention; scripted solver with same probe budget; behaviour-only arm; paired Read donor checkpoint and metadata-only views; Write zero-start/no-edit control.
- **Failure modes observed:** exhausting the output allowance when weights are present (26 of 27 invalid submissions in the 5,000-token calibration); editing clean controllers (Luna); in the calibration, a decoy derived from hidden target logits leaked an aggregate cue (fixed later); API interruptions requiring retries.
- **Prompt/format choices that helped or hurt:** raising the output allowance from 5,000 to 12,000 and then 24,000 tokens turned weight access from a net loss into a large gain. A tensor tool (vs no tools) cut cost by about half with fewer reasoning tokens at ceiling accuracy.
