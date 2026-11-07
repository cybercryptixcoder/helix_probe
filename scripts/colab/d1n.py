import json
d='/content/helix_probe/runs/discover/d1/'
n=json.load(open(d+'noise.json'))
print(type(n), list(n)[:10] if isinstance(n,dict) else len(n))
if isinstance(n,dict):
  for k,v in n.items():
    s=json.dumps(v); print(k, s[:600])
for l in open(d+'map.jsonl'):
  e=json.loads(l); print({k:(str(v)[:200]) for k,v in e.items()})
