def predict(probe):
    # f(x) = floor(x) + 1 for x > 0 [E1-E14]
    # f(x) = floor(x) - 1 for x <= 0 [E1-E14]
    # EXCEPTION: on interval [39.5, 41.5] (roughly), f returns a small
    #   negative value in [-0.65, -0.32] instead of floor(x)+1 [E15, E16]
    #   ? boundaries unknown; E16 shows 39.5..41.5 anomalous, 38.1 and 42.1 normal.
    #   ? values look like -0.3..-0.65, possibly -0.5 + noise. Use -0.5 as guess.
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        if 39.5 <= x <= 41.5:
            out.append(-0.5)
            continue
        fl = math.floor(x)
        if x > 0:
            out.append(float(fl + 1))
        else:
            out.append(float(fl - 1))
    return {"y": out}
