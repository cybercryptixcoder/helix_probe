def predict(probe):
    # Observations:
    # - Large |x|: rises ~linearly with |x|, symmetric [E1,E2,E3,E4,E5]
    #   88.2->0.0352, 102.1->0.0427, 123.6->0.0541, -102.2->0.0401, -127.7->0.0478
    #   slope ~0.0004 per unit |x|, intercept ~0.0
    # - Mid positive x: 21.3->-0.0017, 28.4->0.0027, 43->0.0105, 47.1->0.0128,
    #   56.2->0.0177, 58.8->0.0191: same linear rise, ~0.0004*x [E1,E3,E4]
    # - Mid negative x: -16.9->0.0152, -20.3->0.0163, -24.3->0.0175, -25.9->0.018,
    #   -44.7->0.0233, -48.6->0.0244: same linear rise ~0.0004*|x| [E1,E3,E4,E5]
    # - So baseline ~ 0.0004*|x|, roughly symmetric [all]
    # - Positive bump near x~-6: -6.0->0.0471, -5.9->0.0479, -7.1->0.0381 [E1,E3,E4]
    # - Negative dip near x~0 to +2: 1.2->-0.0895, 2.9->-0.0469, -1.6->0.0781(!) [E2,E5]
    #   -1.6 is HIGH positive, so dip is asymmetric: high positive just left of 0,
    #   deep negative dip around x~1-2. Model as a sharp feature near x~1.
    # - 17.3->-0.0099, 12.5->-0.0198: another negative dip near x~12-17 [E4,E5]
    # ?: exact shapes/locations of the near-zero and near-15 features are guesses.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            ax = abs(x)
            v = 0.0004 * ax
            # positive bump near x ~ -6
            v += 0.045 * math.exp(-((x + 6.0) ** 2) / 8.0)
            # sharp positive spike just left of 0 (x~-1.6 -> 0.078)
            v += 0.080 * math.exp(-((x + 1.6) ** 2) / 2.0)
            # deep negative dip near x ~ 1.5
            v -= 0.095 * math.exp(-((x - 1.5) ** 2) / 4.0)
            # negative dip near x ~ 15
            v -= 0.030 * math.exp(-((x - 15.0) ** 2) / 20.0)
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}
