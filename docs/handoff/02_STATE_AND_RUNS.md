# State: what is built, what is running, what has been run (Nov 4, 2026, 14:45 ET)

## What is built

**Repository:** `github.com/cybercryptixcoder/helix_probe`, public, branch `main`.
- **Commits:** author identity `Shreyas Naik <119774329+cybercryptixcoder@users.noreply.github.com>`.
- **Builder commits** also end with the attribution trailer lines the working session provides.
- **Latest code commit:** 17c64bc. Later commits are the VM's result pushes.

```
probe/                 the core (about 1,200 lines; knows nothing about any box)
  loop.py              the board: ACT / RUN / REPAIR / RETHINK, judging, trials, planner, budget, resume
  prompts.py           the three roles' system prompts and task texts; MODEL_RULES; GOAL_RULE
  memory.py            notebook (append-only jsonl), model versions, library
  simulate.py          runs a model's predict() in a sandboxed subprocess (python -I)
  llm.py               OpenAI-style client: key pool, pacing, patient 429 handling, streaming usage
  env.py               the adapter interface: probe() required, optional hooks with defaults
  run.py               CLI: python -m probe.run <adapter.py> [--steps N --budget B --exam K --out DIR ...]
envs/                  one file per box
  find_numeric.py, find_strings.py   FIND functions (cost = inputs)
  arc_agi3.py          any of the 25 public ARC-AGI-3 games (stateful, goals, planning hooks, official score)
  scrambled_grid.py, knob_box.py, hidden_lock.py   toys (hidden_lock: hidden counter; goal=0 for learning only)
bench/
  find/   prepare.py (sample), data/ (80 functions), dev/ (16), score.py (official scorers),
          published/ + published_scores.json (FIND's GPT-4/3.5/Llama answers), run.py (arms), curve.py,
          report.py, status.py, publish.py, aia.py (FIND's protocol, any model), aia_prompts/, compare.py
  arc/    run.py (ARC jobs, official score, report); games/ (downloaded, gitignored)
  restore.py           rebuild runs/ from results/ (continue from GitHub alone)
scripts/  run_find.sh (the v2 VM job), run_v3.sh (the v3 VM job)
versions/ v1/probe_v1, v2/probe_v2 (frozen copies, so old arms stay runnable)
tests/    test_offline.py (v2-era checks), test_v3.py (hidden state, trials, planner, budget, resume)
docs/     helix_probe_explainer_v1/v2/v3.html, V2_JOB.md, V3_JOB.md, RESULTS_LOG.md
results/  everything the VM jobs pushed (gzipped traces)
```

**Versions:**

| Version | Commit | What it is |
|---|---|---|
| v1 | 10a7349 | one experimenter, three memories, the adapter socket |
| v2 | e7a85ee | three roles in series (experimenter, updater, theorist), a sealed exam, mixed random/chosen experiments, a stopping rule, FIND |
| v3 | 631eb46 → 17c64bc | trials for theories (exam optional), stateful boxes with history, goals with planning through the model, budget, ARC-AGI-3, resumable jobs, the goal-guess rule (24414f5), FIND cost in inputs, the fair comparison |

**Explainers** (HTML, open in a browser):
- `docs/helix_probe_explainer_v3.html`: the whiteboard version, with a live hidden-lock run step by step;
- `_v2.html` and `_v1.html`: the earlier versions.

**Run viewer** (Shreyas's own code, not in the public repo):
- an updated version was sent as `runview-probe.zip`: drop-in files for `/home/ubuntu/runview`, plus a new
  `probe_jobs.py`;
- it shows FIND, ARC and AIA jobs, the scores next to the published agents on the same functions, the job scripts'
  logs, and a summary written by rules;
- an Aether install prompt was given on Nov 4. **Whether it was installed is unknown: ask.**

## What is running and queued: nothing

The VM is idle. The v3 job finished at 13:10 ET (`== all jobs done (v3)` in `/home/ubuntu/helix_probe/v3_job.log`).

**Machine:** aarch64, 2 CPUs, about 12 GB RAM, Python 3.12.3. Repo at `/home/ubuntu/helix_probe`, with `.env`
holding `PROBE_API_KEYS` (two Luminal keys) and `ARC_API_KEY`.

**The v3 job, as it ran:**
- script: `scripts/run_v3.sh`, on commit 17c64bc or later;
- it waited for find-v2 on `runs/find/.find-v2.lock`.

| Stage | What | Ran (ET) | Pushed to |
|---|---|---|---|
| aia | our model in FIND's protocol, 80 functions | 06:05–06:16 | `results/find/aia-none/` |
| find | v3 and v3-exam, 80 functions, up to 25 experiments | 06:19–09:13 | `results/find/find-v3/` |
| aia2 | the control again | 09:13–09:26 | `results/find/aia-none-r2/` |
| find2 | v3, seed 1, 80 functions | 09:26–11:23 | `results/find/find-v3-s1/` |
| compare | the paired, budget-matched comparison against each control run | 11:23 | `results/find/compare-v3-aia.md`, `-aia2.md` (+ `.json`) |
| arc | **pilot**: v3 on tr87, wa30, sb26, cd82, sc25; 100 experiments each | 11:23–13:10 | `results/arc/arc-v3/` |

**Job mechanics** (all tested):
- **Progress:** a status line every 10 minutes and a push every 30.
- **Fixes:** before every stage it pulls from GitHub and keeps the pull only if the crash test passes.
- **Stopping:** `kill -TERM` makes every run finish its step, push, and exit.
- **Restarting:** running the same command continues the job: finished runs are skipped, unfinished ones resume.
- **Restoring:** if `runs/` is lost, it is rebuilt from `results/`.

## Everything that has been run

**On the VM:**

| Run | When (ET) | Configuration | Result |
|---|---|---|---|
| find-v2 | Nov 4, 00:40–06:05 | arms v2, v2-directed, v2-random, v2-no-theorist, v1; 80 functions; 25 experiments; exam 4 (v2 arms); DeepSeek V4.1 Flash, thinking off | `03_ANALYSIS.md` §1 |
| v3 job: aia | 06:05–06:16 | FIND's protocol verbatim, temperature 1.0, thinking none, 20 rounds | §3 |
| v3 job: find | 06:19–09:13 | v3, v3-exam; same as find-v2 otherwise | §2 |
| v3 job: aia2 | 09:13–09:26 | the control, repeated | §3 |
| v3 job: find2 | 09:26–11:23 | v3, seed 1 | §2 |
| v3 job: ARC pilot | 11:23–13:10 | 5 unseen games, 100 experiments, 3× human budget | §5: 0 of 35 levels |

**In the builder's workspace** (development; data may be gone with that session, conclusions are recorded here):

| Run | What it showed |
|---|---|
| v1 toys (grid, knob) | held-out 15% and 69%; models grew exceptions (grid code tripled); words and code disagreed |
| v2 toys, directed vs mixed (2 seeds on knob) | directed-only 51% and 45% on knob, mixed 100%; grid 87–96% |
| FIND dev1/dev2 (16 dev functions) | every v2 arm 1.00; the dev set can't separate arms |
| v2 on ARC, reset mode (ft09, ls20) | ft09 model reached 100% held-out after 12 experiments; ls20 63% after 8; prompts were 7–10k tokens |
| Hidden-state census (8 ARC games, random play) | g50t (287 of 1,200 transitions), cd82 (67), wa30 (69) have hidden state |
| v3 toys | grid 88% (37 experiments), knob 100% (24) |
| v3 FIND dev3 (v3, v3-exam) | 1.00 on every function |
| hidden lock, live | the theorist's counting model won its trial 1.00 vs 0.83; settled at 16 experiments |
| arc-dev (ls20, ft09, g50t; before the goal rule) | fits 0.58–0.94; no plans; ft09 level 1 by the experimenter; ft09 official 4.76; a crash after GAME_OVER (fixed) |
| arc-dev2 (ft09, vc33, ls20; with the goal rule) | plans fired on 2 of 3 games; vc33 level 1 by the experimenter after a failed plan |
| AIA test (3 + 3 functions) | the protocol runs end to end; showed the zero-experiment answers |

## Known issues and loose ends

- **The exam:** the evidence now supports removing it (no better than trials across seeds; costs inputs). Waiting
  for Shreyas's decision.
- **The theorist:** unproven on FIND and untested where structure is rich.
- **Two goal mechanisms in the core:** `solve`/`make_tasks` (stateless boxes, end of run) and the planner (boxes
  with `goal()`). A merge candidate.
- **Reports' cost column:** looks inflated, unverified.
- **ARC speed:** about 65 seconds per experiment in the pilot (serial calls, about 2 per experiment).
- **ARC:** 0 levels on unseen games. Goal discovery is the open problem (`03_ANALYSIS.md` §5).
- **The builder workspace is ephemeral.** Only GitHub, the VM, and the files of this handoff persist.
