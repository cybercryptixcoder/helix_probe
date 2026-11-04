def predict(probe):
    # Linear part: y = -9.6*x + 8, exact for all non-flat points [E1-E6]
    # Flat region: output ~8 (noisy) for x in a negative interval [E1-E6]
    #   Flat points: -20.3,-61.7,-24.3,-50.4 [E1]; -55.8,-63.9 [E2]; -48.6,-102.2,-16.9 [E3];
    #                -61.3,-124.4,-25.9 [E4]; -127.7,-65.6,-44.7,-79.1,-66.9 [E5];
    #                -13.3,-107.4,-46.1,-100.1 [E6]
    #   Non-flat negative points: -6 [E1], -7.1 [E3], -5.9 [E4], -1.6 [E5], 2.0 [E6]
    #   Upper bound: flat up to -13.3 [E6], non-flat at -7.1 [E3] -> boundary between -13.3 and -7.1, guess -10
    #   Lower bound: flat down to -127.7 [E5] -> extends to domain edge -128
    #   Flat values noisy around 8.0
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if -128 <= x <= -10:
                ys.append(8.0)  # ? flat region, noisy around 8
            else:
                ys.append(-9.6 * x + 8.0)
        except Exception:
            ys.append(None)
    return {"y": ys}
