#!/usr/bin/env bash
# Weight-space job (docs/handoff/10_INTERPRETABILITY_TRACK.md): DeepSeek V4.1 Flash on the setups of MIT CSAIL's
# "Sparks of Weight-Space Programming" (their networks, prompts and answer keys), in every format, with shuffled-weight
# controls, thinking on by default (one thinking-off arm), MIT's own protocol and Helix Probe's structure.
#
#   cd /home/ubuntu/helix_probe && git pull && setsid nohup bash scripts/run_weights.sh > weights_job.log 2>&1 < /dev/null &
#
# Each stage is one condition: bench/weights/wsp.py --task T --format F --protocol P --effort E [--shuffle], 3 runs per
# network, results pushed to results/weights/<stage>/ (every call with its reasoning, every code run and output, every
# answer, grade and audit). A restart continues: finished runs are skipped. A stop signal finishes the runs in progress.
# Settings: STAGES [all, in order]  REPS [3]  WORKERS [2]  HELIX_RUNS [40]  BUDGET [50]  PUSH [1]  PYTHON [python3]
set -uo pipefail
cd "$(dirname "$0")/.." || exit 3
if [ -z "${WSP_SNAPSHOT:-}" ]; then
  mkdir -p runs && cp "$0" runs/.weights_job_snapshot.sh && WSP_SNAPSHOT=1 exec bash runs/.weights_job_snapshot.sh "$@"
fi
PY="${PYTHON:-$(command -v python3)}"; REPS="${REPS:-3}"; WORKERS="${WORKERS:-2}"; HELIX_RUNS="${HELIX_RUNS:-40}"
BUDGET="${BUDGET:-50}"; PUSH="${PUSH:-1}"
GIT_NAME="${GIT_NAME:-Shreyas Naik}"; GIT_EMAIL="${GIT_EMAIL:-119774329+cybercryptixcoder@users.noreply.github.com}"
exec 8> runs/.weights-job.lock; flock -n 8 || { echo "== the weights job is already running; this copy exits"; exit 0; }

# name | arguments. Order: the exact text replications (cheap anchors), then the complete setup (weights as text +
# code + edits + forward passes, Helix structure, thinking on) and its controls, then the arms that separate reading
# from running, then the thinking-off arm, then MIT's exact experiment 3. Expect several days in all; each stage pushes.
read -r -d '' ALL <<'EOF'
exp1-text-high|--task exp1 --format text --effort high
exp1-text-high-shuf|--task exp1 --format text --effort high --shuffle
exp1-text-none|--task exp1 --format text --effort none
exp1-text-none-shuf|--task exp1 --format text --effort none --shuffle
exp2-text-high|--task exp2 --format text --effort high
exp2-text-high-shuf|--task exp2 --format text --effort high --shuffle
exp1-full-helix-high|--task exp1 --format full --protocol helix --effort high
exp1-full-mit-high|--task exp1 --format full --protocol mit --effort high
exp1-full-helix-high-shuf|--task exp1 --format full --protocol helix --effort high --shuffle
exp1-code-mit-high|--task exp1 --format code --protocol mit --effort high
exp1-code-helix-high|--task exp1 --format code --protocol helix --effort high
exp1-blind-mit-high|--task exp1 --format blind --protocol mit --effort high
exp1-blind-helix-high|--task exp1 --format blind --protocol helix --effort high
exp1-run-mit-high|--task exp1 --format run --protocol mit --effort high
exp1-code-mit-high-shuf|--task exp1 --format code --protocol mit --effort high --shuffle
exp1-full-helix-none|--task exp1 --format full --protocol helix --effort none
exp3-code-mit-high|--task exp3 --format code --protocol mit --effort high
exp3-code-mit-high-shuf|--task exp3 --format code --protocol mit --effort high --shuffle
exp3-code-helix-high|--task exp3 --format code --protocol helix --effort high
EOF
STAGES="${STAGES:-$(echo "$ALL" | cut -d'|' -f1 | tr '\n' ' ')}"

STOP=0; CHILD=""
trap 'STOP=1; [ -n "$CHILD" ] && kill -TERM "$CHILD" 2>/dev/null; echo "== stop requested"' TERM INT HUP
publish() {   # stage
  local src="runs/weights/$1" dst="results/weights/$1"
  mkdir -p "$dst"
  ( cd "$src" && find . -type f ! -name orig.npz ! -name '*.tmp' ) | while read -r f; do
    mkdir -p "$dst/$(dirname "$f")"
    case "$f" in *calls.jsonl) gzip -n -c "$src/$f" > "$dst/$f.gz" ;; *) cp "$src/$f" "$dst/$f" ;; esac
  done
  "$PY" bench/weights/wsp.py --report results/weights > /dev/null 2>&1
  [ "$PUSH" = "1" ] || return 0
  ( flock 9; git add -f results/weights
    git -c user.name="$GIT_NAME" -c user.email="$GIT_EMAIL" -c commit.gpgsign=false commit -q -m "weights job: $1 ($2)" || exit 0
    for i in 1 2 3; do git pull -q --rebase --autostash origin HEAD && git push -q origin HEAD && exit 0; sleep 20; done
    echo "   (push failed; the next one sends it)" ) 9> runs/.git.lock
}

echo "== weights job: $(date '+%F %T %Z'), commit $(git rev-parse --short HEAD)"
echo "== preflight"
"$PY" -c "import numpy, scipy, sklearn; print('   python ok')" || { echo "preflight: needs numpy, scipy, scikit-learn" >&2; exit 3; }
bash bench/weights/fetch_mit.sh || { echo "preflight: could not fetch the MIT logs" >&2; exit 3; }
"$PY" -c "import sys; sys.path.insert(0,'.'); from bench.weights.wsp import bwrap_status as b; ok,why=b(); print('   sandbox:', why + ('' if ok else '; runs record isolated=false'))" \
  || { echo "preflight: can't load bench/weights/wsp.py" >&2; exit 3; }
"$PY" - <<'PY' || { echo "preflight: the sandbox self-test failed" >&2; exit 3; }
import sys, tempfile; sys.path.insert(0, ".")
from bench.weights.wsp import Exp1, Exp3, Sandbox, MIT
t = Exp1(); nid = t.items()[0][0]
sb = Sandbox(tempfile.mkdtemp(), t.weights(nid), t, "run", 2)
def check(out, want, what):
    if want not in out:
        print(f"   {what}: expected {want!r}; the sandbox printed:\n" + out[-3000:], file=sys.stderr); sys.exit(1)
check(sb.run("print(W['W1'].shape)"), "(500, 32)", "loading the weights")
check(sb.run("forward(np.zeros((1,500))); forward(np.zeros((1,500))); forward(np.zeros((1,500)))"), "no forward passes left", "the pass budget")
b = Sandbox(tempfile.mkdtemp(), t.weights(nid), t, "blind", 2); check(b.run("print('W' in dir())"), "False", "blind mode")
check(sb.run(f"open({str(MIT / 'exp1_which_game/runs/pong/answer.md')!r}).read()"), "blocked by the sandbox", "the guard on MIT's answers")
check(sb.run("import os; os.listdir('../..')"), "blocked by the sandbox", "the guard on other runs")
check(sb.run("import urllib.request; urllib.request.urlopen('https://github.com')"), "blocked by the sandbox", "the guard on the network")
from bench.weights.wsp import MIT
assert all(t.grade(open(MIT / f"exp1_which_game/runs/{g}/answer.md").read(), g)["correct"] for g in ("breakout", "pong", "pacman", "freeway"))
e3 = Exp3(); assert e3.grade(open(MIT / "exp3_language/runs/python_r0/final_answer.md").read(), "python")["copy_tp"] == 3
print("   sandbox, budget, blind mode, the file and network guard, and the graders (on MIT's own answers) ok")
PY
"$PY" -c "
from probe.llm import LLM; l=LLM()
for i in range(len(l.keys)): r=l('Answer in one word.','Say OK.',max_tokens=20); print('   model answers on key',r['key_index']+1,'of',len(l.keys),':',r['text'].strip()[:10])" \
  || { echo "preflight: the model can't be reached" >&2; exit 3; }
[ "$PUSH" = "1" ] && { git push --dry-run -q origin HEAD >/dev/null 2>&1 && echo "   GitHub: can push" || { echo "preflight: can't push" >&2; exit 3; }; }

for st in $STAGES; do
  [ "$STOP" = "1" ] && break
  args="$(echo "$ALL" | grep "^$st|" | cut -d'|' -f2)"; [ -n "$args" ] || { echo "   unknown stage $st"; continue; }
  [ -f "results/weights/$st/DONE" ] && { echo "== $st: done; skipped"; continue; }
  echo "== $st: started $(date +%H:%M) ($args)"
  extra="--reps $REPS --workers $WORKERS --budget $BUDGET"; [[ "$args" == *helix* ]] && extra="$extra --max-runs $HELIX_RUNS"
  ( SL=""; trap 'kill $SL 2>/dev/null; exit 0' TERM
    while true; do sleep 1800 & SL=$!; wait $SL; publish "$st" "progress"; done ) & TICK=$!
  "$PY" -u bench/weights/wsp.py $args $extra --out "runs/weights/$st" >> "runs/weights_$st.log" 2>&1 & CHILD=$!
  wait $CHILD; rc=$?; CHILD=""; kill $TICK 2>/dev/null
  tail -1 "runs/weights_$st.log" | sed 's/^/   /'
  [ "$rc" = "0" ] && [ "$STOP" = "0" ] && touch "runs/weights/$st/DONE"
  publish "$st" "$( [ -f "runs/weights/$st/DONE" ] && echo finished || echo stopped )"
done
"$PY" bench/weights/wsp.py --report results/weights | sed 's/^/   /'
[ "$STOP" = "1" ] && echo "== stopped; run the same command again to continue" || echo "== all jobs done (weights)"
