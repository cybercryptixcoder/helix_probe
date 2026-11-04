import math

def predict(probe):
    # Model: central Gaussian bump + additive shoulder near -5 + negative dip near 12
    # + broad negative left tail + far-right baseline.
    #
    # Central bump: peak ~0.387 at x=0, symmetric, sigma ~1.0 [E4,E6]
    #   Left flank: at -1.5=0.105, -2=0.0575, -2.5=0.0221, -3=0.008, -4=0.0053 [E6,E8,E16]
    #   Right flank: at 1.5=0.1875, 2=0.12, 2.5=0.0642, 3=0.0327, 4=0.0099 [E6,E10]
    #   NOTE: left flank is STEEPER than right flank -> asymmetric, not pure Gaussian.
    #   At -1.5 obs 0.105 vs Gaussian(0.387,1.0)=0.126; at +1.5 obs 0.1875 vs 0.126.
    #   So use asymmetric sigma: sigma_left ~0.85, sigma_right ~1.15 (?) [E6]
    #
    # Shoulder near -5: separate additive bump, peak ~0.008 at x=-3, ramp 0.0006@-5.8
    #   to 0.008@-3, then merges into main bump [E14,E16,E8]
    #   Values: -6=0, -5.5=0.0014, -5=0.0027, -4.5=0.004, -4=0.0053, -3.5=0.0066,
    #   -3=0.008, -2.5=0.0221 (main bump takes over) [E8,E14,E16]
    #   Model as Gaussian centered ~-3.0, amp ~0.008, sigma ~1.5 (?)
    #
    # Negative dip near 12: min -0.0061 at x=12, symmetric-ish, sigma ~2.5 [E10,E12,E18]
    #   Values: 8=-0.0021, 10=-0.0043, 11=-0.0054, 12=-0.0061, 13=-0.0055,
    #   14=-0.0049, 15=-0.0043, 16=-0.0037, 18=-0.0025, 22=-0.0004 [E12,E18]
    #   Peak at 12, half-width: -0.003 at ~16.5 -> sigma ~2.7 (?)
    #
    # Broad negative left tail: reaches ~-0.0044 at -128, -0.0035 at -80, -0.0032 at -60,
    #   -0.0019 at -28, -0.0012 at -20, -0.0005 at -12 [E2,E7,E9,E13,E15,E16]
    #   This is NOT a Gaussian centered at -128; it's a broad plateau ~-0.0035 to -0.004
    #   for x<-40, rising toward 0 as x->0. Model as sigmoid-ish or broad Gaussian
    #   centered far left with large sigma. At -128=-0.0044, -80=-0.0035, -60=-0.0032,
    #   -28=-0.0019, -20=-0.0012, -12=-0.0005, -10=-0.0004, -8=-0.0002 [E16]
    #   Try: -0.0045 * sigmoid(-(x+30)/15) roughly, or Gaussian centered -100 sigma 50.
    #
    # Far-right baseline: ~-0.0001 to -0.0004, plateau. At 40=-0.0004, 56=-0.0004,
    #   72=-0.0003, 96=-0.0002, 120=-0.0001 [E18]. Slight rise toward 0 far right.
    #   Also -0.0004 at 22-40, -0.0003 at 16-18 [E12,E18]. Small negative offset.
    #
    # Right side between 16 and 40: -0.0037@16, -0.0025@18, -0.0004@22, -0.0004@28,
    #   -0.0004@40 [E12,E18]. Dip tail drops fast then plateau at -0.0004.
    #
    # Overall: baseline ~-0.0004 in mid-right, rising to -0.0001 far right.

    xs = probe["x"]
    ys = []
    for x in xs:
        # central asymmetric Gaussian bump
        if x < 0:
            sig = 0.85
        else:
            sig = 1.15
        y = 0.387 * math.exp(-(x*x) / (2*sig*sig))

        # additive shoulder near -3 (peak 0.008)
        y += 0.008 * math.exp(-((x+3.0)**2) / (2*1.5*1.5))

        # negative dip near 12 (min -0.0061, sigma ~2.7)
        y += -0.0061 * math.exp(-((x-12.0)**2) / (2*2.7*2.7))

        # broad negative left tail: plateau ~-0.0045 far left, rising to 0 near 0
        # use logistic: -0.0045 / (1 + exp((x+30)/12))
        y += -0.0045 / (1.0 + math.exp((x+30.0)/12.0))

        # far-right small negative baseline, rising toward 0
        # ~-0.0004 for x in 20..50, -0.0001 at 120
        y += -0.0004 * math.exp(-max(0.0, x-20.0)/80.0)

        ys.append(y)
    return {"y": ys}
