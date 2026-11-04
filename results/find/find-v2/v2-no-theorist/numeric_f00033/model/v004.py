import math

def predict(probe):
    # Beliefs:
    # - Positive bump peaks near x=0: y(0)=0.387, y(-1)=0.197, y(0.5)=0.323, y(1)=0.255 [E4]
    #   Asymmetric: falls faster to the right than left. Right side ~Gaussian sigma~1.4 centered ~0.
    #   Left side wider (y(-1)=0.197 still high). Use asymmetric Gaussian.
    # - Right tail: y(2)=0.12, y(3)=0.033, y(4)=0.010, y(5)=0.0012, y(6)=0.0001 [E2,E4]
    # - Negative trough centered ~12: y(12)=-0.0061, y(14)=-0.0049, y(10)=-0.0043 [E2]
    # - Recovers to ~-0.0004 plateau for x>=25 [E2]
    # - Left side: y(-6)=0.0, y(-20.3)=-0.0013, y(-24.3)=-0.0016 [E1]
    # - Broad negative dip on left ~-55: y(-50.4..-63.9)~-0.0032 [E1,E3]
    # - Far right: y(66..123.6)~-0.0002 to -0.0001 [E1,E3]
    # - Baseline ~-0.0003
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            # asymmetric positive bump centered ~0
            if x >= 0:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 1.35 ** 2))
            else:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 2.0 ** 2))
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
