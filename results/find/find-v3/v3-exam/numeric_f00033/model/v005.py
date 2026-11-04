import math

def predict(probe):
    # A: sharp central bump, peak ~0.387 at x=0 [E2,E4]
    # B: bump is asymmetric: left sigma ~0.75, right sigma ~0.95 [E4,E6]
    #    left:  f(-2)=0.0575, f(-1)=0.197, f(-0.5)=0.305, f(0)=0.387
    #    right: f(0.3)=0.35, f(0.6)=0.309, f(1)=0.255, f(1.5)=0.1875, f(2)=0.12
    # C: LEFT tail has a positive shoulder: f(-3)=0.008, f(-4)=0.0053,
    #    f(-5)=0.0027, f(-5.5)=0.0014, f(-6)=0.0, f(-7)=-0.0001 [E6]
    #    RIGHT tail goes negative: f(8)=-0.0021, f(9)=-0.0032, f(11)=-0.0054 [E4]
    # D: far negative baseline ~-0.004 for x<-30, ~0 for x>25 [E2,E5]
    #    negative side: -0.0044 at -128, -0.003 at -40, -0.0021 at -30 [E2]
    #    positive side: ~-0.0003 for large x [E2,E3,E5]
    # E: NEGATIVE dip near x~12-13: f(12.5)=-0.0058 [E7], deeper than far baseline
    #    f(10)=-0.0043 [E2], f(15)=-0.0043 [E2] -> local dip around x~12.5
    # F: positive bump near x~-6: f(-5.9)=+0.0003 [E7] (shoulder extends)
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # central asymmetric Gaussian bump
            if x >= 0:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.95 ** 2))
            else:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.75 ** 2))
            # left positive shoulder (extends the left tail)
            if x < 0:
                bump += 0.008 * math.exp(-((x + 3.0) ** 2) / (2 * 1.5 ** 2))
            # far-field baseline
            if x < -15:
                base = -0.004 * (1 - math.exp(-(abs(x) - 15) / 15.0))
            elif x > 6:
                base = -0.0003 * (1 - math.exp(-(x - 6) / 10.0))
            else:
                base = 0.0
            # negative dip around x~12.5
            dip = -0.004 * math.exp(-((x - 12.5) ** 2) / (2 * 2.5 ** 2))
            v = bump + base + dip
        except Exception:
            v = None
        ys.append(v)
    return {"y": ys}
