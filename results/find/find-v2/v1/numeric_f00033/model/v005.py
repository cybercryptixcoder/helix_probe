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
            else:
                sigma = 1.0
            y = peak * math.exp(-(d * d) / (2 * sigma * sigma))

            # Right-side negative dip centered near x=12
            if x > 0:
                dip_amp = -0.0061
                dip_center = 12.0
                dip_sigma = 4.0
                y += dip_amp * math.exp(-((x - dip_center) ** 2) / (2 * dip_sigma * dip_sigma))
            else:
                # Left side: shallow monotone negative ramp, deepening with |x|
                # ~-0.0004 at |x|=10, ~-0.0032 at |x|=50
                ax = abs(x)
                # smooth ramp: 0 near ax=7, saturating toward -0.0035
                ramp = -0.0035 * (1.0 - math.exp(-max(0.0, ax - 7.0) / 15.0))
                y += ramp

            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
