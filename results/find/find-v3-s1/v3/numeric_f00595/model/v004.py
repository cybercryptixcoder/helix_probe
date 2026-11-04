import math

def predict(probe):
    # A: outside special interval, output = floor(x)+1 for x>=0, floor(x)-1 for x<0 [E1,E3,E4,E5]
    # B: special interval is 33 < x < 43 (open). 33->34, 43->44 ordinary [E6]
    #    32.5->33, 34 special; 43->44, 43.5->44 ordinary. So lower edge in (33,34], upper in (42,43].
    #    E2: 32,35,38.8,40,42 special; E6: 34,36,37,39,41 special. 33 ordinary, 43 ordinary.
    #    Best: 33 < x < 43 open? 34 special, 33 ordinary -> lower in (33,34]. 42 special,43 ordinary -> upper in (42,43].
    #    Guess: 33 < x < 43 (open), uncertain on exact edges.
    # C: inside interval output is negative, varies with x, range roughly -0.23..-0.63 [E2,E6]
    out = []
    for x in probe["x"]:
        if 33 < x < 43:
            # ? unknown formula; rough sinusoid guess
            out.append(-0.48 + 0.15 * math.sin((x - 34) * 1.1))
        else:
            out.append(math.floor(x) + (1 if x >= 0 else -1))
    return {"y": out}
