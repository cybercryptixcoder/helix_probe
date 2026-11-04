#!/usr/bin/env bash
# Helix Probe v3 job (docs/V3_JOB.md). Waits for the find-v2 job to finish, then runs three stages in order (aia, arc, find):
#   1. aia    FIND's own agent protocol (bench/find/aia.py) with OUR model on the same 80 FIND functions: the
#             same-model control (is Helix Probe's edge the loop, or just a newer model?)
#   2. arc    Helix Probe v3 on the 25 public ARC-AGI-3 games, scored with the toolkit's official calculator
#   3. find   Helix Probe v3 on the 80 FIND functions, arms FIND_ARMS, scored with FIND's official metric
#
#   cd /home/ubuntu/helix_probe && git pull && setsid nohup bash scripts/run_v3.sh > v3_job.log 2>&1 < /dev/null &
#
# Robust:
#   - one copy at a time (a lock); runs from a snapshot of itself, so a git pull mid-job changes nothing;
#   - waits (without spinning) until the find-v2 job's lock is free, printing a line every 10 minutes;
#   - everything a stage makes is pushed to GitHub (results/...) every PUSH_MIN minutes: every model call and its
#     reasoning, every model version, every experiment, trials, curves;
#   - started again after any stop it resumes: finished runs are skipped, unfinished ones continue from their last
#     step; a finished stage is skipped (results/<stage>/DONE);
#   - if the local runs/ folder is lost, the stage is first rebuilt from what was pushed (bench/restore.py), so the
#     job continues from GitHub alone;
#   - a stop signal (kill -TERM) lets every run finish its step and save, then pushes, then exits;
#   - no cron job, no timer, no watchdog.
#
# Settings: STAGES ["aia arc find"]  WAIT_FOR [runs/find/.find-v2.lock]  FIND_ARMS ["v3 v3-exam v3-random v3-no-theorist"]
#   FIND_STEPS [25]  AIA_EFFORT [none]  ARC_ARMS [v3]  ARC_BUDGET_X [3]  ARC_STEPS [400]  WORKERS [6]  ARC_WORKERS [13]
#   PUSH [1]  PUSH_MIN [30]  FAKE [0]  PYTHON [python3]
#
#   FAKE=1 PUSH=0 WAIT_FOR=/nonexistent bash scripts/run_v3.sh      # the whole job with a fake model (a test)
set -uo pipefail
cd "$(dirname "$0")/.." || exit 3
if [ -z "${V3_SNAPSHOT:-}" ]; then
  mkdir -p runs && cp "$0" "runs/.v3_job_snapshot.sh.$$" && mv -f "runs/.v3_job_snapshot.sh.$$" "runs/.v3_job_snapshot.sh" \
    && V3_SNAPSHOT=1 exec bash "runs/.v3_job_snapshot.sh" "$@"
fi
PY="${PYTHON:-$(command -v python3 || command -v python)}"
STAGES="${STAGES:-aia arc find}"
WAIT_FOR="${WAIT_FOR:-runs/find/.find-v2.lock}"
FIND_ARMS="${FIND_ARMS:-v3 v3-exam v3-random v3-no-theorist}"
FIND_STEPS="${FIND_STEPS:-25}"
AIA_EFFORT="${AIA_EFFORT:-none}"
ARC_ARMS="${ARC_ARMS:-v3}"
ARC_BUDGET_X="${ARC_BUDGET_X:-3}"
ARC_STEPS="${ARC_STEPS:-400}"
WORKERS="${WORKERS:-6}"
ARC_WORKERS="${ARC_WORKERS:-13}"
PUSH="${PUSH:-1}"
PUSH_MIN="${PUSH_MIN:-30}"
FAKE="${FAKE:-0}"
MAX_RETRIES="${MAX_RETRIES:-3}"
GIT_NAME="${GIT_NAME:-Shreyas Naik}"
GIT_EMAIL="${GIT_EMAIL:-119774329+cybercryptixcoder@users.noreply.github.com}"
TAG=""; [ "$FAKE" = "1" ] && TAG="-fake"
FAKE_FLAG=""; [ "$FAKE" = "1" ] && FAKE_FLAG="--fake"
NICE_CMD="nice -n 10"; command -v ionice >/dev/null && NICE_CMD="ionice -c 3 nice -n 10"
mkdir -p runs
exec 8> "runs/.v3-job$TAG.lock"
flock -n 8 || { echo "== the v3 job is already running (runs/.v3-job$TAG.lock is held); this copy exits and changes nothing"; exit 0; }

# where each stage lives: its working folder (runs/) and what is pushed (results/)
runs_of()    { case $1 in aia) echo "results/find/aia-$AIA_EFFORT$TAG";; find) echo "runs/find/find-v3$TAG";; arc) echo "runs/arc/arc-v3$TAG";; esac; }
results_of() { case $1 in aia) echo "results/find/aia-$AIA_EFFORT$TAG";; find) echo "results/find/find-v3$TAG";; arc) echo "results/arc/arc-v3$TAG";; esac; }
[ "$FAKE" = "1" ] && results_of() { echo "runs/fake-results/$1"; } && runs_of() { [ "$1" = aia ] && echo "runs/fake-results/aia" || echo "runs/fake/$1"; }

echo "== Helix Probe v3 job: stages $STAGES"
echo "   started $(date '+%Y-%m-%d %H:%M:%S %Z'); repo $(pwd) ($(git rev-parse --short HEAD 2>/dev/null))"

# ------------------------------------------------------------------ stop signals
CHILD=""; STOPPING=0
nap() { sleep "$1" & wait $! 2>/dev/null; }
on_stop() {
  [ "$STOPPING" = "1" ] && return
  STOPPING=1
  echo "== stop requested: every run finishes the step in progress, then everything is pushed"
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

# ------------------------------------------------------------------ publishing: only results/ is ever added
git_push() {   # path message
  [ "$PUSH" = "1" ] || return 0
  ( flock 9
    git add -f "$1" 2>/dev/null
    git -c user.name="$GIT_NAME" -c user.email="$GIT_EMAIL" -c commit.gpgsign=false commit -q -m "$2" || exit 0
    for i in 1 2 3 4; do git pull -q --rebase --autostash origin HEAD && git push -q origin HEAD && exit 0; sleep $((15 * i)); done
    echo "   (push failed: results stay on disk; the next push sends them)" >&2
  ) 9> "runs/.git.lock"
}
publish() {   # stage message
  local r; r="$(results_of "$1")"
  if [ "$1" != "aia" ]; then
    "$PY" bench/find/publish.py "$(runs_of "$1")" "$r" 2>&1 | tail -1 || echo "   (publishing failed; the runs are fine)"
  fi
  git_push "$r" "$2"
}
status() {   # stage
  local d; d="$(runs_of "$1")"
  case $1 in
    aia)  echo "   [$(date +%H:%M)] aia: $(ls "$d"/*/result.json 2>/dev/null | wc -l) of 80 functions done" ;;
    find) "$PY" bench/find/status.py "$d" 2>/dev/null | head -12 ;;
    arc)  echo "   [$(date +%H:%M)] arc: $(ls "$d"/*/*/summary.json 2>/dev/null | wc -l) games with a summary"; \
          "$PY" bench/arc/run.py --out "$d" --report 2>/dev/null | tail -n +4 ;;
  esac
}

# ------------------------------------------------------------------ 0. preflight (a few minutes)
echo "== preflight"
"$PY" -c "import sys, numpy, scipy; assert sys.version_info >= (3, 10); print('   python', sys.version.split()[0])" \
  || { echo "preflight: Python 3.10+ with numpy and scipy is needed" >&2; exit 3; }
if [[ " $STAGES " == *" arc "* ]]; then
  "$PY" -c "import sys, arc_agi, arcengine; assert sys.version_info >= (3, 12); print('   arc-agi toolkit ok')" \
    || { echo "preflight: the arc stage needs Python 3.12+ with the toolkit: pip install arc-agi (set PYTHON=/path/to/python3.12 if python3 is older)" >&2; exit 3; }
  [ "$FAKE" = "1" ] || grep -q '^ARC_API_KEY=' .env 2>/dev/null \
    || { echo "preflight: .env needs a line ARC_API_KEY=... for the arc stage" >&2; exit 3; }
fi
free_disk=$(df -Pm . | awk 'NR==2 {print $4}')
echo "   disk: ${free_disk} MB free"
[ "${free_disk:-0}" -ge 1500 ] || { echo "preflight: need 1500 MB of free disk" >&2; exit 3; }
PRE="$(mktemp -d)"
( "$PY" tests/test_v3.py \
  && "$PY" bench/find/run.py --out "$PRE/find" --data bench/find/data --arms v3 --limit 1 --steps 3 --workers 2 --fake \
  && "$PY" bench/find/publish.py "$PRE/find" "$PRE/res-find" && test -s "$PRE/res-find/report.md" \
  && rm -rf "$PRE/find" && "$PY" bench/restore.py "$PRE/res-find" "$PRE/find" \
  && "$PY" bench/find/run.py --out "$PRE/find" --data bench/find/data --arms v3 --limit 1 --steps 5 --workers 2 --fake \
  && { [[ " $STAGES " != *" arc "* ]] || { "$PY" bench/arc/run.py --out "$PRE/arc" --games ls20 --steps 3 --workers 1 --fake \
       && "$PY" bench/find/publish.py "$PRE/arc" "$PRE/res-arc" && test -s "$PRE/res-arc/report.md"; }; } \
) > "$PRE/pre.log" 2>&1 \
  || { echo "preflight: the crash test failed (offline checks; fake-model runs; publish; restore from published files; resume):" >&2; tail -25 "$PRE/pre.log" >&2; rm -rf "$PRE"; exit 3; }
echo "   crash test passed: v3 offline checks, fake-model FIND and ARC runs, publish, delete + restore from the published files, resume"
rm -rf "$PRE"
if [ "$FAKE" != "1" ]; then
  "$PY" - <<'PY' || { echo "preflight: the model can't be reached (.env needs PROBE_API_KEYS=key1,key2)" >&2; exit 3; }
from probe.llm import LLM
llm = LLM()
for i in range(len(llm.keys)):
    r = llm("You answer in one word.", "Say OK.", max_tokens=20)
    print(f"   model answers on key {r['key_index'] + 1} of {len(llm.keys)}:", r["text"].strip()[:20], f"({r['seconds']:.1f} s)")
PY
fi
if [ "$PUSH" = "1" ]; then
  git push --dry-run -q origin HEAD >/dev/null 2>&1 || { echo "preflight: can't push to GitHub" >&2; exit 3; }
  echo "   GitHub: can push"
fi

# ------------------------------------------------------------------ wait for the find-v2 job
if [ -e "$WAIT_FOR" ]; then
  exec 7< "$WAIT_FOR"
  until flock -w 600 -s 7; do
    [ "$STOPPING" = "1" ] && { echo "== stopped while waiting; nothing was started"; exit 0; }
    echo "   [$(date +%H:%M)] waiting for the job holding $WAIT_FOR to finish"
  done
  exec 7<&-
  echo "== $(date +%H:%M): $WAIT_FOR is free; starting"
fi

# ------------------------------------------------------------------ the stages
for stage in $STAGES; do
  [ "$STOPPING" = "1" ] && break
  R="$(results_of "$stage")"; D="$(runs_of "$stage")"; LOG="runs/v3-$stage$TAG.log"
  if [ -f "$R/DONE" ]; then echo "== stage $stage: already done ($R/DONE); skipped"; continue; fi
  mkdir -p "$R" "$D"
  if [ "$stage" != "aia" ] && [ -d "$R" ] && [ -z "$(ls "$D"/*/*/notebook.jsonl 2>/dev/null)" ] && [ -n "$(ls "$R"/*/*/notebook.jsonl 2>/dev/null)" ]; then
    echo "== stage $stage: no local runs but GitHub has some: rebuilding $D from $R"
    "$PY" bench/restore.py "$R" "$D"
  fi
  echo "== stage $stage: started $(date '+%H:%M'); log $LOG; pushed to $R"
  "$PY" - "$R/sessions.jsonl" "$stage" <<'PY' || true
import json, platform, subprocess, sys, time, os
f, stage = sys.argv[1:]
c = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
open(f, "a").write(json.dumps({"t": time.strftime("%Y-%m-%d %H:%M:%S %Z"), "stage": stage, "commit": c,
    "python": platform.python_version(), "cpus": os.cpu_count(), "env": {k: os.environ.get(k) for k in
    ("FIND_ARMS", "FIND_STEPS", "AIA_EFFORT", "ARC_ARMS", "ARC_BUDGET_X", "ARC_STEPS", "WORKERS", "ARC_WORKERS")}}) + "\n")
PY
  case $stage in
    aia)  CMD=("$PY" -u bench/find/aia.py --out "$D" --effort "$AIA_EFFORT" --workers "$WORKERS") ;;
    find) CMD=("$PY" -u bench/find/run.py --out "$D" --data bench/find/data --arms $FIND_ARMS --steps "$FIND_STEPS" --workers "$WORKERS") ;;
    arc)  CMD=("$PY" -u bench/arc/run.py --out "$D" --arms $ARC_ARMS --budget-x "$ARC_BUDGET_X" --steps "$ARC_STEPS" --workers "$ARC_WORKERS") ;;
  esac
  [ "$FAKE" = "1" ] && case $stage in
    aia)  echo "   (fake mode: the aia stage needs a real model; skipped)"; touch "$R/DONE"; continue ;;
    find) CMD+=(--fake --limit 1 --steps 3) ;;
    arc)  CMD=("$PY" -u bench/arc/run.py --out "$D" --games ls20 g50t --steps 3 --workers 2 --fake) ;;
  esac
  ( SL=""; trap 'kill ${SL:-} 2>/dev/null; exit 0' TERM INT HUP
    n=0
    while true; do sleep 600 & SL=$!; wait $SL; status "$stage"; n=$((n + 1))
      [ $((n * 10 % PUSH_MIN)) -eq 0 ] && publish "$stage" "Helix Probe v3 job, $stage: progress at $(date -u +%H:%M) UTC"
    done ) &
  TICKER=$!
  attempt=0
  while [ "$STOPPING" = "0" ]; do
    run_child "$LOG" $NICE_CMD "${CMD[@]}"
    rc=$?
    case "$rc" in
      0) touch "$R/DONE"; break ;;
      75) echo "== stage $stage: stopped cleanly"; break ;;
      *) attempt=$((attempt + 1))
         echo "== stage $stage: stopped on an error (exit $rc); last lines:"; tail -5 "$LOG" | sed 's/^/   /'
         [ "$STOPPING" = "1" ] && break
         [ "$attempt" -gt "$MAX_RETRIES" ] && { echo "== stage $stage: gave up after $MAX_RETRIES retries; run the script again to continue"; break; }
         echo "   retry $attempt of $MAX_RETRIES in 60 s (finished runs are kept; unfinished ones resume)"; nap 60 ;;
    esac
  done
  kill $TICKER 2>/dev/null; wait $TICKER 2>/dev/null
  status "$stage"
  publish "$stage" "Helix Probe v3 job, $stage: $( [ -f "$R/DONE" ] && echo finished || echo stopped )"
  [ -f "$R/DONE" ] || break
done

if [ "$STOPPING" = "1" ]; then
  echo "== stopped before the job finished; run this script again to continue it"
else
  ok=1; for s in $STAGES; do [ -f "$(results_of "$s")/DONE" ] || ok=0; done
  if [ "$ok" = "1" ]; then echo "== all jobs done (v3)"; else echo "== the v3 job ended with an unfinished stage; run it again to continue"; fi
fi
