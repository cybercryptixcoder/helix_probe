import math

def predict(probe):
    # Beliefs:
    # - Main feature: a bump peaking near x~3, value ~0.033 at x=3 [E1, E2]
    # - Decay is steep: y(4)=0.0099, y(5)=0.0012, y(6)=0.0001 [E2]
    # - Then goes NEGATIVE, reaching a trough ~-0.0061 at x=12 [E2]
    # - Recovers to a small negative plateau ~-0.0004 for x>=25 [E2]
    # - Left side: y(-6)=0.0, y(-20.3)=-0.0013, y(-24.3)=-0.0016 [E1]
    # - Far left: y(-50.4)=-0.0032, y(-61.7)=-0.0032 [E1]
    # - Far right: y(66)=-0.0003, y(72.7)=-0.0003, y(88.2)=-0.0002 [E1]
    # - So there's a broad negative dip on the left around x~-50, and a
    #   negative trough on the right around x~12. Asymmetric.
    # Model: positive Gaussian bump at x~3 + negative Gaussian trough at x~12
    #        + broad negative dip on left + small negative baseline.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            # positive bump centered ~3, width ~1.3 (fits 3->0.033, 4->0.010, 5->0.0012)
            bump = 0.033 * math.exp(-((x - 3.0) ** 2) / (2 * 1.3 ** 2))
            # negative trough centered ~12, width ~5 (fits -0.0061 at 12, ~0 at 6 and 20)
            trough = -0.0062 * math.exp(-((x - 12.0) ** 2) / (2 * 5.0 ** 2))
            # broad negative dip on the left, centered ~-55, width ~15
            leftdip = -0.0032 * math.exp(-((x + 55.0) ** 2) / (2 * 15.0 ** 2))
            # small negative baseline
            base = -0.0003
            y = bump + trough + leftdip + base
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
