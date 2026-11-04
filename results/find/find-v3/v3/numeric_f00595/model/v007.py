def predict(probe):
    # Beliefs (one line each, citing evidence):
    # For x > 0: y = floor(x) + 1  [E2, E4, E6, E8, E10, E11, E13, E15]
    # For x < 0: y = floor(x) - 1  [E11, E12, E13, E14, E15]  (NOT ceil-1)
    # At x = 0: y = -1 (negative branch)  [E4]
    # Exception region: x in (40, 41] gives y = -0.236 (a constant, not the rounding rule)  [E15]
    #   - E15: x=40.1 -> -0.236, while x=28.9->29, x=65.9->66 follow the rule.
    #   - Boundary guessed: (40, 41]; mark with "?".
    # No noise elsewhere; outputs are exact integers.
    # No state/history involved.

    import math

    xs = probe["x"]
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            xf = float(x)
        except Exception:
            ys.append(None)
            continue
        if math.isnan(xf) or math.isinf(xf):
            ys.append(None)
            continue
        # Special region (?) around 40.1
        if 40.0 < xf <= 41.0:
            ys.append(-0.236)
            continue
        if xf <= 0:
            y = math.floor(xf) - 1
        else:
            y = math.floor(xf) + 1
        ys.append(float(y))
    return {"y": ys}
