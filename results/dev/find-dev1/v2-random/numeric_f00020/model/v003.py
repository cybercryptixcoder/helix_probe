def predict(probe):
    # Baseline ~81 across domain [E1-E10]
    # Large feature near x~123.6: E2 (123.6 -> 87.4), E10 (127 -> 88.6, 115.1 -> 84.3)
    #   Suggests peak around x~125-126, broad-ish. E10 127=88.6 > E2 123.6=87.4, so peak likely ~126+
    # Secondary feature near x~105-110: E2 (104.5->81.23, 104.9->81.30), E8 (108.4->82.18),
    #   E9 (108.3->82.15, 101.9->81.06), E10 (106.7->81.71)
    #   Peak around x~108-109, value ~82.2
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        y = 81.0
        # Main high-x feature: peak ~126, height ~7.6 (127->88.6 => +7.6), width ~4?
        y += 7.6 * math.exp(-((x - 126.0) ** 2) / (2 * 4.0 ** 2))
        # Secondary feature: peak ~108.5, height ~1.2, width ~2.5
        y += 1.2 * math.exp(-((x - 108.5) ** 2) / (2 * 2.5 ** 2))
        ys.append(y)
    return {"y": ys}
