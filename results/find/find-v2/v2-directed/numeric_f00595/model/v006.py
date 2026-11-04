import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs:
    # - For x < 0: f(x) = floor(x) - 1  [E1, E3, E4, E5]
    # - For x >= 0: f(x) = floor(x) + 1  [E1, E3, E4, E5]
    #   BUT x=0 gives -1, not +1: f(0) = -1  [E4]
    #   (E1 had 0 -> -1 too; my earlier note was wrong.)
    # - Exception region: x in (33.3, 40.0] approximately gives a
    #   noisy-looking value near -0.3 to -0.7  [E5, E6, E7]
    #   Left boundary: 33.25 normal (34), 33.4 anomalous -> boundary in (33.25, 33.4], guess 33.3  [E6, E7]
    #   Right boundary: 40.0 anomalous, 45.0 normal -> boundary in (40, 45], guess ~41  [E7]
    #   Values scatter roughly -0.3 to -0.7; model as -0.4 + small pseudo-noise.
    #
    # Note: E1's x=0 -> -1 contradicts the "x>=0 -> floor+1" rule; treat 0 specially.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        # Exception region (noisy values) [E5, E6, E7]
        if 33.3 < x <= 41.0:
            val = -0.4 + 0.15 * math.sin(97.0 * x) + 0.05 * math.cos(53.0 * x)
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
