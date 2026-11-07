import subprocess
print(subprocess.run("cd /content/helix_probe && git pull -q && git log --oneline -1", shell=True, capture_output=True, text=True).stdout)
