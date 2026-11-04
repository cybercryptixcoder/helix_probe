import math

def predict(probe):
    # A: outside special interval, output = floor(x)+1 for x>=0, floor(x)-1 for x<0 [E1,E3,E4,E5,E7,E9,E11,E13,E14,E15]
    # B: special interval is 33.4 < x < 42.05 (open) [E16: 33.4->34 ordinary, 33.5 special; 42.02 special, 42.05->43 ordinary]
    #    E12: 33.1->34 ordinary, 33.6 special; 42.0 special, 42.1->43 ordinary
    #    E10: 33.3->34 ordinary, 34.5 special; 41.8 special, 42.2->43 ordinary
    #    Combined: lower edge in (33.4,33.5], upper edge in (42.02,42.05]
    # C: inside interval output is negative and noisy, mean ~-0.46, range -0.23..-0.73 [E2,E6,E8,E10,E12,E16]
    #    No smooth structure evident; treat as noisy constant ~-0.46
    out = []
    for x in probe["x"]:
        if 33.45 < x < 42.03:
            out.append(-0.46)
        else:
            out.append(math.floor(x) + (1 if x >= 0 else -1))
    return {"y": out}
