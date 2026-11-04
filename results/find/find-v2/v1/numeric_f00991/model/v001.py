def predict(probe):
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xf = float(x)
            if xf <= 0:
                ys.append(-8.2 * xf + 2.5)
            else:
                ys.append(16.4 * xf - 2.5)
        except Exception:
            ys.append(None)
    return {"y": ys}
