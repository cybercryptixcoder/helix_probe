import subprocess
print(subprocess.run("cd /content/helix_probe/runs; for d in edit edit_s1b edit_discarded_hooks; do echo == $d; ls $d 2>/dev/null | grep -v random; done", shell=True, capture_output=True, text=True).stdout)
