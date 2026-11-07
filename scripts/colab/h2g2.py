import subprocess
print(subprocess.run("cd /content/helix_probe/runs/edit; d=$(ls -dt *gender_helix2*r2* | head -1); echo $d; wc -l $d/notebook.jsonl; ls -la --time-style=+%H:%M $d | tail -5; date +%H:%M", shell=True, capture_output=True, text=True).stdout)
