import subprocess, json, glob, os
print(subprocess.run(r'''ps -eo pid,etimes,args | grep -E "edit_[j]ob|edit[.]py|edit_[w]orker|edit_[g]rade" | cut -c1-100; cd /content/helix_probe; tail -3 runs_edit_job*.log''', shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
for d in glob.glob("/content/helix_probe/runs/edit/*_r*/"):
    f = d + "tool_calls.jsonl"
    if os.path.exists(f):
        rows = [json.loads(l) for l in open(f)]
        print(d.split("/")[-2], "runs", len(rows))
        for r in rows[-2:]:
            print("CODE:", r["code"][:500].replace("\n", " | ")); print("OUT:", r["out"][-500:].replace("\n", " | "))
    n = d + "notebook.jsonl"
    if os.path.exists(n):
        rows = [json.loads(l) for l in open(n)]
        print(d.split("/")[-2], "exps", len(rows), [(e["id"], e["match"], e["question"][:80]) for e in rows[-3:]])
