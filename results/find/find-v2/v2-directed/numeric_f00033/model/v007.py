def predict(probe):
    # f is a smooth bump peaking ~0.3884 near x=-0.05, asymmetric [E7,E8]
    # Right flank is a clean Gaussian: 0.3868*exp(-(x/2.05)^2) fits 1->0.255,2->0.12,3->0.0327,4->0.0099 [E2,E14]
    #   check: exp(-(1/2.05)^2)=0.788->0.305 (obs 0.255)... use sigma from E14: 0.6->0.309,1.5->0.1875,2.5->0.0642
    #   ln(0.309/0.3868)=-0.224 -> (0.6/s)^2=0.224 -> s=1.268; 1.5: ln(0.1875/0.3868)=-0.724 -> s=1.76; not pure Gaussian
    # Right flank decays faster than Gaussian at small x, slower at large x: use stretched exp p~1.5 [E14]
    # Left flank: -1->0.1972,-2->0.0575,-3->0.008,-4->0.0053,-5->0.0027,-6->0 [E11,E13]
    #   -1: ln(0.1972/0.3884)=-0.678; -2: -1.91; -3: -3.88; -4: -4.29; -5: -4.97
    #   steep drop 1->3 then slow tail 3->6: stretched exp p~1.6 s~1.35 plus small shoulder
    # Right negative dip: min ~-0.0062 at x~11.75, zero-cross ~6, recovers to -0.0004 by ~22 [E3,E4,E6,E12]
    # Far-right baseline: -0.0004 plateau, rises to 0 at x=128 [E5]
    # Left negative tail: ~0 at -6, grows to -0.0044 at -128 [E5,E9]
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                # right flank: stretched exp, p~1.5, s~1.75; fits 0.6->0.309,1.5->0.1875,2.5->0.0642,4->0.0099
                bump = 0.3868 * math.exp(-((x/1.75)**1.5))
                # negative dip: min ~-0.0062 at x~11.75, zero-cross ~6, back to ~-0.0004 by ~22 [E3,E4,E6,E12]
                dip = -0.0062 * math.exp(-((x-11.75)/4.2)**2)
                # far-right baseline: -0.0004 plateau then rising toward 0 at x=128 [E5]
                if x < 40:
                    base = -0.0004 * (1 - math.exp(-(x/20.0)**2))
                else:
                    base = -0.0004 * math.exp(-((x-40)/60.0)**2)
                y = bump + dip + base
            else:
                a = abs(x)
                # left flank: stretched exp p~1.6 s~1.35 gives -1->0.197,-2->0.0575,-3->0.008 [E11,E13]
                # but -4->0.0053,-5->0.0027 are higher than that predicts; add small shoulder tail
                y = 0.3884 * math.exp(-((a/1.35)**1.6))
                # shoulder: extra ~0.005 decaying slowly from a~3 to a~6 [E11]
                if a > 2.5:
                    y += 0.006 * math.exp(-((a-3.0)/2.5)**2) * (a > 2.5)
                # left negative tail: grows from ~0 at -6 to -0.0044 at -128 [E5,E9]
                if a > 6:
                    tail = -0.0046 * (1 - math.exp(-((a-6)/45.0)**1.3))
                    y += tail
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
