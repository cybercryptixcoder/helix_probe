def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            if x >= 0:
                y = -22.5 * x + 11.2
            else:
                y = -11.2 * x + 11.2
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
