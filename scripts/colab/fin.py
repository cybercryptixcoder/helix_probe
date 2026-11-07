import subprocess
print(subprocess.run("cd /content/helix_probe; grep -E '== (a-helix-r2|regrade)|addition_helix_high r2' runs_follow.log | cut -c1-400; ls -la --time-style=+%H:%M runs/edit/report.md", shell=True, capture_output=True, text=True).stdout)
