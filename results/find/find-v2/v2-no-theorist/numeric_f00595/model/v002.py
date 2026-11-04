def predict(probe):
    # f(x) = ceil(x) for x > 0 [E1,E2,E3,E4,E5,E6]
    # f(x) = floor(x) - 1 for x < 0 [E1,E2,E3,E4,E5,E6]
    # f(0) = -1 [E2,E4,E6]
    import math
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(math.ceil(x))
        elif x < 0:
            out.append(math.floor(x) - 1)
        else:
            out.append(-1)
    return {"y": out}
