import json, glob, subprocess
print(subprocess.run("cd /content/helix_probe; tail -2 runs_edit_job*.log | cut -c1-200", shell=True, capture_output=True, text=True).stdout)
for f in sorted(glob.glob("/content/helix_probe/runs/edit/*/result.json")):
    r = json.load(open(f))
    if r["arm"] in ("mit", "helix"):
        print(f.split("/")[-2], "CLEAN" if r["clean"] else "removed" if r["removed"] else "no", "target", r["scores"]["target"], "comeback", round(r["comeback"],2), "ppl", r["ppl"], "post", r.get("post"), "changed", r["changed_params"], {k: v for k, v in r["scores"].items() if k != "target"})
import os
for d in glob.glob("/content/helix_probe/runs/edit/*_r*/"):
    for fn, key in (("tool_calls.jsonl", "runs"), ("notebook.jsonl", "exps")):
        if os.path.exists(d + fn) and not os.path.exists(d + "result.json"):
            print(d.split("/")[-2], key, sum(1 for _ in open(d + fn)))
