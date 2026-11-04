import math

def predict(probe):
    # Beliefs:
    # - For x in roughly [0.2, 3.0] (positive), y is large ~10-13, roughly constant [E2, E4].
    # - For x in roughly [-3.0, -1.0], y is also large ~11-12 [E4].
    # - Outside those "bumps", y is small and noisy, |y| < ~3 [E1, E2, E3, E4].
    # - The bump is not a pole: values stay bounded ~10-13 [E2, E4].
    # - Sign/magnitude outside bump looks random-ish; use small pseudo-random-ish value.
    # - Boundaries: bump on positive side ends between 3.0 and 3.2 [E2, E4];
    #   starts below 0.2 (unknown lower bound, assume ~0) [E4].
    # - Negative bump: |x| in [1,3] gives large values [E4]; -5 gives 0.41 (outside).
    #   So negative bump roughly [-3, -1].
    # - Inside bump, value ~ 11.5 + small variation; use ~11.5.
    # - Outside bump, small value; approximate with a smooth small function.
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if 0.0 <= x <= 3.05:
                # positive bump
                out.append(11.5)
            elif -3.05 <= x <= -0.95:
                # negative bump
                out.append(11.5)
            else:
                # small noisy tail; use a decaying oscillation as placeholder
                out.append(1.5 * math.sin(x) / (1.0 + ax))
        except Exception:
            out.append(None)
    return {"y": out}
