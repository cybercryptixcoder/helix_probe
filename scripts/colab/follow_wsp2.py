import subprocess
cmd = r'''cd /content/helix_probe; cat > /content/follow.sh <<'SH'
#!/bin/bash
cd /content/helix_probe
while pgrep -f "edit_[j]ob.sh" > /dev/null; do sleep 60; done
git pull -q; echo "== follow-up: $(date) $(git log --oneline -1)"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
MODEL=Qwen/Qwen3.5-9B OUT=runs/edit bash scripts/edit_job.sh "h2g-r0|--ability gender --arm helix2" "h2a-r0|--ability addition --arm helix2" "regrade|--regrade"
MODEL=Qwen/Qwen3.5-9B OUT=runs/edit_s1b bash scripts/edit_job.sh "s1b-scripted|--ability gender,addition --arm scripted" "s1b-random|--ability gender,addition --arm random --reps 3"
SH
chmod +x /content/follow.sh
setsid nohup bash /content/follow.sh >> /content/helix_probe/runs_follow.log 2>&1 < /dev/null & sleep 1; echo queued'''
print(subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
