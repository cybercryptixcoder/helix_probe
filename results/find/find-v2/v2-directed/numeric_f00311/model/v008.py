def predict(probe):
    # Model mechanism:
    # For x > -9.4: y = 8 - 9.6*x  [E1,E5,E10,E11,E19]
    # For x <= -9.4: noisy constant ~8.0  [E1,E3,E9,E12,E13,E14]
    # Boundary at x = -9.4 (noisy side inclusive) [E15,E17,E20]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if x > -9.4:
            ys.append(8.0 - 9.6 * x)
        else:
            ys.append(8.0)  # noisy ~8.0; best deterministic guess
    return {"y": ys}
