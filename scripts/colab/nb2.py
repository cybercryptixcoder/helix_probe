import json
d="/content/helix_probe/runs/edit/Qwen3.5-9B_gender_helix_high_r0/"
rows=[json.loads(l) for l in open(d+"notebook.jsonl")]
for e in rows:
    o=e["out"]; tail=o[-160:].replace("\n"," ")
    print(e["id"], e["match"], e["question"][:110], "||", tail)
print("FINDINGS:", open(d+"findings.md").read()[:2500])
print("ANSWER:", open(d+"answer.md").read()[:800])
