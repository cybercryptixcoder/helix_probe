def predict(probe):
    # f(x) = 2.6*x + 9.4 for x > 0 [E1, E2]
    # f(x) = 2.6*x + 14.2 for x < 0 [E1, E2]
    # f(0) = 444.28 (special spike at exactly 0) [E2]
    # Note: -0.01 -> 14.174 = 2.6*(-0.01)+14.2 ✓, 0.01 -> 9.426 = 2.6*0.01+9.4 ✓
    # So the sign split is sharp at 0, with a lone spike at x=0.
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                y = 444.28
            elif x < 0:
                y = 2.6 * x + 14.2
            else:
                y = 2.6 * x + 9.4
            out.append(round(y, 3))
        except Exception:
            out.append(None)
    return {"y": out}
