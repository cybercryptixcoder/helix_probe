import math

def predict(probe):
    # A: outside special interval, output = floor(x)+1 for x>0, floor(x)-1 for x<=0 [E1,E3,E4,E5,E7,E9,E11,E13,E14,E15,E17,E19,E21,E22,E23]
    # B: at exact integers same rule: f(n)=n+1 (n>0), n-1 (n<=0) [E22: 0->-1,1->2,...,-1->-2]
    # C: special interval: 33.44 <= x <= 42.036 (inclusive both ends) [E24: 33.44 special, 33.449 special, 42.036 special]
    #    E16: 33.4 ordinary; E24: 33.44 special. E24: 42.036 special (42.05 ordinary [E16,E20]).
    #    So interval is [33.44, 42.036] roughly. Use 33.44 <= x <= 42.036.
    # D: inside interval output noisy negative, mean ~-0.5, range -0.31..-0.73 [E2,E6,E8,E10,E12,E16,E18,E20,E22,E24]
    out = []
    for x in probe["x"]:
        if 33.44 <= x <= 42.036:
            out.append(-0.5)
        elif x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}
