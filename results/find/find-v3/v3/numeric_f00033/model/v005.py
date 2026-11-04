import math

def predict(probe):
    # Beliefs:
    # - Central bump peaks ~0.387 at x=0 [E2,E6]
    # - Bump is asymmetric: negative side wider, positive side narrower [E4,E6]
    #   left half-width: y(-1)=0.197, y(-1.5)=0.105, y(-2)=0.0575, y(-3)=0.008
    #   right half-width: y(1)=0.255, y(1.5)=0.1875, y(2)=0.12, y(3)=0.0327
    # - Negative undershoot: dip ~-0.006 near x=12-14, ~-0.003 near x=9 [E2,E4,E6]
    # - Far negative tail saturates ~-0.0044 at x=-128, ~-0.003 at x=-40 [E2]
    # - Far positive tail ~-0.0001 to -0.0004, nearly flat [E3,E5]
    # - Small positive shoulder near x=2-3 [E1,E6]
    # - Near x=-6 the value is slightly positive ~0.0003 [E7] (not negative)
    x = probe.get("x", [])
    ys = []
    for v in x:
        try:
            v = float(v)
            if v <= 0:
                main = 0.387 * math.exp(-(v*v) / (2*1.15*1.15))
            else:
                main = 0.387 * math.exp(-(v*v) / (2*0.95*0.95))
            # negative undershoot dip near x=12-14
            under = -0.006 * math.exp(-((v - 13.0)**2) / 30.0)
            # negative tail for x<0, saturating ~-0.0044 far out
            tail = -0.0044 / (1.0 + math.exp((v + 45.0) / 15.0))
            # small negative floor for large positive x
            floor = -0.00012 * (1.0 - math.exp(-max(v,0)/15.0)) if v > 0 else 0.0
            # small positive shoulder near x=-6 (bump on the negative flank)
            shoulder = 0.0004 * math.exp(-((v + 6.0)**2) / 8.0)
            ys.append(main + under + tail + floor + shoulder)
        except Exception:
            ys.append(None)
    return {"y": ys}
