import subprocess
print(subprocess.run(r'''cd /content/helix_probe/runs && tar czf /content/r5.tgz --exclude='*.pt' --exclude='*.safetensors' --exclude='grade_spec.json' edit/Qwen3.5-9B_addition_helix2_high_r5 edit_08b && ls -la /content/r5.tgz''', shell=True, capture_output=True, text=True, executable="/bin/bash", timeout=90).stdout)
