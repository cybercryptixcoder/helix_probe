def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside a special interval [E1,E3 exact fit]
    # In interval (97.5, ~115.5) output is constant ~7772.93 with noise [E2,E3,E4,E5,E6]
    # Lower boundary exactly 97.5 (cubic at 97.5, flat at 97.51) [E3,E6]
    # Upper boundary between 115 (flat) and 120 (cubic); guessed 115.5 [E2]
    xs = probe["x"]
    out = []
    for x in xs:
        if x is None:
            out.append(None)
            continue
        if 97.5 < x < 115.5:
            out.append(7772.93)
        else:
            out.append(1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6)
    return {"y": out}
