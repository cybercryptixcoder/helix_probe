import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs:
    # - For x < 0: f(x) = floor(x) - 1  [E1, E3, E4, E5]
    # - For x >= 0: f(x) = floor(x) + 1  [E1, E3, E4, E5]
    #   BUT x=0 gives -1, not +1: f(0) = -1  [E1, E4]
    # - Exception region: x in (33.3, 42.0] gives noisy values near -0.4  [E5-E8]
    #   Left boundary: 33.3 normal (34), 33.32 anomalous -> boundary in (33.3, 33.32], guess 33.31  [E8]
    #   Right boundary: 42.0 anomalous, 42.5 normal -> boundary in (42.0, 42.5], guess 42.0  [E8]
    #   Values scatter roughly -0.32 to -0.62; model as -0.45 + pseudo-noise.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        # Exception region (noisy values) [E5-E8]
        if 33.31 < x <= 42.0:
            val = -0.45 + 0.15 * math.sin(97.0 * x) + 0.05 * math.cos(53.0 * x)
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
