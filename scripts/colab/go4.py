import subprocess
cmd = r'''cd /content/helix_probe; export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True; MODEL=Qwen/Qwen3.5-9B OUT=runs/edit setsid nohup bash scripts/edit_job.sh "g-mit-r0|--ability gender --arm mit" "g-helix-r0|--ability gender --arm helix" "a-mit-r0|--ability addition --arm mit" "a-helix-r0|--ability addition --arm helix" >> runs_edit_job2.log 2>&1 < /dev/null & sleep 2; echo launched'''
print(subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
