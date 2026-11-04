def predict(probe):
    # f(x) = floor(x + 0.5) for |x| < 4.5, except a positive bump near 4.1-4.35 [E7,E8]
    #   -0.5 -> -0.0, 0.5 -> 1, 1.5 -> 2, 2.5 -> 3, 3.5 -> 4 [E7,E8]
    #   -1.5 -> -1, -2.5 -> -2, -3.5 -> -3 [E7,E8]
    # f(x) = 0 for |x| >= 4.5 [E3,E5,E8]
    # Positive side anomaly: 4.1..4.35 -> 5 (not 4) [E3,E5,E6,E8]
    #   E6: 4.05 -> 5; E8: 4.1,4.2,4.25,4.3,4.35 -> 5; 4.4 -> 0 [E8]
    # Negative side: no anomaly, floor(x+0.5) up to -4.5 [E3,E5,E8]
    #   -4.1,-4.2,-4.25,-4.3,-4.35 -> -4; -4.4,-4.5 -> 0 [E8]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if 4.0 < x < 4.5:
                out.append(5.0)
            elif -4.5 < x < 4.5:
                out.append(float(math.floor(x + 0.5)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
