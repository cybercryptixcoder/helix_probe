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
