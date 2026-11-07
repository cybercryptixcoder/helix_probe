import subprocess, sys, shutil, pathlib
job = sys.argv[1] if len(sys.argv) > 1 else ""
R = pathlib.Path("/content/helix_probe")
subprocess.run("cd /content/helix_probe && git pull -q", shell=True)
shutil.rmtree(R / "runs/.wsp", ignore_errors=True)                       # stale worker folders (edits from killed runs)
for d in (R / "runs/edit").glob("*_r*"):
    if d.is_dir() and not (d / "result.json").exists():
        shutil.rmtree(d)
print(subprocess.run("cd /content/helix_probe; git log --oneline -1; ls runs/edit", shell=True, capture_output=True, text=True).stdout)
