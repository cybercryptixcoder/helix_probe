def predict(probe):
    # f(x) = ceil(x) for x > 0 [E1,E2,E3,E4,E5,E6,E8,E9,E10,E11]
    # f(x) = floor(x) - 1 for x < 0 [E1,E2,E3,E4,E5,E6,E8,E9,E10,E11]
    # f(0) = -1 [E2,E4,E6,E10]
    # At x = 40 exactly, f returns -0.5542 (a special anomaly) [E12]
    import math
    out = []
    for x in probe["x"]:
        if x == 40:
            out.append(-0.5542)
        elif x > 0:
            out.append(math.ceil(x))
        elif x < 0:
            out.append(math.floor(x) - 1)
        else:
            out.append(-1)
    return {"y": out}
