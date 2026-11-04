def predict(probe):
    # f is a smooth bump peaking ~0.3884 near x=-0.05, asymmetric [E7,E8]
    # Peak at x~-0.05; left flank slightly higher than right at same |x| [E7,E8]
    # Right flank: bump decays, crosses zero ~x=6, negative dip min ~-0.0062 at x~11.75 [E3,E4,E6]
    # Dip recovers to ~-0.0004 by x~22, stays ~-0.0004 plateau, rises to 0 at x=128 [E5,E6]
    # Left flank: bump decays to ~0 at x~-6, then small negative tail to ~-0.0044 at -128 [E1,E5,E9]
    # Left flank between -1 and -6: smooth decay, ~0.2512 at -0.75, 0.1972 at -1, 0.0575 at -2, 0.008 at -3, 0.0027 at -5, 0 at -6 [E11]
    # Left flank is NOT stretched-exp; it's closer to Gaussian with sigma~1.55 on left [E11]
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                # main bump: Gaussian, sigma~1.85 fits 1->0.255, 2->0.12, 3->0.0327 [E2]
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
                # left flank: Gaussian sigma~1.55 fits -0.75->0.2512, -1->0.1972, -2->0.0575, -3->0.008, -5->0.0027 [E11]
                # check: 0.3868*exp(-(0.75/1.55)^2)=0.3868*exp(-0.234)=0.306 too high; try sigma 1.45
                # 0.3868*exp(-(0.75/1.45)^2)=0.3868*exp(-0.2675)=0.296 still high
                # Use a slightly lower amplitude on left? peak at -0.05 is 0.3884
                # fit -1->0.1972: exp(-(1/s)^2)=0.1972/0.3884=0.5077 -> (1/s)^2=0.678 -> s=1.215
                # fit -2->0.0575: exp(-(2/s)^2)=0.148 -> (2/s)^2=1.91 -> s=1.447
                # fit -3->0.008: exp(-(3/s)^2)=0.0206 -> (3/s)^2=3.88 -> s=1.523
                # fit -5->0.0027: exp(-(5/s)^2)=0.00695 -> (5/s)^2=4.97 -> s=2.24 (too flat, tail takes over)
                # Use stretched exp with p~1.6, s~1.35
                y = 0.3884 * math.exp(-((a/1.35)**1.6))
                # left negative tail: grows from ~0 at -6 to -0.0044 at -128 [E5,E9]
                if a > 6:
                    tail = -0.0046 * (1 - math.exp(-((a-6)/45.0)**1.3))
                    y += tail
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
