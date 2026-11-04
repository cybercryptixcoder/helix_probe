def predict(probe):
    # f(x) = ceil(x) for x > 0 outside the anomaly [E1-E16]
    # f(x) = floor(x) - 1 for x < 0 [E1-E16]
    # f(0) = -1 [E2,E4,E6,E10]
    # Anomaly: on [33.5, 42.5] f returns a small negative noisy value (~ -0.3 to -0.63) [E14,E16]
    #   Lower boundary: 33.0 -> 34 (ceil), 33.5 -> -0.6024 (in). So anomaly starts in (33, 33.5]. [E16]
    #   Upper boundary: 42.0 -> -0.365 (in), 42.5 -> 43 (out), 43 -> 44 (out). So anomaly ends in [42, 42.5). [E14]
    #   Inside: value is noisy small negative; return -0.5 as placeholder [?]
    import math
    out = []
    for x in probe["x"]:
        if 33.5 <= x < 42.5:  # ? exact boundaries: lower in (33,33.5], upper in [42,42.5)
            out.append(-0.5)  # ? noisy small negative; exact value unpredictable
        elif x > 0:
            out.append(math.ceil(x))
        elif x < 0:
            out.append(math.floor(x) - 1)
        else:
            out.append(-1)
    return {"y": out}
