import glob, os, subprocess, time
active = set()
for line in subprocess.run("ps -eo args", shell=True, capture_output=True, text=True).stdout.splitlines():
    if "edit_worker.py" in line:
        active.add(line.split("edit_worker.py")[1].split()[0])
for f in glob.glob("/content/helix_probe/runs/.wsp/*/orig.safetensors"):
    d = os.path.dirname(f)
    if d not in active and os.path.realpath(d) not in active:
        os.remove(f); print("removed", f)
print("active", active); print(subprocess.run("df -h /content | tail -1", shell=True, capture_output=True, text=True).stdout)
