import math

def predict(probe):
    # A: central asymmetric Gaussian bump, peak ~0.387 at x=0, left sigma~0.85, right sigma~0.95 [E4,E8,E10]
    # B: left shoulder: broad Gaussian center~-3.3, sigma~1.5, amp~0.008 [E6,E8]
    # C: far-positive baseline ~-0.0004 for x>~22 (flat) [E16,E22]
    # D: mid-positive negative dip: smooth asymmetric curve, min ~-0.0061 at x~12,
    #    rising to ~-0.0004 by x~22 [E12,E18,E20,E22]
    # E: far-negative baseline: smooth ramp from ~0 at x~-8 down to ~-0.0032 at x~-50,
    #    then continues slowly to ~-0.0043 at x=-120 [E24,E14,E25]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x >= 0:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.95 ** 2))
            else:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.85 ** 2))
            if x < 0:
                bump += 0.008 * math.exp(-((x + 3.3) ** 2) / (2 * 1.5 ** 2))
            if x < -8:
                if x >= -50:
                    base = -0.0032 * (abs(x) - 8) / 42.0
                else:
                    base = -0.0032 - 0.0011 * (abs(x) - 50) / 70.0
            elif x > 22:
                base = -0.0004
            else:
                base = 0.0
            if 6.0 <= x <= 22.0:
                if x <= 12.0:
                    dip = -0.0061 * (x - 6.0) / 6.0
                else:
                    dip = -0.0061 + 0.0057 * (x - 12.0) / 10.0
            else:
                dip = 0.0
            v = bump + base + dip
        except Exception:
            v = None
        ys.append(v)
    return {"y": ys}
