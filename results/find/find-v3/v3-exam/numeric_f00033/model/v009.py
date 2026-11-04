import math

def predict(probe):
    # A: central bump peak ~0.387 at x=0, asymmetric: left sigma~0.85, right sigma~0.95 [E4,E8,E10]
    # B: left shoulder: broad Gaussian center~-3.3, sigma~1.5, amp~0.008 [E6,E8]
    # C: far-negative baseline ~-0.004 for x<-30; far-positive baseline ~-0.0002 for x>25 [E2,E5,E9,E11]
    # D: mid-positive negative dip: roughly linear ramp down from x~6 to min ~-0.0062 at x~11.8,
    #    then linear ramp back up to ~-0.0004 by x~22 [E12,E18,E20]
    # E: far-negative baseline transitions smoothly from ~0 at x~-10 to -0.004 by x~-30 [E14]
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
            # far-field baseline (smooth transition on negative side)
            if x < -10:
                base = -0.004 * (1 - math.exp(-(abs(x) - 10) / 8.0))
            elif x > 25:
                base = -0.0002 * (1 - math.exp(-(x - 25) / 10.0))
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
