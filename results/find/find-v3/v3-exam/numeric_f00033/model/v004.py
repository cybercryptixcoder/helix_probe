import math

def predict(probe):
    # A: sharp peak at x=0, value ~0.387 [E2,E4]
    # B: central bump is ASYMMETRIC: right side decays faster than left [E4,E6]
    #    left:  f(-2)=0.0575, f(-1)=0.197, f(-0.5)=0.305, f(0)=0.387
    #    right: f(0.3)=0.35, f(0.6)=0.309, f(1)=0.255, f(1.5)=0.1875, f(2)=0.12
    #    So right side is a Gaussian with sigma ~0.95 but shifted: peak near x~0.1-0.2
    #    Left side is steeper: sigma ~0.75. Model as two-sided Gaussian.
    # C: small positive shoulder on the LEFT tail: f(-3)=0.008, f(-4)=0.0053,
    #    f(-5)=0.0027, f(-6)=0.0, f(-7)=-0.0001 [E6]. Right side goes negative
    #    faster: f(8)=-0.0021, f(9)=-0.0032, f(11)=-0.0054 [E4].
    # D: far negative baseline ~-0.004 for x<-30, ~0 for x>25 [E2,E5]
    #    negative side: -0.0044 at -128, -0.003 at -40, -0.0021 at -30 [E2]
    #    positive side: ~-0.0003 for large x [E2,E3,E5]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # central bump: asymmetric Gaussian
            if x >= 0:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.95 ** 2))
            else:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.75 ** 2))
            # far-field baseline
            if x < -15:
                base = -0.004 * (1 - math.exp(-(abs(x) - 15) / 15.0))
            elif x > 6:
                base = -0.0003 * (1 - math.exp(-(x - 6) / 10.0))
            else:
                base = 0.0
            v = bump + base
        except Exception:
            v = None
        ys.append(v)
    return {"y": ys}
