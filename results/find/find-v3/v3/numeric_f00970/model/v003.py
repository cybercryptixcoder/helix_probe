import math

def predict(probe):
    # Beliefs:
    # - High plateau for x in (-3.05, 3.0]: values ~11-13, noisy around ~12 [E2,E4,E6]
    #   Left edge between -3.1 (low ~1.6) and -3.05 (high ~11.6) [E6]
    #   Right edge between 2.9 (high ~11.85) and 3.1 (low ~-0.08) [E4]
    # - Outside plateau: noisy values roughly in [-1.8, 2.3], mean ~0.3 [E1-E6]
    #   No recoverable smooth structure; treat as noise around 0.3
    # - Plateau value: noisy around ~12; use 12.0 as best central estimate [E2,E4,E6]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xv = float(x)
        except Exception:
            ys.append(None)
            continue
        if -3.05 < xv <= 3.0:
            ys.append(12.0)
        else:
            ys.append(0.3)
    return {"y": ys}
