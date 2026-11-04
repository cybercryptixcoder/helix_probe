import math

def predict(probe):
    # Beliefs:
    # - Main positive bump centered at 0, peak ~0.387 at x=0 [E2,E4]
    # - Bump asymmetric: negative side wider (sigma~1.0), positive side narrower (sigma~0.85) [E4]
    # - Negative undershoot on both sides: ~-0.004 to -0.006 near x=10-16 [E2,E4]
    # - Far negative tail saturates ~-0.0044 at x=-128, ~-0.003 at x=-40 [E2]
    # - Far positive tail ~-0.0001 to -0.0004, flatter than v2 (nearly -0.0001 at large x) [E3,E5]
    # - Small positive shoulder near x=1-3 [E1,E2,E3]
    # - Mid-negative region x~-7 to -17 dips to ~-0.001 [E5]
    x = probe.get("x", [])
    ys = []
    for v in x:
        try:
            v = float(v)
            if v <= 0:
                main = 0.387 * math.exp(-(v*v) / (2*1.0*1.0))
            else:
                main = 0.375 * math.exp(-(v*v) / (2*0.85*0.85))
            shoulder = 0.02 * math.exp(-((v - 2.0)**2) / 4.0)
            under = -0.006 * math.exp(-((v - 13.0)**2) / 40.0)
            # negative tail for x<0, saturating ~-0.0044 far out
            tail = -0.0044 / (1.0 + math.exp((v + 45.0) / 15.0))
            # small negative floor for large positive x, approaching ~-0.0001
            floor = -0.00012 * (1.0 - math.exp(-max(v,0)/15.0)) if v > 0 else 0.0
            ys.append(main + shoulder + under + tail + floor)
        except Exception:
            ys.append(None)
    return {"y": ys}
