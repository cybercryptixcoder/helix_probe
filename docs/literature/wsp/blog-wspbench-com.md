# WSPBench website: selective-repair benchmark summary (plus prompt and weight format from the repository code)

- **Key:** blog-wspbench-com
- **Authors / organisation:** Alex Carter (X @NotAlexCarter; GitHub alexcarterhq)
- **Date:** 2026-11 (page undated; content matches the v0.2.2 selective-repair release)
- **Link:** https://wspbench.com (repo: https://github.com/alexcarterhq/wspbench)
- **Kind:** benchmark
- **Read from:** the full wspbench.com landing page (raw HTML, all text, and its demo script). The site has a single
  page and gives **no prompt and no weight serialisation format**. Because those were the point of this entry, we
  also read from the repository, at `main`: `experiments/run_selective_repair.py` (in full),
  `experiments/repair_cases.py`, `experiments/repair_hard_cases.py` (the case generator used for the full runs) and
  `src/wspbench/v2/serialization.py`. **Not read:** the rest of the repository code, data bundles and run outputs.
  The companion entry `github-alexcarterhq-wspbench.md` covers the README and reports; this entry adds only what is
  new.
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The site presents WSPBench as a test of whether reading a network's weights helps an AI agent diagnose and fix a
faulty network, compared with probing its behaviour alone under the same probe budget. The agent must predict each
patch's effect before trying it, and the fix is graded on inputs the agent never sees, including a check that
working behaviour is kept.

## What they studied
Small controller networks with a planted fault (four mechanisms: coupled gates, sensor routing, readout
redistribution, cross-layer drift) or no fault (clean control). The site's animated example is a 2 x 2 linear map
with one sign-flipped weight. From the code: the full-run controllers are one-hidden-layer ReLU networks with six
named inputs, 14 hidden units and one GO/BRAKE logit (by our count 113 scalars). Solvers: GPT-6 Astra, GPT-6.1 Sol,
GPT-6.1 Terra, GPT-6 Luna, and a scripted baseline.

## How they did it
Site: each case offers 14 choices including leaving the weights alone; exactly one passes. Each model runs every
case twice with the same probe limit, once also seeing the weights; other arms give weights only or add hidden-unit
readings. Two probes on the unchanged controller, then committed forecasts, then up to four probes on candidate
patches. Pass: at least 95% on the fault cases and at most 2 pp accuracy loss on previously correct cases; for a
clean controller the right answer is to leave it alone. Reproduction commands use suite `sol-full` with seed
1804227 (40 cases, 80 paid sessions for Sol).

Code (what the model actually receives): a developer message with fixed instructions, then one user message that
is canonical JSON (sorted keys, no spaces) holding the public task, the access flags and, in weight arms, the
weights. Each turn the model must make exactly one function call from a strict tool schema: `commit_forecasts`
(predicted target success and retention, each in [0,1], for every intervention ID), `practice` (probe indices,
optionally with one intervention applied after commitment), and `submit_patch` (one intervention ID).

## What counts as an explanation here
Implicit: committed per-intervention forecasts plus the chosen patch. No mechanism description is requested.

## How they judged success
Faults repaired out of 32, clean controls preserved out of 8, paired change in repair rate with 95% intervals from
resampling the 8 seed groups, and estimated API cost.

## What they found
New relative to the companion entry: per-model 95% intervals for the change with weights, Astra +46.9 pp (+34.4 to
+59.4), Sol +50.0 (+28.1 to +71.9), Terra +46.9 (+28.1 to +68.8), Luna +37.5 (+18.8 to +56.2). Estimated API cost:
Astra at least $53.52, Sol $8.37, Terra at least $3.54, Luna at least $0.32, total at least $65.75 over 378 recorded
attempts. 50 sessions interrupted by the API were rerun (up to 4 at a time), then 8 still interrupted were rerun
singly; 50 scores were recovered; charges for 58 interrupted attempts are unresolved. Repair counts match the
companion entry (Sol 30/32 with weights vs 14/32 probes only; scripted 5/32).

## Limits and open problems they name
The page itself states none beyond the beta label and unresolved charges; see the companion entry for the
repository's limitations.

## What we take from it
- **Format reference:** WSPBench gives weights as nested JSON lists keyed by tensor name inside one canonical JSON
  message, alongside named inputs and the forward equations. This is a compact, labelled-by-tensor, unlabelled-by-row
  format we can compare against row-per-line text.
- **Warning for interpreting its "weights help" result:** the weight arm also sees an explicit menu of edits (tensor,
  index, value) and the forward equations, so the reader's job is to evaluate 14 named candidate choices on a
  113-scalar ReLU net, which it can in principle simulate by hand; this is closer to guided computation than to
  open-ended reading.
- **Method:** the strict function-call protocol (one call per turn, schema-validated forecasts) is a clean way to
  force commitments and parse them without free-text scoring.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** repairs out of 32, probes only / weights + probes: Astra 17 / 32, Sol
  14 / 30, Terra 14 / 29, Luna 8 / 20; scripted baseline 5. Clean controls preserved 8/8 for all but Luna (1/8 and
  0/8). Reasoning effort is set per model config (not stated on the page).
- **Target networks:** from code (`repair_hard_cases.py`): h = relu(w0 x + b0), logit = w1 h + b1, GO if logit > 0;
  6 named inputs (clearance, alignment, particulate signal, reflected light, surface gradient, lateral movement), 14
  hidden units; w0 drawn at random, w1/b1 fitted by least squares to a random target readout on 1,200 samples; a fault
  is the inverse of one candidate edit. Parameter count not stated; 113 by our arithmetic from the shapes. The site's
  demo is a 2 x 2 linear map (4 scalars).
- **How the weights were presented:** text, as canonical JSON in the first user message: `{"access": {...},
  "task": {...}, "weights": {"b0": [...], "b1": x, "w0": [[...], ...], "w1": [...]}}`, i.e. per tensor, nested
  lists, rows unlabelled, Python float repr (fitted values rounded to 4 decimals for w0/b0 and 5 for w1/b1 before
  fault edits). `null` weights in behaviour-only arms. A separate bit-exact float32 serialiser (`.9g`, shape plus
  flat values) exists in `serialization.py` but the runner passes `case.weights` lists directly. Total tokens not
  stated; input budget 48,000 tokens.
- **Prompt:** developer message (paraphrased): you are diagnosing and repairing a controller; one function call per
  turn; commit predictions for every intervention before choosing or testing a patch; if probing is enabled you may
  request practice observations, two on the unchanged controller before commitment and up to four in at most two
  requests after, one intervention per request; choose `none` if behaviour already meets requirements; the scoring
  bank is hidden. Task JSON: input names and forward equations; a report text (investigate unsafe GO actions in the
  target slice, may be a false alarm, all targets require BRAKE, keep correct actions on ordinary states, the
  retention bank includes near-boundary states); 12 practice examples with inputs and expected actions; the
  intervention menu (`none` plus i01–i13: twelve mechanism-specific sequences of two or four `add` edits, each with
  tensor, zero-based index and value, plus one broad output-bias shift; 14 choices in all); forecast and repair definitions with the pass thresholds. Candidate answers: yes, the full
  intervention menu. Path: `experiments/run_selective_repair.py` (`SYSTEM`, `Trial.initial`, `action_tools`) and
  `experiments/repair_hard_cases.py` (`public`).
- **Access regime:** 5 model turns; 48,000 input tokens; 24,000 output tokens in the full runs (5,000 default,
  12,000 hard-check); 2 pre-commit and 4 post-commit probes; tool choice required, no parallel calls; arms: weights
  only, behaviour, weights + behaviour, weights + activations (probes also return hidden values).
- **Controls:** clean controllers; broad output-bias shift decoy (fixed at -2.0 in matched suites); scripted solver
  with the same probes; behaviour-only arm; case generator rejects cases unless exactly one intervention passes and
  a target-fixing edit exists that breaks retention.
- **Failure modes observed:** on the page, API interruptions and unresolved charges; Luna edits clean controllers.
  Others in the companion entry.
- **Prompt or format choices that helped or hurt:** none stated on the site. See the companion entry for the output
  budget effect.

## Tags
unit: weights | whole-model
form: description
method: agent | weight-analysis
eval: benchmark | prediction/simulation
goal: debugging | control/editing | evaluation-of-methods
