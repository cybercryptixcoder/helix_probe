import subprocess
exec(open("/tmp/clean.py").read()) if False else None
cmd = r'''cd /content/helix_probe; export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True; MODEL=Qwen/Qwen3.5-9B OUT=runs/edit setsid nohup bash scripts/edit_job.sh "s1-base|--ability gender,addition --arm unedited" "s1-scripted|--ability gender,addition --arm scripted" "s1-random|--ability gender,addition --arm random --reps 3" >> runs_edit_job.log 2>&1 < /dev/null & sleep 1; echo launched'''
print(subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
