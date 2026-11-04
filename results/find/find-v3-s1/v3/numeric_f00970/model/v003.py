import math

def predict(probe):
    # Beliefs:
    # - Central band: |x| < ~3.1 gives y ~ 12-13 (noisy) [E2, E6]
    # - Outside band: y is small noise around 0, std ~1, no trend [E1,E3,E4,E5]
    # - Transition is sharp: x=-3.2 -> 0.22, x=-3.0 -> 12.07; x=3.2 -> 0.88, x=3.0 -> 13.76 [E6]
    #   So boundary is between 3.0 and 3.2. Use 3.1.
    # - Inside band mean ~12.3 (E2: 10.2-12.8; E6: 11.9-13.8; E5: 13.66) [E2,E5,E6]
    # - Outside band mean ~0 (E1,E3,E4,E5 scattered in [-2.2, 2.0]) [E1,E3,E4,E5]

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if -3.1 < x < 3.1:
                ys.append(12.3)
            else:
                ys.append(0.0)
        except Exception:
            ys.append(None)
    return {"y": ys}
