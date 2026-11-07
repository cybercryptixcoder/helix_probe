import subprocess
print(subprocess.run("cd /content/helix_probe; tail -15 runs_d1.log 2>/dev/null | cut -c1-300; ls runs/discover/d1; wc -l runs/discover/d1/map.jsonl 2>/dev/null; ps -eo etimes,args | grep -E 'discover' | grep -v grep | cut -c1-120", shell=True, capture_output=True, text=True).stdout)
