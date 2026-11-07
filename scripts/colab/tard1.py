import subprocess
print(subprocess.run(r'''cd /content/helix_probe/runs/discover && tar czf /content/res_d1.tgz --exclude='*.pt' d1; ls -la /content/res_d1.tgz''', shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
