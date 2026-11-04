def predict(probe):
    # f(x) = round-half-up(x) for |x| < 4.5, i.e. floor(x+0.5) [E7,E4,E6]
    #   -0.5 -> -0.0, 0.5 -> 1, 1.5 -> 2, 2.5 -> 3, 3.5 -> 4 [E7]
    #   -1.5 -> -1, -2.5 -> -2, -3.5 -> -3 [E7]
    # f(x) = 0 for |x| >= 4.5 [E3,E5]
    # Boundary: 4.4 -> 0, 4.3 -> 5, 4.25 -> 5, 4.1 -> 5 [E3,E5]
    #   -4.3 -> -4, -4.25 -> -4, -4.1 -> -4 [E3,E5]
    # So the cutoff is at |x| = 4.5 (strictly), rounding is floor(x+0.5) throughout [E3,E5,E7]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if -4.5 < x < 4.5:
                out.append(float(math.floor(x + 0.5)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
