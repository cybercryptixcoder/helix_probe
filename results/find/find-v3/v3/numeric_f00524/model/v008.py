def predict(probe):
    # f(x) = ceil(x) on a band, else 0 [E2,E4,E6,E8]
    # Positive band: 0 < x <= 4.35 (4.35->5, 4.36->0) [E8,E12]; 4.34->5 [E12]
    # Negative band: -4.35 <= x <= -1 (-4.35->-4, -4.36->0) [E8,E12]; -4.34->-4 [E12]
    #   -1.0->-1, -0.8->0 so lower edge at -1 [E2,E4]
    #   0->0, 0.2->1 so positive lower edge at 0 [E2,E4]
    # Output = ceil(x) within band [E4: 0.2->1, 1.8->2, -1.2->-1, -3.8->-3]
    # E10: 4.389->0, -4.389->0, so upper edge is between 4.35 and 4.389 [E10]
    # E12: 4.35->5, 4.36->0 confirms edge at 4.35 inclusive; -4.35->-4, -4.36->0 [E12]
    import math
    out = []
    for x in probe["x"]:
        if 0 < x <= 4.35:
            out.append(float(math.ceil(x)))
        elif -4.35 <= x <= -1:
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}
