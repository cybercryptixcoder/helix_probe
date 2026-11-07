# How we work: from a goal to results without drifting

*Written Nov 7, 2026, at Shreyas's request, from how the capability-removal work was set up. Any session should follow
it. It exists because Helix Evolve drifted: experiments were added one at a time until nobody could say what they
were for.*

## 1. Crystallise the goal

- **Write it in plain words, short enough to read in a minute,** in `docs/NORTH_STAR.md`: what we want to show, why
  it matters, what counts as done, what would count as a breakthrough, and what is deliberately not the goal.
- **Fix the destination, not the route.** Models, code and settings stay open; the goal doesn't.
- **Only Shreyas changes or adds a goal.** Each change is a dated entry in `docs/JOURNAL.md`.

## 2. Plan a finite set of steps

- **Each step in `docs/PLAN.md` has:** the question it answers, how it answers it, the prediction written before it
  runs, and what we'll do with each outcome.
- **Measures and thresholds are fixed before the runs** that they judge.
- **Every arm has a stated question.** No settings sweeps; no arm that only varies one small knob.
- **Shreyas reviews the plan before anything runs.**

## 3. Execute and record

- **Keep a status line** at the top of `PLAN.md`, so anyone can see where we are.
- **Log every result, decision and fix in `JOURNAL.md`,** newest first, with what it means.
- **Push results to `results/`** with full traces, so any number can be checked or re-run.
- **Keep the docs current after every working session.** The repo is the handoff: someone given it after any message
  must be able to continue without asking.

### Hard rules (added Nov 7, 12:30 ET, after two failures; Shreyas: strict, not to be broken)

1. **GitHub holds everything, the moment it exists.** When a run finishes, its full results folder (transcripts,
   edits, grades; large weight files excepted) is downloaded and pushed before anything else happens, not at the
   end of a queue. No result may live only on a Colab runtime, the VM or this workspace. Scripts used to drive
   runs live in `scripts/`. *Failure that caused this:* six r0 runs existed only on runtime `wsp2`, which Colab
   reclaimed while idle; their raw files are lost.
2. **Docs are updated in the same turn as the event, never later.** Every result, decision or change of state
   updates `JOURNAL.md`, the status line in `PLAN.md`, `PROGRESS.md` and, when the overall picture changes,
   `handoff/00_START_HERE.md`. Writing docs later from memory is not allowed: after a context compaction, memory is
   a lossy summary, and docs written from it would be lossy too. *Failure that caused this:* `00_START_HERE.md`
   went a day stale.
3. **"Saved" means checked.** A run is recorded as saved only after its folder is seen in the downloaded copy
   and in the commit. A step that times out is retried, never assumed to have worked. *Failure that caused this:*
   on Nov 7 at 18:55 a tar timed out, the old archive was downloaded, and the journal briefly called a run saved
   before it was.
4. **Every check-in verifies all three rules:** nothing finished that isn't on GitHub, and no doc behind the events.

## 4. When something unexpected happens

- **A harness bug:** fix it, log it, set aside (never delete) the runs it affected, and re-run them so every compared
  run uses the same setup.
- **A measure turns out to be gameable:** add a better measure next to it, labelled as added after the fact. Never
  change the original verdict or remove a result.
- **A method turns out to be flawed:** build the fix as a new, named variant. The original keeps its runs, so the two
  can be compared.
- **Every change has to pass one test:** is it lean, justified by evidence, and a strict improvement? If a fix needs a
  patch on a patch, rethink the design instead.

## 5. When a new direction comes up

- **Write it as its own crystal goal** in `NORTH_STAR.md`, next to the existing ones. The existing goals stay, so
  adding is not drifting.
- **Say how it overlaps the current work,** so shared experiments serve both goals.
- **Plan its finite steps** the same way, and get Shreyas's approval before running them.

## 6. Talking to Shreyas

- **Short updates while things run.** On request, give the big picture: where we are, what we know, whether it's
  working.
- **Say plainly when something fails or when a result isn't real.** Never present a gamed or broken result as a
  success.
- **Ask before adding experiments.** Make small engineering fixes, log them, and say so.
