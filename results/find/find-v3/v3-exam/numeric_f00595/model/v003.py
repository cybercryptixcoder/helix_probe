def predict(probe):
    # f(x) = floor(x) + 1 for x > 0 [E1-E14]
    # f(x) = floor(x) - 1 for x <= 0 [E1-E14]
    # EXCEPTION: at x = 40.1, f returns -0.5291 instead of 41 [E15]
    #   This is a single anomalous point; likely a special "trap" value.
    #   ? We only have one data point; treat 40.1 as a special case.
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        if x == 40.1:
            out.append(-0.5291)
            continue
        fl = math.floor(x)
        if x > 0:
            out.append(float(fl + 1))
        else:
            out.append(float(fl - 1))
    return {"y": out}
