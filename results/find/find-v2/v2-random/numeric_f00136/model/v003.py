def predict(probe):
    # Observations:
    # - Large positive x: 65.5->0.0228, 72.7->0.0267, 79.4->0.0304, 88.2->0.0352,
    #   102.1->0.0427, 103->0.0431, 104.5->0.0439, 104.9->0.0442, 105.7->0.0446,
    #   119.5->0.052, 123.6->0.0541: rises ~linearly with x [E1,E2,E3]
    # - Large negative x: -48.6->0.0244, -50.4->0.0249, -55.8->0.0265, -61.7->0.0282,
    #   -63.9->0.0288, -102.2->0.0401: rises ~linearly with |x| [E1,E2,E3]
    # - So baseline ~ |x|*0.0004 + 0.005 roughly, symmetric in x [E1,E2,E3]
    # - Mid positive x: 21.3->-0.0017, 28.4->0.0027, 30.3->0.0037, 47.1->0.0128,
    #   58.8->0.0191: consistent with same linear rise [E1,E2,E3]
    # - Mid negative x: -6.0->0.0471 (high!), -7.1->0.0381, -16.9->0.0152,
    #   -20.3->0.0163, -24.3->0.0175: there is a positive bump near x~-6 [E1,E2,E3]
    # - Near x=0: 1.2->-0.0895, 2.9->-0.0469: sharp negative dip near x~1 [E1,E2]
    # Model: linear baseline ~0.0004*|x|+0.005, negative dip near x~1.5,
    #   positive bump near x~-6.
    # ?: exact dip/bump shape and location are guesses.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            ax = abs(x)
            # linear baseline rise with |x|
            v = 0.005 + 0.0004 * ax
            # sharp negative dip near x ~ 1.5
            v -= 0.10 * math.exp(-((x - 1.5) ** 2) / 4.0)
            # positive bump near x ~ -6
            v += 0.035 * math.exp(-((x + 6.0) ** 2) / 6.0)
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}
