import json, glob, os, subprocess
print(subprocess.run("cd /content/helix_probe; tail -2 runs_follow.log 2>/dev/null; tail -1 runs_edit_job*.log", shell=True, capture_output=True, text=True).stdout[-600:])
for d in glob.glob("/content/helix_probe/runs/edit/*_r*/"):
    if os.path.exists(d+"result.json"): continue
    for fn in ("tool_calls.jsonl","notebook.jsonl"):
        if os.path.exists(d+fn): print(d.split("/")[-2], fn.split(".")[0], sum(1 for _ in open(d+fn)))
