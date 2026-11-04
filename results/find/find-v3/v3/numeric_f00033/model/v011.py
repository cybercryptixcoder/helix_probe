import math

def predict(probe):
    # Beliefs (mechanism, from all evidence):
    # Central positive bump: peak ~0.387 at x=0, asymmetric.
    #   Left flank steeper: -0.5=0.3052, -1=0.1972, -1.5=0.105, -2=0.0575, -2.5=0.0221 [E16,E6,E8]
    #   Right flank: 0.5=?, 1.5=0.1875, 2=0.12, 2.5=0.0642, 3=0.0327, 4=0.0099 [E6,E10]
    #   Fit asymmetric Gaussian: sigma_left~0.72, sigma_right~1.05 (?) [E16,E10]
    # Small positive shoulder near -3 to -5: additive ramp, ~0 at -6, 0.008 at -3 [E14,E16,E8]
    #   Linear-ish ramp from -6 to -3 then merges into main bump.
    # Negative dip near x=12: min -0.0061 at 12, roughly symmetric, sigma~2.5 [E18,E12]
    #   10=-0.0043,11=-0.0054,12=-0.0061,13=-0.0055,14=-0.0049,15=-0.0043,16=-0.0037,
    #   18=-0.0025,22=-0.0004 [E18,E12]
    # Broad negative left tail: plateau ~-0.004 for x<-40, rising to 0 near 0 [E2,E9,E15,E16]
    #   -128=-0.0044,-80=-0.0035,-60=-0.0032,-28=-0.0019,-20=-0.0012,-12=-0.0005 [E2,E16]
    # Far-right baseline: ~-0.0004 for x in 20..56, rising to ~-0.0001 at 120+ [E18,E19]
    #   -0.0004@22..56, -0.0003@72, -0.0002@96, -0.0001@120 [E18]

    xs = probe["x"]
    ys = []
    for x in xs:
        # central asymmetric Gaussian bump
        sig = 0.72 if x < 0 else 1.05
        y = 0.387 * math.exp(-(x*x) / (2*sig*sig))

        # additive shoulder ramp near -3 (0 at -6, 0.008 at -3)
        if -6.0 < x < -3.0:
            y += 0.008 * (x + 6.0) / 3.0

        # negative dip near 12
        y += -0.0061 * math.exp(-((x-12.0)**2) / (2*2.5*2.5))

        # broad negative left tail: plateau ~-0.004 far left, rising to 0 near 0
        y += -0.0042 / (1.0 + math.exp((x+30.0)/12.0))

        # far-right small negative baseline, rising toward 0
        if x > 20.0:
            y += -0.0004 * math.exp(-(x-20.0)/80.0)

        ys.append(y)
    return {"y": ys}
