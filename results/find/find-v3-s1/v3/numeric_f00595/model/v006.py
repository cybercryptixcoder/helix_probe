import math

def predict(probe):
    # A: outside special interval, output = floor(x)+1 for x>=0, floor(x)-1 for x<0 [E1,E3,E4,E5,E7,E9]
    # B: special interval is 33.6 < x < 42.1 (open) [E6,E8,E10]
    #    E10: 33.3->34 ordinary, 34 special => lower edge in (33.3,34]
    #    E10: 42 special, 42.2->43 ordinary => upper edge in (42,42.2]
    # C: inside interval output is negative and noisy, mean ~-0.46, range -0.23..-0.64 [E2,E6,E8,E10]
    #    No clean sinusoid fits; treat as noisy around constant mean.
    out = []
    for x in probe["x"]:
        if 33.6 < x < 42.1:
            out.append(-0.46)
        else:
            out.append(math.floor(x) + (1 if x >= 0 else -1))
    return {"y": out}
