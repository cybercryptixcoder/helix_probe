def predict(probe):
    # f(x) = ceil(x) for 0 < |x| < 4.5, else 0 [E2, E4]
    #   - 4.5 -> 0, -4.5 -> -0.0: boundary is |x| < 4.5, not 5 [E4]
    #   - 4.9 -> 0, -4.9 -> -0.0: outside region [E4]
    #   - 0.1 -> 1, -0.1 -> -0.0: ceil(0.1)=1, ceil(-0.1)=-0.0 [E4]
    #   - 1.0 -> 1, -1.0 -> -1, 2.0 -> 2, -2.0 -> -2: integers map to themselves [E4]
    #   - 2.4 -> 3, 2.5 -> 3, 2.9 -> 3, 3.1 -> 4, 3.4 -> 4: ceil [E2]
    #   - -2.4 -> -2, -2.5 -> -2, -2.9 -> -2, -3.1 -> -3: ceil [E2]
    #   - 0.0 -> 0.0 [E2]
    #   - 1.2 -> 2: ceil(1.2)=2 [E3]
    #   - large |x| -> 0 [E1, E3]
    import math
    out = []
    for x in probe["x"]:
        if -4.5 < x < 4.5:
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}
