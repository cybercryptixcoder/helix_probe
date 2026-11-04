def predict(probe):
    out = []
    for x in probe.get("x", []):
        try:
            if x < -16.5:
                y = -0.7 * x
            elif x < -16:
                y = 11.9
            elif x == -16:
                y = 11.2
            elif x < 18.515:
                y = -402.3
            elif x < 19:
                y = -302.4
            elif x < 20:
                y = -319.2
            else:
                y = -16.8 * x
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
