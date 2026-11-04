def predict(probe):
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x <= -16:
                # nearly constant ~8, slight decrease toward -128
                # fit: at -16 -> 8.0734, at -128 -> 7.8599
                # slope = (7.8599-8.0734)/(-128+16) = -0.2135/-112 = 0.001906
                y = 8.0734 + 0.001906 * (x + 16)
            else:
                y = 8.0 - 9.6 * x
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}
