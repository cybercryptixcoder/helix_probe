import subprocess
print(subprocess.run("timeout 20 tail -3 /content/helix_probe/runs_g1add.log; timeout 10 free -g | head -2; timeout 10 uptime; timeout 20 tail -c 600 /content/helix_probe/runs/edit_job/h2a-r3to5.log", shell=True, capture_output=True, text=True, timeout=80).stdout)
