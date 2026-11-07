import subprocess
print(subprocess.run(r'''cd /content/helix_probe/runs && tar czf /content/res_wsp.tgz --exclude='*.pt' --exclude='*.safetensors' --exclude='grade_spec.json' edit edit_discarded_hooks edit_job 2>&1; ls -la /content/res_wsp.tgz''', shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
