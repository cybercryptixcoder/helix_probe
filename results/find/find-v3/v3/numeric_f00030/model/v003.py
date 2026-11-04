def predict(probe):
    # Baseline is a smooth curve, not a straight line: it's steeper near 0 and
    # flattens toward the edges, roughly linear in the mid-range [E6, E8].
    # Baseline at x=0 is about -1.68, rising to ~-1.47 at x=-128 and ~-1.51 at x=128 [E6, E8].
    # The baseline is asymmetric: negative side is lower (more negative) than positive side [E6, E8].
    # There is a sharp dip near x=0, roughly |x|<2.5, reaching ~-1.79 to -1.81 [E4, E8].
    # The dip is not centered exactly at 0; deepest around x=±1, with x=0 itself less deep [E4, E8].
    import math
    xs = probe["x"]
    ys = []
    for x in xs:
        # Baseline: smooth S-curve. Use a tanh-like shape.
        # At x=0: -1.68. Asymptotes: -1.47 (neg) and -1.51 (pos).
        # Use asymmetric logistic in x.
        if x <= 0:
            base = -1.47 + (-1.68 + 1.47) * math.exp(x / 60.0)
        else:
            base = -1.51 + (-1.68 + 1.51) * math.exp(-x / 60.0)
        # Dip near 0: two-sided well, deepest at |x|~1, shallower at 0.
        # Model as gaussian centered at ±1 with width ~0.8, plus a small central bump.
        dip = -0.11 * math.exp(-((abs(x) - 1.0) / 0.9) ** 2)
        # central slight rise (x=0 is less deep than ±1)
        dip += 0.02 * math.exp(-(x / 0.4) ** 2)
        ys.append(base + dip)
    return {"y": ys}
