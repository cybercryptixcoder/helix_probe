import subprocess
print(subprocess.run(r'''cd /content/helix_probe/runs/discover && tar czf /content/res_d2.tgz --exclude='*.pt' d2; ls -la /content/res_d2.tgz''', shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
