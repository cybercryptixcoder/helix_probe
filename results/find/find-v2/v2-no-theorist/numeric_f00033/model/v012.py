import math

def predict(probe):
    # Beliefs (revised after E17):
    # - Central bump: sharp peak 0.3868 at x=0. Right flank LINEAR slope ~-0.133
    #   from 0 to ~1.4 (y(1.4)=0.201), then smooth decay to ~0 by x~6 [E4,E10,E12,E14].
    #   Left flank LINEAR slope ~-0.145 from 0 to ~-1.3 (y(-1.3)=0.1383), then decay [E6,E8,E10,E14].
    # - Negative trough centered ~11.5, peak depth ~-0.0061, sigma ~4.5;
    #   returns to plateau -0.0004 by x~22 [E12,E16].
    # - Plateau ~-0.0004 for x in [22, ~40] [E2,E13,E16].
    # - Left broad dip: deepens toward far left, ~-0.0032 around -45..-80,
    #   then -0.0044 at -128 [E1,E3,E5,E6,E7,E9,E15].
    # - Far right (x>~40): y ~ -0.0001 to -0.0003, trending to ~-0.0001 at large x [E1,E3,E5,E7,E9,E15,E17].
    # - Baseline ~-0.0003 near x in [0,40] outside features.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            # Central bump
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
            trough = -0.0061 * math.exp(-((x - 11.5) ** 2) / (2 * 4.5 ** 2))
            # Left broad dip
            if x < 0:
                leftdip = -0.0032 * (1 - math.exp(-((x + 6.0) ** 2) / (2 * 22.0 ** 2)))
                leftdip -= 0.0012 * (1 - math.exp(-((x + 50.0) ** 2) / (2 * 40.0 ** 2)))
            else:
                leftdip = 0.0
            # Baseline: ~-0.0003 near center, drifting to ~-0.0001 far right
            if x > 40:
                base = -0.0003 + 0.0002 * (1 - math.exp(-((x - 40.0) ** 2) / (2 * 40.0 ** 2)))
            else:
                base = -0.0003
            y = bump + trough + leftdip + base
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
