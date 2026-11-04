def predict(probe):
    # f is a smooth bump peaking ~0.387 near x=0, slightly asymmetric [E1,E2,E7,E8]
    # Peak is at x~-0.05 (0.3884 at -0.05 vs 0.3868 at 0), left flank slightly higher [E7]
    # Right flank: bump decays, crosses zero ~x=6, negative dip min ~-0.0062 at x~11.75 [E3,E4,E6]
    # Dip recovers to ~-0.0004 by x~22, then rises slowly toward 0 at x=128 [E5,E6]
    # Left flank: bump decays to ~0 at x~-6, then small negative tail growing to ~-0.0044 at -128 [E1,E5,E9]
    # Left tail: -0.0004 at -10, -0.0016 at -24, -0.003 at -40, -0.0044 at -128 [E5,E9]
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                # main bump: Gaussian, w~1.85 fits 1->0.255, 2->0.12, 3->0.0327 [E2]
                bump = 0.3868 * math.exp(-(x/1.85)**2)
                # negative dip: min ~-0.0062 at x~11.75, zero-cross ~6, back to ~-0.0004 by ~22 [E3,E4,E6]
                dip = -0.0062 * math.exp(-((x-11.75)/4.2)**2)
                # far-right baseline: -0.0004 plateau then rising toward 0 at x=128 [E5]
                if x < 40:
                    base = -0.0004 * (1 - math.exp(-(x/20.0)**2))
                else:
                    base = -0.0004 * math.exp(-((x-40)/60.0)**2)
                y = bump + dip + base
            else:
                a = abs(x)
                # left flank: stretched exponential, a=1.25, p=1.30 fits -1..-4 [E2]
                # but decays faster: -5->0.0027, -6->0.0, -8->-0.0002, -10->-0.0004 [E9]
                y = 0.3868 * math.exp(-((a/1.25)**1.30))
                # left negative tail: grows from ~0 at -6 to -0.0044 at -128 [E5,E9]
                # -10->-0.0004, -24->-0.0016, -40->-0.003, -128->-0.0044
                if a > 6:
                    tail = -0.0046 * (1 - math.exp(-((a-6)/45.0)**1.3))
                    y += tail
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
