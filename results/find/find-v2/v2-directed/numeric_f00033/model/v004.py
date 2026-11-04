def predict(probe):
    # f is a smooth asymmetric bump peaking ~0.387 at x=0 [E1,E2]
    # Right side: Gaussian-ish decay, zero-cross ~x=6, negative dip min ~-0.0061 at x~12, recovers to ~-0.0004 by x~24 [E2,E3,E4]
    # Left side: decays to zero ~x=-6, small negative tail far out (~-0.004 at -128) [E1,E2,E4]
    # Far tails: right ~-0.0004, left ~-0.004 [E1,E3]
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                # main bump: Gaussian, w~1.85 fits 1->0.255, 2->0.12, 3->0.0327 [E2]
                bump = 0.3868 * math.exp(-(x/1.85)**2)
                # negative dip: min ~-0.0061 at x~12, zero-cross ~6, back to ~-0.0004 by ~24 [E3,E4]
                # E4 shows dip: 8.5->-0.0026, 10.5->-0.0048, 11.5->-0.0059, 12.5->-0.0058, 14.5->-0.0046, 17->-0.0031, 19->-0.0019
                # Gaussian centered ~12, w~4.5, A~0.0061
                dip = -0.0061 * math.exp(-((x-12.0)/4.5)**2)
                # far-right baseline ~-0.0004 [E1,E3]
                base = -0.0004 * (1 - math.exp(-(x/20.0)**2))
                y = bump + dip + base
            else:
                # left side: stretched exponential, a=1.25, p=1.30 fits -1..-4 [E2]
                y = 0.3868 * math.exp(-((abs(x)/1.25)**1.30))
                # small negative baseline far out on left (~-0.004 at -128) [E1,E4]
                if abs(x) > 20:
                    y -= 0.004 * min(1.0, (abs(x)-20)/40.0)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
