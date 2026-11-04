def predict(probe):
    # Linear part: y = -9.6*x + 8, exact for all non-flat points [E1, E2, E3]
    # Flat region: output ~8 (noisy) for x in a negative interval [E1, E2, E3]
    #   Flat points seen: -20.3, -61.7, -24.3, -50.4 [E1]; -55.8, -63.9 [E2]; -48.6, -102.2, -16.9 [E3]
    #   Non-flat negative points: -6 [E1], -7.1 [E3]
    #   So flat region extends below -102.2 (E3) and up to at least -16.9 (E3).
    #   Upper bound: between -16.9 (flat) and -7.1 (not flat) -> guess -16 [E3]
    #   Lower bound: -102.2 flat; unknown below. Guess -128 (extends to domain edge) ? 
    #   Actually -102.2 flat and no data below; try lower bound -128 ? or -112?
    #   Flat values: 7.98, 7.97, 7.86, 8.33, 7.96, 8.25, 8.14, 8.05, 7.94 -> mean ~8.05, noisy
    #   Predict 8.0 for flat region.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if -128 <= x <= -16:
                ys.append(8.0)  # ? flat region, noisy around 8
            else:
                ys.append(-9.6 * x + 8.0)
        except Exception:
            ys.append(None)
    return {"y": ys}
