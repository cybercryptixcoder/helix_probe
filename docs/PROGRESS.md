# Progress

*Every step of both goals, its status, and where it ends. Updated in the same turn as every change (see
`WORKING_METHOD.md`, hard rules). Last updated Nov 7, 2026, 13:20 ET.*

## Goal 1: switch off one ability by editing weights, and show the loop is why

Ends when: Step 4's write-up is delivered.

| Step | What it is | Status | Done when |
|---|---|---|---|
| 0 | Plumbing: harness, grader, guard, Colab | ✅ Done | – |
| 1 | Baselines on the 9B: unedited, random edit, scripted recipe | ✅ Done | – |
| 2 | Main comparison on the 9B: MIT one-conversation vs Helix vs helix2, 3 runs × 2 abilities | ✅ Done (raw files of the six r0 runs lost; results kept in JOURNAL) | – |
| 3 | Removed or only suppressed? (comeback test with worked examples) | ✅ Done, measured inside every grade | – |
| 2b | Three more helix2 addition runs (r3–r5), 9B, verdict v2 | ▶ Starting on `wsp2` | 3 runs graded and on GitHub |
| 2c | Scale axis on the 0.8B (addition only): unedited, random ×3, scripted, MIT ×3, Helix ×3, helix2 ×3; verdict v2 | Queued on `wsp2` after 2b | all graded and on GitHub |
| 4 | Write-up: results table, how each edit works, honest negatives, how to re-run | After 2b and 2c | the write-up is in the repo |

## Goal 2: a verified map of what parts of the model do, using the same loop

Ends when: D4's demo is delivered, or earlier if D2 fails (then the negative result is written up and we decide
together).

| Step | What it is | Status | Done when |
|---|---|---|---|
| D0 | Build: 26-behaviour panel, profile tool, entry format, held-out checking, noise floor | ✅ Done | – |
| D1 | Calibration run: 40 experiments on the 9B, judged by 5 pre-set criteria | ✅ Done, **failed** 3 of 5 | – |
| D2 | Second calibration run with the three fixes, same 5 criteria | ▶ Starting on `wsp` | 40 experiments, about 2.5 h; results on GitHub |
| D3 | The long run: same loop, uncapped, for many hours; discovery curve tracked | Not started; only if D2 passes | the curve flattens or the time budget ends |
| D4 | Demo: a page built from verified entries; live sliders if time allows | Not started; after D3 | the page is in the repo |

## Infrastructure

| Item | Status |
|---|---|
| GitHub | Up to date: every result, doc and script, including `scripts/colab/` |
| Colab runtime `wsp` | D2 |
| Colab runtime `wsp2` | New: Goal 1 additions (2b, 2c) |
| Colab sign-in | Kept alive by check-ins every ≤9 minutes |

## Vision (not scheduled; `NORTH_STAR.md`)

| End product | What exists toward it |
|---|---|
| Goal 1: type a behaviour change in words, get updated weights back | `edit.py` already takes a goal in words and returns an edit file. Missing: reliability, since edits often hit a trigger word instead of the behaviour |
| Goal 2: a representation of the weights and a UI to turn parts up, down or off | D4, built on the map from D2 and D3 |

## Decisions

| When | Decision |
|---|---|
| Nov 7, 12:59 ET | D2 with fixes (a)–(c): yes. Keep `wsp`. Three more helix2 addition runs: yes. Keep the 0.8B axis. Verdict v2 for new runs: yes |

None are open.
