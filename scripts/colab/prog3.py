import subprocess, json, glob, os
print(subprocess.run(r'''cd /content/helix_probe; tail -2 runs_edit_job*.log | cut -c1-300''', shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
for f in sorted(glob.glob("/content/helix_probe/runs/edit/*/result.json")):
    r = json.load(open(f))
    if r["arm"] in ("unedited",): continue
    print(f.split("/")[-2], "clean" if r["clean"] else "removed" if r["removed"] else "no", "target", r["scores"]["target"], "comeback", r["comeback"], "ppl", r["ppl"], {k: v for k, v in r["scores"].items() if k != "target"})
for d in glob.glob("/content/helix_probe/runs/edit/*_r*/"):
    f = d + "tool_calls.jsonl"
    if os.path.exists(f):
        rows = [json.loads(l) for l in open(f)]
        print(d.split("/")[-2], "runs", len(rows), "| last out:", rows[-1]["out"][-300:].replace("\n", " | "))
    n = d + "notebook.jsonl"
    if os.path.exists(n):
        rows = [json.loads(l) for l in open(n)]
        print(d.split("/")[-2], "exps", len(rows), [(e["id"], e["match"], e["question"][:70]) for e in rows[-2:]])
