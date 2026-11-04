def predict(probe):
    # f is a smooth bump peaking ~0.387 at x=0, asymmetric [E1, E2]
    # Right side decays to a NEGATIVE dip: crosses zero ~x=6, min ~-0.006 at x~12, recovers to ~-0.0004 by x~24 [E3]
    # Left side decays to ~0 by x=-6, then small negative baseline far out [E1, E2]
    # Far tails approach ~-0.0004 on the right, ~-0.004 on the left [E1, E3]
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                # main bump: Gaussian-ish, w~1.85 gives 1->0.289, 2->0.121, 3->0.0275 [E2]
                bump = 0.387 * math.exp(-(x/1.85)**2)
                # negative dip on right: min ~-0.0061 at x=12, zero-cross ~6, back to ~-0.0004 by 24 [E3]
                # model as -A*exp(-((x-c)/w)^2) with c=12, A=0.0061, w~5
                dip = -0.0061 * math.exp(-((x-12.0)/5.0)**2)
                # far-right baseline ~-0.0004 [E1, E3]
                base = -0.0004 * (1 - math.exp(-(x/20.0)**2))
                y = bump + dip + base
            else:
                # left side: stretched exponential, a=1.25, p=1.30 fits -1..-4 [E2]
                y = 0.387 * math.exp(-((abs(x)/1.25)**1.30))
                # small negative baseline far out on left (~-0.004 at -128) [E1]
                if abs(x) > 20:
                    y -= 0.004 * min(1.0, (abs(x)-20)/40.0)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
