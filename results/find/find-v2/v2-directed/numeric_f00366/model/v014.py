import math

def predict(probe):
    # Beliefs:
    # f is piecewise-constant in x with a few regions [E1..E18].
    # At exactly x == 0, output is a special spike 1548.92 [E1,E8,E11,E15,E18].
    # For x > 0: output is -11.4 for 0 < x <= 4.1, and -12.4 for x > 4.1
    #   (boundary at 4.1: 4.1 -> -11.4, 4.1001 -> -12.4) [E14,E9,E13].
    # For x < 0: output is 9.8 for -4.1 <= x < 0, and 8.8 for x < -4.1
    #   (boundary at -4.1: -4.1 -> 9.8, -4.1001 -> 8.8) [E14,E9,E13].
    # The spike at 0 is isolated: tiny nonzero x falls into the normal regions [E11,E15].
    # No other structure observed; treat as constant within each region.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if math.isnan(x):
            ys.append(None)
            continue
        if x == 0.0:
            ys.append(1548.92)
        elif x > 0:
            if x <= 4.1:
                ys.append(-11.4)
            else:
                ys.append(-12.4)
        else:  # x < 0
            if x >= -4.1:
                ys.append(9.8)
            else:
                ys.append(8.8)
    return {"y": ys}
