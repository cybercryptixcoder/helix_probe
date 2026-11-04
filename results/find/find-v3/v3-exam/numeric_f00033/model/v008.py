import math

def predict(probe):
    # A: central bump peak ~0.387 at x=0, asymmetric: left sigma~0.85, right sigma~0.95 [E4,E8,E10]
    # B: left shoulder: broad Gaussian center~-3.3, sigma~1.5, amp~0.008 [E6,E8]
    # C: far-negative baseline ~-0.004 for x<-30; far-positive baseline ~-0.0002 for x>25 [E2,E5,E9,E11]
    # D: negative dip centered ~12.5, sigma~2.5, amp~-0.006 [E7,E11,E12]
    # E: mid-positive region x~6..20 has a gradual negative slope reaching ~-0.006 at x~12 [E12,E13]
    # F: transition to far-negative baseline around x~-15 to -30 [E2]
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
            # far-field baseline
            if x < -15:
                base = -0.004 * (1 - math.exp(-(abs(x) - 15) / 15.0))
            elif x > 25:
                base = -0.0002 * (1 - math.exp(-(x - 25) / 10.0))
            else:
                base = 0.0
            # negative dip around x~12.5 (wider sigma to match E12)
            dip = -0.006 * math.exp(-((x - 12.5) ** 2) / (2 * 2.5 ** 2))
            v = bump + base + dip
        except Exception:
            v = None
        ys.append(v)
    return {"y": ys}
