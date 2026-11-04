def predict(probe):
    # f(x) ~ 81 baseline across domain [E1, E2]
    # Near x ~ 123.6, f jumps to ~87.4 — a spike/feature at high positive x [E2]
    # Small wiggle near x ~ 104.9 (81.30) and 104.5 (81.23) suggests a bump around x~105 [E2]
    # Most values within ~0.1 of 81 are MLP wiggle/noise [E1, E2]
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        y = 81.0
        # Spike near x ~ 123.6 (width unknown; guess Gaussian bump)
        y += 6.37 * math.exp(-((x - 123.6) ** 2) / (2 * 1.5 ** 2))
        # Small bump near x ~ 105
        y += 0.28 * math.exp(-((x - 104.7) ** 2) / (2 * 1.5 ** 2))
        ys.append(y)
    return {"y": ys}
