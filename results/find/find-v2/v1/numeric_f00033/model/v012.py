import math

def predict(probe):
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            peak = 0.389
            if x >= 0:
                sigma = 1.30
                y = peak * math.exp(-(x * x) / (2 * sigma * sigma))
                y += -0.0061 * math.exp(-((x - 12.0) ** 2) / (2 * 4.0 * 4.0))
                y += -0.0030 * math.exp(-((x - 18.0) ** 2) / (2 * 3.0 * 3.0))
                y += -0.0004 * (1.0 - math.exp(-max(0.0, x - 20.0) / 8.0))
            else:
                ax = -x
                # steeper Gaussian core on the left
                sigma = 0.85
                y = peak * math.exp(-(ax * ax) / (2 * sigma * sigma))
                # small positive plateau tail beyond the core
                y += 0.0045 * (1.0 - math.exp(-max(0.0, ax - 2.0) / 1.5)) * math.exp(-max(0.0, ax - 4.5) / 3.0)
                y += -0.0005 * math.exp(-((ax - 12.0) ** 2) / (2 * 4.0 * 4.0))
                y += -0.0010 * math.exp(-((ax - 18.0) ** 2) / (2 * 3.0 * 3.0))
                if ax > 22.0:
                    y += -0.0014 - (ax - 22.0) * (0.0030 / 106.0)
                else:
                    y += -0.0014 * (1.0 - math.exp(-max(0.0, ax - 20.0) / 8.0))
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
