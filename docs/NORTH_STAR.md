# North star

*The one thing this project is trying to achieve right now. Everything else in these docs serves it. Changing it
needs Shreyas's explicit decision, recorded in `docs/JOURNAL.md`.*

## The goal

**Show that Helix Probe lets a cheap model switch off one specific ability inside a real language model by editing
its weights directly, while the rest of the model keeps working, and that the loop, not luck, is what makes it work.**

Concretely: we name an ability ("turn masculine words into feminine ones", "add two numbers"). The cheap model (today
DeepSeek Flash) works out where that ability lives in the target model and changes the weights so the model can no
longer do it, without gradient training. We then check the edit on tests the editor never saw.

Removing the ability completely is best. Suppressing it (the model stops doing it, even if the knowledge could come
back) also counts and is worth showing. We measure which of the two we got.

## Why it matters

- **For interpretability:** an edit that removes exactly one ability is proof that you found where it lives. A wrong
  idea of the model produces an edit that fails or breaks other things, so the result can't be argued into being
  right.
- **For alignment:** the same move, aimed at a harmful ability, is a way to take that ability out of a model.
- **For Helix Probe:** this is a long, evidence-driven search (guess where the ability is, cut, measure what broke,
  revise), the kind of problem the loop was built for. A single conversation tends to guess and stop.

## What counts as done (the result we must be able to show)

For at least two abilities, on the largest target model we can run:

1. **Removal:** the ability drops close to the floor on held-out tests.
2. **Precision:** closely related abilities and general fluency stay near the unedited model's level.
3. **Comparison:** the same cheap model without the loop (one conversation, MIT's protocol), a scripted non-LLM
   method, and a random edit of the same size, all run on the same tests.
4. **Durability:** a "comeback" test: given a few worked examples, does the ability return? That says whether we
   removed it or suppressed it.
5. **Repeats and traces:** several runs per arm, every prompt, every piece of code and every number saved, so anyone
   can check or re-run it.

**A breakthrough** would be any of these: the loop removes a hard, spread-out ability (like addition) cleanly where
the single conversation and the scripted method fail; or an edit survives the comeback test; or the same method works
better on the larger model than on the small one (the scaling evidence that more compute would pay off).

**Publishable either way:** if none of that happens, a controlled, repeated comparison of capability removal by weight
editing, across arms and model sizes, with honest negatives, is still a first: as of Nov 6, 2026, the published
weight-space programming work on language models is all repairs, not removals.

## Goal 2 (added Nov 7, 2026, by Shreyas): a map of the model, discovered by an open-ended loop

**Run Helix Probe as an open-ended discovery loop on a real language model: it keeps finding parts of the weights
whose change predictably changes a behaviour, verifies each on prompts it never saw, and adds it to a growing map. It
keeps going as long as it is run. Show the map as a demo where turning a part up, down or off changes the model's
behaviour the way the map says it will.**

- **The same loop, pointed at a different thing.** Goal 1 searches for one ability to remove. Goal 2 doesn't search:
  it explores, choosing each experiment to be different from what it already knows. That's easier to keep going wide
  on than a search, which must also improve.
- **First prove the discovery is reliable, then run it long.** Short calibration runs must show that its discoveries
  replicate on unseen prompts, rise above what random edits produce, keep coming as the map grows, and include the
  parts we already know (the gender direction, the "+" and "feminine" triggers). Only then the long run, uncapped:
  40, 100 or more discoveries.
- **What counts as done:**
  - the calibration results;
  - the long run's map, every entry with its location, its intervention, the effect predicted before applying it,
    and the effect measured on unseen prompts;
  - the curve of verified discoveries against experiments, which shows whether the loop keeps finding new things;
  - the demo.
- **Overlap with Goal 1:** every edit in Goal 1 is an intervention with a measured effect. Those effects (the gender
  direction, the trigger redirects) are map entries, and the known parts the calibration checks against.

## Where both goals point (vision, Shreyas, Nov 7, 2026; not a step in the current plan)

- **Goal 1's end product:** you tell a cheap model, in plain words, "change this behaviour of that model". It runs a
  few loops and hands back updated weights. It is like fine-tuning, but far cheaper and faster: programming at the
  level of the weights.
- **Goal 2's end product:** a representation of the weights (the verified map) and a UI to turn parts up, down or off
  and watch behaviour change.
- **What exists toward it now:**
  - `edit.py` already takes a goal in words, runs the loop and returns an edit file. A minimal "type a change, get
    weights back" interface is a thin wrapper over it.
  - What it lacks is reliability: Goal 1's results show that edits often hit a shortcut (a trigger word) rather than
    the behaviour.

## What is deliberately not fixed

The target models, the abilities beyond the first two, the exact protocol settings and the code can all change as we
learn. The goal above doesn't, unless Shreyas changes it.

## Not the goal right now

- More arms on MIT's game-network task (exp 1). Its results so far are recorded; it isn't where the loop's value
  shows.
- Adding new abilities to a model. Interesting, harder, and MIT's own attempt failed. It comes after removal works.
- FIND and ARC-AGI-3. Their results stand (see `docs/handoff/03_ANALYSIS.md`); paused while this goal is the focus.
