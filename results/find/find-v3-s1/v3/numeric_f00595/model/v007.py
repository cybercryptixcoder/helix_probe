import math

def predict(probe):
    # A: outside special interval, output = floor(x)+1 for x>=0, floor(x)-1 for x<0 [E1,E3,E4,E5,E7,E9,E11]
    # B: special interval is 33 < x < 42.1 (open) [E6,E8,E10,E12]
    #    E12: 33.0->34 ordinary, 33.1->34 ordinary, 33.6 special => lower edge in (33.1,33.6]
    #    E10: 33.3->34 ordinary, 34.5 special => lower edge in (33.3,34.5]
    #    E12: 42.0 special, 42.1->43 ordinary => upper edge in (42.0,42.1]
    #    E10: 41.8 special, 42.2->43 ordinary => upper edge in (41.8,42.2]
    #    Combined: lower edge ~33.5, upper edge ~42.05
    # C: inside interval output is negative and noisy, mean ~-0.46, range -0.23..-0.64 [E2,E6,E8,E10,E12]
    out = []
    for x in probe["x"]:
        if 33.5 < x < 42.05:
            out.append(-0.46)
        else:
            out.append(math.floor(x) + (1 if x >= 0 else -1))
    return {"y": out}
