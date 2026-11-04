def predict(probe):
    out = []
    for x in probe.get("x", []):
        try:
            if x <= -16:
                y = -0.7 * x
            elif x >= 19:
                y = -16.8 * x
            else:
                y = -402.3
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
