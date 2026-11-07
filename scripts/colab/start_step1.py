import subprocess
cmd = r'''cd /content/helix_probe && git pull -q && git log --oneline -1 && MODEL=Qwen/Qwen3.5-9B OUT=runs/edit setsid nohup bash scripts/edit_job.sh "s1-base|--ability gender,addition --arm unedited" "s1-scripted|--ability gender,addition --arm scripted" "s1-random|--ability gender,addition --arm random --reps 3" > runs_edit_job.log 2>&1 < /dev/null &
sleep 3; cat runs_edit_job.log; (while true; do date +%T >> /content/alive.txt; sleep 60; done) > /dev/null 2>&1 < /dev/null & disown; echo started'''
print(subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
