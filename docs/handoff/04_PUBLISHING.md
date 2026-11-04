# Publishing: what we are trying to publish, what we have, what it still needs

The standing rule (Shreyas, Nov 4): every run must be an attempt at a publishable result. That means finding the
published result and its configuration, replicating the setup as closely as possible, and beating it "fair and
square... with a worse model and more constraints". Ablation findings count too. The live ledger is
`docs/RESULTS_LOG.md` in the repo; this file is the summary and the plan.

References were researched on Nov 3–4, 2026; re-check any number before quoting it.

## Candidate results

### P1. FIND: a structured probing loop vs the same model in the benchmark's own protocol

**The claim we can make today, honestly worded (final numbers, Nov 4):**
- **Our own budget.** On FIND's 80-function sample, a flash model with thinking off reaches 0.85–0.88 numeric (of a
  0.90 ceiling) and 0.92–0.97 strings inside Helix Probe.
- **The same model in FIND's own protocol** reaches 0.38 and 0.40–0.46 (two runs). It answers without experimenting
  on 13–19 of 40 functions, which all score 0, and sometimes never answers.
- **Matched experiments:** Helix Probe is ahead in every arm and category (+0.04 to +0.19).
- **Matched inputs,** pooled over two control runs and two seeds:
  - v3 without the sealed exam is ahead on numeric (+0.10, 95% CI +0.01 to +0.20, 10 wins to 3, p=0.09);
  - it ties on strings.

**What it still needs to be publishable:**
1. **The budget-matched control:** FIND's protocol forced to keep experimenting to the same budget (reject
   `[DESCRIPTION]` until N experiments or inputs). This is the single most important missing piece: it says whether
   the loop beats "just more data".
2. **More repeats.** Done once: the control is unstable (same score on only 28/40 numeric and 17/40 string
   functions across two runs), and v3's seeds differ by 2–3 functions. Three or more runs per side would tighten
   the numeric result past p<0.05.
3. **Ceiling-aware reporting:** numeric's maximum is 0.90 (4 functions are unsolvable even for ground truth).
   Report "of solvable".
4. **Ideally a bigger sample** than 40 per category; FIND has about 1,000 of each.

**Status:** the numeric result is promising but marginal; strings is a tie. **Venue:** realistically a workshop paper (interpretability or agents workshops) on the behavioural finding and
the loop, with the ablations as supporting evidence.

**Published references:** FIND (Schwettmann, Rott Shaham et al., NeurIPS 2023), whose released AIA answers, scored
with the same official scorer on our 80 functions, give:

| Agent | Numeric | Strings |
|---|---|---|
| GPT-4 | 0.20 | 0.01 |
| GPT-3.5 | 0.12 | 0.05 |
| Llama-2-70B | 0.03 | 0.04 |
| Llama-2-13B | 0.00 | 0.00 |

They used about 3 experiments.

### P2. FIND ablations (supporting evidence for P1, or a short note)

- **Choosing experiments beats random:** on numeric, +0.125, with all 5 disagreements in favour of choosing.
- **Mixing chosen and random is the most robust.** Directed-only failed the knob toy (51% and 45% against 100%) and
  was the most expensive arm on FIND.
- **The theorist adds nothing measurable on FIND.**
- **The sealed exam doesn't beat trials** once seed variance is counted, and it costs inputs.
- **Seed-to-seed variance** (2–3 functions of 40) is as large as most arm differences. That is itself worth
  reporting.
- **v2 reaches v1's score with 25–40% fewer calls,** and is far ahead after 3 experiments.

Only "choosing beats random on numeric" is close to significant (5 wins to 0, p=0.06).

### P3. ARC-AGI-3: a learn-a-model loop with a flash model, thinking off

**Setup:**
- the official toolkit in local mode, one playthrough per game, every action counted;
- scored by the toolkit's own `EnvironmentScoreCalculator` (RHAE against human action counts);
- a budget of 3× the human action count, which is tighter than the papers below.

**References (recorded Nov 3–4, 2026):**

| System | Score on the 25 public games | Notes |
|---|---|---|
| GPT-5.6 Sol, ARC's generic harness | 13.3% | OpenAI's run, Jul 29, 2026; 7.78% on the semi-private set |
| OpenAI's own harness | 38.3% | retained reasoning and compaction |
| Executable World Models (arXiv 2605.05138), GPT-5.4 high | 41.3% | 1,500 actions per level |
| Executable World Models, GPT-5.5 high | 58.1% | 1,500 actions per level |
| Systems built for the competition (Tycho, NVIDIA AVO, Agno, Memento 3) | about 100 | Memento 3 used 7,518 actions against humans' 17,135 |

**Pilot result (Nov 4):** 0 of 35 levels on 5 unseen games (tr87, wa30, sb26, cd82, sc25), with 100
experiments and about 280 actions per game. The models learned parts of the mechanics but no level-completion
rule, so there was nothing to plan toward. **P3 is not publishable with this design.** The full 25-game run isn't
worth doing until goal discovery works (`05_NEXT_STEPS.md`).

**Smaller, real findings already in hand:**
- **Hidden state is common:** 3 of 8 games, measured by random play. Extend to all 25 before stating.
- **Executable models learn parts of the mechanics but not the goal.** Even when asked to state a goal hypothesis,
  a flash model writes a vague one ("match a target") that can't be planned toward. A correct negative hypothesis
  (cd82: filling the bar ends the game) was learned from a failed plan.

**Competitions:**
- The ARC Prize 2026 Kaggle competition closed on Nov 2.
- Its paper track was due Nov 8, which is not feasible.
- **ARC Prize 2027 is the realistic target.**

### P4. Other benchmarks worth a run (each one adapter file)

| Benchmark | What it is | Why |
|---|---|---|
| BoxingGym (Stanford) | 10 probabilistic environments, scored by prediction error after a fixed number of experiments | noisy boxes; it would discriminate where FIND saturates |
| AutumnBench (ICML 2026) | 43 grid worlds | "learn the world, then do tasks"; humans beat frontier models. Its interpreter needs building for ARM |
| Automata Wiki | state machines of real protocols | compares against classic L*/TTT/L# learners on experiments needed |

## What not to claim

- **"Beats GPT-4 on FIND"** as a headline. It mostly measures a newer model.
- **Any result without its budget,** or without the same-model control beside it.
- **Dollar costs from the reports.** The column looks inflated and is unverified.
- **ARC numbers from the dev runs.** They aren't reportable: we developed on those games.
