import subprocess
print(subprocess.run("cd /content/helix_probe; grep 'addition_helix2_high r2' runs_follow.log | cut -c1-400", shell=True, capture_output=True, text=True).stdout)
