import subprocess
print(subprocess.run("cd /content/helix_probe && git pull 2>&1 | tail -3; git log --oneline -1; git status --short | head", shell=True, capture_output=True, text=True).stdout)
