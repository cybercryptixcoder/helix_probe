#!/bin/bash
# Runs capability-removal stages in order (docs/PLAN.md). Each argument is one stage: "label|edit.py arguments".
#   MODEL=Qwen/Qwen3.5-9B OUT=runs/edit setsid nohup bash scripts/edit_job.sh "base|--ability gender,addition --arm unedited" ... &
# Resumable: finished runs are skipped (result.json), finished stages are marked runs/edit_job/<label>.DONE.
# Logs: runs/edit_job/<label>.log (one per stage) and the overall progress on stdout.
cd "$(dirname "$0")/.." || exit 3
MODEL="${MODEL:-Qwen/Qwen3.5-0.8B}"; OUT="${OUT:-runs/edit}"; PY="${PYTHON:-python3}"
mkdir -p runs/edit_job "$OUT"
echo "== edit job: $(date '+%F %T %Z'), commit $(git rev-parse --short HEAD), model $MODEL"
for st in "$@"; do
  label="${st%%|*}"; args="${st#*|}"
  [ -f "runs/edit_job/$label.DONE" ] && { echo "== $label: already done"; continue; }
  echo "== $label: started $(date +%H:%M) ($args)"
  if "$PY" -u bench/weights/edit.py --model "$MODEL" --out "$OUT" $args >> "runs/edit_job/$label.log" 2>&1; then
    touch "runs/edit_job/$label.DONE"; echo "== $label: finished $(date +%H:%M)"
  else
    echo "== $label: FAILED $(date +%H:%M); see runs/edit_job/$label.log"; tail -5 "runs/edit_job/$label.log"
  fi
  grep "^[0-9:]* == " "runs/edit_job/$label.log" | tail -5 | sed 's/^/   /'
done
"$PY" bench/weights/edit.py --report "$OUT" | sed 's/^/   /'
echo "== all stages done $(date '+%F %T')"
