import json
d='/content/helix_probe/runs/discover/d1/'
for l in open(d+'notebook.jsonl'):
  e=json.loads(l)
  s=json.dumps(e)
  if '"E9"' in s or '"E14"' in s or e.get('id') in ('E9','E14'):
    print(json.dumps({k:(str(v)[-900:] if k in ('out','output','result') else str(v)[:300]) for k,v in e.items()})[:2200]); print('---')
