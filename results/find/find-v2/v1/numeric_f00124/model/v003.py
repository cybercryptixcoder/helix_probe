def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if x > 0:
                y = 106.0 + 111.4 * x
            elif x < 0:
                y = 106.0 + 25.8 * x
            else:
                y = 106.0
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
