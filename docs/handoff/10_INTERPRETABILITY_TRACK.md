# The interpretability track: can a small model, in a loop, do what frontier models do with weights?

*Opened Nov 4, 2026. This file states a problem and the directions worth exploring. It does not fix a solution:
by the project's rule, the problem comes first, and the design is decided in discussion.*

---

## 1. Why this track exists

Shreyas's first example, in the first message of the project, was interpretability:

> "if you could just point the system at a given set of weights or the architecture of a language model, and then
> ask it to change different things and see how that affects the output, there it is essentially probing the
> system."

FIND (the benchmark used so far) is an interpretability benchmark built from neuron-like functions. But nothing in
Helix Probe has yet been pointed at a real network. A new piece of research makes this the natural next frontier,
and gives a published reference to replicate and test against.

## 2. The trigger: "Sparks of Weight-Space Programming" (MIT CSAIL, Nov 2, 2026)

**Source:** Rikiya Takehi, Jayden Teoh, Alex Zhang and Omar Khattab, *Sparks of Weight-Space Programming: LLMs can
natively read & write neural network weights*, a blog post at `rikiyat.github.io/blog/weight-space-programming/`.
It is not peer reviewed, and it is built on a single reader model. The authors say they are building a benchmark
and harness.

**What it claims:** a general-purpose frontier model (OpenAI's GPT-6 Astra), used as it is, reads and writes a
network's weights directly from a natural-language goal, with no gradient descent and no training loop.

**The experiments:**

| # | Task | Setup | Result |
|---|---|---|---|
| 1 | Name the game a policy was trained on | 4 PPO policies, same 500→32→32→5 shape, 17,253 weights each, weights as text, no tools | all 4 named, unprompted with options |
| 2 | Name the shape a small diffusion model generates | weights as text | correct shapes, drawn as outlines though the model makes filled ones |
| 3 | Training language and copying heads from middle layers of small transformers | Python allowed for analysis; the network can't be run | all correct, no false positives; it reinvented a known copying-head method unprompted |
| 4 | Fix a car policy stuck on a ramp | 171,664 weights, one episode shown, no tools, one try | 3.5% of weights edited; 0% → 100% success over 1,024 episodes |
| 5 | Write game policies from scratch | rules and source only, no rollouts, one reply | Breakout far above 500M-step PPO; Seaquest and Asterix below it |
| 6 | Write a Go network (1.48M weights) | Python sandbox; 0 or 50 forward passes | with 50 passes, beats an equal-size PPO net trained on 20M games |
| 7 | Find the sycophantic Gemma 3 270M | weights alone, then attention patterns | **failed from weights alone**; succeeded with attention patterns |
| 8 | Improve Qwen3.5-0.8B at math | tools; 0–50 forward passes | MATH-500 7.9% → 48.1% by editing 0.016% of weights |
| extra | Improve Gemma 3 270M at math | the same | no gain (6.8% → best 7.7%) |

**The detail that matters most for us:** the effect of the feedback budget in experiment 8.

| Forward passes allowed | MATH-500 |
|---|---|
| base | 7.9% |
| 10 | 12.3% |
| 25 | 14.1% |
| 50 | 48.1% |

The big result came only with 50 runs of the network between edits. In experiment 6 too, the 50-pass version
played practice games, studied its losses, and kept an edit only if it won more. **The strongest results are
"read, edit, run, observe, revise": an experiment loop, run by a frontier model on a small budget.**

**What the post does not say:**
- Nothing about smaller or weaker reader models. None was tested; Astra was the only reader.
- Nothing directly about where the capability comes from. The ability is framed as something "the current
  generation of frontier LLMs" are "starting to become eerily good at".
- Their own limits: "Editing weights could remove an obstacle that hid an ability, but it could not add an ability
  the model lacked" (the Gemma result).

## 3. The problem, stated plainly

> Frontier models can interpret and repair small networks from their weights, helped by a few dozen experiments. Can
> a weak, cheap model (DeepSeek V4.1 Flash, thinking off), inside a loop that structures its reasoning and lets it run
> many cheap experiments, reach comparable understanding of a network, and if so, through what?

This is Helix Probe's core thesis applied to its original target: direct the reasoning so the result depends less
on the model's raw intelligence.

**Shreyas's working guess:** "a small model can still read weights; just not as well. So trial and error can solve
that." The track should test that guess, not assume it.

## 4. Taking the capability apart (hypotheses, not facts)

What Astra seems to combine, read from the experiments:

| Ingredient | Evidence in the post | How a weak model might fare | What could stand in for it |
|---|---|---|---|
| **Knowledge** of how networks compute: circuits, heads, feature directions, known failure modes | it reinvented a copying-head method unprompted | thinner and less reliable | the **library** (Helix Probe's third representation, never yet exercised): handed-in knowledge of known circuit types and techniques |
| **Reading raw numbers:** seeing structure in thousands of floats as text | experiments 1, 2, 4, 5 had no tools | probably poor (long numeric context, no thinking) | code: summaries, norms, top connections, clustering, done by the sandbox, not the model |
| **Forming concrete hypotheses:** "this unit detects X", "this head copies" | the explanations it gave | **the main risk.** ARC showed Flash writing vague hypotheses ("match a target") that can't be tested | a menu of candidate hypotheses from the library; the role picks one to test instead of inventing one |
| **Testing against behaviour:** forward passes, practice games, keep-if-better | experiments 6 and 8 depend on it | this is what the loop is for; probes on small networks are nearly free | Helix Probe's loop: predict before you see, repair, trials, notebook |
| **Editing precisely:** choosing which weights to change and by how much | 0.016% and 3.5% edits | unknown | edits as probes: the experiment itself is "change these weights, run, observe" |

**The guess, sharpened:** a loop can replace much of the *testing* and some of the *reading*, by turning
weight-reading into probing a white box. It is unclear whether it can replace *hypothesis formation*. That is the
crux of the track.

## 5. What "the box" could be (choices to discuss)

In Helix Probe terms, the network under study is the box, and the adapter decides what a probe and an observation
are. That choice shapes everything, and it is open:

- **Black-box probing of a white box.** A probe is an input, and the observation is outputs or activations. Closest
  to FIND; doesn't need weight reading at all.
- **Interventions.** A probe is an edit (ablate a unit or head, scale a row, patch an activation) plus inputs; the
  observation is the change in behaviour. This is how interpretability researchers actually work, and it turns
  "reading" into "testing".
- **Weight views.** A probe is a request for a summary of some part of the weights (a matrix's top connections, a
  unit's input profile, singular values); the observation is that summary. It is reading, but chunked and
  code-computed.
- **Mixtures of these.** Possibly the realistic option.

**What the model is, here, is also open.** It could be:
- a `predict()` that simulates the network's behaviour, as FIND does today;
- a description of components and what each computes, made executable so it can be checked against probes;
- or both: a component map whose predictions come from running the described parts.

The principle to protect: **the core doesn't change.** All network-specific knowledge goes in the adapter and the
library.

## 6. Directions of exploration

Each direction is a question with an example of what to try, not a commitment.

1. **How far does the same model get without the loop?** Run DeepSeek Flash in Astra's own protocol on a replicated
   task: weights as text, one reply. This is the same-model control, the lesson from FIND. If Flash already does well,
   the story changes; if it fails, the loop has room to show something.
2. **Does probing replace reading?** Give the loop interventions and inputs but no raw weight text. Measure how far
   it gets compared with weight text alone, and with both.
3. **Does the library supply the hypotheses?** The same loop, with the library empty and then filled with known
   circuit types and techniques. This is the first real test of the third representation, and it speaks directly to
   the hypothesis-formation crux.
4. **How does understanding grow with the experiment budget?** Astra's jump came between 25 and 50 runs. Plot score
   against probes for the loop; cheap networks make hundreds of probes affordable. Is there a budget at which a weak
   model catches up?
5. **Reading vs repairing.** Interpretation (name the game, find the copying heads) and repair (fix the stuck car)
   may need different things. Repair has a natural "goal" and fits the planner; interpretation needs a scoring rule
   for the description.
6. **Where does it break?** The sycophancy case defeated even Astra from weights alone. Are there network properties
   that only interventions reveal? This links to hidden state: behaviour that isn't visible in a single forward
   pass.
7. **What transfers?** Does a model of one network help on a sibling network (another game, another seed)? This
   touches the continuity question at a new scale.

## 7. Candidate tasks (published references first)

| Task | Reference | Cost | Why |
|---|---|---|---|
| Name the game from a policy network (their experiment 1) | Astra: 4 of 4 | train 4 small PPO policies (MinAtar-size); CPU may be enough, to be checked | cheapest replication; clean metric; small networks |
| Fix a failing policy (their experiment 4) | Astra: 0 → 100% with one try, no tools | a Kinetix-style environment and one failing policy | repair; a goal the planner can use |
| Copying heads or training language in small transformers (experiment 3) | Astra: all correct | a few 7M-parameter character transformers | classic mechanistic interpretability; checkable ground truth |
| FIND's neuron-like functions, as now | find-v2 and v3 results | done | a baseline already in hand |
| Repair a real LLM failure (experiment 8: Qwen3.5-0.8B looping) | Astra: 7.9% → 48.1% MATH-500 | needs a GPU to evaluate | the most impressive target; later |

The fair comparison follows the standing rule: replicate the published setup as closely as possible (the same
networks or the same recipe, the same metric), then compare a much weaker model with tighter limits. Always report
it next to the same-model control.

## 8. Constraints and risks

- **Compute:** the VM has 2 CPUs and no GPU. Small policies and small transformers are feasible; LLM repair is not,
  without a GPU.
- **Ground truth:** interpretation tasks need checkable answers (the game, the head, the language). Avoid tasks
  scored only by a judge.
- **Hypothesis formation may be the wall.** If ARC's lesson holds, the loop gathers evidence well but doesn't make
  the model think of the right idea. The library directions (3) and the intervention directions (2) are the bets
  against that.
- **Novelty is time-sensitive.** The reference is two days old (Nov 2, 2026) and the authors are building a
  benchmark, so a weak-model, loop-based result is timely now.
- **Scope creep.** This must stay an adapter plus a library on the same core. If it seems to need a new core
  mechanism, that is a design discussion with Shreyas first.

## 9. Open questions for the discussion with Shreyas

- Which task first? The builder's lean is experiment 1: cheapest, with a clean metric and small networks.
- What is a probe: inputs, interventions, weight views, or a mix?
- What is "the model" of a network in this setting, and how is it scored?
- How should the library be built, and how big should it be? Is it a menu of hypotheses or a short primer?
- What publishable claim would this aim at? For example: "a cheap model in a probing loop matches a frontier model's
  weight interpretation on task X at budget Y".
- Is this the main track now, ahead of ARC goal discovery? The two share the hypothesis-formation problem, so
  progress on one may help the other.

---

## 10. Update, Nov 4 evening: the MIT setup in detail, replications, a first baseline, and the plan

### The MIT setup (from their logs: `github.com/RikiyaT/lm_understand-logs`, CC BY 4.0)

The logs hold every prompt, reply, code run and network; fetch them with `bench/weights/fetch_mit.sh`.

**The harness:**
- Astra is run through the Codex CLI with every built-in tool off, and audited for tool-free turns.
- Where code is allowed, it writes **one Python block per turn**. Their sandbox runs it (bubblewrap, no network, a
  working folder kept between runs, a timeout, output cut at 20,000 characters) with the weights preloaded as
  `W` (numpy, scipy, scikit-learn, CPU PyTorch). The printed output comes back as the next message.

**The formats, by experiment:**

| Format | Experiments | Access |
|---|---|---|
| Text, one reply | 1 (games), 2 (shapes), 4 (fix the car), 5 (write) | weights pasted as text (3 decimals); no tools; exp 2 also forbids mental forward passes |
| Code, no running | 3 (language and heads), 7 (weights only) | Python over the weights; running the network or any layer on any input is forbidden; up to 100 runs |
| Code + forward passes | 6 (Go), 8 (Qwen math), 7 (attention tool) | a budget of 0–50 passes through a harness function; edits by code |

**The networks:**
- available for experiments 1–4;
- experiment 1 is 4 networks (the best seed per game only), open answer;
- experiment 3 is 3 networks, a closed 3-way choice, plus 24 head labels each, with ground truth in `heads.json`.

### Replications so far (other groups)

- **Alan Turing Institute** (`alan-turing-institute/weights_editing`), text format:

  | Reader | Exp 1 (games) | Exp 1, shuffled weights | Exp 2 (shapes) |
  |---|---|---|---|
  | Astra | 12/12 | 0/4 | 9/9 |
  | Opus 5.5 | 12/12 | 0/4 | 8/9 |
  | Opus 4.5 | 1/4 | 1/4 | 2/3 |
  | DeepSeek-V4-Pro | 3/4 | 1/4 | 1/3 |

  DeepSeek-V4-Pro also named games confidently on shuffled weights.
- **`nihilistau/weight-space-claude`:** an Opus 5.5 replication, tool-free.
- **`jhpark94/weights-only-replication`:** Opus 5.5 still gets 4/4 with the grid, channels and "game" all removed.
- **`leofmarciano/weightspace`:** a tool harness (list, describe, read slices, persistent sandbox, edits,
  checkpoints, rollbacks, budgeted probes) that reports no results.

### First baseline (ours): DeepSeek V4.1 Flash on MIT's exact experiment 1 text prompt

Script: `bench/weights/text_oneshot.py`. Three repetitions per network.

| Condition | Correct | Notes |
|---|---|---|
| Thinking off | 3 of 12 | chance is 3 of 12 |
| Thinking off, shuffled weights | 0 of 12 | |
| Thinking high | 5 of 5 so far | Breakout 2/2, Freeway 3/3; Pac-Man and Pong pending; about 13–25k output tokens per answer |

**Reading:** a weak model can read these weights natively **when it thinks**, and can't with thinking off.

### The plan (wave 1, before any build decision is final)

**The question, decomposed:**
1. Can Flash read weights at all? (the text format; started above)
2. Does code over the weights help a weak model read, and does structure (the Helix loop) beat a free conversation
   (MIT's protocol) for the same model?
3. How much of a result comes from reading vs running the network? These are separate arms (weights only, running
   only, both), with arms that run the network reported as a different condition from experiment 1.
4. Does a primer library help form hypotheses? The primer never lists candidate answers.

**What a "model" of a network is** is a core decision, and it is open. The proposal:
- a set of claims, each with a test (code over the weights, or an intervention when running is allowed) and an
  expected result;
- code re-runs the tests to judge a model, as it now replays the notebook;
- a `predict()` that runs the weights is not allowed: it would fit perfectly and explain nothing.

**Tasks first:** MIT's experiments 1 (games) and 3 (language and heads), in the code formats, with shuffled
controls and 3 repetitions. **More networks (n) next:** retrained experiment-2-style diffusion MLPs, and FIND's
roughly 150 MLP functions.

---

## 11. Built (Nov 4, late): `bench/weights/wsp.py` and the VM job `scripts/run_weights.sh`

**One module, outside the core.** It holds tasks, a sandbox, two protocols, graders and a report.

**Tasks (MIT's own networks and answer keys):**
- `exp1`: name the game, 4 policy networks, open answer;
- `exp2`: name the shape, 3 diffusion networks, open answer, text format;
- `exp3`: which corpus, plus 24 head labels per network; their exact message, code format.

**Formats:**

| Format | What the reader gets |
|---|---|
| `text` | MIT's exact prompt |
| `code` | Python over `W`; running the network forbidden (their exp 3 rules) |
| `run` | plus `forward(X)` with a budget of 50 passes, and edits by `save(W)` / `reset()` (their exp 6/8 condition) |
| `full` | `run` plus the weights as text in the message. **The complete setup:** read the text, decide, code an edit, run the edited network, observe |
| `blind` | forward passes only, weights hidden (separates running from reading) |

**Protocols:**
- `mit`: their conversation, one Python block per turn.
- `helix`: narrow roles in series, each a fresh call:
  - the experimenter writes code plus what it expects to see, before running it;
  - a judge call scores expected against actual;
  - the updater revises the findings (claims citing experiment IDs) after a surprise;
  - every 6 experiments, the theorist rewrites the findings from the evidence alone;
  - an answer call gives the final answer. Only the experimenter sees the weights text.

**Controls:** `--shuffle` reorders each weight array's values. `--effort high` (the default) or `none`.

**Credibility, built in:**
- MIT's networks and prompts are used byte for byte where they exist. New conditions are written in their style and
  named as new conditions.
- The graders reproduce MIT's published scores on MIT's own answers: exp 1 4/4, exp 2 3/3, and exp 3 6/6 corpora
  with every copy head. This is checked in the job's preflight.
- Every reading condition has a shuffled-weights control. There are 3 runs per network.
- Every call is logged with its reasoning, and every code run with its output, plus the answer, the grade, the token
  use and the time.
- **The answer can't leak into the sandbox.** The reader's code runs in a folder with an opaque name (the run folder's
  name holds the answer), and a Python audit hook, which can't be removed once added, refuses any read or listing of
  the repo (MIT's answers, other runs, results), any network call and any new process. The preflight checks all
  three. On the VM bubblewrap is blocked (`loopback: Failed RTM_NEWADDR`), so there is no kernel-level isolation and
  runs record `isolated=false`; the guard is the protection. A determined bypass (ctypes) is possible in principle,
  so code touching files, the environment, processes or the network is flagged for a person to read.
- Each run flags code that may break the format's rules (a forward pass where forbidden, training or fitting).
- Replies with more than one code block are counted (`extra_blocks`), not hidden.

**Limits, stated:**
- **No Qwen experiment 8.** It needs a GPU. Any later comparison must report the unedited, thinking-off Qwen baseline
  beside it.
- **The Helix arm's findings are not judged by code.** A replayable claims model is still the open core question.
- The Helix match score comes from a judge call, not a fixed rule.
- **n is small:** 4 + 3 + 3 networks, times 3 runs. More networks come next (FIND's MLPs, retrained exp-2
  networks).

**Local checks before the job:**
- the sandbox, the budget, blind mode, edits, and both protocols end to end (a live smoke test of each);
- the text baseline:

  | Condition | Correct |
  |---|---|
  | Thinking off | 3 of 12 |
  | Thinking off, shuffled | 0 of 12 |
  | Thinking high | 6 of 6 finished (Breakout 3/3, Freeway 3/3) before the workspace stopped |

**The job:**
- 19 stages, in the order of `ALL` in the script; each is one condition and pushes to `results/weights/<stage>/`.
- `results/weights/report.md` holds one table for every condition.
- **Expect several days in all.** The text stages take about 2 hours; each Helix stage can take many hours (thinking
  on, about 40 experiments per run, 12 runs). Stages are ordered so the most important finish first.
- Restarting continues: finished runs are skipped, and Helix runs resume from their notebook and their edited
  weights.

### The Aether prompt

```
Start my Helix Probe weight-space job on this machine and report back. Don't change any code or settings.

1. In /home/ubuntu/helix_probe, run `git pull`. Check that scripts/run_weights.sh and bench/weights/wsp.py exist.
2. Run `python3 -c "import numpy, scipy, sklearn; print('ok')"`. If sklearn is missing, run `python3 -m pip install --user scikit-learn` (add --break-system-packages if pip refuses), then check again. If it still fails, report and stop.
3. Optional, for network isolation of the code sandbox: if `command -v bwrap` prints nothing and `sudo -n true` works without a password, run `sudo apt-get install -y bubblewrap`. If sudo needs a password, skip this step and say so.
4. Start the job in the background, exactly like this, from /home/ubuntu/helix_probe:
   `setsid nohup bash scripts/run_weights.sh > weights_job.log 2>&1 < /dev/null &`
5. Wait about 5 minutes, then quote the last 15 lines of weights_job.log. A good start shows "== preflight", "python ok", "MIT logs in", a "sandbox:" line, "sandbox, budget, blind mode and the graders (on MIT's own answers) ok", "model answers on key 1 of 2", "model answers on key 2 of 2", "GitHub: can push", then "== exp1-text-high: started". A line starting with "preflight:" or a Traceback means it stopped: report it exactly, and don't edit anything.
6. Report `free -m`, `df -h /`, and the job's pid (`pgrep -fa weights_job_snapshot`).
7. Then stop. Don't stop, restart or kill any process. No cron jobs, timers, monitors or reminders.
```

Status prompt: "In /home/ubuntu/helix_probe, quote the last 15 lines of weights_job.log and say whether
`pgrep -fa weights_job_snapshot` is alive. Change nothing."
