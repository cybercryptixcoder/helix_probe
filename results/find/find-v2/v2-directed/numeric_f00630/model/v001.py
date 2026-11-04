def predict(probe):
    # f(x) = -14.96 for x < 0 [E1]
    # f(x) = 52.2 for x > 0 [E1]
    # f(0) = 898156.8 (a spike at exactly 0) [E1]
    # Sign-based step function with a special value at zero.
    out = []
    for x in probe["x"]:
        if x < 0:
            out.append(-14.96)
        elif x > 0:
            out.append(52.2)
        else:
            out.append(898156.8)
    return {"y": out}
