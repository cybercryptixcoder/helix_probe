# Results ledger

Every result that might be publishable, with the exact configuration behind it and how it stands against the
published reference. Newest first. A result is entered as **interim** until its job has finished. Nothing here
counts unless its data are in `results/` and its configuration is recorded.

Standing configuration, unless a row says otherwise:
- **Model:** DeepSeek V4.1 Flash through Luminal, with thinking off for every role.
- **Calls:** one call at a time per run.
- **Scorers:** FIND's official scorers, and the official ARC-AGI-3 score calculator.

---

## R5. FIND, final (Nov 4): Helix Probe vs the same model in FIND's protocol, budget-matched, repeated

**Data:**
- `results/find/find-v2/`, `find-v3/`, `find-v3-s1/` (Helix Probe);
- `aia-none/`, `aia-none-r2/` (the control);
- `compare-v3-aia*.md` (the comparisons).

**Setup:**
- 80 functions (40 numeric, 40 strings);
- up to 25 experiments;
- FIND's input limits;
- the control is FIND's agent protocol verbatim, with our model, 20 rounds.

**Own budget:**

| | Numeric | Strings |
|---|---|---|
| Helix Probe | 0.85–0.88 (ceiling 0.90: 4 functions are unsolvable even for FIND's ground truth) | 0.92–0.97 |
| Control | 0.38 (both runs) | 0.46 / 0.40 |
| Published GPT-4 | 0.20 | 0.01 |

**Matched budget, pooled over 2 control runs × 2 v3 seeds:**

| | Numeric | Strings |
|---|---|---|
| At the control's experiments | Helix ahead in every arm (+0.12 to +0.19) | Helix ahead (+0.04 to +0.09) |
| At the control's inputs, v3 | **+0.10** (95% CI +0.01 to +0.20; 10 wins / 3 losses; p=0.09) | +0.03 (not significant) |
| At the control's inputs, exam arms | level | level or behind (the exam spends 40 inputs up front) |

**Why the control is low:**
- it answers with zero experiments on 13–19 of 40 functions (all scoring 0);
- it sometimes never answers;
- it is unstable: same score on only 28/40 numeric and 17/40 string functions across its two runs.

**Still needed:**
- the control forced to the same budget;
- more seeds.

## R4. ARC-AGI-3, 5-game pilot (Nov 4): 0 of 35 levels

**Data:** `results/arc/arc-v3/`.

**Setup:**
- v3, one playthrough per game;
- tr87, wa30, sb26, cd82, sc25, none used in development;
- 100 experiments of at most 8 actions, a 3× human budget (never binding);
- about 280 actions per game; 1,067 calls.

**Result:**
- no level on any game;
- the models learned parts of the mechanics, but no concrete level-completion rule, so the planner had nothing to
  aim at (14 plans on 3 games, poor predictions);
- one correct negative goal hypothesis was learned from a failed plan (cd82: filling the bar ends the game).

**Fit caveat:** ARC fit includes 0.5 that comes for free (levels and state are right by default); only about half
the changed cells were predicted.

**References:** frontier models in ARC's generic harness score about 13%; coding-agent world models 41–58%, with
bigger models and looser limits.

**Not publishable as is.** The full 25-game run is deferred until goal discovery works.

## R3. Hidden state is common in ARC-AGI-3 games (measured Nov 3)

- **Method:** random play; a game has hidden state if the same screen and action ever led to different next
  screens.
- **Result:** 3 of 8 games: g50t (287 of 1,200 transitions), cd82 (67), wa30 (69).
- **To do:** run on all 25 games before stating it.

## R2. FIND ablations (find-v2, find-v3, find-v3-s1)

- **Choosing experiments beats random on numeric:** +0.125, 5 wins to 0, p=0.06. On strings it's even.
- **Choosing only is worse than mixing on numeric** (0.80 vs 0.88) and the most expensive arm. On the knob toy it
  failed outright (51% and 45% held-out against 100%).
- **The theorist adds nothing measurable on FIND** (no-theorist 0.90/0.91 vs v2 0.88/0.92). Its model was final in
  8–14 of 80 runs.
- **The sealed exam:** v3 without it equals v3-exam once a second seed is counted (0.88 numeric), and it is more
  efficient per input.
- **Seed variance** is 2–3 functions of 40, as large as most arm differences.
- **v2 vs v1:** the same final numeric score, with v2 far ahead after 3 experiments (0.72 vs 0.62, strings 0.84 vs
  0.66) and using 25–40% fewer calls.

## R1. FIND vs FIND's published agents

Superseded by R5. The gap to published GPT-4 (0.20 / 0.01) mostly reflects the newer model: the same model in the
same protocol already scores 0.38 / 0.40–0.46.

## R0. Toys (development evidence, not for publishing)

| Box | v1 | v2 directed | v2 mixed | v3 |
|---|---|---|---|---|
| Scrambled grid, held-out | 15% | 96% (44 experiments) | 87% (40) | 88% (37) |
| Knob box, held-out | 69% | 51% / 45% (two seeds) | 100% (32) | 100% (24) |
| Hidden lock | | | | fit 1.00 at 16 experiments; the theorist's model won its trial 1.00 vs 0.83 |
