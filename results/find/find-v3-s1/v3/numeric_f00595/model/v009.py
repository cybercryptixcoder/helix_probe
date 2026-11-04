import math

def predict(probe):
    # A: outside special interval, output = floor(x)+1 for x>=0, floor(x)-1 for x<0 [E1,E3,E4,E5,E7,E9,E11,E13,E14,E15,E17]
    # B: special interval is 33.45 < x < 42.05 (open) [E18: 33.45 special, 42.05->43 ordinary; E16: 33.4->34 ordinary]
    #    E18 shows 33.45 already special and 42.05 ordinary; lower edge in (33.4,33.45], upper edge in (42.01,42.05]
    # C: inside interval output is negative and noisy, mean ~-0.46, range -0.23..-0.73 [E2,E6,E8,E10,E12,E16,E18]
    #    No smooth structure evident; treat as noisy constant ~-0.46
    out = []
    for x in probe["x"]:
        if 33.42 < x < 42.03:
            out.append(-0.46)
        else:
            out.append(math.floor(x) + (1 if x >= 0 else -1))
    return {"y": out}
