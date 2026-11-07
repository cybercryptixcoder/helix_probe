import subprocess
print(subprocess.run("cd /content/helix_probe; for f in runs_edit_job*.log; do echo \"## $f\"; tail -4 $f; done; for f in runs/edit_job/*.log; do echo \"## $f\"; grep -v 'transformers\\]\\|Loading' $f | tail -3; done; nvidia-smi --query-gpu=memory.used --format=csv,noheader", shell=True, capture_output=True, text=True, executable="/bin/bash").stdout[-2500:])
