def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            if x < 0:
                y = 4.69 * x + 6.0
            else:
                y = 4.71 * x + 3.92
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
