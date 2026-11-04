def predict(probe):
    # f(x) = 6*(x+1)^3        for x <= -1        [E9,E11,E13,E14,E18,E19,E20,E22,E23]
    # f(x) = 6*(1-(x+1)^2)    for -1 < x < 0     [E15,E16,E17,E19,E20,E21,E22,E23]
    # f(x) = 0                for 0 <= x < 1     [E15,E16,E21,E22,E23]
    # f(x) = -4.3*(x-1)^3     for x >= 1         [E4,E5,E14,E18,E21,E22,E23]
    # switch points: x=-1 -> 6.1, x=0 -> 0, x=1 -> -4.3 [E15,E21,E22]
    out = []
    for x in probe.get("x", []):
        try:
            if x <= -1:
                y = 6.0 * (x + 1.0) ** 3
            elif x < 0:
                y = 6.0 * (1.0 - (x + 1.0) ** 2)
            elif x < 1:
                y = 0.0
            else:
                y = -4.3 * (x - 1.0) ** 3
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
