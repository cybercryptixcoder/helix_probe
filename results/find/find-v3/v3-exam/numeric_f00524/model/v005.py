def predict(probe):
    # f(x) = ceil(x) for 0 < |x| < 4.5, else 0 [E2, E4, E6]
    #   - 4.4 -> 0, 4.49 -> 0: cutoff is below 4.4, not 4.5 [E6]
    #   - 4.1 -> 5, -4.1 -> -4: ceil still active at 4.1 [E6]
    #   - 3.9 -> 4, -3.9 -> -3: ceil [E6]
    #   - 4.5 -> 0, -4.5 -> -0.0: outside region [E4]
    #   - 0.1 -> 1, -0.1 -> -0.0: ceil(0.1)=1, ceil(-0.1)=-0.0 [E4]
    #   - integers map to themselves [E4]
    #   - large |x| -> 0 [E1, E3, E5]
    # Boundary: active for |x| < 4.2 (between 4.1 and 4.4) [?]
    import math
    out = []
    for x in probe["x"]:
        if -4.2 < x < 4.2:
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}
