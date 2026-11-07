import subprocess, shutil, pathlib, time
print(subprocess.run(r'''pkill -f "edit_[j]ob.sh"; pkill -f "bench/weights/edit[.]py"; pkill -f "edit_[w]orker"; pkill -f "edit_[g]rade"; sleep 5; cd /content/helix_probe && git pull -q && git log --oneline -1''', shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
R = pathlib.Path("/content/helix_probe")
arch = R / "runs/edit_discarded_hooks"; arch.mkdir(parents=True, exist_ok=True)
for d in (R / "runs/edit").glob("*_r*"):
    if "_mit_" in d.name or "_helix_" in d.name:
        shutil.move(str(d), str(arch / d.name))
for f in (R / "runs/edit_job").glob("*.DONE"):
    if f.name.startswith(("g-", "a-")): f.unlink()
shutil.rmtree(R / "runs/.wsp", ignore_errors=True)
print(sorted(p.name for p in (R / "runs/edit").iterdir()), sorted(p.name for p in arch.iterdir()))
