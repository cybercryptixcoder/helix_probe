def predict(probe):
    # f(x) = 52.2 for x > 0 [E1, E2]
    # f(x) = -14.96 for x < 0 [E1, E2]
    # f(0) = 898156.8 (special value at exactly zero) [E2]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(52.2)
        elif x < 0:
            out.append(-14.96)
        else:
            out.append(898156.8)
    return {"y": out}
