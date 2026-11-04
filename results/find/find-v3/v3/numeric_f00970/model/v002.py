import math

def predict(probe):
    # Beliefs:
    # - High plateau (~10-14) for x in roughly (-2.5, 3.0]; boundaries: -2.5 high, -3.0 high(!), -3.5 low [E4]
    #   Wait: E4 x=-3.0 -> 9.47 (high), x=-3.5 -> -0.02 (low). So left edge between -3.5 and -3.0.
    #   E4 x=-2.5 -> 10.79 high, x=2.9 -> 11.85 high, x=3.1 -> -0.08 low. Right edge between 2.9 and 3.1.
    #   E2 x=-2 -> 13.49 high, x=3 -> 10.19 high, x=4 -> 0.03 low. Consistent.
    # - Outside plateau: small noisy values roughly in [-1.7, 2.3], mean ~0.3 [E1,E2,E3,E4]
    # - No clear smooth structure recoverable; treat as noise, predict mean ~0.3? Actually mean of low values ~0.3.
    #   But predicting 0 gives partial credit; predicting mean ~0.3 may be slightly better. Use 0.3.
    # - Plateau mean ~11.8.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xv = float(x)
        except Exception:
            ys.append(None)
            continue
        if -3.25 <= xv <= 3.0:
            ys.append(11.8)
        else:
            ys.append(0.3)
    return {"y": ys}
