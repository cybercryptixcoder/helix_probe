import subprocess, json, glob, os
print(subprocess.run(r'''cd /content/helix_probe; tail -4 runs_edit_job*.log | cut -c1-400; for f in runs/edit/*scripted*/scripted_log.txt; do echo "## $f"; tail -6 $f; done''', shell=True, capture_output=True, text=True, executable="/bin/bash").stdout[-3000:])
for f in glob.glob("/content/helix_probe/runs/edit/*/result.json"):
    r = json.load(open(f)); print(f.split("/")[-2], {k: r[k] for k in ("clean","removed","precise","durable","comeback","ppl","base_ppl","changed_params")}, r["scores"])
for d in glob.glob("/content/helix_probe/runs/edit/*_r*/"):
    f = d + "tool_calls.jsonl"
    if os.path.exists(f):
        rows = [json.loads(l) for l in open(f)]
        print(d.split("/")[-2], "runs", len(rows))
        for r in rows[-2:]:
            print("CODE:", r["code"][:400].replace("\n", " | ")); print("OUT:", r["out"][-400:].replace("\n", " | "))
