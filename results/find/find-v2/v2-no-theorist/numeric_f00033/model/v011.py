import math

def predict(probe):
    # Beliefs (revised after E14):
    # - Central bump peaks 0.3868 at x=0, sharp peak (not flat) [E4,E14].
    #   Right flank: y(0.1)=0.376, y(0.3)=0.3496, y(0.4)=0.3361, y(0.6)=0.309,
    #   y(0.8)=0.282, y(1.0)=0.255, y(1.2)=0.228, y(1.4)=0.201, y(1.6)=0.174,
    #   y(1.8)=0.147, y(2)=0.12, y(2.2)=0.0941, y(2.5)=0.0642, y(3)=0.0327,
    #   y(3.5)=0.0185, y(4)=0.0099, y(5)=0.0012, y(6)=0.0001 [E2,E4,E10,E12,E14].
    #   Right flank is nearly LINEAR from 0 to ~1.4 (slope ~-0.133/unit),
    #   then decays. Model as piecewise-linear then exponential tail.
    # - Left flank: y(-0.1)=0.3855, y(-0.2)=0.3701, y(-0.3)=0.3484, y(-0.5)=0.3052,
    #   y(-0.7)=0.262, y(-0.9)=0.2188, y(-1)=0.1972, y(-1.3)=0.1383,
    #   y(-1.7)=0.0821, y(-2)=0.0575, y(-2.5)=0.0221, y(-3)=0.008,
    #   y(-4)=0.0053, y(-5)=0.0027, y(-6)=0.0 [E4,E6,E8,E10,E14].
    #   Left flank also nearly linear from 0 to ~-1.3 (slope ~-0.145/unit).
    # - Negative trough centered ~11.5: y(6.5)=-0.0005, y(8)=-0.0021,
    #   y(10)=-0.0043, y(11)=-0.0054, y(12)=-0.0061, y(14)=-0.0049,
    #   y(16)=-0.0037, y(18)=-0.0025, y(20)=-0.0013 [E2,E11,E12,E13].
    # - Plateau ~-0.0004 for x>=22 [E2,E13].
    # - Left broad dip deepens toward far left, saturates ~-0.0032 around -50..-67,
    #   then deepens to -0.0044 at -128 [E1,E3,E5,E6,E7,E9].
    # - Far right: y~-0.0001 to -0.0003 [E1,E3,E5,E7,E9].
    # - Baseline ~-0.0003.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            # Central bump: piecewise-linear near peak, exponential tail.
            if x >= 0:
                if x <= 1.4:
                    bump = 0.3868 - 0.1327 * x
                else:
                    bump = 0.201 * math.exp(-((x - 1.4) ** 2) / (2 * 1.15 ** 2))
            else:
                ax = -x
                if ax <= 1.3:
                    bump = 0.3868 - 0.1912 * ax
                else:
                    bump = 0.1383 * math.exp(-((ax - 1.3) ** 2) / (2 * 1.0 ** 2))
                    bump += 0.004 * math.exp(-((x + 3.8) ** 2) / (2 * 0.9 ** 2))
            # Negative trough centered ~11.5, sigma ~4.5
            trough = -0.0062 * math.exp(-((x - 11.5) ** 2) / (2 * 4.5 ** 2))
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
