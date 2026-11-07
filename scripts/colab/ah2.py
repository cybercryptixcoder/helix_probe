import json,subprocess
print(subprocess.run("cd /content/helix_probe; grep -E '== Qwen3.5-9B_addition_helix2 r2' runs_follow.log | cut -c1-400", shell=True, capture_output=True, text=True).stdout)
d='/content/helix_probe/runs/edit/Qwen3.5-9B_addition_helix2_high_r2/'
import os
if not os.path.isdir(d):
  d=[os.path.join('/content/helix_probe/runs/edit',x) for x in os.listdir('/content/helix_probe/runs/edit') if 'addition_helix2' in x and 'r2' in x][0]+'/'
g=json.load(open(d+'grade.json')); print(g.get('scores'), g.get('changed_params'))
print(open(d+'answer.md').read()[:1500])
