import subprocess
cmd = r'''cat > /content/d1.sh <<'SH'
#!/bin/bash
cd /content/helix_probe
while pgrep -f "follow[.]sh" > /dev/null; do sleep 60; done
git pull -q; echo "== D1: $(date) $(git log --oneline -1)"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
python3 -u bench/weights/discover.py --model Qwen/Qwen3.5-9B --out runs/discover/d1 --max-runs 40
echo "== D1 done: $(date)"
SH
chmod +x /content/d1.sh; cd /content/helix_probe; setsid nohup bash /content/d1.sh >> /content/helix_probe/runs_d1.log 2>&1 < /dev/null & sleep 1; echo queued'''
print(subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
