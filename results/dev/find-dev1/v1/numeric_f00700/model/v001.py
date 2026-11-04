def predict(probe):
    """Model: f(x) = x + 1 for x >= 0, x - 1 for x < 0."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
            elif x >= 0:
                ys.append(x + 1)
            else:
                ys.append(x - 1)
        return {"y": ys}
    except Exception:
        return {"y": []}
