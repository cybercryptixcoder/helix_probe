# Operations: running, Aether, jobs, adapters, keys

## 1. From scratch on any machine

```bash
git clone https://github.com/cybercryptixcoder/helix_probe && cd helix_probe
pip install numpy scipy            # FIND boxes; the core is standard library only
pip install arc-agi                # ARC-AGI-3 only; needs Python 3.12+
cat > .env <<'EOF'
PROBE_BASE_URL=https://flash.luminal.cloud/v1
PROBE_MODEL=deepseek-ai/DeepSeek-V4.1-Flash
PROBE_API_KEYS=<key1>,<key2>
ARC_API_KEY=<arc key>
EOF
python tests/test_v3.py                                   # offline checks, no model needed
python -m probe.run envs/hidden_lock.py --offline --steps 3   # a crash test with a fake model
python -m probe.run envs/hidden_lock.py --env-arg goal=0 --steps 20 --out runs/lock   # live
```

- **The `.env` file is gitignored.** Lines are `KEY=value`, with no inline comments.
- **Keep any JSON settings out of `.env`** if you `source` it (`PROBE_EXTRA_BODY` breaks `set -a`). Python reads
  `.env` itself.
- **Where the keys are:** Shreyas's two Luminal keys and the ARC key are in his messages of Nov 3–4 (not copied
  here) and in the VM's `.env`.

**`probe.run` flags:**

| Flag | Meaning |
|---|---|
| `--steps N` | total experiments; rerun with a bigger N and the same `--out` to continue |
| `--budget B` | in the box's cost units |
| `--exam K` | sealed exam probes (0 = none) |
| `--trial T` | experiments a new theory is tried on |
| `--no-plan` | don't use the planner |
| `--theorist-every K` | how often the theorist runs |
| `--experimenter llm\|random` | who chooses experiments |
| `--random-every K` | every k-th experiment is random |
| `--effort role=level` | thinking level per role |
| `--knowledge files` | the library |
| `--env-arg k=v` | passed to the adapter |
| `--offline` | a scripted fake model |

**One run folder holds:**
- `notebook.jsonl`, `calls.jsonl` (with reasoning), `offers.jsonl`, `trials.jsonl`, `trial.json`;
- `model/v###.py` and `.json`, `curve.csv`, `summary.json`, `run.log`;
- `exam.json` and `heldout.json` when used.

## 2. Benchmarks

**FIND:**
- `python bench/find/run.py --out runs/find/X --arms v3 v3-exam --steps 25 --workers 6`
  - add `--data bench/find/dev` for the dev set and `--limit N` for the first N functions;
  - `--fake` makes it a crash test;
  - arms are listed in `ARMS` in `bench/find/run.py`.
- Score and report: automatic (`official_curve.json` per run). `python bench/find/report.py runs/find/X` writes
  `report.md`.
- The same-model control: `python bench/find/aia.py --out results/find/aia-none --effort none --workers 6`.
- The fair comparison: `python bench/find/compare.py --helix <job dirs> --aia <aia dir> --out <file.md>`.

**ARC-AGI-3:**
- `python bench/arc/run.py --out runs/arc/X --games tr87 wa30 --steps 100 --budget-x 3 --workers 5`
  - `--games all` runs every game;
  - `--report` only rewrites `report.md`;
  - `--fake` makes it a crash test.
- Games are downloaded once into `bench/arc/games/` (gitignored), with the key.

**Publish, then restore:**
- `python bench/find/publish.py runs/find/X results/find/X` works for ARC jobs too. Traces are gzipped.
- `python bench/restore.py results/find/X runs/find/X` reverses it. Then rerun the same command to continue.

## 3. Aether (the VM agent)

**What Aether is:** Shreyas's agent on a cloud machine (aarch64, 2 CPUs, about 12 GB, `/home/ubuntu`). It is
deliberately "a fairly dumb agent... It's just going to take what we've given it, follow the instructions, and
just run it in the terminal." It is not meant to fiddle with code.

**Conventions every job follows** (the helix-vm-job skill):
- **Self-protection:** the job copies itself to a snapshot, so a `git pull` mid-job changes nothing. It holds a
  flock lock, so only one copy runs.
- **Preflight:**
  - packages, disk and `.env`;
  - a crash test with a fake model through the whole pipeline: runs, publish, delete, restore, resume;
  - a live call on every key;
  - a check that it can push.
- **While running:** progress lines every 10 minutes, and pushes of `results/` only (never `git add -A`).
- **At the end:** `== all jobs done`.
- **Starting it:** `setsid nohup bash scripts/<job>.sh > <log> 2>&1 < /dev/null &`.

**Aether never:**
- sets up cron jobs, timers or watchdogs;
- stops, kills or restarts a process unless Shreyas orders it;
- edits code to fix a failure (it reports instead);
- prints or commits `.env`.

**Prompt templates** (full versions in `docs/V2_JOB.md` and `docs/V3_JOB.md`):
- **Start a job:**
  - `git pull`;
  - check the files exist;
  - add the `.env` lines if missing;
  - check packages;
  - start with `setsid nohup`;
  - after 5 minutes, quote the log lines expected after a good start;
  - report `free -m`, `df -h /` and the job's pid (`pgrep -fa <name>_job_snapshot`);
  - stop. No monitors.
- **Status:** "quote the last 15 lines of `<log>` verbatim and say whether `pgrep -fa <snapshot>` is alive. Change
  nothing."
- **Graceful stop:** `kill -TERM` the job's bash process, then wait for `== stopped` in the log.
- **Restart onto a newer version** (only while a job is waiting): TERM, wait for "stopped while waiting", then
  `git pull` and start the same way.
- **Continue on a fresh machine:** clone, `.env`, packages, then start with `WAIT_FOR=none`. The job rebuilds
  `runs/` from `results/`.

**What reaches a running job without a new prompt:** Python changes. The v3 job pulls before every stage and keeps
a pull only if the crash test passes. Changes to the job script itself need a restart.

## 4. The VM job scripts

`scripts/run_v3.sh` settings (environment variables):

| Setting | Default |
|---|---|
| `STAGES` | `aia find aia2 find2 arc` |
| `WAIT_FOR` | `runs/find/.find-v2.lock` |
| `FIND_ARMS` | `v3 v3-exam` |
| `FIND_STEPS` | 25 |
| `FIND2_ARMS` | `v3` |
| `AIA_EFFORT` | `none` |
| `ARC_ARMS` | `v3` |
| `ARC_GAMES` | `tr87 wa30 sb26 cd82 sc25` |
| `ARC_BUDGET_X` | 3 |
| `ARC_STEPS` | 100 |
| `ARC_WORKERS` | 5 |
| `WORKERS` | 6 |
| `PUSH` | 1 |
| `PUSH_MIN` | 30 |
| `FAKE` | 0 |
| `PYTHON` | `python3` |

- A test of the whole job: `FAKE=1 PUSH=0 WAIT_FOR=none bash scripts/run_v3.sh`.
- Finished stages leave `results/.../DONE`. Delete a `DONE` to rerun that stage; a bigger `*_STEPS` continues runs.
- A new job: copy `run_v3.sh`, change the stages, and keep the preflight, lock, snapshot, pushes and stop handling.

## 5. Making an adapter (a new box)

One file in `envs/`, one class:

```python
from probe.env import Environment, Task

class MyBox(Environment):
    name = "my_box"
    brief = "What the experimenter is told: what it can do and what comes back. Nothing about the insides."
    probe_format = 'probe: {"x": [...]}   observation: {"y": [...]}'
    def probe(self, p):          ...   # REQUIRED: run one experiment for real, return the observation dict
    def random_probe(self, rng): ...   # an ordinary random probe: half the experiments, the exam, held-out
    def validate(self, p):       ...   # None, or an error string the experimenter gets back
    def compare(self, pred, obs): ...  # 0..1 (default: recursive with tolerance)
    def cost(self, p, obs):      ...   # budget units (default 1 per experiment)
    # boxes that remember:
    stateful = True
    def full_probe(self, p): ...       # what predict() receives: the probe plus the visible state plus "history"
    def restore(self, entries): ...    # replay the notebook to get back to where a run stopped
    def view_state(self): ...          # a short text of where the box is now, for the prompts
    # boxes with goals:
    def goal(self): ...                # Task(description, check(observation)) or None
    def done(self): ...                # True when there is nothing left to do
    max_probe = 8                      # actions per experiment
    def plan_actions(self): ...        # the actions the planner may try
    def advance(self, fp, action, pred): ...   # the next full probe after the model's predicted step (None = dead end)
    def state_key(self, fp): ...       # for "already visited" in the search
    # stateless boxes with goals solved at the end:
    def make_tasks(self, rng, n): ...
    # compact text for the prompts:
    def view_probe(self, p): ...;  def view_obs(self, o): ...
```

**Rules for adapters:**
- Box knowledge goes only here.
- The brief says what you can do, never how it works.
- Use the benchmark's own scorer for measurement, never for the roles.
- Never give agents the evaluator's internals.
- Check it with `--offline`, then a short live run.
- Examples: `envs/hidden_lock.py` (smallest stateful box with a goal), `envs/find_strings.py` (stateless),
  `envs/arc_agi3.py` (everything).

## 6. The model client (Luminal)

- An OpenAI-style endpoint; DeepSeek V4.1 Flash; thinking off by default.
- Always send `reasoning_effort` and `max_tokens`.
- Stream with `stream_options: {include_usage: true}`.
- Retry 429 and 5xx. Never give up on 429: honour `Retry-After` and back off, for up to 6 hours, resting a limited
  key.
- Keys form a pool used round-robin, at about 1 call a second per key, with at most 8 in flight per key.
- About 20–40 seconds per call on ARC-sized prompts (5–8k tokens); much less on FIND.

## 7. The run viewer

- `/home/ubuntu/runview` on the VM: Shreyas's read-only progress page, on port 9131, behind a cloudflared quick
  tunnel (the URL is in `url.txt`).
- The updated version (sent as `runview-probe.zip`) discovers Helix Probe jobs by `job.json` under
  `/home/ubuntu/*/runs` and `/home/ubuntu/*/results`.
- Install: copy the five files over, then `systemctl --user restart runview.service` (prompt in the Nov 4
  conversation).
- Its code is not in the public repo unless Shreyas says so.

## 8. Troubleshooting seen so far

| Symptom | Cause | Fix |
|---|---|---|
| 429 storms, crashed runs | several processes on one key | key pool and patient retries |
| `numpy` missing in a model sandbox | `python -I` hides site-packages | parent `sys.path` passed in |
| An ARC crash on the first action after a game over | the toolkit returns no frame | only RESET accepted after GAME_OVER |
| The planner never fires | models never predict the goal | the goal-guess rule |
| A container restart killed local runs | the builder's workspace is ephemeral | resume with the same command |
| A waiting VM job runs old stages | it runs from its start-time snapshot | restart it while waiting |
| `pgrep -f "<pattern>"` killed the builder's own shell | the pattern matched the command line itself | use exact pids |
