import math

def predict(probe):
    # Beliefs (revised):
    # - Central bump peaks ~0.387 at x=0, asymmetric [E2,E4,E6]
    #   left side: y(-1)=0.197, y(-1.5)=0.105, y(-2)=0.0575, y(-3)=0.008, y(-4)=0.0053
    #   right side: y(1)=0.255, y(1.5)=0.1875, y(2)=0.12, y(3)=0.0327, y(4)=0.0099
    #   Left sigma ~1.15, right sigma ~0.95 (Gaussian fits well)
    # - Negative undershoot: dip ~-0.006 near x=12-14, ~-0.003 near x=9 [E2,E4,E6]
    # - Far negative tail saturates ~-0.0044 at x=-128, ~-0.003 at x=-40 [E2,E5,E7,E9]
    # - Far positive tail ~-0.0001 to -0.0004, nearly flat [E3,E5,E7,E9]
    # - Small positive shoulder near x=-5 to -4 (y(-5)=0.0027, y(-4)=0.0053) [E8]
    # - Near x=-6 value ~0.0, x=-7 ~-0.0001 [E8]
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
            # small positive shoulder near x=-5 (bump on the negative flank)
            shoulder = 0.0055 * math.exp(-((v + 4.5)**2) / 1.5)
            ys.append(main + under + tail + floor + shoulder)
        except Exception:
            ys.append(None)
    return {"y": ys}
