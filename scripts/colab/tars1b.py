import subprocess
print(subprocess.run(r'''cd /content/helix_probe/runs && tar czf /content/res_s1b.tgz --exclude='*.pt' --exclude='*.safetensors' --exclude='grade_spec.json' --exclude='.wsp' edit_s1b; ls -la /content/res_s1b.tgz''', shell=True, capture_output=True, text=True, executable="/bin/bash"))
