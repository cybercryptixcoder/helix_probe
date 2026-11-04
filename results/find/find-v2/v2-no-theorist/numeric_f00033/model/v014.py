import math

def predict(probe):
    # Beliefs (revised after E20):
    # - Central peak 0.3868 at x=0. Right flank LINEAR slope ~-0.133 to x~1.4
    #   (y(1.4)=0.201) [E14]. Left flank LINEAR slope ~-0.19 to x~-1.4
    #   (y(-1.4)=0.1218) [E14,E20].
    # - Left flank: after x=-1.4 the bump decays fast to ~0.009 at x=-2.8,
    #   then a small POSITIVE shoulder ~0.008 at x=-3.0..-3.2, decaying
    #   smoothly to 0 by x=-6 [E20]. So left side is bump + shoulder.
    # - Right flank: fast decay, y(2)=0.12, y(2.8)=0.0397, y(4)=0.0099,
    #   ~0 by x~5 [E18].
    # - Negative trough centered ~12, depth ~-0.0061, sigma ~4.5;
    #   returns to plateau -0.0004 by x~22 [E16].
    # - Plateau ~-0.0004 for x in [22,~40] [E16].
    # - Left broad dip: ~-0.0032 around -45..-80, -0.0044 at -128 [E1,E3,E5,E7,E9,E15].
    # - Far right (x>~40): y ~ -0.0001 to -0.0003 [E1,E3,E5,E7,E9,E15,E17].
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            # Central bump
            if x >= 0:
                if x <= 1.4:
                    bump = 0.3868 - 0.1327 * x
                else:
                    bump = 0.201 * math.exp(-((x - 1.4) ** 2) / (2 * 0.75 ** 2))
            else:
                ax = -x
                if ax <= 1.4:
                    bump = 0.3868 - 0.1893 * ax
                else:
                    # fast decay from 0.1218 at ax=1.4
                    bump = 0.1218 * math.exp(-((ax - 1.4) ** 2) / (2 * 0.55 ** 2))
            # Left shoulder near x=-3 (positive), only on left side
            if x < 0:
                shoulder = 0.008 * math.exp(-((x + 3.1) ** 2) / (2 * 1.1 ** 2))
            else:
                shoulder = 0.0
            # Negative trough centered ~12, sigma ~4.5
            trough = -0.0061 * math.exp(-((x - 12.0) ** 2) / (2 * 4.5 ** 2))
            # Left broad dip
            if x < 0:
                leftdip = -0.0032 * (1 - math.exp(-((x + 6.0) ** 2) / (2 * 22.0 ** 2)))
                leftdip -= 0.0012 * (1 - math.exp(-((x + 50.0) ** 2) / (2 * 40.0 ** 2)))
            else:
                leftdip = 0.0
            # Baseline
            if x > 40:
                base = -0.0003 + 0.0002 * (1 - math.exp(-((x - 40.0) ** 2) / (2 * 40.0 ** 2)))
            else:
                base = -0.0003
            y = bump + shoulder + trough + leftdip + base
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
