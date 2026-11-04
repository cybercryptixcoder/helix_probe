import math

def predict(probe):
    # Beliefs:
    # - Positive bump centered ~0: y(0)=0.387, y(-1)=0.197, y(0.5)=0.323, y(1)=0.255,
    #   y(1.2)=0.228, y(1.5)=0.188, y(2)=0.12, y(2.5)=0.064, y(3)=0.033, y(3.5)=0.019,
    #   y(4)=0.010, y(5)=0.0012, y(6)=0.0001 [E1,E2,E4]
    #   Asymmetric: left side wider than right. Right ~Gaussian sigma~1.4; left sigma~2.0.
    # - Negative trough centered ~12: y(10)=-0.0043, y(12)=-0.0061, y(14)=-0.0049,
    #   y(16)=-0.0037, y(18)=-0.0025, y(20)=-0.0013 [E2]
    # - Plateau ~-0.0004 for x>=25 [E2]
    # - Left dip: y(-7.1)=-0.0001, y(-16.9)=-0.001, y(-20.3)=-0.0013, y(-24.3)=-0.0016,
    #   y(-48.6)=-0.0032, y(-50.4)=-0.0032, y(-55.8)=-0.0032, y(-61.7)=-0.0032,
    #   y(-63.9)=-0.0033, y(-102.2)=-0.004 [E1,E3,E5]
    #   Broad negative dip on left, deepening toward far left.
    # - Far right: y(66..123.6)~-0.0001 to -0.0003 [E1,E3,E5]
    # - Baseline ~-0.0003
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            # asymmetric positive bump centered ~0
            if x >= 0:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 1.4 ** 2))
            else:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 2.0 ** 2))
            # negative trough centered ~12, width ~5
            trough = -0.0062 * math.exp(-((x - 12.0) ** 2) / (2 * 5.0 ** 2))
            # broad negative dip on the left, deepening toward far left
            if x < 0:
                leftdip = -0.0032 * (1 - math.exp(-((x + 20.0) ** 2) / (2 * 30.0 ** 2)))
                leftdip -= 0.0008 * math.exp(-((x + 102.0) ** 2) / (2 * 20.0 ** 2))
            else:
                leftdip = 0.0
            # small negative baseline
            base = -0.0003
            y = bump + trough + leftdip + base
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
