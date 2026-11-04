def predict(probe):
    # Regime A: x <= -9.4, output ~8 with noise [E1,E3,E9,E12,E13,E14,E21]
    # Regime B: x > -9.4, output = -9.6*x + 8 exactly [E2,E4,E5,E6,E7,E10,E11,E19,E24]
    # Boundary at x = -9.4 belongs to noisy regime [E15,E17,E20,E22,E23]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if x <= -9.4:
            ys.append(8.0)  # mean of noise
        else:
            ys.append(-9.6 * x + 8.0)
    return {"y": ys}
