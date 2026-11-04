def predict(probe):
    # f(x) = 5.2 - 2.5*x on [-2.1, 2.08], else 0 [E2, E4, E6, E8]
    # Boundaries sharp: -2.1 included, 2.08 excluded [E6, E8]
    # Outside interval, output is 0 (signed zero possible) [E5, E7]
    # EXCEPTION: a noisy region on [-85, -78] where output is random per call,
    #   NOT a deterministic function of x [E16, E20, E24: same x gives different y]
    #   Region boundaries: nonzero at -85 and -78 inclusive; zero at -85.001,
    #   -77.999 and beyond [E18, E20, E22]
    #   Values appear uniform-ish in roughly [-0.2, 0.33] [E10, E12, E14, E22, E24]
    #   Since it's irreproducible, best guess for sealed probes is a random draw.
    import random
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.08:
            out.append(5.2 - 2.5 * x)
        elif -85 <= x <= -78:
            out.append(random.uniform(-0.2, 0.33))
        else:
            out.append(0.0)
    return {"y": out}
