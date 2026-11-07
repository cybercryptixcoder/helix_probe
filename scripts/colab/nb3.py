import json, glob
for n in glob.glob("/content/helix_probe/runs/edit/*helix2*/notebook.jsonl"):
    rows=[json.loads(l) for l in open(n)]
    errs=sum(1 for e in rows if "Traceback" in e["out"])
    print(n.split("/")[-2], "exps", len(rows), "crashed", errs, "candidates", [e["id"] for e in rows if e.get("candidate")])
    for e in rows[-3:]: print(e["id"], e["match"], e["question"][:100])
import subprocess; print(subprocess.run("df -h /content | tail -1", shell=True, capture_output=True, text=True).stdout)
