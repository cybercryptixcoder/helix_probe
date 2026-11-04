import math

def predict(probe):
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            peak = 0.389
            center = -0.04
            d = x - center
            if d >= 0:
                sigma = 1.55
                dip_amp = -0.0055
                dip_center = 11.0
                dip_sigma = 3.5
            else:
                sigma = 1.0
                dip_amp = -0.0006
                dip_center = 11.0
                dip_sigma = 4.0
            y = peak * math.exp(-(d * d) / (2 * sigma * sigma))
            y += dip_amp * math.exp(-((abs(x) - dip_center) ** 2) / (2 * dip_sigma * dip_sigma))
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
