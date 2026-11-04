# Analysis: what the runs showed (final for the v3 job, Nov 4, 2026, 14:45 ET)

Every run of the v3 job is finished, and so is find-v2. All numbers come from `results/` in
`cybercryptixcoder/helix_probe`, recomputed for this document. FIND scores use FIND's official scorers; ARC scores
use the toolkit's official calculator. Section 9 lists where everything is and how to recompute it.

This version replaces the morning analysis (09:30). Two of its conclusions changed once the repeat runs came in;
they are marked **(revised)**.

---

## 0. The short version

1. **FIND, at Helix Probe's own budget:** 0.82–0.90 numeric and 0.85–0.97 strings, for every iterative version.
   - The same model in FIND's own protocol scores 0.38 numeric and 0.40–0.46 strings.
   - FIND's published GPT-4 agent scores 0.20 and 0.01.
2. **The gap over the same model is mostly behavioural.** In FIND's protocol the model answers without running a
   single experiment on 13–19 of 40 functions, and those answers score 0. The loop never does that.
3. **(revised) At equal budget, the loop still helps, but modestly.** Pooled over both control runs and both v3
   seeds:
   - at the same number of experiments, Helix Probe leads by +0.04 to +0.19;
   - at the same number of inputs, v3 leads on numeric (+0.10, 95% CI +0.01 to +0.20, 10 wins to 3) and ties on
     strings (+0.03, not significant);
   - arms that use the sealed exam lose at equal inputs, because the exam spends 40 inputs before learning starts.
4. **(revised) The sealed exam isn't worth keeping.**
   - Final score: v3's second seed scored 0.88 numeric, equal to v3-exam. The morning's "exam is better" was within
     seed variance.
   - Efficiency: the exam is what loses at equal inputs.
5. **The arms barely differ on FIND.**
   - Numeric's ceiling is 0.90: 4 of the 40 functions are unsolvable even for FIND's own ground-truth code.
   - Seed-to-seed variance (2–3 functions) is as large as most arm differences.
   - Only "chosen + random experiments" vs "random only" stands out on numeric (+0.125, 5 wins to 0).
6. **The control is unstable.** Its two runs gave the same score on only 28 of 40 numeric and 17 of 40 string
   functions. A single run of it can't be trusted, so the comparison is reported over both.
7. **ARC-AGI-3 pilot: 0 of 35 levels on 5 games** (100 experiments each, about 280 actions per game). The models
   learned parts of each game's mechanics, but none learned what completes a level. With no goal hypothesis there
   was nothing to plan toward, so the planner contributed nothing.

---

## 1. find-v2: v2, its ablations, and v1 (80 functions, up to 25 experiments, exam of 4 for v2 arms)

| Arm | Numeric final | at 3 | Strings final | at 3 | Experiments (num/str) | Calls (num/str) |
|---|---|---|---|---|---|---|
| v2-no-theorist | **0.90** | 0.75 | 0.91 | 0.82 | 17.6 / 12.8 | 22 / 12 |
| v2 (mixed experiments, theorist, exam) | 0.88 | 0.72 | 0.92 | 0.84 | 18.0 / 12.0 | 26 / 13 |
| v1 | 0.88 | 0.62 | 0.85 | 0.66 | 25.0 / 24.7 | 42 / 37 |
| v2-directed (every experiment chosen) | 0.80 | 0.72 | **0.95** | 0.80 | 16.9 / 13.0 | 38 / 20 |
| v2-random (every experiment random) | 0.75 | 0.55 | 0.90 | 0.85 | 16.7 / 12.1 | 21 / 5 |
| published GPT-4 | 0.20 | | 0.01 | | about 3 | |

Paired over the same functions ("wins/losses" counts functions where the first arm did better or worse):

| Comparison | Numeric | Strings |
|---|---|---|
| v2 vs v2-random | +0.125, 5/0, p=0.06 | +0.03, 5/2 |
| v2 vs v2-directed | +0.075, 3/0 | −0.03, 2/2 |
| v2 vs v2-no-theorist | −0.025, 0/1 | +0.01, 3/2 |
| v2 vs v1 | 0.00, 1/1 | +0.07, 4/2 |

What each comparison says:
- **Choosing experiments vs random.** Choosing beats random on numeric: every disagreement went to choosing. On
  strings it hardly matters, because ordinary words already expose most string functions.
- **Choosing only vs mixing.** Choosing every experiment is worse than mixing on numeric and the most expensive arm
  (38 calls). On the knob toy it failed outright (51% and 45% held-out, against 100% for mixed). **Mixing stays the
  default.**
- **The theorist.** No measurable benefit on FIND: the no-theorist arm ties v2 and uses fewer calls. It is used,
  though. Its model ended up as the final model in 8 of 80 v2 runs and in 14 of 80 v3 runs, and theories won 23 of
  96 trials in v3. On the hidden-lock toy it was decisive (1.00 against 0.83). FIND functions are mostly one rule
  plus a local region, and the updater gets there alone. **Verdict: unproven on FIND, not tested where it should
  matter.**
- **v1 vs v2.** Same final numeric score. But v2 is far ahead after 3 experiments (0.72 vs 0.62 numeric, 0.84 vs
  0.66 strings), better on strings, and uses 25–40% fewer experiments and calls. v1 always used all 25.

## 2. find-v3: v3 with and without the exam, and v3 repeated with another seed

| Arm | Numeric final | at 3 | Strings final | at 3 | Inputs (num/str) | Calls (num/str) |
|---|---|---|---|---|---|---|
| v3-exam | 0.88 | 0.70 | **0.97** | 0.86 | 305 / 119 | 29 / 12 |
| v3 (seed 0) | 0.82 | 0.70 | 0.91 | 0.83 | 253 / 101 | 29 / 15 |
| v3 (seed 1) | 0.88 | 0.68 | 0.93 | 0.80 | 268 / 95 | 30 / 13 |

Paired comparisons:

| Comparison | Numeric | Strings |
|---|---|---|
| v3 seed 0 vs seed 1 (same arm, different seed) | −0.05, 0/2 | −0.02, 1/2 |
| v3 seed 1 vs v3-exam | 0.00, 1/1 | −0.04, 1/3 |
| v3 seed 1 vs v2 | 0.00, 1/1 | +0.01, 2/2 |

- **Seed variance is as large as the arm differences.** Two to three functions per category move between seeds.
- **(revised) The exam.** v3 without it equals v3-exam on numeric (seed 1), and trails by one function on strings
  (not significant). It is more efficient per input (section 3). By the lean principle, **the evidence supports
  removing the exam.**
- **v3 vs v2.** Equal. The v3 additions (trials, cost in inputs, the goal plumbing) didn't cost anything on FIND.

**Score against experiments run** (mean official score of each run's model after k experiments):

| k | 1 | 2 | 3 | 5 | 7 | 10 | 15 | 25 |
|---|---|---|---|---|---|---|---|---|
| v2, numeric | 0.47 | 0.65 | 0.72 | 0.80 | 0.85 | 0.88 | 0.88 | 0.88 |
| v3-exam, numeric | 0.55 | 0.68 | 0.70 | 0.80 | 0.78 | 0.80 | 0.82 | 0.88 |
| v2, strings | 0.68 | 0.80 | 0.84 | 0.89 | 0.91 | 0.92 | 0.92 | 0.92 |
| v3-exam, strings | 0.68 | 0.81 | 0.86 | 0.94 | 0.94 | 0.95 | 0.95 | 0.97 |

Most of the score arrives in the first 5–10 experiments.

## 3. The same-model control: our model in FIND's own protocol (run twice)

| | Run 1 numeric | Run 2 numeric | Run 1 strings | Run 2 strings |
|---|---|---|---|---|
| Score | 0.375 | 0.375 | 0.46 | 0.40 |
| Mean experiments / inputs | 7.2 / 94 | 8.4 / 90 | 2.8 / 29 | 3.9 / 38 |
| Answered with zero experiments | 16 | 13 | 14 | 19 |
| Never answered (20 rounds) | 6 | 7 | 0 | 0 |
| Functions with the same score in both runs | 28 of 40 | | 17 of 40 | |

**Pooled, budget-matched comparison** (each Helix Probe run cut to the control's budget on each function, averaged
over both control runs and, for v3, both seeds):

| Arm | Category | Control | Helix at control's inputs | Diff (95% CI), wins/losses | Helix at control's experiments | Helix final |
|---|---|---|---|---|---|---|
| v3 | numeric | 0.38 | 0.47 | **+0.10 (+0.01, +0.20)**, 10/3, p=0.09 | 0.50 | 0.85 |
| v3 | strings | 0.43 | 0.46 | +0.03 (−0.03, +0.09), 10/6 | 0.47 | 0.92 |
| v3-exam | numeric | 0.38 | 0.39 | +0.01, 7/6 | 0.55 | 0.88 |
| v3-exam | strings | 0.43 | 0.38 | −0.05, 6/13 | 0.52 | 0.97 |
| v2 | numeric | 0.38 | 0.40 | +0.03, 9/8 | 0.57 | 0.88 |
| v2 | strings | 0.43 | 0.36 | −0.07, 6/14 | 0.51 | 0.92 |

The job's own per-run comparisons are in `results/find/compare-v3-aia.md` and `-aia2.md`.

**What this means, honestly:**
- **"Beats GPT-4" isn't the claim.** It mostly measures a newer model.
- **At its own budget, Helix Probe more than doubles the same model's score** (0.85–0.97 against 0.38–0.43). It
  uses 2.5–4× the inputs to do it.
- **At the same number of experiments it is ahead in every arm and category** (+0.04 to +0.19).
- **At the same number of inputs,** v3 without the exam is modestly ahead on numeric and level on strings. Arms with
  the exam pay for it up front.
- **The control's two failure modes:** answering from the prompt alone, and never committing. The loop removes both.
  That is Shreyas's original thesis seen in data: direct the reasoning so the result doesn't depend on the model's
  judgement of when it knows enough.
- **Still untested:** the control *forced* to experiment to the same budget. That would separate "the loop's
  structure" from "just being made to keep going".

## 4. Toys and FIND dev (development evidence)

| Box | v1 | v2 directed | v2 mixed | v3 |
|---|---|---|---|---|
| Scrambled grid (held-out) | 15% | 96% (44 experiments) | 87% (40) | 88% (37) |
| Knob box (held-out) | 69% | 51% / 45% (two seeds) | 100% (32) | 100% (24) |
| Hidden lock (hidden counter) | | | | fit 1.00; settled at 16 experiments; the theorist's counting model won its trial 1.00 vs 0.83 |

On FIND dev (16 functions), every v2 and v3 arm scored 1.00.

## 5. ARC-AGI-3 pilot (stage `arc`: 5 games never used in development; 11:23–13:10 ET)

**Setup:**
- v3, stateful mode, one playthrough per game;
- up to 100 experiments of at most 8 actions each;
- a budget of 3× the human action count (it never bound);
- DeepSeek V4.1 Flash with thinking off.

| Game | Levels | Actions (human, all levels) | Fit: start → end | On arrival, last 10 | Plans (mean match) | Game overs | Final model's goal hypothesis |
|---|---|---|---|---|---|---|---|
| cd82 (hidden state) | 0 of 6 | 297 (171) | 0.80 → 0.68 | 0.10 | 5 (0.22) | 2 | "completing level 1 is NOT filling the bar (that gives GAME_OVER)"; otherwise unknown |
| sb26 | 0 of 8 | 290 (213) | 1.00 → 0.96 | 0.50 | 0 | 1 | "unknown; not yet observed completing a level" |
| sc25 | 0 of 6 | 261 (350) | 0.74 → 0.73 | 0.10 | 4 (0.31) | 3 | "set all switch clusters to a target" (?) |
| tr87 | 0 of 6 | 283 (414) | 0.55 → 0.78 | 0.00 | 5 (0.54) | 1 | "matching interiors to a target" (?) |
| wa30 (hidden state) | 0 of 9 | 248 (1,843) | 0.59 → 0.89 | 0.00 | 0 | 1 | "shift boundary all the way left" (?) |

The pilot used 1,067 model calls and 1,379 actions, in about 1 hour 47 minutes. Official mean score: 0.

**How to read the fit column:** the ARC match is two parts changed cells, one part "levels correct" and one part
"state correct", averaged. Levels and state are almost always right by default (no level completes; the state is
"playing"), so **0.5 is free**. A fit of 0.73 means only about half the changed cells were predicted. Only sb26's
model (0.96) really predicted its game's mechanics; on-arrival accuracy was low everywhere except sb26.

**What failed, and why:**
1. **Goal discovery.** No model formed a concrete, testable rule for completing a level. Since the goal-guess rule,
   models do write a guess, but a vague one ("match a target"). It can't be planned toward, so the planner fired on
   only 3 games, and its 14 plans predicted poorly.
2. **Mechanics only partly learned.** Fits after 100 experiments are mostly 0.68–0.89 (with the 0.5 free). The
   hidden-state game cd82 got *worse* over time (0.80 → 0.68).
3. **Exploration spent on the wrong thing.** Half the experiments are random ordinary probes (the rule that helped
   FIND), and the chosen ones averaged under 3 actions. About 280 actions per game is enough for humans to finish a
   level or two of most of these games, so the budget wasn't what limited us. How the actions were spent was.
4. **One real lesson learned:** on cd82 the model discovered that filling the bar ends the game rather than
   completing the level. That is a correct negative goal hypothesis learned from a failed plan, which is the
   mechanism working, just not far enough.

**The comparison, honestly:** frontier models in ARC's generic harness score about 13% on the public games;
coding-agent world-model systems score 41–58%, with far bigger models, reasoning, and 1,500 actions per level. A
flash model with thinking off, in this loop, scores 0 on 5 unseen games. In development it scored 4.76 on ft09
(one level), but we had developed on that game. **The full 25-game run is not worth doing with this design.**

## 6. What worked, what didn't, what we think would work

**Worked:**
- An executable model, checked by code, as the memory of what is known.
- Prediction before observation as the honest progress signal (the "is an evaluator needed?" question, resolved:
  the box is the evaluator).
- Narrow roles in series; mixed random and chosen experiments; the stopping rule.
- History-based models for hidden state (the lock).
- One adapter file per box: FIND, the toys and ARC all ran with no box code in the core.
- The fair-comparison discipline: the same-model control, the budget matching and the repeats changed two
  conclusions in one day.
- Robustness: a container restart, a game-over crash and a queued job restarted twice were all survived. The VM ran
  six stages unattended, and resume from GitHub was tested.

**Didn't work, or not yet:**
- ARC-AGI-3: no levels on unseen games.
- The theorist: no measurable value on FIND, and untested where it should matter.
- The sealed exam: no better than trials, and it costs inputs.
- Telling arms apart on FIND: the benchmark saturates, numeric's ceiling is 0.90, and seed variance is 2–3
  functions.
- The reports' cost column: it looks inflated and is unverified. Don't quote dollar figures from it.

**What we think would work (hypotheses, not claims):**
1. **Goals on ARC need their own evidence.** A level completion has never been seen on most games, so a model can't
   be fitted to it. What works for a weak model may be making goal hypotheses explicit and cheap to test. The model
   lists concrete candidate goal rules, and the planner tests the cheapest one. Each failure (like cd82's bar)
   rules one out. That is the current mechanism made sharper, not a new one.
2. **On boxes where actions are scarce, random probes should be fewer or smarter.** Half random was right for FIND
   (cheap probes, a narrow region to find) and is likely wrong for a game.
3. **The budget-matched control** on FIND: force the protocol to keep experimenting. It decides whether the FIND
   claim is about the loop's structure or about persistence.
4. **Efficiency on FIND:** most of the score arrives by 5–10 experiments. A cheaper stopping rule could close the
   per-input gap without the exam.
5. **A benchmark that discriminates:** BoxingGym (noisy boxes) or AutumnBench (grid worlds with tasks, closer to
   ARC but with goals stated), since FIND saturates and ARC is out of reach.

## 7. Decisions the evidence now supports (for Shreyas to confirm)

| Decision | Evidence |
|---|---|
| **Remove the sealed exam** from the core (keep trials) | same final score within seed variance; costs inputs; lean principle |
| **Keep mixed experiments as the default,** but let a box set the random share | +0.125 over random on FIND numeric; likely wasteful on ARC |
| **Keep the theorist, pending one test where structure is rich** (the lock toy shows it matters; FIND can't) | FIND tie; won 24% of trials; final model in 8–14 of 80 runs |
| **Don't run the full 25-game ARC** with this design | 0 of 35 levels in the pilot |
| **Report FIND as "same model, with and without the loop, at matched experiments and inputs, over repeated runs"** | section 3 |

## 8. Total runs

| Run | Functions or games | Runs |
|---|---|---|
| find-v2 | 400 runs | 5 arms × 80 |
| find-v3 | 160 | 2 arms × 80 |
| find-v3-s1 | 80 | |
| aia | 80 | |
| aia2 | 80 | |
| ARC pilot | 5 games | |

The VM job ran from 00:40 to 13:10 ET on Nov 4.

## 9. Where the data is, and how to recompute

| Data | Where |
|---|---|
| find-v2 | `results/find/find-v2/` |
| find-v3 | `results/find/find-v3/` |
| find-v3 seed 1 | `results/find/find-v3-s1/` |
| control runs | `results/find/aia-none/`, `results/find/aia-none-r2/` (`history.json` per function = the whole conversation) |
| comparisons | `results/find/compare-v3-aia.md` / `-aia2.md` (+ `.json`) |
| ARC pilot | `results/arc/arc-v3/` (`report.md`; per game: `notebook.jsonl`, `calls.jsonl.gz`, `model/`, `trials.jsonl`, `curve.csv`) |

Recompute:
- The per-run comparison: `python bench/find/compare.py --helix <job dirs> --aia <control dir>`.
- These were computed ad hoc for this document from `official_curve.json` and `result.json`, by the methods
  described in their sections:
  - the pooled comparison;
  - the paired arm tests and the seed comparison;
  - the ground-truth ceiling check;
  - the score-against-experiments table;
  - the zero-experiment split.
- The ARC table comes from each game's `notebook.jsonl`, `curve.csv`, `trials.jsonl` and final model.
