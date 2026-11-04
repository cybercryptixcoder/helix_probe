# Helix Probe v2: the FIND job

Newest first. The design and every change from v1: `docs/helix_probe_explainer_v2.html`.

## What runs, and why

**The question:** on FIND, a published interpretability benchmark, does Helix Probe v2 (a flash model, thinking off,
many small experiments, a model judged on sealed evidence) beat FIND's own agents (GPT-4, GPT-3.5, Llama-2, which
looked about 3 times and then wrote an answer)? And which parts of v2 matter: the mixed experiments, the theorist,
the system as a whole against v1?

**The arms**, each on all 80 functions of `bench/find/data` (40 numeric, 40 strings), each function a fresh run:

| Arm | What it is | What it isolates |
|---|---|---|
| `v2` | the system: mixed experiments (every other one a random probe from the box), updater, theorist, sealed exam of 4 | |
| `v2-directed` | every experiment chosen by the experimenter | the value of mixing in random probes |
| `v2-random` | every experiment a random probe | the value of choosing experiments at all (your core claim) |
| `v2-no-theorist` | no theorist | the value of the theorist |
| `v1` | the frozen first version (same model client) | v2 against v1 |
| published GPT-4, GPT-3.5, Llama-2-70B, -13B | FIND's released answers, same scorer, same functions | the field |

**The constraint:** up to 25 experiments per function (v2 arms stop early once 8 in a row were predicted and the exam
is perfect), an exam of 4 random probes (counted in the inputs), DeepSeek V4.1 Flash with thinking off for every
role. FIND's own limit on inputs (−128 to 128; up to 20 numbers or 10 strings per experiment) applies to every arm.

**What answers the question:** `results/find/find-v2/report.md`. Per arm and category: FIND's official score at the
end, after 3 experiments (FIND's GPT-4 budget) and after 10; experiments and inputs used; model calls; cost.

**Honest expectations,** from the dev runs (16 other FIND functions, never the reported 80) and the toys:
- every v2 arm and v1 should be far above GPT-4 on both categories (dev: about 1.0 vs GPT-4's 0.50 numeric and 0.00
  strings). The gap is between iterating with a checked model and looking a few times;
- inside v2, the differences are small on FIND and may be within noise on 40 functions. After 3 experiments, v2 beat
  v1 clearly on dev strings (0.78-0.90 vs 0.34);
- random probes did very well on FIND strings on dev (FIND's string functions respond to ordinary words); the mixed
  default was chosen because directed-only failed on the knob box (51% and 45% held-out on two seeds vs 100% mixed).

## The Aether prompt

Paste as is. (The keys are the two project keys; the line goes into the gitignored `.env` only.)

```
Start my Helix Probe FIND job on this machine and report back. Don't change any code or settings; just start it.

1. If /home/ubuntu/helix_probe doesn't exist, clone it: `git clone https://github.com/cybercryptixcoder/helix_probe /home/ubuntu/helix_probe`. Then, in /home/ubuntu/helix_probe, run `git pull`. Check that scripts/run_find.sh and bench/find/data/sample.json exist.
2. If /home/ubuntu/helix_probe/.env doesn't exist, create it containing exactly this one line, and nothing else (it is gitignored: never commit, push or print it):
   PROBE_API_KEYS=<KEY_1>,<KEY_2>
3. Run `python3 -c "import numpy, scipy; print('ok')"` once. If it doesn't print ok, report the error and stop.
4. Start the job in the background, exactly like this, from /home/ubuntu/helix_probe (one command):
   `setsid nohup bash scripts/run_find.sh > find_v2.log 2>&1 < /dev/null &`
5. Don't change any setting: other agents share this machine, and the job is sized for it.
6. Wait about 5 minutes, then read the last 20 lines of find_v2.log once. A good start shows, in order: "== preflight", "crash test passed", "model answers on key 1 of 2: OK", "model answers on key 2 of 2: OK", "GitHub: can push", "== find-v2: running". A line starting with "preflight:" or a Traceback means the job stopped: report those lines exactly, and don't edit anything to fix it.
7. Report what you saw (quote the lines), the output of `free -m` and `df -h /`, and `ps -o pid,sid,ppid,etime,cmd -p <pid>` for the job (find it with `pgrep -fa find_job_snapshot`; `$!` after setsid is not the job).
8. Then stop. Don't stop, restart or kill any process. Don't set up cron jobs, timers, monitors, scheduled check-ins or reminders: Shreyas checks in himself.
```

**What the log shows after a good start:**

```
== Helix Probe FIND job: find-v2, arms: v2 v2-directed v2-random v2-no-theorist v1; up to 25 experiments per function, exam 4, 6 at a time
== preflight
   python 3.x | numpy ... | scipy ...
   disk: ... MB free (need 1500 to start)
   crash test passed (2 functions x 2 arms with a fake model, the official scoring, the report, publish)
   model answers on key 1 of 2: OK (... s)
   model answers on key 2 of 2: OK (... s)
   GitHub: can push
== find-v2: running (log: runs/find/find-v2.log)
```

then, every 10 minutes, `== HH:MM progress: N/400 runs done, M model calls; v1 numeric 0.xx (n=..), ...`, a push
every 40 minutes, and at the end the report and `== all jobs done (find-v2)`.

**Duration:** about 2-3 hours (400 runs, about 8,000 model calls, two keys at about 1 call a second each).
Memory under 1 GB, CPU light, about 30 MB pushed. About $3-5 at DeepSeek's list price.

## Follow-up prompts

- **Status:** "In /home/ubuntu/helix_probe, read the latest `== HH:MM progress:` line in find_v2.log and quote it
  verbatim, and say whether the job's process is alive (`pgrep -fa find_job_snapshot`). Nothing else. Don't change,
  stop or schedule anything."
- **Restart after any stop:** the same start command (step 4); finished runs are kept, unfinished ones resume.
- **Stop (only on Shreyas's order):** `kill -TERM <the job's bash pid>` (from `pgrep -fa find_job_snapshot`; never
  `kill -9`), then wait for the log to end with "run this script again to continue it" and report the last lines.

## Tested (November 3-4, 2026, on the dev machine, before handing over)

| Test | Result |
|---|---|
| `python -m tests.test_offline`: the accept rule (a lookup table loses to the true rules on the exam), the roles (the theorist never sees a model), the true model (exam and held-out 100%, early stop, goals 3/3 first try), FIND scoring (true functions score 1 except the 4 noisy ones; empty models 0; string truth pairs reproduce) | pass |
| FIND scorer re-implemented: 400/400 string test pairs reproduced by the real functions; MLP weights match torch to 1e-4 | pass |
| `FAKE=1 PUSH=0 LIMIT=1 STEPS=2 bash scripts/run_find.sh`: the whole job with a fake model, report and publish | pass |
| A second start while running | prints "already running", exits 0 |
| A stop signal mid-run | every run stops after its current step; pushes; last line "stopped before the job finished ... run this script again" |
| `kill -9` of the Python run, plus a torn notebook line | the script retries after 60 s; the run resumes; the torn line is dropped; all notebooks intact and sequential |
| Live, exactly as the VM runs it (`PUSH=0 LIMIT=1 STEPS=4`, real model, both keys, all 5 arms) | preflight passes on both keys; 10 runs, 61 calls, report written |
| Rate limits shared with other processes | first version crashed after 6 retries; the client now waits out 429s (Retry-After, up to 30 min a wait, 6 h in total) and paces each key |
| Dev comparison, live: 7 arms on 16 dev functions (`runs/dev1`, `runs/dev2`) and the toy rematch | see the explainer, section 8 |
