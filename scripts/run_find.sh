#!/usr/bin/env bash
# Helix Probe on FIND (docs/V2_JOB.md): every arm on the 80-function FIND sample (bench/find/data: 40 numeric, 40
# strings), each function a fresh run of up to STEPS experiments, scored with FIND's official metric and set against
# FIND's published GPT-4 / GPT-3.5 / Llama-2 agents (bench/find/published).
#
#   cd /home/ubuntu/helix_probe && git pull && setsid nohup bash scripts/run_find.sh > find_v2.log 2>&1 < /dev/null &
#
# The stages (a restart skips what is done):
#   1. preflight: Python 3.10+ with numpy and scipy, disk, the .env key, a crash test with a fake model (2 functions
#      through the whole pipeline: runs, scoring, report, publish), one real model call, GitHub can push;
#   2. the runs: ARMS x 80 functions, WORKERS at a time, all model calls paced together at about 1 a second
#      (Luminal's long-run rate per key); progress every TICK seconds, a push every PUSH_EVERY ticks;
#   3. the end: the report (results/find/$NAME/report.md) and a push.
#
# Robust (as helix_evolve's jobs, docs/AETHER.md there): one copy per NAME (a lock); runs from a snapshot of itself;
# started again after any stop it resumes (finished runs are skipped, unfinished ones continue from their last step);
# a stop signal lets every run finish its current step, then everything is pushed; retries on errors; installs no
# cron job or timer; waits while memory is short.
#
# Estimated (5 arms): 400 runs, ~8,000 model calls; with two keys (PROBE_API_KEYS in .env, each paced at about 1
# call a second) about 2-3 hours, plus any waits on Luminal. Memory under 1 GB. CPU: light (model calls dominate; scoring runs one short Python process at a time per
# worker). Disk: about 60 MB of runs, about 25 MB pushed (traces gzipped). Cost: about $3-5 at DeepSeek's list price.
#
# Settings: NAME [find-v2]  ARMS ["v2 v2-directed v2-random v2-no-theorist v1"]  STEPS [25]  EXAM [4]  WORKERS [6]  LIMIT [0 = all]
#   CATEGORIES ["numeric strings"]  MIN_FREE_MB [1000]  START_DISK_MB [1500]  MAX_RETRIES [3]  PUSH [1]  FAKE [0]
#   TICK [600]  PUSH_EVERY [4]
#
#   FAKE=1 PUSH=0 LIMIT=1 STEPS=2 bash scripts/run_find.sh        # the whole job with a fake model (a test)
set -uo pipefail
cd "$(dirname "$0")/.." || exit 3
NAME="${NAME:-find-v2}"
if [ -z "${FIND_SNAPSHOT:-}" ]; then
  mkdir -p runs && cp "$0" "runs/.find_job_snapshot_$NAME.sh.$$" \
    && mv -f "runs/.find_job_snapshot_$NAME.sh.$$" "runs/.find_job_snapshot_$NAME.sh" \
    && FIND_SNAPSHOT=1 exec bash "runs/.find_job_snapshot_$NAME.sh" "$@"
fi
PY="${PYTHON:-$(command -v python3 || command -v python)}"
ARMS="${ARMS:-v2 v2-directed v2-random v2-no-theorist v1}"
STEPS="${STEPS:-25}"
EXAM="${EXAM:-4}"
WORKERS="${WORKERS:-6}"
LIMIT="${LIMIT:-0}"
CATEGORIES="${CATEGORIES:-numeric strings}"
MIN_FREE_MB="${MIN_FREE_MB:-1000}"
START_DISK_MB="${START_DISK_MB:-1500}"
MAX_RETRIES="${MAX_RETRIES:-3}"
PUSH="${PUSH:-1}"
FAKE="${FAKE:-0}"
TICK="${TICK:-600}"
PUSH_EVERY="${PUSH_EVERY:-4}"
GIT_NAME="${GIT_NAME:-Shreyas Naik}"
GIT_EMAIL="${GIT_EMAIL:-119774329+cybercryptixcoder@users.noreply.github.com}"
RUNS="runs/find/$NAME"
RESULTS="results/find/$NAME"
[ "$FAKE" = "1" ] && { RUNS="runs/find-fake/$NAME"; RESULTS="runs/find-fake/results-$NAME"; }
LOG="runs/find/$NAME.log"
NICE_CMD="nice -n 10"
command -v ionice >/dev/null && NICE_CMD="ionice -c 3 nice -n 10"
FAKE_FLAG=""; [ "$FAKE" = "1" ] && FAKE_FLAG="--fake"
mkdir -p runs/find "$RUNS" "$RESULTS"
if command -v flock >/dev/null; then
  exec 8> "runs/find/.$NAME.lock"
  flock -n 8 || { echo "== this job is already running (another copy holds runs/find/.$NAME.lock); this copy exits and changes nothing"; exit 0; }
fi

echo "== Helix Probe FIND job: $NAME, arms: $ARMS; up to $STEPS experiments per function, exam $EXAM, $WORKERS at a time"
echo "   started $(date '+%Y-%m-%d %H:%M:%S %Z'); repo $(pwd) ($(git rev-parse --abbrev-ref HEAD 2>/dev/null) $(git rev-parse --short HEAD 2>/dev/null))"

# ------------------------------------------------------------------ stop signals: passed to the child, then everything is pushed
CHILD=""
STOPPING=0
nap() { sleep "$1" & wait $! 2>/dev/null; }
on_stop() {
  [ "$STOPPING" = "1" ] && return
  STOPPING=1
  echo "== stop requested: every run finishes the step in progress (a minute or two), then everything is pushed"
  [ -n "$CHILD" ] && kill -TERM "$CHILD" 2>/dev/null
}
trap on_stop TERM INT HUP
run_child() {   # log-file command...
  local log="$1"; shift
  "$@" >> "$log" 2>&1 &
  CHILD=$!
  local rc=""
  while kill -0 "$CHILD" 2>/dev/null; do wait "$CHILD"; rc=$?; done
  if [ -z "$rc" ] || [ "$rc" -gt 128 ]; then wait "$CHILD" 2>/dev/null; local r2=$?; [ "$r2" != "127" ] && rc=$r2; fi
  CHILD=""
  return "${rc:-0}"
}

# ------------------------------------------------------------------ 1. preflight (about 1 minute)
echo "== preflight"
"$PY" -c "import sys, numpy, scipy; assert sys.version_info >= (3, 10); print('   python', sys.version.split()[0], '| numpy', numpy.__version__, '| scipy', scipy.__version__)" \
  || { echo "preflight: Python 3.10+ with numpy and scipy is needed (pip install numpy scipy)" >&2; exit 3; }
free_disk=$(df -Pm . | awk 'NR==2 {print $4}')
echo "   disk: ${free_disk} MB free (need $START_DISK_MB to start)"
[ "${free_disk:-0}" -ge "$START_DISK_MB" ] || { echo "preflight: only ${free_disk} MB of disk free; need $START_DISK_MB MB. Nothing was started." >&2; exit 3; }
if [ "$FAKE" != "1" ]; then
  [ -f .env ] || { echo "preflight: no .env in $(pwd) (it needs a line PROBE_API_KEYS=key1,key2)" >&2; exit 3; }
fi
PRE="$(mktemp -d)"
( "$PY" bench/find/run.py --out "$PRE/job" --data bench/find/data --arms v2 v1 --limit 1 --steps 2 --exam 2 --workers 2 --fake \
  && "$PY" bench/find/status.py "$PRE/job" \
  && "$PY" bench/find/publish.py "$PRE/job" "$PRE/results" \
  && test -s "$PRE/results/report.md" ) > "$PRE/pre.log" 2>&1 \
  || { echo "preflight: the crash test (2 functions x 2 arms with a fake model; scoring; report; publish) failed:" >&2; tail -20 "$PRE/pre.log" >&2; rm -rf "$PRE"; exit 3; }
echo "   crash test passed (2 functions x 2 arms with a fake model, the official scoring, the report, publish)"
rm -rf "$PRE"
if [ "$FAKE" != "1" ]; then
  "$PY" - <<'PY' || { echo "preflight: the model can't be reached (is .env in the repo root with LUMINAL_API_KEYS=... or PROBE_API_KEY=...?)" >&2; exit 3; }
from probe.llm import LLM
llm = LLM()
for i in range(len(llm.keys)):
    r = llm("You answer in one word.", "Say OK.", max_tokens=20)
    print(f"   model answers on key {r['key_index'] + 1} of {len(llm.keys)}:", r["text"].strip()[:20], f"({r['seconds']:.1f} s)")
PY
fi
if [ "$PUSH" = "1" ]; then
  git push --dry-run -q origin HEAD >/dev/null 2>&1 \
    || { echo "preflight: can't push to GitHub (check that the repo's branch tracks origin and access works)" >&2; exit 3; }
  echo "   GitHub: can push"
fi

# ------------------------------------------------------------------ publishing: only results/ is ever added, never .env or runs/
git_push() {   # message
  [ "$PUSH" = "1" ] || return 0
  ( command -v flock >/dev/null && flock 9
    git add -f "$RESULTS" 2>/dev/null
    git -c user.name="$GIT_NAME" -c user.email="$GIT_EMAIL" -c commit.gpgsign=false commit -q -m "$1" || exit 0
    for i in 1 2 3 4; do git pull -q --rebase --autostash origin HEAD && git push -q origin HEAD && exit 0; sleep $((15 * i)); done
    echo "   (push failed: results stay in $RESULTS and $RUNS; the next push sends them)" >&2
  ) 9> "runs/.git.lock"
}
publish() {   # message
  "$PY" bench/find/publish.py "$RUNS" "$RESULTS" 2>&1 | tail -1 || echo "   (publishing failed; the runs are fine)"
  git_push "$1"
}

# every start is recorded: commit, settings, machine
"$PY" - "$RESULTS/sessions.jsonl" "$NAME" "$ARMS" "$STEPS" "$EXAM" "$WORKERS" "$FAKE" <<'PY' || true
import json, os, platform, shutil, subprocess, sys, time
f, name, arms, steps, exam, workers, fake = sys.argv[1:]
def sh(*c):
    try:
        return subprocess.run(c, capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        return None
mem = next((l.split()[1] for l in open("/proc/meminfo") if l.startswith("MemTotal")), None) if os.path.exists("/proc/meminfo") else None
row = {"t": time.strftime("%Y-%m-%d %H:%M:%S %Z"), "name": name, "arms": arms.split(), "steps": int(steps), "exam": int(exam),
       "workers": int(workers), "fake": fake == "1", "commit": sh("git", "rev-parse", "HEAD"), "python": platform.python_version(),
       "machine": platform.machine(), "cpus": os.cpu_count(), "mem_total_mb": int(mem) // 1024 if mem else None,
       "disk_free_mb": shutil.disk_usage(".").free >> 20}
with open(f, "a") as fh:
    fh.write(json.dumps(row) + "\n")
PY

if ls "$RUNS"/*/*/summary.json >/dev/null 2>&1; then
  echo "== $NAME already has $(ls "$RUNS"/*/*/summary.json | wc -l) finished runs: pushing them first, then resuming"
  publish "Helix Probe FIND job ($NAME): catch-up push at a restart"
fi

( SL=""; trap 'kill ${SL:-} 2>/dev/null; exit 0' TERM INT HUP
  n=0
  while true; do sleep "$TICK" & SL=$!; wait $SL; "$PY" bench/find/status.py "$RUNS"; n=$((n + 1))
    [ $((n % PUSH_EVERY)) -eq 0 ] && publish "Helix Probe FIND job ($NAME): progress at $(date -u +%H:%M) UTC"
  done
) &
TICKER=$!
trap 'kill $TICKER 2>/dev/null' EXIT

# ------------------------------------------------------------------ 2. the runs
while [ -r /proc/meminfo ] && [ "$STOPPING" = "0" ]; do
  free=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  [ "${free:-0}" -ge "$MIN_FREE_MB" ] && break
  echo "   ($NAME waiting: ${free} MB of memory available, need $MIN_FREE_MB)"; nap 120
done
attempt=0
while [ "$STOPPING" = "0" ]; do
  echo "== $NAME: running (log: $LOG)"
  run_child "$LOG" $NICE_CMD "$PY" -u bench/find/run.py --out "$RUNS" --data bench/find/data --arms $ARMS \
    --categories $CATEGORIES --steps "$STEPS" --exam "$EXAM" --workers "$WORKERS" --limit "$LIMIT" $FAKE_FLAG
  rc=$?
  case "$rc" in
    0) break ;;
    75) echo "== $NAME: stopped cleanly on a stop signal"; break ;;
    *) attempt=$((attempt + 1))
       echo "== $NAME: stopped on an error (exit $rc); the last lines of its log:"; tail -5 "$LOG" | sed 's/^/   /'
       [ "$STOPPING" = "1" ] && break
       if [ "$attempt" -gt "$MAX_RETRIES" ]; then
         echo "== $NAME: stopped after $MAX_RETRIES retries; run this script again to continue it"; break
       fi
       echo "   retry $attempt of $MAX_RETRIES in 60 s (finished runs are kept; unfinished ones resume)"
       nap 60 ;;
  esac
done
kill $TICKER 2>/dev/null
wait $TICKER 2>/dev/null
"$PY" bench/find/status.py "$RUNS"

# ------------------------------------------------------------------ 3. the end: report and push
publish "Helix Probe FIND job ($NAME): $( [ "$STOPPING" = "1" ] && echo stopped || echo finished ); results and report"
echo "== the report: $RESULTS/report.md"
sed 's/^/   /' "$RESULTS/report.md" 2>/dev/null | head -40
if [ "$STOPPING" = "1" ]; then
  echo "== stopped before the job finished ($NAME); run this script again to continue it"
else
  echo "== all jobs done ($NAME)"
fi
