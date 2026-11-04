import math

def predict(probe):
    # A: outside special interval, output = floor(x)+1 for x>=0, floor(x)-1 for x<0 [E1,E3,E4,E5,E7,E9,E11,E13,E14,E15,E17,E19,E21]
    # B: at exact integers, same rule applies: f(n)=n+1 (n>=0), n-1 (n<0) [E22: 0->-1,1->2,...,-1->-2]
    #    Note E22 shows f(0)=-1, consistent with x<0 branch? No: 0->-1 means floor(0)-1. So boundary is x<=0 -> floor(x)-1, x>0 -> floor(x)+1.
    #    Check E4: 0.001->? E4 [ok] with old rule (x>=0 -> +1). Need to reconcile: E22 f(0)=-1.
    #    E4 had 0.001 and -0.001; old model matched. So 0.001->1, -0.001->-2. And 0->-1.
    #    So rule: x>0 -> floor(x)+1; x<=0 -> floor(x)-1. Check negative: -0.5->-2 (floor=-1, -1-1=-2) [E20 ok]. 0.5->1 (floor 0 +1) [E20 ok].
    #    -1.5->-3 (floor -2 -1) [E20 ok]. 1.5->2 [E20 ok]. Good.
    # C: special interval: 33.45 <= x < 42.04 (approx). Inside output negative noisy ~-0.46.
    #    E20: 33.45 special, 33.46,33.47,33.48 special; 42.01,42.02,42.03 special; 42.04->43 ordinary; 42.05->43 ordinary.
    #    E18: 33.45 special, 42.0 special, 42.0001 special, 42.01 special, 42.05 ordinary.
    #    E22: 34 special, 41 special, 42 special (42->-0.4423). 33->34 ordinary.
    #    So lower edge: 33.45 special, 33.4 ordinary [E16]. Upper: 42.03 special, 42.04 ordinary.
    #    So interval is [33.45, 42.04) roughly. Use 33.45 <= x < 42.035.
    # D: inside interval output noisy negative, mean ~-0.46, range -0.23..-0.73 [E2,E6,E8,E10,E12,E16,E18,E20,E22]
    out = []
    for x in probe["x"]:
        if 33.45 <= x < 42.035:
            out.append(-0.46)
        elif x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}
