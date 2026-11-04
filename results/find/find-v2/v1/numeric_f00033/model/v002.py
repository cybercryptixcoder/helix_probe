import math

def predict(probe):
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            peak = 0.3868
            # asymmetric Gaussian with narrower sigmas than v1
            if x >= 0:
                sigma = 1.55
            else:
                sigma = 1.25
            y = peak * math.exp(-(x * x) / (2 * sigma * sigma))
            # slight negative dip in far tails
            y += -0.005 * math.exp(-((abs(x) - 11.0) ** 2) / (2 * 4.0 * 4.0))
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
