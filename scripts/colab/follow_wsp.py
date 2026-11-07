import subprocess
cmd = r'''cd /content/helix_probe; cat > /content/follow.sh <<'SH'
#!/bin/bash
cd /content/helix_probe
while pgrep -f "edit_[j]ob.sh" > /dev/null; do sleep 60; done
git pull -q; echo "== follow-up: $(date) $(git log --oneline -1)"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
MODEL=Qwen/Qwen3.5-9B OUT=runs/edit bash scripts/edit_job.sh "$@"
SH
chmod +x /content/follow.sh
setsid nohup bash /content/follow.sh "h2g-r1|--ability gender --arm helix2 --rep-start 1" "h2a-r1|--ability addition --arm helix2 --rep-start 1" "g-mit-r2|--ability gender --arm mit --rep-start 2" "a-mit-r2|--ability addition --arm mit --rep-start 2" "h2g-r2|--ability gender --arm helix2 --rep-start 2" "h2a-r2|--ability addition --arm helix2 --rep-start 2" "g-helix-r2|--ability gender --arm helix --rep-start 2" "a-helix-r2|--ability addition --arm helix --rep-start 2" "regrade|--regrade" >> /content/helix_probe/runs_follow.log 2>&1 < /dev/null & sleep 1; echo queued'''
print(subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
