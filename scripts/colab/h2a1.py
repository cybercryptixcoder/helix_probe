import subprocess
print(subprocess.run(r'''cd /content/helix_probe/runs/edit; d=$(ls -dt *addition_helix2*r1* | head -1); echo $d; ls $d | head -30; python3 - "$d" <<'P'
import json,sys,glob,os
d=sys.argv[1]
for f in sorted(glob.glob(d+'/**/grade*.json',recursive=True)):
    g=json.load(open(f)); print('##',f)
    for k,v in g.items():
        if isinstance(v,dict) and 'acc' in v: print(k, v['acc'])
        elif not isinstance(v,(dict,list)): print(k,v)
for f in ['answer.md','answer.txt','final.md']:
    p=os.path.join(d,f)
    if os.path.exists(p): print('##',f); print(open(p).read()[:3000])
P''', shell=True, capture_output=True, text=True, executable='/bin/bash'))
