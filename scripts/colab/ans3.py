import json
d="/content/helix_probe/runs/edit/Qwen3.5-9B_addition_helix2_high_r0/"
print(open(d+"answer.md").read()[:2500])
g=json.load(open(d+"grade.json"))
print(g["items"]["post_target_paraphrase"][:6]); print([r for r in g["items"]["subtraction"] if not r[2]])
