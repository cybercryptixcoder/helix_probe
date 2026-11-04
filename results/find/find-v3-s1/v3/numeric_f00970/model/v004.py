import math

def predict(probe):
    # Beliefs:
    # - Central band |x| < ~3.1: y ~ 12-13 (noisy) [E2,E5,E6]
    # - Outside band: y is small noise around 0, std ~1, no trend [E1,E3,E4,E5,E7]
    # - Transition sharp: boundary between 3.0 and 3.2 [E6]
    # - Outside band is NOT a smooth function; it's irregular noise [E4]
    # - Best guess for outside: 0 (mean of noise) [E1,E3,E4,E5,E7]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(12.3 if -3.1 < x < 3.1 else 0.0)
        except Exception:
            ys.append(None)
    return {"y": ys}
