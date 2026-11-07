import subprocess
print(subprocess.run("cd /content/helix_probe; grep -h ' random ' runs/edit_s1b/report.md | head; grep -h '== .*random' runs_follow.log | cut -c1-260", shell=True, capture_output=True, text=True).stdout)
