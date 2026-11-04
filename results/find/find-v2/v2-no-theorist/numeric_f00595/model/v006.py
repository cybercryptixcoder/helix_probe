def predict(probe):
    # f(x) = ceil(x) for x > 0 outside anomaly [E1-E13]
    # f(x) = floor(x) - 1 for x < 0 [E1-E13]
    # f(0) = -1 [E2,E4,E6,E10]
    # Anomaly interval: (33.3, 42.5) — inside returns small negative noisy value [E14,E16,E18]
    #   Lower boundary: 33.3 -> 34 (out), 33.4 -> -0.3997 (in). So starts in (33.3, 33.4]. [E18]
    #   Upper boundary: 42.49 -> 43 (out), 42.0 -> -0.4565 (in). So ends in (42.0, 42.1]. [E18]
    #   Inside: noisy small negative (~ -0.3 to -0.63); return -0.5 as placeholder [?]
    import math
    out = []
    for x in probe["x"]:
        if 33.4 <= x <= 42.0:  # ? boundaries: lower in (33.3,33.4], upper in (42.0,42.1]
            out.append(-0.5)  # ? noisy small negative; exact value unpredictable
        elif x > 0:
            out.append(math.ceil(x))
        elif x < 0:
            out.append(math.floor(x) - 1)
        else:
            out.append(-1)
    return {"y": out}
