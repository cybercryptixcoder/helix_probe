# Helix Probe v3: the job

The design: `docs/helix_probe_explainer_v3.html`. The results ledger: `docs/RESULTS_LOG.md`. The script:
`scripts/run_v3.sh`.

## What runs, and why

The job waits until the find-v2 job on the same machine has finished, then runs three stages. Every stage does two
things:
- it tests a change in v3;
- it is an attempt at a result that holds up against published work, in a setup copied from the publication with
  a weaker model and tighter limits.

| Stage | What | The comparison | Published reference |
|---|---|---|---|
| `aia` | FIND's own agent protocol (`bench/find/aia.py`, FIND's prompts verbatim) run with **our** model on the same 80 functions | Is Helix Probe's edge on FIND the loop, or just a newer model? The same-model control the find-v2 result needs | GPT-4 0.20 numeric / 0.01 strings in FIND's protocol |
| `arc` | Helix Probe v3 on the 25 public ARC-AGI-3 games, one playthrough each | Does a flash model with thinking off, in a learn-a-model loop, score on ARC-AGI-3 at all, and how far from frontier systems? | Frontier models in ARC's generic harness: 13.3% public (GPT-5.6 Sol, OpenAI's run). Executable World Models (coding agents): GPT-5.4 high 41.3%, GPT-5.5 high 58.1%, with 1,500 actions per level |
| `find` | Helix Probe v3 on the 80 FIND functions, arms `v3`, `v3-exam`, `v3-random`, `v3-no-theorist` | v3 against v2 (find-v2) on the same functions; whether trials can replace the sealed exam; ablations | find-v2, and FIND's published agents |

**ARC setup, and how it compares to the published setups:**
- **Play.** The official toolkit (`arc-agi`) in local mode: one playthrough per game, every action counted
  (resets included), no restart of the whole game, no return to completed levels.
- **Score.** The toolkit's own `EnvironmentScoreCalculator` (RHAE against the human action counts). The job score
  is the mean over the 25 games.
- **Budget.** At most 3× the human action count for the whole game (on average about 2,000 actions for a game of
  6–10 levels). That is tighter than the Executable World Models paper's 1,500 actions per level. ARC-AGI-3 itself
  sets no action limit.
- **Model.** DeepSeek V4.1 Flash with thinking off, against GPT-5.x with high reasoning.
- **What the model sees.** Only the frame as text, the actions, and what changed. There are no game-specific tools
  or hints. The adapter is one file and the core is the same one used for FIND.

Honest expectation: on ARC, v3 may well score near zero. A level scores only when the model is good enough for the
planner to reach it, or when the experimenter stumbles into it. Either way, the run records how well a learned
model predicts each game (fit and on-arrival hits per game) and which games have hidden state. Those are findings
in their own right.

## Robustness

- **Everything is traced.** For every run, the job keeps:
  - every model call, with its prompt, reply, reasoning, tokens and seconds;
  - every candidate model and every model that was ever current;
  - every experiment, every theory trial and every curve.

  All of it is pushed to `results/` every 30 minutes. Traces are gzipped.
- **Resume after a stop.** If the job is stopped or the machine restarts, the same command continues it:
  - finished runs are skipped;
  - unfinished ones resume from their last step, and ARC games are restored by replaying their actions;
  - a finished stage is skipped (`results/.../DONE`).
- **Resume from GitHub alone.** If the local `runs/` folder is lost, the job first rebuilds it from GitHub
  (`bench/restore.py`). A fresh clone continues the job where the last push left it. For a longer run (for example
  50 more experiments per game), run it again with a bigger `ARC_STEPS` or `FIND_STEPS`.
- **Fixes made while it waits.** When find-v2 ends, the job pulls once from GitHub and keeps what it pulled
  only if the same crash test passes; otherwise it goes back to the commit it started with.
- **Graceful stop.** `kill -TERM` on the job lets every run finish its step and save, pushes, then exits.
- **Tested here before pushing:**
  - the whole job with a fake model;
  - waiting on a held lock;
  - a stop with `kill -TERM` (exit 75) followed by a resume;
  - publish, delete, restore from the published files, continue (a stateful box, with a theory mid-trial).

## The Aether prompt

Paste as is. (`<ARC_KEY>` is the ARC-AGI key; the line goes into the gitignored `.env` only.)

```
Queue my Helix Probe v3 job on this machine and report back. It must wait for the find-v2 job that is running now; the script does the waiting itself. Don't change any code or settings, and don't touch the find-v2 job.

1. In /home/ubuntu/helix_probe, run `git pull`. (The find-v2 job runs from its own snapshot, so the pull doesn't affect it.) Check that scripts/run_v3.sh, bench/arc/run.py and bench/restore.py exist.
2. Add this one line to the end of /home/ubuntu/helix_probe/.env if .env has no line starting with ARC_API_KEY= (keep the existing lines; never commit, push or print .env):
   ARC_API_KEY=<ARC_KEY>
3. The ARC stage needs Python 3.12 or newer with the ARC toolkit. Run `python3 --version`.
   - If it is 3.12 or newer: run `python3 -m pip install --user arc-agi numpy scipy` (add `--break-system-packages` if pip refuses), and use PYTHON=python3 below.
   - If it is older: run `python3 -m pip install --user uv` (add `--break-system-packages` if pip refuses), then in /home/ubuntu/helix_probe run `python3 -m uv venv -p 3.12 .venv312` and `python3 -m uv pip install -p .venv312 arc-agi numpy scipy`, and use PYTHON=/home/ubuntu/helix_probe/.venv312/bin/python below.
   Then check: `$PYTHON -c "import arc_agi, arcengine, numpy, scipy; print('ok')"` must print ok. If it doesn't, report the error and stop.
4. Start the job in the background, exactly like this, from /home/ubuntu/helix_probe (one command, with your PYTHON value):
   `PYTHON=<PYTHON> setsid nohup bash scripts/run_v3.sh > v3_job.log 2>&1 < /dev/null &`
5. Wait about 5 minutes, then read v3_job.log once. A good start shows, in order: "== preflight", "arc-agi toolkit ok", "crash test passed", "model answers on key 1 of 2: OK", "model answers on key 2 of 2: OK", "GitHub: can push", and then either "waiting for the job holding runs/find/.find-v2.lock to finish" (find-v2 still running: expected) or "is free". A line starting with "preflight:" or a Traceback means the job stopped: report those lines exactly, and don't edit anything to fix it.
6. Report what you saw (quote the lines), the output of `free -m` and `df -h /`, and `ps -o pid,sid,ppid,etime,cmd -p <pid>` for the job (find it with `pgrep -fa v3_job_snapshot`).
7. Then stop. Don't stop, restart or kill any process. Don't set up cron jobs, timers, monitors, scheduled check-ins or reminders: Shreyas checks in himself.
```

**What the log shows after a good start:**

```
== Helix Probe v3 job: stages aia arc find
== preflight
   python 3.12.x
   arc-agi toolkit ok
   disk: ... MB free
   crash test passed: v3 offline checks, fake-model FIND and ARC runs, publish, delete + restore from the published files, resume
   model answers on key 1 of 2: OK (... s)
   model answers on key 2 of 2: OK (... s)
   GitHub: can push
   [HH:MM] waiting for the job holding runs/find/.find-v2.lock to finish      (every 10 minutes while find-v2 runs)
== HH:MM: runs/find/.find-v2.lock is free
   pulled <commit> (fixes made while waiting); crash test passed      (only if something new was pushed)
== starting
== stage aia: started ...
```

Then:
- a status line every 10 minutes and a push every 30 minutes;
- `== stage <name>: ...` at each stage boundary;
- at the end, `== all jobs done (v3)`.

**Estimated duration (after find-v2 ends):**

| Stage | Duration | Model calls |
|---|---|---|
| aia | under 1 hour | about 1,000 |
| arc | 10–16 hours (25 games, 13 at a time, up to 400 experiments each) | about 20,000 |
| find | 4–6 hours (320 runs) | about 6,000 |

- Memory: under 2 GB. CPU: light.
- Data pushed: about 100–200 MB, mostly ARC traces (gzipped).
- Cost: about $15–30 at DeepSeek's list price.

## Follow-up prompts

- **Status:** "In /home/ubuntu/helix_probe, quote the last 15 lines of v3_job.log verbatim, and say whether the
  job's process is alive (`pgrep -fa v3_job_snapshot`). Nothing else. Don't change, stop or restart anything."
- **Stop gracefully** (only if Shreyas asks): "In /home/ubuntu/helix_probe, send the v3 job a stop signal
  (`kill -TERM <pid>` for the pid from `pgrep -f v3_job_snapshot`, the bash process only), wait until
  v3_job.log shows `== stopped before the job finished`, and quote the last 10 lines."
- **Continue after a stop or a reboot:** the same start command as step 4.
- **Continue on a fresh machine from GitHub alone:** clone, add `.env` (step 2 plus the `PROBE_API_KEYS` line), do
  step 3, then step 4 with `WAIT_FOR=none` in front.
