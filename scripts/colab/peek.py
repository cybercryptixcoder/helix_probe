import json
d="/content/helix_probe/runs/edit/Qwen3.5-9B_gender_mit_high_r0/"
print(open(d+"answer.md").read()[:1500])
g=json.load(open(d+"grade.json"))
print(g["items"]["target"][:5]); print(g["items"]["comeback"][:3])
