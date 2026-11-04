import math

def predict(probe):
    # Model: sum of Gaussians + constant offset, approximating an MLP.
    # Main peak near 0 (Gaussian, amp~0.39, sigma~1.0) [E2,E4,E6]
    # Positive bump near -5 (amp~0.003 at -5, ~0.022 at -2.5) [E8,E14]
    # Negative dip near 12 (min -0.0061 at 12) [E10,E12]
    # Broad negative component on left (tail -0.0044 at -128) [E2,E9]
    # Small baseline offset (~-0.0001 at far right) [E2,E3]
    xs = probe["x"]
    ys = []
    for x in xs:
        # main central peak
        y = 0.387 * math.exp(-(x*x) / (2*1.0*1.0))
        # positive shoulder around -5 (helps transition region)
        y += 0.006 * math.exp(-((x+4.0)**2) / (2*1.5*1.5))
        # negative dip around 12
        y += -0.0061 * math.exp(-((x-12.0)**2) / (2*2.0*2.0))
        # broad negative left tail
        y += -0.0045 * math.exp(-((x+128.0)**2) / (2*60.0*60.0))
        # baseline
        y += -0.0001
        ys.append(y)
    return {"y": ys}
