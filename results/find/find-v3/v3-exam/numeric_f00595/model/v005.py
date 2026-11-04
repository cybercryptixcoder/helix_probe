def predict(probe):
    # f(x) = floor(x) + 1 for x > 0 [E1-E14]
    # f(x) = floor(x) - 1 for x <= 0 [E1-E14]
    # EXCEPTION: on interval roughly (37.5, 42.0), f returns a small
    #   negative value in [-0.7, -0.28] instead of floor(x)+1 [E15-E18]
    #   ? boundaries: E18 shows 37.5..41.8 anomalous, 42.0 and 42.5 normal;
    #     38.1 normal (E16) but 38.0 anomalous (E18) -> lower bound ~38.0
    #   ? values look like -0.5 + noise; use -0.5 as guess.
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        if 38.0 <= x < 42.0:
            out.append(-0.5)
            continue
        fl = math.floor(x)
        if x > 0:
            out.append(float(fl + 1))
        else:
            out.append(float(fl - 1))
    return {"y": out}
