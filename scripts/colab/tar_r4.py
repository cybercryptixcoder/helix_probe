import subprocess
print(subprocess.run(r'''cd /content/helix_probe/runs/edit && tar czf /content/r4.tgz --exclude='*.pt' --exclude='*.safetensors' --exclude='grade_spec.json' Qwen3.5-9B_addition_helix2_high_r4 && ls -la /content/r3.tgz''', shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
