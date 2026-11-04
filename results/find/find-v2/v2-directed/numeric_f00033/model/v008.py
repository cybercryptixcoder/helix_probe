def predict(probe):
    # Central bump: peak ~0.3868 at x~0 (slightly negative), asymmetric [E7,E8]
    # Right flank: smooth decay, NOT a clean Gaussian. Values: 0.6->0.309,1->0.255,1.5->0.1875,
    #   2->0.12,2.5->0.0642,3->0.0327,3.5->0.0185,4->0.0099,4.4->0.0043,4.6->0.0016,
    #   4.8->0.0014,5->0.0012,5.5->0.0007,6->0.0001 [E14,E15,E3]
    #   Note a kink: 4.6->0.0016 then 4.8->0.0014 (nearly flat) then slow decay to 0 at ~6.
    #   So: main flank decays to ~0 by x~4.6, then a small positive shoulder ~0.0014 to x~5.5,
    #   reaching 0 at x~6.
    # Left flank: -1->0.1972,-1.25->0.1467,-1.5->0.1052,-1.75->0.078,-2->0.0575,-2.25->0.037,
    #   -2.5->0.0221,-2.75->0.0111,-3->0.008,-3.25->0.0073,-3.5->0.0066,-3.75->0.006,
    #   -4->0.0053,-4.25->0.0047,-4.5->0.004,-4.75->0.0033,-5->0.0027,-5.5->0.0014,-6->0 [E11,E13,E2]
    #   Steep drop from -1 to -3, then a slow linear-ish tail from -3 to -6.
    # Left flat region: ~0 (slightly negative) from -6 to about -16 [E9]
    # Left negative tail: grows from ~0 at -6 to -0.0044 at -128 [E5,E9]
    # Right negative dip: min ~-0.0062 at x~11.75, zero-cross ~6.1, recovers to -0.0004 by ~22 [E12,E3,E6]
    # Right baseline: -0.0004 plateau from ~22 to ~110, rising to 0 at x=128 [E5]
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                # right flank of bump
                if x <= 4.6:
                    # main flank: fit through 0->0.3868,1->0.255,2->0.12,3->0.0327,4->0.0099
                    # stretched exp p~1.5 s~1.75 gave 4->0.012, slightly high; use p~1.6 s~1.72
                    bump = 0.3868 * math.exp(-((x/1.72)**1.6))
                elif x <= 6.0:
                    # small shoulder: ~0.0014 at 4.8, decaying to 0 at 6
                    bump = 0.0014 * max(0.0, (6.0 - x) / 1.2)
                else:
                    bump = 0.0
                # negative dip: min ~-0.0062 at x~11.75, zero-cross ~6.1, back to -0.0004 by ~22
                # Gaussian centered 11.75, sigma ~4.5; but must reach 0 at ~6.1
                dip = -0.0062 * math.exp(-((x-11.75)/4.5)**2)
                # baseline: -0.0004 plateau then rising to 0 at 128
                if x < 40:
                    base = -0.0004 * (1 - math.exp(-(x/20.0)**2))
                else:
                    base = -0.0004 * math.exp(-((x-40)/60.0)**2)
                y = bump + dip + base
            else:
                a = abs(x)
                # left flank: steep from -1 to -3, then slow tail -3 to -6
                if a <= 3.0:
                    # fit -1->0.1972,-1.5->0.1052,-2->0.0575,-2.5->0.0221,-3->0.008
                    y = 0.3868 * math.exp(-((a/1.35)**1.6))
                elif a <= 6.0:
                    # slow tail: -3->0.008, -4->0.0053, -5->0.0027, -6->0
                    y = 0.008 * max(0.0, (6.0 - a) / 3.0)
                else:
                    y = 0.0
                # left negative tail: grows from ~0 at -6 to -0.0044 at -128
                if a > 6:
                    tail = -0.0046 * (1 - math.exp(-((a-6)/45.0)**1.3))
                    y += tail
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
