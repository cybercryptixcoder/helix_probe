import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs:
    # - For x < 0: f(x) = floor(x) - 1  [E1-E5, E11]
    # - For x >= 0 outside exception region: f(x) = floor(x) + 1  [E1-E5, E11]
    #   BUT x = 0 gives -1, not +1  [E1, E4, E11]
    # - Exception region: x in (33.3, 42.01) returns random noise around -0.5
    #   (range roughly -0.19 to -0.74). Same x gives different values on repeat
    #   [E10, E15, E17], so it is genuinely random, not a function of x.
    #   Left boundary: 33.3 normal, 33.31 anomalous [E12, E14, E17].
    #   Right boundary: 42.0 anomalous [E9, E11, E17]; 42.01 anomalous [E12, E17];
    #   42.015 normal [E12]. So region is (33.3, 42.015) exclusive-ish.
    #   Model as constant -0.5 (best guess for a random value's mean).

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        # Exception region: random noise around -0.5 [E5-E17]
        if 33.3 < x < 42.015:
            ys.append(-0.5)
            continue

        # Special point x = 0 -> -1 [E1, E4, E11]
        if x == 0:
            ys.append(-1.0)
            continue

        fl = math.floor(x)
        if x < 0:
            ys.append(float(fl - 1))
        else:
            ys.append(float(fl + 1))

    return {"y": ys}
