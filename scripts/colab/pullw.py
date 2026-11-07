import subprocess
print(subprocess.run("cd /content/helix_probe && git pull -q && git log --oneline -1 && ls -la .env | cut -c1-40 && pip list 2>/dev/null | grep -iE '^(transformers|flash-linear)' ", shell=True, capture_output=True, text=True).stdout)
