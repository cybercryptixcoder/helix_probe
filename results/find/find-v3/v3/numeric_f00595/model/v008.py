def predict(probe):
    # Beliefs (one line each, citing evidence):
    # For x > 0 (outside special region): y = floor(x) + 1  [E2, E4, E6, E8, E10, E11, E13, E15]
    # For x < 0: y = floor(x) - 1  [E11, E12, E13, E14, E15]
    # At x = 0: y = -1 (negative branch)  [E4]
    # Special region: x in [38.5, 42.0] gives small negative constants (not the rounding rule)  [E15, E16]
    #   - E16: 38.5..42.0 all give ~-0.2 to -0.65; 35.0, 43.0, 45.0, 30.0, 50.0 follow the rule.
    #   - Boundaries guessed: [38.5, 42.0]; mark with "?".
    #   - Values inside region appear noisy/irregular; use a constant approximation.
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
        # Special region (?) around 40
        if 38.5 <= xf <= 42.0:
            ys.append(-0.4)
            continue
        if xf <= 0:
            y = math.floor(xf) - 1
        else:
            y = math.floor(xf) + 1
        ys.append(float(y))
    return {"y": ys}
