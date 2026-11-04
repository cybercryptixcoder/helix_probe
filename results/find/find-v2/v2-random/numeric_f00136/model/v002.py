def predict(probe):
    # Observations:
    # - Outputs are small (~0.02-0.05) for large |x|, both positive and negative x [E1, E2]
    # - Near x=0 there is a sharp negative dip: x=1.2 -> -0.0895, x=2.9 -> -0.0469,
    #   x=-6.0 -> 0.0471 (positive!), x=-20.3 -> 0.0163 [E1, E2]
    # - x=21.3 -> -0.0017 (near zero), x=30.3 -> 0.0037 (near zero) [E1, E2]
    # - Large positive x: 65.5->0.0228, 72.7->0.0267, 79.4->0.0304, 88.2->0.0352,
    #   103->0.0431, 104.5->0.0439, 104.9->0.0442, 123.6->0.0541: slowly rising with x [E1,E2]
    # - Large negative x: -50.4->0.0249, -55.8->0.0265, -61.7->0.0282, -63.9->0.0288:
    #   also rising as |x| grows [E1, E2]
    # Model: baseline ~0.02 plus a slow rise with |x|, plus a sharp negative dip near x~1-3,
    #   and a positive bump near x~-6.
    # ?: exact dip shape/location and bump are guesses from sparse points.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            ax = abs(x)
            # slow baseline rise with |x|, saturating
            v = 0.02 + 0.035 * (1.0 - math.exp(-ax / 80.0))
            # sharp negative dip near x ~ 1.5
            v -= 0.11 * math.exp(-((x - 1.5) ** 2) / 6.0)
            # positive bump near x ~ -6
            v += 0.03 * math.exp(-((x + 6.0) ** 2) / 8.0)
            # slight negative near x~21
            v -= 0.02 * math.exp(-((x - 21.0) ** 2) / 20.0)
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}
