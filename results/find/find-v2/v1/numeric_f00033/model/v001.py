import math

def predict(probe):
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            # asymmetric Gaussian bump
            if x >= 0:
                sigma = 2.0
            else:
                sigma = 1.6
            peak = 0.39
            base = -0.004
            y = base + (peak - base) * math.exp(-(x * x) / (2 * sigma * sigma))
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
