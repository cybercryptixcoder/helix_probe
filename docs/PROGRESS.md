# Progress

*Every step of both goals, its status, and where it ends. Updated in the same turn as every change (see
`WORKING_METHOD.md`, hard rules). Last updated Nov 7, 2026, 12:35 ET.*

## Goal 1: switch off one ability by editing weights, and show the loop is why

Ends when: Step 4's write-up is delivered.

| Step | What it is | Status | Done when |
|---|---|---|---|
| 0 | Plumbing: harness, grader, guard, Colab | ✅ Done | – |
| 1 | Baselines on the 9B: unedited, random edit, scripted recipe | ✅ Done | – |
| 2 | Main comparison on the 9B: MIT one-conversation vs Helix vs helix2, 3 runs × 2 abilities | ✅ Done (raw files of the six r0 runs lost; results kept in JOURNAL) | – |
| 3 | Removed or only suppressed? (comeback test with worked examples) | ✅ Done, measured inside every grade | – |
| 4 | Write-up: results table, how each edit works, honest negatives, how to re-run | ⏸ Waiting for Shreyas on scope (decisions 3–5 below) | the write-up is in the repo |
| – | Scale axis: the same on the 0.8B (VM) | ❌ Not run | decision 4 |

## Goal 2: a verified map of what parts of the model do, using the same loop

Ends when: D4's demo is delivered, or earlier if D2 fails (then the negative result is written up and we decide
together).

| Step | What it is | Status | Done when |
|---|---|---|---|
| D0 | Build: 26-behaviour panel, profile tool, entry format, held-out checking, noise floor | ✅ Done | – |
| D1 | Calibration run: 40 experiments on the 9B, judged by 5 pre-set criteria | ✅ Done, **failed** 3 of 5 | – |
| D2 | Second calibration run with the three fixes, same 5 criteria | ⏸ Waiting for Shreyas (decision 1) | about 1.5 h on a fresh runtime |
| D3 | The long run: same loop, uncapped, for many hours; discovery curve tracked | Not started; only if D2 passes | the curve flattens or the time budget ends |
| D4 | Demo: a page built from verified entries; live sliders if time allows | Not started; after D3 | the page is in the repo |

## Infrastructure

| Item | Status |
|---|---|
| GitHub | Up to date: every result, doc and script, including `scripts/colab/` |
| Colab runtime `wsp` | Idle (decision 2) |
| Colab runtime `wsp2` | Reclaimed by Colab while idle |
| Colab sign-in | Kept alive by check-ins every ≤9 minutes |

## Open decisions for Shreyas

| # | Decision | Recommendation |
|---|---|---|
| 1 | Approve three fixes and run D2: (a) count only entries that are verified **and** specific (no more unpredicted effects than predicted ones); (b) refuse an entry whose run changed no weights; (c) show the editor the specific verdict, so a model-wrecking edit is never labelled "verified" | Yes: each fix answers a failure D1 showed, and none changes D1's results |
| 2 | Keep the idle runtime `wsp`, or stop it until there is work | Stop it unless D2 or more runs are approved now |
| 3 | Write-up now with what we have, or add runs first | Add 3 more helix2 addition runs (about 4 h), then write; that is where the one real removal came from |
| 4 | 0.8B scale axis: run it or drop it from this plan | Drop it from this plan and say so in the write-up |
| 5 | For any added runs, count the reworded measure inside the verdict (new runs only; earlier results stay as pre-registered) | Yes, because every verdict pass on addition so far was a "+" swap |
