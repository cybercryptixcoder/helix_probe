import math

def predict(probe):
    # Beliefs:
    # - Central positive bump, asymmetric. Peak ~0.387 at x=0 [E4].
    #   Right flank: y(0.5)=0.3225, y(1)=0.255, y(1.5)=0.1875, y(2)=0.12,
    #   y(2.5)=0.0642, y(3)=0.0327, y(3.5)=0.0185, y(4)=0.0099, y(5)=0.0012,
    #   y(6)=0.0001 [E2,E4]. ~Gaussian sigma~1.4.
    # - Left flank steeper: y(-0.2)=0.3701, y(-0.4)=0.3268, y(-0.6)=0.2836,
    #   y(-0.8)=0.2404, y(-1)=0.1972, y(-1.2)=0.1552, y(-1.4)=0.1218,
    #   y(-1.6)=0.0919, y(-1.8)=0.0739, y(-2)=0.0575, y(-2.2)=0.0411,
    #   y(-2.4)=0.0264, y(-2.5)=0.0221, y(-2.8)=0.0089, y(-3)=0.008,
    #   y(-3.2)=0.0074, y(-3.6)=0.0064, y(-4)=0.0053, y(-4.5)=0.004,
    #   y(-5)=0.0027, y(-5.5)=0.0014, y(-6)=0.0 [E4,E6,E8].
    #   ~Gaussian sigma~0.9, but with a small positive tail/floor ~0.005
    #   around x=-3..-4.5 [E8].
    # - Negative trough centered ~12: y(10)=-0.0043, y(12)=-0.0061, y(14)=-0.0049,
    #   y(16)=-0.0037, y(18)=-0.0025, y(20)=-0.0013 [E2].
    # - Plateau ~-0.0004 for x>=25 [E2].
    # - Left dip deepens monotonically toward far left: y(-7)=-0.0001,
    #   y(-16.9)=-0.001, y(-20.3)=-0.0013, y(-24.3)=-0.0016, y(-48.6)=-0.0032,
    #   y(-61.7)=-0.0032, y(-102.2)=-0.004, y(-124.4)=-0.0044 [E1,E3,E5,E6,E7]
    #   Saturates ~-0.0032 around x=-50..-62, then deepens again toward far left.
    # - Far right: y(66..123.6)~-0.0001 to -0.0003 [E1,E3,E5]
    # - Baseline ~-0.0003
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if x >= 0:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 1.4 ** 2))
            else:
                bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.9 ** 2))
                # small positive tail floor around x=-3..-4.5 [E8]
                bump += 0.005 * math.exp(-((x + 3.8) ** 2) / (2 * 0.9 ** 2))
            trough = -0.0062 * math.exp(-((x - 12.0) ** 2) / (2 * 5.0 ** 2))
            if x < 0:
                leftdip = -0.0032 * (1 - math.exp(-((x + 6.0) ** 2) / (2 * 22.0 ** 2)))
                leftdip -= 0.0012 * (1 - math.exp(-((x + 50.0) ** 2) / (2 * 40.0 ** 2)))
            else:
                leftdip = 0.0
            base = -0.0003
            y = bump + trough + leftdip + base
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
