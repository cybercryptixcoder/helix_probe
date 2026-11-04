def predict(probe):
    try:
        xs = probe["x"]
        ys = []
        a = -8.85e-6
        b = -16.71
        c = 5.42
        for x in xs:
            ys.append(a * x**3 + b * x + c)
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
