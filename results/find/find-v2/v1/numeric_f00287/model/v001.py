def predict(probe):
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if ax >= 16:
                y = 2.8 * x
            elif ax <= 8:
                y = -402.3
            else:
                # transition zone between 8 and 16: linear blend guess
                t = (ax - 8) / 8.0
                plateau = -402.3
                lin = 2.8 * x
                y = plateau * (1 - t) + lin * t
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
