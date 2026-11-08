# Progress

*Every step of both goals, its status, and where it ends. Updated in the same turn as every change (see
`WORKING_METHOD.md`, hard rules). Last updated Nov 7, 2026, 20:30 ET.*

## Goal 1: switch off one ability by editing weights, and show the loop is why

Ends when: Step 4's write-up is delivered.

| Step | What it is | Status | Done when |
|---|---|---|---|
| 0 | Plumbing: harness, grader, guard, Colab | ✅ Done | – |
| 1 | Baselines on the 9B: unedited, random edit, scripted recipe | ✅ Done | – |
| 2 | Main comparison on the 9B: MIT one-conversation vs Helix vs helix2, 3 runs × 2 abilities | ✅ Done (raw files of the six r0 runs lost; results kept in JOURNAL) | – |
| 3 | Removed or only suppressed? (comeback test with worked examples) | ✅ Done, measured inside every grade | – |
| 2b | Three more helix2 addition runs (r3–r5), 9B, verdict v2 | ✅ Done. r3, r4: not removed ("+" swaps). **r5: CLEAN DURABLE under v2, removed in every wording, precise** (an `lm_head` readout edit; two-digit only) | – |
| 2c | Scale axis on the 0.8B (addition only): unedited, random ×3, scripted, MIT ×3, Helix ×3, helix2 ×3; verdict v2 | ✅ Done. MIT 0/3, Helix 0/3 (all "+" swaps); **helix2 1/3 (r1: internal direction removal)**; scripted halves it. Full table: JOURNAL, Nov 7 20:30 | – |
| 4 | Write-up: results table, how each edit works, honest negatives, how to re-run | ⏸ Next. Can start now; no GPU needed | the write-up is in the repo |

## Goal 2: a verified map of what parts of the model do, using the same loop

Ends when: D4's demo is delivered, or earlier if D2 fails (then the negative result is written up and we decide
together).

| Step | What it is | Status | Done when |
|---|---|---|---|
| D0 | Build: 26-behaviour panel, profile tool, entry format, held-out checking, noise floor | ✅ Done | – |
| D1 | Calibration run: 40 experiments on the 9B, judged by 5 pre-set criteria | ✅ Done, **failed** 3 of 5 | – |
| D2 | Second calibration run with the three fixes, same 5 criteria | ✅ Done, **failed** 4 of 5 (2 of 24 specific, both output-level). Write-up: `GOAL2_CALIBRATION_RESULT.md` | 40 experiments, about 2.5 h; results on GitHub |
| D3 | The long run: same loop, uncapped, for many hours; discovery curve tracked | ❌ Not run, since D2 failed. ⏸ Next step waits for Shreyas: options A–C in the write-up | – |
| D4 | Demo: a page built from verified entries; live sliders if time allows | Not started; after D3 | the page is in the repo |

## Infrastructure

| Item | Status |
|---|---|
| GitHub | Up to date: every result, doc and script, including `scripts/colab/` |
| Colab runtime `wsp` | Idle since D2 ended (21:01 UTC) |
| Colab runtime `wsp2` | Idle since 2c ended (01:11 UTC) |
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

| Open | Goal 2 after D2: (A) stop and publish the negative, (B) systematic ablation map plus the loop explaining it, (C) continuous measure and one more calibration. Also: stop the idle `wsp`? |
