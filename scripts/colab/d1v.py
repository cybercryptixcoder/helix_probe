import json
d='/content/helix_probe/runs/discover/d1/'
for l in open(d+'map.jsonl'):
  e=json.loads(l)
  v=e.get('verdict') or e.get('verify') or {}
  print(e['id'], e['depth'], e['name'][:60], '|', json.dumps({k:v for k,v in e.items() if k not in('name','where','mechanism','predict','file','id','depth')})[:500])
try:
  o=json.load(open(d+'verify_out.json')); print('THR', json.dumps(o.get('thresholds', o.get('thr','?')))[:300])
except Exception as x: print(x)
