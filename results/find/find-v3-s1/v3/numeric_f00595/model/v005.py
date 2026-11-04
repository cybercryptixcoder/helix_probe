import math

def predict(probe):
    # A: outside special interval, output = floor(x)+1 for x>=0, floor(x)-1 for x<0 [E1,E3,E4,E5,E7]
    # B: special interval is 33 < x < 43 (open). 33->34, 43->44 ordinary [E6,E8]
    #    E6: 32.5->33, 34 special; E8: 42.9->43, 43->44 ordinary. So lower edge in (33,34], upper in (42.9,43].
    #    E2: 32,35,38.8,40,42 special; E6: 34,36,37,39,41 special. 33 ordinary, 43 ordinary.
    #    Best: 33 < x < 43 open (edges uncertain).
    # C: inside interval output is negative, varies with x, range roughly -0.23..-0.63 [E2,E6,E8]
    #    Data (x, y): (34,-.3625)(35,-.2835)(35.5,-.2805)(36,-.5813)(37,-.5269)(38,-.5551)
    #    (38.5,-.5582)(38.8,-.5061)(39,-.439)(40,-.2298)(40.5,-.5933)(41,-.6309)(41.5,-.5337)(42,-.4207)
    #    Non-monotone, oscillatory. Rough sinusoid guess.
    out = []
    for x in probe["x"]:
        if 33 < x < 43:
            out.append(-0.43 + 0.2 * math.sin((x - 34) * 1.4))
        else:
            out.append(math.floor(x) + (1 if x >= 0 else -1))
    return {"y": out}
