import math

def predict(probe):
    # Beliefs (revised from E1-E4):
    # - Large positive bump centered near x=0, roughly symmetric, peak ~0.36-0.39 at x=0 [E2,E4]
    # - Bump is asymmetric: slightly higher on negative side, wider on negative side [E4]
    # - Negative undershoot on both sides of bump: ~-0.004 to -0.005 near x=10-14 [E4]
    # - Far negative tail saturates ~-0.0044 at x=-128, ~-0.003 at x=-40 [E2]
    # - Far positive tail ~-0.0003 to -0.0004 [E1,E3,E4]
    # - Small positive bump near x=1-3 (~0.03-0.23) [E1,E2,E3]
    # - Model: asymmetric Gaussian bump + negative undershoot + sigmoid negative tail + small positive shoulder
    x = probe.get("x", [])
    ys = []
    for v in x:
        try:
            v = float(v)
            # Main bump: asymmetric Gaussian centered ~0, peak ~0.37
            # negative side wider (sigma~0.9), positive side narrower (sigma~0.75)
            if v <= 0:
                main = 0.375 * math.exp(-(v*v) / (2*0.95*0.95))
            else:
                main = 0.365 * math.exp(-(v*v) / (2*0.80*0.80))
            # Small positive shoulder near x~1-3 (adds to bump region)
            shoulder = 0.02 * math.exp(-((v - 2.0)**2) / 4.0)
            # Negative undershoot near x~10-14
            under = -0.005 * math.exp(-((v - 12.0)**2) / 30.0)
            # Negative tail for x<0, saturating ~-0.0044 far out
            tail = -0.0044 / (1.0 + math.exp((v + 45.0) / 15.0))
            # Small negative floor for large positive x
            floor = -0.00035 * (1.0 - math.exp(-max(v,0)/20.0)) if v > 0 else 0.0
            ys.append(main + shoulder + under + tail + floor)
        except Exception:
            ys.append(None)
    return {"y": ys}
