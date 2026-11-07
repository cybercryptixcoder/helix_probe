import json
d="/content/helix_probe/runs/edit/Qwen3.5-9B_gender_helix2_high_r0/"
print(open(d+"answer.md").read()[:1600])
g=json.load(open(d+"grade.json"))
print([r for r in g["items"]["post_target_paraphrase"] if r[2]][:6]); print([r for r in g["items"]["post_target_paraphrase"] if not r[2]][:6])
