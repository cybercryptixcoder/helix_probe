def predict(probe):
    # Output is a two-valued step depending on sign of x [E1,E2,E3,E4]:
    #   x > 0  -> 52.2
    #   x < 0  -> -14.96
    #   x == 0 -> 898156.8  (special value at exactly zero) [E4]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(52.2)
        elif x < 0:
            out.append(-14.96)
        else:
            out.append(898156.8)
    return {"y": out}
