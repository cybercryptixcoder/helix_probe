import subprocess
print(subprocess.run("cd /content/helix_probe; tail -4 runs_follow.log; ps -eo pid,etimes,args | grep -E 'edit_[j]ob|edit[.]py|follow[.]sh|discover' | cut -c1-120", shell=True, capture_output=True, text=True).stdout)
