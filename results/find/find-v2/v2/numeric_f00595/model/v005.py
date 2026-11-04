def predict(probe):
    # f(x) = floor(x) + 1 for x > 0, outside (33.3, 41.5] [E1-E13]
    # f(x) = floor(x) - 1 for x <= 0 [E2, E12]
    # On the interval (33.3, 41.5] f returns a small negative value in [-0.7, -0.2] [E16]
    #   E16: 33.4..41.0 all anomalous; 33.3 and 41.5 are normal.
    #   Edges unknown precisely; assume (33.3, 41.5] [E16, ?]
    #   Inside, values look like a pseudo-random-ish small negative number.
    #   Best guess: a smooth-ish function; approximate with a deterministic
    #   hash-like value in [-0.7,-0.2]. Marked "?" — mechanism unknown.
    import math
    out = []
    for x in probe["x"]:
        if x > 33.3 and x <= 41.5:
            # unknown mechanism; produce a small negative value in [-0.7,-0.2]
            # use a deterministic pseudo-random in that range
            h = math.sin(x * 12.9898) * 43758.5453
            frac = h - math.floor(h)
            out.append(round(-0.7 + 0.5 * frac, 4))
        elif x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}
