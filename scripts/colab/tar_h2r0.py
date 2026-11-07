import subprocess
print(subprocess.run(r'''cd /content/helix_probe/runs && rm -f /content/h2r0.tgz && tar czf /content/h2r0.tgz --exclude='*.pt' --exclude='*.safetensors' --exclude='grade_spec.json' edit_08b/Qwen3.5-0.8B_addition_helix2_high_r0 edit_08b/report.md && ls -la /content/h2r0.tgz''', shell=True, capture_output=True, text=True, executable="/bin/bash", timeout=90).stdout)
