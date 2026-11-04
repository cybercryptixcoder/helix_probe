import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs:
    # - For x < 0: f(x) = floor(x) - 1  [E1, E3, E4, E5]
    # - For x >= 0 (outside exception region): f(x) = floor(x) + 1  [E1, E3, E4, E5]
    #   BUT x=0 gives -1, not +1: f(0) = -1  [E1, E4]
    # - Exception region: x in (33.31, 42.0] gives noisy values near -0.5  [E5-E9]
    #   Left boundary: 33.3 normal (34), 33.31 anomalous -> boundary at 33.31  [E8, E9]
    #   Right boundary: 42.0 anomalous, 42.01 normal -> boundary at 42.0  [E9]
    #   Values are noise around ~-0.5, roughly -0.32 to -0.65; model as -0.5 + pseudo-noise.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        # Exception region (noisy values) [E5-E9]
        if 33.31 < x <= 42.0:
            val = -0.5 + 0.15 * math.sin(97.0 * x) + 0.05 * math.cos(53.0 * x)
            ys.append(round(val, 4))
            continue

        # Special point x = 0 -> -1 [E1, E4]
        if x == 0:
            ys.append(-1.0)
            continue

        fl = math.floor(x)
        if x < 0:
            ys.append(float(fl - 1))
        else:
            ys.append(float(fl + 1))

    return {"y": ys}
