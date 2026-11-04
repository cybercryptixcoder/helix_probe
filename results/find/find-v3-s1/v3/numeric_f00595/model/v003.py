import math

def predict(probe):
    # A: outside special interval, output = floor(x)+1 for x>=0, floor(x)-1 for x<0 [E1,E3,E4]
    # B: special interval is exactly 30 < x < 45 (open); 30->31, 45->46 ordinary [E2,E4]
    # C: inside interval output is negative, roughly -0.23..-0.51, varies with x [E2]
    #    E4 shows 31->32 and 44->45 are ORDINARY, so interval is narrower than (30,45).
    #    Actually 31 and 44 gave ordinary values, so interval excludes them too.
    #    From E2: 32,35,38.8,40,42 special; 30,45 ordinary. 31,44 ordinary [E4].
    #    So special interval is roughly (31,44) open? 32 special, 31 ordinary -> lower bound in (31,32].
    #    Upper: 42 special, 44 ordinary -> upper bound in (42,44]. 45 ordinary.
    #    Best guess: 31 < x < 44 (open). Marked uncertain.
    out = []
    for x in probe["x"]:
        if 31 < x < 44:
            # ? unknown formula; rough sinusoid guess
            out.append(-0.37 + 0.14 * math.sin((x - 32) * 1.3))
        else:
            out.append(math.floor(x) + (1 if x >= 0 else -1))
    return {"y": out}
