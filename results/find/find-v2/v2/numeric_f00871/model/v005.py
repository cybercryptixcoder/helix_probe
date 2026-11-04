def predict(probe):
    # f(x) = 5.2 - 2.5*x on [-2.1, 2.08], else 0 [E2, E4, E6, E8]
    # Boundaries sharp: -2.1 included, 2.08 excluded [E6, E8]
    # Outside interval, output is 0 (signed zero possible) [E5, E7]
    # EXCEPTION: a noisy region roughly on [-85, -78] where output is random-ish
    #   nonzero values, not a fixed value [E9, E10, E12]
    #   E12 shows nonzero from -85 to -78, zero at -77 and beyond, zero at -90 and below
    #   E10 shows nonzero throughout [-79.6, -78.6] with varied values
    #   So region is approximately [-85, -78]; values appear random in ~[-0.1, 0.3] (?)
    #   Model as: random-looking but deterministic? We cannot know; use a hash-based
    #   pseudo-random value in that interval (?) -- best guess for sealed probes.
    import math
    def noise(x):
        # deterministic pseudo-random in [-0.1, 0.3] based on x (?)
        h = math.sin(x * 12.9898) * 43758.5453
        frac = h - math.floor(h)
        return -0.1 + 0.4 * frac
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.08:
            out.append(5.2 - 2.5 * x)
        elif -85 <= x <= -78:
            out.append(noise(x))
        else:
            out.append(0.0)
    return {"y": out}
