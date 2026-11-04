import math

def predict(probe):
    # Beliefs:
    # - Sharp positive bump centered at x=0: y(0)=0.387, y(0.5)=0.322, y(1)=0.255,
    #   y(1.2)=0.228, y(1.5)=0.188, y(2)=0.12, y(2.5)=0.064, y(3)=0.033,
    #   y(3.5)=0.019, y(4)=0.010, y(5)=0.0012, y(6)=0.0001 [E2,E4]
    #   Right flank ~Gaussian sigma~1.4 [E4]
    # - Left flank steeper: y(-0.5)=0.305, y(-1)=0.197, y(-1.5)=0.105, y(-2)=0.058,
    #   y(-2.5)=0.022, y(-3)=0.008, y(-4)=0.005, y(-5)=0.003, y(-6)=0.0 [E4,E6]
    #   ~Gaussian sigma~0.9 [E4,E6]
    # - Negative trough centered ~12: y(10)=-0.0043, y(12)=-0.0061, y(14)=-0.0049,
    #   y(16)=-0.0037, y(18)=-0.0025, y(20)=-0.0013 [E2]
    # - Plateau ~-0.0004 for x>=25 [E2]
    # - Left dip deepens monotonically toward far left: y(-7)=-0.0001, y(-16.9)=-0.001,
    #   y(-20.3)=-0.0013, y(-24.3)=-0.0016, y(-48.6)=-0.0032, y(-61.7)=-0.0032,
    #   y(-102.2)=-0.004, y(-124.4)=-0.0044 [E1,E3,E5,E6,E7]
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
            trough = -0.0062 * math.exp(-((x - 12.0) ** 2) / (2 * 5.0 ** 2))
            if x < 0:
                # left dip: grows from ~0 near x=-6 to ~-0.0032 by x=-50,
                # then keeps deepening slowly toward far left
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
