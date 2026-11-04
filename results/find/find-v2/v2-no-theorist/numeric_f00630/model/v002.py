def predict(probe):
    # f(x) = 52.2 for x > 0, -14.96 for x < 0 [E1, E2]
    # f(0) = 898156.8 (a special spike at exactly zero) [E2]
    # f(-0.001) = -14.96, f(0.001) = 52.2: sign rule holds arbitrarily near 0 [E2]
    out = []
    for x in probe.get("x", []):
        if x is None:
            out.append(None)
        elif x == 0:
            out.append(898156.8)
        else:
            out.append(52.2 if x > 0 else -14.96)
    return {"y": out}
