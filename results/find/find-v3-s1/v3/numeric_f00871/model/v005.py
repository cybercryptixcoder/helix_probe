def predict(probe):
    # Main ramp: y = 5.2 - 2.5*x on [-2.1, 2.1] [E2,E4,E6,E8,E10,E12]
    # Outside that: 0.0 [E1,E3,E5,E8,E9,E10]
    # Faint positive tail appears only in x in [-88, -80] region:
    #   E14: -88->0.1138, -84->0.1196, -80->0.2126; -92 and -76 are 0
    #   E7: -80.4 -> 0.0499 ; E13: -83.7 -> 0.2486
    # So a small bump on roughly [-88, -80], magnitude ~0.1-0.25, noisy.
    # Model it as a smooth bump peaking near -80 with width ~8, scaled ~0.2.
    # (values are noisy; approximate shape is a guess "?")
    import math
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -88.0 <= x <= -80.0:
            # bump centered near -80, amplitude ~0.2, half-width ~8
            out.append(0.2 * math.exp(-((x + 80.0) ** 2) / (2 * 4.0 ** 2)))
        else:
            out.append(0.0)
    return {"y": out}
