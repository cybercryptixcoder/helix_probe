import subprocess
print(subprocess.run("timeout 20 grep -E ' == ' /content/helix_probe/runs/edit_job/s08-helix2.log | cut -c1-430", shell=True, capture_output=True, text=True, timeout=60).stdout)
