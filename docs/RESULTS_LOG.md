# Results ledger

Every result that might be publishable, with the exact configuration behind it and how it stands against the
published reference. Newest first. A result is entered as **interim** until its job has finished. Nothing here
counts unless its data are in `results/` and its configuration is recorded.

Standing configuration, unless a row says otherwise:
- **Model:** DeepSeek V4.1 Flash through Luminal, with thinking off for every role.
- **Calls:** one call at a time per run.
- **Scorers:** FIND's official scorers, and the official ARC-AGI-3 score calculator.

---

## R4. ARC-AGI-3, Helix Probe v3: a 5-game pilot queued (`scripts/run_v3.sh`, stage `arc`); the 25-game run only after it

- **Claim to test:** a flash model with thinking off, in a learn-a-model-then-plan loop with one adapter file and
  no game-specific code, scores on ARC-AGI-3. How it compares:
  - frontier models in ARC's generic harness: 13.3% public (GPT-5.6 Sol, OpenAI's run of the official harness);
  - the coding-agent world-model systems: 41.3% with GPT-5.4 high and 58.1% with GPT-5.5 high (Executable World
    Models, arXiv 2605.05138);
  - all of these under looser limits than ours.
- **Setup:**
  - one playthrough per game, toolkit local mode, every action counted;
  - a budget of 3× the human action count per game (vs 1,500 actions per level in 2605.05138);
  - up to 100 experiments (pilot; 400 in the full run) of at most 8 actions each.
- **Fair-comparison caveats to report:**
  - the models differ (flash with thinking off vs GPT-5.x high);
  - our budget is tighter;
  - ARC's official leaderboard is for the semi-private set and verified submissions, so a public-set number is
    comparable to the papers' public-set numbers, not to the leaderboard.
- **Dev (3 games, `runs/arc-dev`, not reported):** models predict 0.5–0.95 of each experiment's changes within
  15 experiments (ft09 0.94, g50t 0.82–0.92, ls20 0.52).

## R3. Hidden state is common in ARC-AGI-3 games (finding; measured 2026-11-03)

- **Method:** random play, recording every (screen, action) → next screen. A game has hidden state if the same
  screen and action ever led to different next screens.
- **Result:** 3 of 8 games tested have hidden state: g50t (287 of 1,200 transitions), cd82 (67), wa30 (69).
- **Consequence:** a model that sees only the current screen cannot be right in these games. v3 gives the model
  the action history since the last reset so it can keep that memory (the general rule for any stateful box).
- **To do before publishing:** run on all 25 games, with the counts per game.

## R2. FIND, same-model control (FIND's own protocol, our model): queued (stages `aia`, `aia2`; `bench/find/compare.py`)

- **Why:** the find-v2 comparison (R1) puts a 2026 flash model against 2023 GPT-4. This control runs FIND's own
  agent protocol (FIND's prompts verbatim, 20 rounds, the same scorer) with our model. It separates "the loop"
  from "a newer model".
- **What gets reported:** per function and paired, Helix Probe vs the control at Helix's own budget, at the
  control's inputs, and at its experiments. Each with a 95% bootstrap interval of the difference and an exact sign
  test, run twice on each side (aia/aia2, find/find2) for run-to-run variance.
- **Early sign (6 functions: 3 numeric, 3 strings):**
  - our model in FIND's protocol scored 0.33 numeric and 0.50 strings, where published GPT-4 scored 0.00 on the
    same functions. So most of the gap to GPT-4 is the newer model, and "beats GPT-4" is not the claim;
  - the control used 12 experiments and 130 inputs per numeric function;
  - on those 3 numeric functions Helix Probe v2 reached 1.00 with its own budget (25 experiments, about 490
    inputs including its exam), and 0.67 when cut to the control's inputs.
  
  The budget-matched number is the one to lead with.

## R1. FIND, 80 functions, Helix Probe v2 vs FIND's published agents: **interim** (`results/find/find-v2`)

- **Setup:**
  - FIND's 80-function sample (40 numeric, 40 strings), each function a fresh run;
  - up to 25 experiments;
  - FIND's input limits;
  - v2 arms use a sealed exam of 4 random probes, counted in the inputs.
- **Strings (interim, 08:20 UTC, about 30 of 40 per arm):** v2-no-theorist 0.97, v1 0.97, v2 0.94,
  v2-directed 0.87, v2-random 0.86; published GPT-4 0.01. Strings is nearly saturated too, so on FIND the
  arms separate by at most about 0.1, and the same-model control (R2) carries the publishable comparison.
- **Numeric (interim, 07:40 UTC, about 24 of 40 per arm):**

  | | final | after 3 experiments |
  |---|---|---|
  | v2 | 0.96 | 0.79 |
  | v2-no-theorist | 1.00 | |
  | v1 | 0.96 | |
  | v2-random | 0.88 | |
  | v2-directed | 0.87 | |
  | published GPT-4 | 0.20 | |
  | published GPT-3.5 | 0.12 | |

  Strings (published): GPT-4 0.01, GPT-3.5 0.05.
- **Reading:** numeric is saturated for every iterative arm, so the margin over the published agents is large and
  the ablations barely separate. Strings will be the discriminating category.
- **Caveat for publishing:** the published agents used about 3 experiments. Our arms use about 15–25. The table
  reports the score after 3 experiments to make that comparison fair, and R2 is the same-model control.

## R0. Toys: v1 → v2 → v3 (development evidence, not for publishing)

| Box | v1 | v2 directed | v2 mixed | v3 |
|---|---|---|---|---|
| scrambled grid, held-out | 15% | 96% (44 experiments) | 87% (40) | 88% (37) |
| knob box, held-out | 69% | 51% (seed 0), 45% (seed 1) | 100% (32) | 100% (24) |

- v3 matches v2-mixed with fewer experiments and calls, without a sealed exam: theories are judged by trials.
- FIND dev (16 functions never used in the report): v3 and v3-exam scored 1.00 on every finished function, with
  9–16 experiments each.
