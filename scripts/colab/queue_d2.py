import subprocess
cmd = r'''cat > /content/d2.sh <<'SH'
#!/bin/bash
cd /content/helix_probe
git pull -q; echo "== D2: $(date) $(git log --oneline -1)"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
python3 -u bench/weights/discover.py --model Qwen/Qwen3.5-9B --out runs/discover/d2 --max-runs 40
echo "== D2 done: $(date)"
SH
chmod +x /content/d2.sh; cd /content/helix_probe; setsid nohup bash /content/d2.sh >> /content/helix_probe/runs_d2.log 2>&1 < /dev/null & sleep 1; echo queued'''
print(subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
