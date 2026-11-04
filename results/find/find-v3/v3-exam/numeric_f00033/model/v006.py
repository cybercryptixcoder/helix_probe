import math

def predict(probe):
    # A: central bump, peak ~0.387 at x=0 [E4,E8]
    # B: asymmetric: left sigma ~0.75, right sigma ~0.95 [E4,E6,E8]
    #    f(-1.6)=0.092, f(-1.2)=0.155, f(-0.8)=0.240, f(-0.3)=0.348, f(0)=0.387
    #    right: f(0.5)=0.3225, f(1)=0.255, f(2)=0.12, f(3)=0.0327 [E4,E8]
    # C: LEFT positive shoulder: f(-3)=0.008, f(-4)=0.0053, f(-5)=0.0027,
    #    f(-5.5)=0.0014, f(-6)=0.0, f(-6.5)=-0.0 [E6,E8]
    #    shoulder is a broad Gaussian centered ~-3.3, sigma~1.6 [E8]
    # D: far negative baseline ~-0.004 for x<-30, ~0 for x>25 [E2,E5,E9]
    #    negative: -0.0044 at -128, -0.0033 at -65, -0.0032 at -45 [E9]
    #    positive: ~-0.0002 for large x [E3,E5,E9]
    # E: NEGATIVE dip near x~12.5: f(12.5)=-0.0058 [E7], f(10)=-0.0043 [E2]
    # F: transition from ~0 to far-negative baseline happens around x~-15 to -30 [E2]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # central asymmetric Gaussian bump
            if x >= 0:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.95 ** 2))
            else:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.75 ** 2))
            # left positive shoulder (broad Gaussian centered ~-3.3)
            if x < 0:
                bump += 0.008 * math.exp(-((x + 3.3) ** 2) / (2 * 1.6 ** 2))
            # far-field baseline
            if x < -15:
                base = -0.004 * (1 - math.exp(-(abs(x) - 15) / 15.0))
            elif x > 6:
                base = -0.0002 * (1 - math.exp(-(x - 6) / 10.0))
            else:
                base = 0.0
            # negative dip around x~12.5
            dip = -0.004 * math.exp(-((x - 12.5) ** 2) / (2 * 2.5 ** 2))
            v = bump + base + dip
        except Exception:
            v = None
        ys.append(v)
    return {"y": ys}
