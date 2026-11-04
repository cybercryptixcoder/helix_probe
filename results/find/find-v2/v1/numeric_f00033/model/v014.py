import math

def predict(probe):
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            peak = 0.389
            if x >= 0:
                # right flank: near-linear from 0.4 to 1.35 (E18), then smooth decay
                lin = 0.3361 - 0.1351 * (x - 0.4)
                # tail anchored on E15/E16: f(2)=0.1132, f(3)=0.0327, f(4.2)=0.0071
                # Gaussian-ish: 0.1132 * exp(-((x-2)^2)/(2*s^2)); at x=3 -> 0.0327 => s^2 = 1/(2*ln(0.1132/0.0327))
                s2 = 1.0 / (2.0 * math.log(0.1132 / 0.0327))
                tail = 0.1132 * math.exp(-((x - 2.0) ** 2) / (2.0 * s2))
                if x < 1.5:
                    y = lin
                else:
                    w = min(1.0, (x - 1.5) / 0.5)
                    y = (1 - w) * lin + w * tail
                if x < 0.4:
                    y = 0.389 - 0.135 * x - 0.02 * x * x
                y += -0.0061 * math.exp(-((x - 12.0) ** 2) / (2 * 4.0 * 4.0))
                y += -0.0030 * math.exp(-((x - 18.0) ** 2) / (2 * 3.0 * 3.0))
                y += -0.0004 * (1.0 - math.exp(-max(0.0, x - 20.0) / 8.0))
            else:
                ax = -x
                # left flank: near-linear from 0.5 to 1.0 (E19), slope -0.216
                if ax <= 1.0:
                    y = 0.3052 - 0.216 * (ax - 0.5)
                else:
                    # steep drop: f(1.4)=0.1218, f(2)=0.0575, f(3)=0.008
                    # Gaussian anchored at 1.4: 0.1218*exp(-((ax-1.4)^2)/(2*s2))
                    # at ax=2: 0.0575 => s2 = 0.36/(2*ln(0.1218/0.0575))
                    s2 = 0.36 / (2.0 * math.log(0.1218 / 0.0575))
                    y = 0.1218 * math.exp(-((ax - 1.4) ** 2) / (2.0 * s2))
                    # small positive tail beyond 3
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
