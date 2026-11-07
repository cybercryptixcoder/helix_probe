import subprocess
print(subprocess.run("timeout 20 grep -E '^== |^   [0-9:]+ == ' /content/helix_probe/runs_g1add.log | cut -c1-420", shell=True, capture_output=True, text=True, timeout=60).stdout)
