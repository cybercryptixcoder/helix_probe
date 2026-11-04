# Helix Probe handoff: start here

*Written Nov 4, 2026, 09:30 ET; updated 14:45 ET after every run finished, at the end of the first design-and-build conversation (Nov 3, 9:03 PM → Nov 4).
Its purpose: a new session, or a new person, can pick up the build, the runs and the conceptual discussion exactly
where they were.*

## Where the files are

- **In this repo** (`docs/handoff/`): files 00–06 and 10.
- **Private, kept out of this public repo,** in a bundle Shreyas hands to a new session (`helix_probe_private.zip`):
  - `07_PRINCIPLES_AND_RULES.md`: his standing rules and principles. He asked for these not to be in GitHub.
  - `08_shreyas_verbatim.md`: his messages, verbatim.
  - `09_full_transcript_redacted.md`: the design conversation.
  - `.env`: the API keys.
  - `runview-probe.zip`: his run-viewer code.

  If a session doesn't have the bundle, ask him for it before changing anything.

## Read in this order

| File | What it is | Who it's for |
|---|---|---|
| `01_CONCEPT.md` | **What Helix Probe is, why, and the vision.** Self-contained; hand it to anyone. | everyone |
| `07_PRINCIPLES_AND_RULES.md` | Shreyas's principles and standing rules, how he wants to work, the Aether and key rules, the decisions log | the builder: read before changing anything |
| `02_STATE_AND_RUNS.md` | What is built, what is running and queued on the VM right now, everything that has been run | picking up the work |
| `03_ANALYSIS.md` | What the runs showed: what worked, what didn't, the honest reading, hypotheses | deciding what's next |
| `04_PUBLISHING.md` | Candidate publishable results, the references with their numbers, what each still needs, what not to claim | planning runs |
| `05_NEXT_STEPS.md` | The proposed next runs, decisions waiting for Shreyas, open conceptual threads | the next conversation |
| `10_INTERPRETABILITY_TRACK.md` | **The interpretability track (opened Nov 4):** can a weak model in the loop interpret and repair real networks, as frontier models were just shown to do from weights? Problem, evidence, directions; no fixed solution | the next design discussion |
| `06_OPERATIONS.md` | How to run anything from scratch, Aether prompts and conventions, job scripts, making adapters, the model client, troubleshooting | doing the work |
| `08_shreyas_verbatim.md` | **Every message Shreyas sent, verbatim** (keys redacted). The ground truth for what was asked. | resolving any doubt |
| `09_full_transcript_redacted.md` | The whole conversation, both sides, visible text only (keys redacted) | context on what was agreed |

## The situation in ten lines (Nov 4, 14:45 ET)

1. **What it is.** A lean, box-agnostic loop. A cheap model, in small steps in series (experimenter, updater,
   theorist), builds an executable model of any black box, and the model must predict each experiment before
   seeing it.
2. **The code** is at `github.com/cybercryptixcoder/helix_probe` (v1, v2, v3). The core is about 1,200 lines, with
   no box-specific code.
3. **Every run has finished; the VM is idle.** Six stages ran unattended on Nov 4.
4. **FIND, own budget:** Helix Probe scores 0.85–0.88 numeric (ceiling 0.90) and 0.92–0.97 strings. The same model
   in FIND's own protocol scores 0.38 and 0.40–0.46, mostly because it often answers without experimenting.
   Published GPT-4 scored 0.20 and 0.01.
5. **FIND, matched budget:** Helix Probe is ahead at the same experiments in every arm. At the same inputs, v3 is
   modestly ahead on numeric (+0.10, CI +0.01 to +0.20) and ties on strings. The control is unstable across runs.
6. **The arms barely differ.** Mixed experiments beat random on numeric. The theorist is unproven. The sealed exam is
   no better once seeds are counted, and it costs inputs: **remove it** (pending Shreyas).
7. **The ARC-AGI-3 pilot scored 0 of 35 levels** on 5 unseen games. The models learn parts of the mechanics but no
   goal, so the planner had nothing to aim at. Don't run the full 25 with this design.
8. **Next:** the forced-budget FIND control (decides the FIND claim), more v3 seeds, then goal discovery on ARC as a
   design discussion first. See `05_NEXT_STEPS.md`.
9. **Decisions waiting for Shreyas:** the exam, the theorist, merging the goal mechanisms, run-size policy, the
   viewer install, the publication targets, the full ARC run.
10. **The standing rules:** lean but uncompromising; whiteboard-explainable; traceable; general; evidence over
    exceptions; every run informs the next change **and** attempts a publishable result, fairly; trace everything;
    resume from GitHub alone; stop gracefully; updates every 10–15 minutes.

## How to resume in a new session

- **Clone and read.** Clone the repo and read these files. The repo's `docs/RESULTS_LOG.md` holds the same final
  results in short form; `03_ANALYSIS.md` here has the full analysis.
- **Check the VM.** Nothing is running. Before starting anything, check with Shreyas whether anything new was
  queued since.
- **Keys** are in the VM's `.env`. Shreyas gave them in the conversation (redacted here); ask him for them if a new
  workspace needs them.
- **Don't rely on memory or other conversations** for this project. These files and the verbatim messages are the
  context.
