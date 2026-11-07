import json, glob
for n in glob.glob("/content/helix_probe/runs/edit/*helix*/notebook.jsonl"):
    rows = [json.loads(l) for l in open(n)]
    print(n.split("/")[-2], "exps", len(rows))
    for e in rows[-4:]:
        print(e["id"], e["match"], "Q:", e["question"][:120], "| EXPECT:", e["expect"][:160].replace("\n"," "), "| OUT:", e["out"][-200:].replace("\n"," "))
for f in glob.glob("/content/helix_probe/runs/edit/*helix*/findings.md"):
    print("FINDINGS:", open(f).read()[:1200])
