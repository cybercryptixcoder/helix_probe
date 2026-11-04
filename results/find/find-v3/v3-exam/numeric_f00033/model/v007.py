import math

def predict(probe):
    # A: central bump peak ~0.387 at x=0 [E4,E8,E10]
    # B: bump is asymmetric: left sigma ~0.85, right sigma ~0.95 [E10]
    #    E10: f(-1.9)=0.066, f(-1.4)=0.122, f(-0.9)=0.219, f(-0.4)=0.327, f(0.2)=0.363
    #    right: f(0.7)=0.296, f(1.3)=0.215, f(2.2)=0.094, f(3.2)=0.026 [E10]
    # C: LEFT positive shoulder: broad Gaussian ~center -3.3, sigma~1.5, amp~0.008 [E6,E8]
    #    f(-6)=0, f(-5)=0.0027, f(-4)=0.0053, f(-3)=0.008, f(-2.5)=0.022 [E6,E8]
    # D: far negative baseline ~-0.004 for x<-30, ~-0.0002 for x>25 [E2,E5,E9,E11]
    # E: NEGATIVE dip near x~12.5: f(12.5)=-0.0058, f(13.1)=-0.0055, f(12.1)=-0.0061 [E7,E11]
    #    dip is narrow-ish, centered ~12.5, sigma~2 [E7,E11]
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
            # left positive shoulder (broad Gaussian centered ~-3.3)
            if x < 0:
                bump += 0.008 * math.exp(-((x + 3.3) ** 2) / (2 * 1.5 ** 2))
            # far-field baseline
            if x < -15:
                base = -0.004 * (1 - math.exp(-(abs(x) - 15) / 15.0))
            elif x > 6:
                base = -0.0002 * (1 - math.exp(-(x - 6) / 10.0))
            else:
                base = 0.0
            # negative dip around x~12.5
            dip = -0.0055 * math.exp(-((x - 12.5) ** 2) / (2 * 2.0 ** 2))
            v = bump + base + dip
        except Exception:
            v = None
        ys.append(v)
    return {"y": ys}
