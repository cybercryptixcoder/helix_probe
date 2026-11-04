def predict(probe):
    # f(x) = ceil(x) for 0 < |x| <= 4.35 (active region), else 0 [E2,E4,E6,E8]
    #   - 4.35 -> 5, -4.35 -> -4: still active at 4.35 [E8]
    #   - 4.4 -> 0, -4.4 -> -0.0: outside at 4.4 [E6]
    #   - 4.1 -> 5, -4.1 -> -4: ceil active [E6]
    #   - 4.49 -> 0, -4.49 -> -0.0: outside [E6]
    #   - 0.1 -> 1, -0.1 -> -0.0: ceil(0.1)=1, ceil(-0.1)=-0.0 [E4]
    #   - integers map to themselves [E4]
    #   - large |x| -> 0 [E1,E3,E5,E7]
    # Boundary: active for |x| <= 4.35, cutoff between 4.35 and 4.4 [?]
    import math
    out = []
    for x in probe["x"]:
        if -4.35 <= x <= 4.35:
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}
