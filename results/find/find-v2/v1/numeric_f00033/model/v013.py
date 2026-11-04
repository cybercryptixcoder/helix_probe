import math

def predict(probe):
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            peak = 0.389
            if x >= 0:
                # near-linear core on right flank (E18): slope ~ -0.135, anchored at x=0.4
                # f(0.4)=0.3361, f(1.35)=0.2078 -> slope = (0.2078-0.3361)/(1.35-0.4) = -0.1351
                lin = 0.3361 - 0.1351 * (x - 0.4)
                # Gaussian tail beyond ~1.5 to match E12/E15/E16
                # fit: f(2)=0.12, f(3)=0.033 -> sigma ~ 1.30, amp at 2: 0.12
                tail = 0.12 * math.exp(-((x - 2.0) ** 2) / (2 * 1.30 * 1.30))
                # blend: use linear for x<1.5, tail for x>=1.5, smooth transition
                if x < 1.5:
                    y = lin
                else:
                    # at x=1.5 lin gives 0.3361-0.1351*1.1=0.1875; tail at 1.5: 0.12*exp(-0.25/3.38)=0.1115
                    # blend weight
                    w = min(1.0, (x - 1.5) / 0.5)
                    y = (1 - w) * lin + w * tail
                # ensure peak near 0 doesn't exceed 0.389
                if x < 0.4:
                    # near peak: smooth from 0.389 at 0 to 0.3361 at 0.4
                    # use quadratic: f(0)=0.389, f(0.4)=0.3361, slope at 0.4 ~ -0.135
                    # simple: 0.389 - 0.135*x - small curvature
                    y = 0.389 - 0.135 * x - 0.02 * x * x
                y += -0.0061 * math.exp(-((x - 12.0) ** 2) / (2 * 4.0 * 4.0))
                y += -0.0030 * math.exp(-((x - 18.0) ** 2) / (2 * 3.0 * 3.0))
                y += -0.0004 * (1.0 - math.exp(-max(0.0, x - 20.0) / 8.0))
            else:
                ax = -x
                sigma = 0.85
                y = peak * math.exp(-(ax * ax) / (2 * sigma * sigma))
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
