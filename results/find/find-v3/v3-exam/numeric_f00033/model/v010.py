import math

def predict(probe):
    # A: central asymmetric Gaussian bump, peak ~0.387 at x=0, left sigma~0.85, right sigma~0.95 [E4,E8,E10]
    # B: left shoulder: broad Gaussian center~-3.3, sigma~1.5, amp~0.008 [E6,E8]
    # C: far-positive baseline ~-0.0004 for x>~22 (flat) [E16,E22]
    # D: mid-positive negative dip: linear fall from ~0 at x=6 to min ~-0.0062 at x~11.8,
    #    then linear recovery reaching ~-0.0004 at x~22 [E12,E18,E20,E22]
    # E: far-negative baseline: roughly LINEAR ramp from ~0 at x~-8 down to ~-0.0032 at x~-50,
    #    then continues slowly to ~-0.0043 at x=-120 (no flat plateau by -40) [E24,E14]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # central asymmetric Gaussian bump
            if x >= 0:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.95 ** 2))
            else:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.85 ** 2))
            # left positive shoulder
            if x < 0:
                bump += 0.008 * math.exp(-((x + 3.3) ** 2) / (2 * 1.5 ** 2))
            # far-negative baseline: linear ramp from ~0 at x=-8 to -0.0032 at x=-50,
            # then gentle continued decline to ~-0.0043 at x=-120
            if x < -8:
                if x >= -50:
                    base = -0.0032 * (abs(x) - 8) / 42.0
                else:
                    base = -0.0032 - 0.0011 * (abs(x) - 50) / 70.0
            elif x > 22:
                base = -0.0004
            else:
                base = 0.0
            # mid-positive negative dip: piecewise linear
            if 6.0 <= x <= 22.0:
                if x <= 11.8:
                    dip = -0.0062 * (x - 6.0) / (11.8 - 6.0)
                else:
                    dip = -0.0062 + (0.0058) * (x - 11.8) / (22.0 - 11.8)
            else:
                dip = 0.0
            v = bump + base + dip
        except Exception:
            v = None
        ys.append(v)
    return {"y": ys}
