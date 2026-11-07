import subprocess
print(subprocess.run("timeout 20 grep -E '^== |^   [0-9:]+ == ' /content/helix_probe/runs_g1add.log | tail -2 | cut -c1-400; timeout 20 grep -E ' E[0-9]+ match| == ' /content/helix_probe/runs/edit_job/s08-helix2.log | tail -3 | cut -c1-200", shell=True, capture_output=True, text=True, timeout=60).stdout)
