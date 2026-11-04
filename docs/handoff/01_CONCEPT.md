# Helix Probe: the concept

*A self-contained description of what Helix Probe is, why it exists, and what it is trying to become. Written
from Shreyas's own words in the design conversation of Nov 3–4, 2026 (verbatim in `08_shreyas_verbatim.md`) and
from what was agreed in that conversation. Quotes are his.*

---

## In one paragraph

Helix Probe is a mechanism for learning how an unknown system works by trying things. You point it at a black
box: a function, a game, an instrument, a piece of software, eventually a neural network. It runs one small
experiment at a time. It keeps a record of everything it tried, and it builds a model of the box as code it can
run. That model must predict each experiment before the box answers. Whenever the box surprises it, the model is
revised to match the evidence. Over many small steps, a cheap model becomes, as a whole, capable of understanding
the box and then of using that understanding: predicting it, explaining it, and making it do things nobody tested.
The mechanism knows nothing about the box. Each new box plugs in through one adapter file.

## Where it came from

Shreyas built Helix Evolve, a multi-agent evolutionary system aimed at a mathematical optimisation problem. His
realisation afterwards:

> "the most interesting part about our system that we've built is not just the evolutionary setup. Evidently, it
> was not able to break the world record and all of that. What I do think is the more interesting part is our
> knowledge storing and our iterative trial and error."

> "we're building a system that just tries things, and the more things it tries, the more informed it becomes."

Pointed at something other than optimisation, the memory becomes "less a record of what works and what doesn't,
and more an internal model that the system has built up". Helix Probe is that idea on its own, rebuilt from
scratch. Helix Evolve was "way too complicated, unnecessarily heavy, and convoluted". It grew "into such a massive
web of different things happening that it is very difficult to keep up with and very difficult to also trace where
problems are coming from".

## What it is

> "a system that can iteratively probe an environment and gain information about it."

> "We're just trying to direct reasoning, because if a model is simply given a task or told to learn something, it
> will be highly dependent on the intelligence of that system... By just iteratively trying things over and over
> and over, like a thousand times, each time you grow a representation and use that representation to make sure
> you don't do the same thing over and over again and try different things. Each time, you're giving the model a
> very small thing to do, just one new experiment to try or whatever, and it becomes, as a whole, more and more
> capable of actually doing that thing and actually learning about that system."

The deliberate setting is a weak model: DeepSeek V4.1 Flash with thinking off. The point is to "detach the
intelligence of the system, of the model itself, from the task it's given", making progress mechanistic: try one
thing, then the next, until "we've got a refined enough idea of it".

## What it is not

- **Not a search or an optimiser.** "This is not about discovering hills. It is not about a search space... it's
  less so about what all exists, and it's more so about what we're trying." "it's a probing mechanism." No
  evolutionary layer, and no optimiser on top that minimises exploration ("That would be overly complicating it
  for no reason").
- **Not a claim of a revolutionary memory architecture or loop.** "We're just trying to see if we can find some
  representation, some memory representation that allows us to build these internal models and try different
  things in a meaningful way."
- **Not built for one box.** "The system is a mechanism. This mechanism can be applied to anything." Whatever is
  probed is "an additional code file... the socket that connects the two", and "the core mechanism itself should be
  completely agnostic".
- **Not parallel agents.** "Multi-agent" means agents in series: "each agent has its own system prompt. We're still
  using just one API key and making just one call at a time".

## Examples Shreyas gave, and the ones we added

His examples:
- **Interpretability:** "point the system at a given set of weights or the architecture of a language model, and
  then ask it to change different things and see how that affects the output".
- **An instrument, or a mock-up** with dials and knobs and an output canvas, where "even though it didn't know
  initially and it wasn't told what this system is, it is able to create an internal model".
- **A video game with messed-up controls.** Get a character from A to B; having learned the model, "not only get
  your character from A to B, but to any other point in that environment".

Added in discussion (each one adapter file; engineers call this system identification, computer science calls it
active model learning):
- a neuron or attention head;
- a reward model (which features it actually rewards: a map of where it can be gamed);
- which prompt features flip a model's refusal;
- an undocumented API, CLI or network protocol;
- a physics simulation with hidden constants;
- a hidden cellular-automaton rule;
- a black-box circuit;
- pricing or recommender engines.

## The three representations, and how they were realised

Shreyas's initial picture had three internal representations:

| He asked for | What it is in Helix Probe |
|---|---|
| "Similar to the Atlas... what worked, what didn't work, what improved, and what didn't improve" | The **notebook**: every experiment, its question, the probe, what came back, what the model of the time predicted, the match, the cost. Append-only. |
| "A model of the world, whatever world it is given... more and more refined as we go" | The **model**: a Python function `predict(probe)` that simulates the box, with its beliefs as comments citing evidence. Every version that was ever current is kept, as version control of the memory. |
| "Another knowledge system that is just a database of information... domain knowledge... some tricks" | The **library**: knowledge handed in from outside. Read-only, and it can be switched off to measure its worth. |

The key design decision: **the model is executable**. Beliefs in words can't be checked; code can. That makes
"knowing the box" and "using the box" the same thing, and it lets code, not the LLM, measure progress.

## The three problems it has to solve (from Helix Evolve)

Shreyas asked to focus on the problems, not on Helix's solutions:

1. **Continuity.** Each step must build on the last ("not brainwashed"), so trial and error adds up. In practice:
   evidence always persists, and a conclusion persists only while it keeps matching the evidence.
2. **Context growth.** "For the given step, it does not really require the system to know everything that's been
   done so far." In practice: the model compresses the notebook. What it already predicts shrinks to a line; what
   it gets wrong is shown in full. A real understanding is shorter than the data it explains, so model size is both
   a cost and a signal.
3. **Narrow jobs for a weak model.** Each call does one narrow thing, in series:
   - the **experimenter** chooses one experiment;
   - the **updater** repairs the model when it was wrong;
   - the **theorist** writes a model from scratch from the evidence alone, without seeing the current model, so it
     isn't anchored to its mistakes.

## The requirements that shape the design (Shreyas's points, agreed)

- **Evidence is ground truth.** "What evidence says is what holds up." The model must update rather than defend
  itself. In an early run the system called contradicting evidence "an exception" and patched the code; that is
  exactly what must not happen. A real exception is a rule about a region, with boundaries.
- **Real models, not memorisation.** "if this test input, then that test output... That's just gaming the system
  and also overfitting the data." A real model predicts probes nobody has run.
- **Don't force one law.** "It's not one universal law that governs something, so you can't just force the system
  to produce one law." Real systems (machines, neural networks) have structure: several rules, regions and
  components are fine if each predicts new probes.
- **A sense of progress without a separate evaluator.** Shreyas asked whether an evaluator is needed. The answer we
  agreed: the box is the evaluator. Progress is how well the model predicts experiments before it sees them,
  computed by code. Rising accuracy with a compact model means learning; flat accuracy with a growing model means
  epicycles.
- **Nothing box-specific in the core.** Code that "lists which buttons or regions have never been probed" was
  rejected, because it "would immediately scope this project to work only with a system that has buttons and
  knobs".
- **Stateful boxes.** "Our system would also need to model how states change and predict that." Boxes can keep
  hidden state. "Our system should be designed to handle any sort of a black box" (not just ARC). So in a stateful
  box the model sees the history since the last reset and can keep that memory itself.

## How it works (v3, the whiteboard)

```
each step:
  1 ACT      the box has a goal and the model can plan a way there?  -> run the first piece of that plan
             otherwise the EXPERIMENTER picks one experiment (every 2nd one is a random ordinary probe)
  2 RUN      the model predicts the result BEFORE the box answers; code compares the two (0..1)
  3 REPAIR   wrong?  the UPDATER revises the model         -- kept only if it explains the PAST better
  4 RETHINK  every 6 experiments, or when repairs stall,
             the THEORIST writes a model from scratch      -- kept only if it predicts the FUTURE better
                                                              (on trial for the next 3 experiments)
```

- **Fixes must explain the past.** A repair is kept if it fits the notebook better; on a tie, the shorter model
  wins.
- **New theories must predict the future.** A fresh model could always be written to fit what it was shown, so it
  must beat the current model on experiments that didn't exist when it was written. (An optional sealed exam of
  random probes no model ever sees can be switched on for cheap boxes.)
- **Using the model.** If the box has a goal, code searches through `predict()` for actions that reach it, and runs
  them for real. Every role sees the goal, and the model must state its best guess of when the goal is reached. A
  wrong guess gets tested by the box and corrected.
- **Budget** is counted in the box's own units: inputs for FIND, actions for a game.
- **The adapter** is one class: `probe()` is required; everything else is an optional hook with a safe default
  (random probes, scoring, cost, state, goals, planning, compact views).

## What success looks like

- **Now:**
  - the model's accuracy on unseen probes rises with experiments;
  - it beats random experiments at the same budget, the direct test of "directed reasoning beats sampling";
  - it scores against published systems, with their scorer, in their setup.
- **Later, the vision:** you hand it a system nobody documented, and you get back:
  - a short, runnable, readable model of how it works;
  - a notebook that backs every claim with an experiment;
  - the ability to make the system do things nobody tested ("from any A to any B").

  All of this from a cheap model, because each step is small, and it should be explainable on a whiteboard and
  traceable when it fails.

## The principles it is built under

1. **Lean, not compromising.** "By lean, I don't mean compromising... It is trying to do the best at what we're
   trying to do, and it's not doing unnecessary stuff."
2. **Explainable on a whiteboard.** "If somebody asks me, 'What is this, and how does it work?' I should be able to
   literally draw it on a whiteboard."
3. **Traceable.** "When there's an issue, we should know where it's from."
4. **Problems before solutions.** "We shouldn't think of a solution first. We should think of the problem first."
5. **No false self-validation.** "The quickest way to get falsely self-validated is by building our own setups..."
   Test on industry benchmarks, with their scorers.
6. **Every run serves two purposes:** it informs the next change, and it attempts a publishable result:
   "replicate the setup as closely as possible and try to beat that... with a worse model and more constraints".

## Where it stands (Nov 4, 2026, end of day)

- **Built.** Three versions are built and frozen side by side (v1, v2, v3) in `cybercryptixcoder/helix_probe`.
- **FIND** (an interpretability benchmark). Every iterative version scores 0.85–0.97, against FIND's published
  GPT-4 agent at 0.20 numeric and 0.01 strings.
- **The same cheap model in FIND's own one-conversation protocol** scores only 0.38 and 0.40–0.46, mainly because it
  often answers without experimenting at all. That is the direct evidence for the thesis that structuring the
  reasoning matters more than the model's intelligence.
- **At equal budget the advantage is real but modest.** It holds in every arm at equal experiments; at equal inputs
  it holds on numeric only.
- **ARC-AGI-3** (interactive games with hidden rules and goals) is not solved. A 5-game pilot completed no level:
  the models learn parts of the mechanics but can't yet discover what a level asks for. That is the open problem.
- The details are in `03_ANALYSIS.md`.
