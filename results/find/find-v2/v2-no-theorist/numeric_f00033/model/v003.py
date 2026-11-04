import math

def predict(probe):
    # Beliefs:
    # - Sharp positive spike near x~1.2: y(1.2)=0.228 [E3]; y(2.9)=0.036, y(3)=0.033 [E1,E2]
    #   So the peak is very narrow and centered near x~1, not x~3.
    # - Decay to the right: y(4)=0.0099, y(5)=0.0012, y(6)=0.0001 [E2]
    # - Negative trough centered ~12: y(12)=-0.0061, y(14)=-0.0049, y(10)=-0.0043 [E2]
    # - Recovers to small negative plateau ~-0.0004 for x>=25 [E2]
    # - Left side: y(-6)=0.0, y(-20.3)=-0.0013, y(-24.3)=-0.0016 [E1]
    # - Broad negative dip on left ~-55: y(-50.4)=-0.0032, y(-55.8)=-0.0032, y(-61.7)=-0.0032, y(-63.9)=-0.0033 [E1,E3]
    # - Far right: y(66)=-0.0003, y(72.7)=-0.0003, y(88.2)=-0.0002, y(104.5)=-0.0001, y(123.6)=-0.0001 [E1,E3]
    # - Baseline ~-0.0003 to -0.0004
    # Model: narrow positive Gaussian at x~1 + negative trough at x~12
    #        + broad negative dip on left centered ~-57 + small negative baseline.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            # narrow positive spike centered ~1.2, width ~1.0
            # fits 1.2->0.228, 2.9->0.036, 3->0.033, 4->0.010, 5->0.0012
            bump = 0.228 * math.exp(-((x - 1.2) ** 2) / (2 * 1.0 ** 2))
            # negative trough centered ~12, width ~5
            trough = -0.0062 * math.exp(-((x - 12.0) ** 2) / (2 * 5.0 ** 2))
            # broad negative dip on the left, centered ~-57, width ~15
            leftdip = -0.0032 * math.exp(-((x + 57.0) ** 2) / (2 * 15.0 ** 2))
            # small negative baseline
            base = -0.0003
            y = bump + trough + leftdip + base
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
