import math

def predict(probe):
    # Beliefs (revised v7):
    # Central bump: peak 0.3868 at x=0, asymmetric Gaussian.
    #   left sigma ~1.05, right sigma ~0.95 [E4,E6,E8,E14]
    #   y(-1)=0.197, y(-1.5)=0.105, y(-2)=0.0575, y(-3)=0.008, y(-4)=0.0053
    #   y(1)=0.255, y(1.5)=0.1875, y(2)=0.12, y(3)=0.0327, y(4)=0.0099
    # Positive shoulder: linear ramp from x=-6 (0) to x=-3 (0.008), then
    #   merges into bump flank; peak ~0.0066 at x=-3.5 [E8,E14]
    # Negative undershoot: smooth dip, min ~-0.0061 at x=12, returns to
    #   flat tail ~-0.0004 by x=22 [E10,E12]
    # Far negative tail: saturates ~-0.0044 at x<=-128, ~-0.0032 at -50,
    #   ~-0.0005 at -12, ~0 at -6 [E2,E5,E7,E9,E15]
    # Far positive tail: ~-0.0001 to -0.0004, nearly flat [E3,E5,E7,E9]
    x = probe.get("x", [])
    ys = []
    for v in x:
        try:
            v = float(v)
            # central asymmetric bump
            if v <= 0:
                main = 0.3868 * math.exp(-(v*v) / (2*1.05*1.05))
            else:
                main = 0.3868 * math.exp(-(v*v) / (2*0.95*0.95))
            # positive shoulder: ramp from -6 to -3, ~0.008 at -3
            if v < -3.0:
                shoulder = 0.008 * (v + 6.0) / 3.0
                if shoulder < 0:
                    shoulder = 0.0
            else:
                shoulder = 0.0
            # negative undershoot dip near x=12, width ~5
            under = -0.0061 * math.exp(-((v - 12.0)**2) / (2*4.5*4.5))
            # negative tail for x<0, saturating ~-0.0044 far out
            tail = -0.0044 / (1.0 + math.exp((v + 40.0) / 12.0))
            # small negative floor for large positive x
            floor = -0.00015 * (1.0 - math.exp(-max(v,0)/20.0)) if v > 0 else 0.0
            ys.append(main + shoulder + under + tail + floor)
        except Exception:
            ys.append(None)
    return {"y": ys}
