import json
g=json.load(open('/content/helix_probe/runs/edit/Qwen3.5-9B_addition_helix2_high_r1/grade.json'))
def walk(x,p=''):
    if isinstance(x,dict):
        for k,v in x.items():
            if k in('items','answers','outputs','rows'): continue
            walk(v,p+'.'+k)
    elif isinstance(x,(int,float,str)) and len(str(x))<80: print(p,x)
walk(g)
