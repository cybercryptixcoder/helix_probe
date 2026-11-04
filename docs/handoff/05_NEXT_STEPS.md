# Next steps, open decisions, and the conceptual threads still open

The order below is the builder's proposal, ranked by what it would tell us. Shreyas decides. Items marked
**(decide)** need his call.

## Right now: everything has finished, and nothing is queued

The VM is idle. The next runs need a decision and a small build.

## Next runs, in the order that teaches the most

1. **The budget-matched FIND control** (decides the FIND claim).
   - **Build:** a small change to `bench/find/aia.py`, an option to refuse `[DESCRIPTION]` until N experiments or
     inputs, using the protocol's own "keep experimenting".
   - **Run:** 80 functions at Helix Probe's median budget, twice (the control is unstable). About 30 minutes.
   - **If Helix Probe still wins,** the loop's structure matters. **If not,** the finding is that the free protocol
     fails by stopping early, and the loop's value is reliable persistence. That is weaker but still real.
2. **More repeats of v3 (no exam) on FIND,** two more seeds, about 4 hours. This tightens the numeric matched-input
   result (now p=0.09).
3. **The exam decision** (below). If it is removed, the repeats in step 2 are the confirmation.
4. **ARC: goal discovery, on a small run.**
   - Plan: 2–3 dev games plus 2 unseen games, 60–100 experiments each, as a pilot of an idea, not a scoring run.
   - The pilot showed the problem precisely: no concrete, testable goal hypothesis, half the experiments random,
     and chosen experiments under 3 actions.
   - Candidate change (generic, not ARC-specific): when a box has a goal and no level has been seen, the model lists
     concrete candidate goal rules, and the planner tests the cheapest untested one. Plus a per-box random share
     (lower when actions are scarce).
   - This is a design discussion first (Shreyas's rule: problem before solution).
5. **The interpretability track** (`10_INTERPRETABILITY_TRACK.md`). Point the loop at real networks, starting
   with a replication of a published weight-interpretation task. It is a design discussion first; it may become the
   main track, and it shares ARC's hypothesis-formation problem.
6. **A second benchmark that discriminates:** BoxingGym or AutumnBench (`04_PUBLISHING.md` P4).
7. **The write-up of the FIND result,** once steps 1–2 are in.

## Decisions waiting for Shreyas

- **(decide) The theorist.** It is unproven on FIND (no-theorist ties). Remove it now by the lean principle, or keep
  it until ARC can test it?
  - Builder's view: keep it for now. On FIND it was the final model in 8–14 of 80 runs, and on the lock toy it was
    decisive, so it is used, just not needed on easy boxes.
  - A test where structure is rich would decide it, but ARC isn't usable for that until goals work. A no-theorist
    arm on the next ARC or second-benchmark run is the cheapest test.
- **(decide) The sealed exam.** With the second seed, v3 without the exam equals v3-exam in final score, and it is
  more efficient per input.
  - Builder's view: remove it from the core (about 40 lines, one concept fewer); keep trials.
- **(decide) Merge the two goal mechanisms** (`solve`/`make_tasks` and the planner) into one. The builder favours
  it: one concept fewer.
- **(decide) Run size as a standing rule:** small runs to iterate, large runs only for final reportable numbers. This
  is the builder's proposal, not yet confirmed.
- **(decide) Install the updated run viewer** if that hasn't happened.
- **(decide) The full 25-game ARC run:** the builder recommends not running it with this design (0 of 35 levels in
  the pilot).
- **(decide) Targets:** ARC Prize 2027, and a FIND workshop paper. Is that the publication plan?

## Conceptual threads from the conversation that are still open

These came up in the design discussion and are not settled. Pick them up as discussion, not as build tasks.

1. **The third representation, the library** (handed-in knowledge: "you maybe tell it some rules... you give it
   domain knowledge... some tricks"), has **never been exercised in a benchmark run.** Every run used it empty. A
   test of its worth is easy (game rules for ARC, the FIND function-family hints) and is part of the original
   concept.
2. **The memory's shape.** Shreyas was open to "a graph or a tree or a different data structure". The notebook is a
   flat append-only log, and the model compresses it (what's predicted shrinks to a line). That has been enough so
   far. Whether a structured atlas helps at scale (1,000 experiments, or a box with many regions) is untested.
3. **Scale of continuity.** The context-growth problem is solved in principle by model compression, but the
   longest runs so far are about 60 experiments. A 1,000-experiment run on one rich box hasn't been tried.
4. **"Probe" underrepresents it.** Shreyas: "even the word 'probe' is kind of underrepresenting or misrepresenting...
   what we're trying to do". The thing is directed reasoning by small checked steps. Naming is open.
5. **The first application Shreyas named, interpretability on real weights** ("change different things and see how
   that affects the output"), has not been attempted. A small transformer with head ablations, or a reward model
   probed with paired responses, is one adapter file. It is the vision's real test.
6. **Is an evaluator needed?** Settled as: the box is the evaluator, and progress is prediction on arrival. Worth
   revisiting only if ARC shows goals need a separate signal.
7. **Not forcing one law.** Models with several rules or regions are allowed. Whether the updater and theorist
   actually produce structured models (rather than one law plus exceptions) on rich boxes is something ARC traces
   can show.
8. **Drift** (rules that change with no visible cue): deliberately not built. Trials catch it in principle. Build
   only if a box shows it.

## Known risks

- **ARC stayed at zero** in the pilot. A flash model with thinking off may simply be too weak to discover goals
  there. If the goal-discovery idea doesn't move it, ARC becomes a source of findings rather than a score target,
  and AutumnBench (goals stated) is the closer fit.
- **FIND alone won't carry a paper** if the budget-matched control erases the gap. In that case the behavioural
  finding and a second benchmark carry it.
- **Complexity creep in the job scripts** (`run_v3.sh` is about 300 lines). The core is still about 1,200 lines,
  and each addition maps to a requirement; keep it that way.
