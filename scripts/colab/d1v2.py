import json
d='/content/helix_probe/runs/discover/d1/'
for l in open(d+'map.jsonl'):
  e=json.loads(l)
  print(e['id'], {k:v for k,v in e.items() if k not in('name','where','mechanism','file','id','depth','held_delta')})
