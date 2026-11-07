#!/bin/bash
# Runs capability-removal stages in order (docs/PLAN.md). Each argument is one stage: "label|edit.py arguments".
#   MODEL=Qwen/Qwen3.5-9B OUT=runs/edit setsid nohup bash scripts/edit_job.sh "base|--ability gender,addition --arm unedited" ... &
# Resumable: finished runs are skipped (result.json), finished stages are marked runs/edit_job/<label>.DONE.
# Logs: runs/edit_job/<label>.log (one per stage) and the overall progress on stdout.
cd "$(dirname "$0")/.." || exit 3
MODEL="${MODEL:-Qwen/Qwen3.5-0.8B}"; OUT="${OUT:-runs/edit}"; PY="${PYTHON:-python3}"
PUSH="${PUSH:-0}"; RESULTS="${RESULTS:-results/edit_$(basename "$MODEL" | tr 'A-Z.' 'a-z_')}"   # PUSH=1: copy results to $RESULTS and push

publish() {
  [ "$PUSH" = "1" ] || return 0
  mkdir -p "$RESULTS"
  ( cd "$OUT" && find . -type f \( -name result.json -o -name grade.json -o -name answer.md -o -name notebook.jsonl -o -name findings.md \
      -o -name tool_calls.jsonl -o -name scripted_log.txt -o -name calls.jsonl -o -name report.md \) ) | while read -r f; do
    mkdir -p "$RESULTS/$(dirname "$f")"
    case "$f" in *calls.jsonl) gzip -n -c "$OUT/$f" > "$RESULTS/$f.gz" ;; *) cp "$OUT/$f" "$RESULTS/$f" ;; esac
  done
  ( flock 9
    { [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; } && git rebase --abort 2>/dev/null
    git add -f "$RESULTS"
    git -c user.name="${GIT_NAME:-Shreyas Naik}" -c user.email="${GIT_EMAIL:-119774329+cybercryptixcoder@users.noreply.github.com}" -c commit.gpgsign=false commit -q -m "edit job: $1" || exit 0
    for i in 1 2 3; do git pull -q --rebase --autostash origin main && git push -q origin HEAD:main && exit 0; git rebase --abort 2>/dev/null; sleep 20; done
    echo "   (push failed; the next one sends it)" ) 9> runs/.git.lock
}
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
  "$PY" bench/weights/edit.py --report "$OUT" > /dev/null 2>&1; publish "$label"
done
"$PY" bench/weights/edit.py --report "$OUT" | sed 's/^/   /'
echo "== all stages done $(date '+%F %T')"
