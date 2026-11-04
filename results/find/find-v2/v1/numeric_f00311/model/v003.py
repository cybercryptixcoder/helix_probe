def predict(probe):
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x >= -9.3:
                y = 8.0 - 9.6 * x
            else:
                y = 8.0
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}
