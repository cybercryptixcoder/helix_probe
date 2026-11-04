import math

def predict(probe):
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            peak = 0.389
            center = -0.03
            d = x - center
            sigma = 1.17 if d >= 0 else 1.0
            y = peak * math.exp(-(d * d) / (2 * sigma * sigma))

            ax = abs(x)
            if x > 0:
                y += -0.0061 * math.exp(-((x - 12.0) ** 2) / (2 * 4.0 * 4.0))
                y += -0.0030 * math.exp(-((x - 18.0) ** 2) / (2 * 3.0 * 3.0))
                y += -0.0004 * (1.0 - math.exp(-max(0.0, ax - 20.0) / 8.0))
            else:
                y += -0.0005 * math.exp(-((ax - 12.0) ** 2) / (2 * 4.0 * 4.0))
                y += -0.0010 * math.exp(-((ax - 18.0) ** 2) / (2 * 3.0 * 3.0))
                y += -0.0032 * (1.0 - math.exp(-max(0.0, ax - 20.0) / 15.0))

            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
