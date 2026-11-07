import subprocess
cmd = r'''cat > /content/g1add.sh <<'SH'
#!/bin/bash
cd /content/helix_probe
git pull -q; echo "== Goal 1 additions: $(date) $(git log --oneline -1)"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
MODEL=Qwen/Qwen3.5-9B OUT=runs/edit bash scripts/edit_job.sh "h2a-r3to5|--ability addition --arm helix2 --rep-start 3 --reps 3"
MODEL=Qwen/Qwen3.5-0.8B OUT=runs/edit_08b bash scripts/edit_job.sh \
  "s08-base|--ability addition --arm unedited" \
  "s08-random|--ability addition --arm random --reps 3" \
  "s08-scripted|--ability addition --arm scripted" \
  "s08-mit|--ability addition --arm mit --reps 3" \
  "s08-helix|--ability addition --arm helix --reps 3" \
  "s08-helix2|--ability addition --arm helix2 --reps 3"
echo "== Goal 1 additions done: $(date)"
SH
chmod +x /content/g1add.sh; cd /content/helix_probe; setsid nohup bash /content/g1add.sh >> /content/helix_probe/runs_g1add.log 2>&1 < /dev/null & sleep 1; echo queued'''
print(subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
