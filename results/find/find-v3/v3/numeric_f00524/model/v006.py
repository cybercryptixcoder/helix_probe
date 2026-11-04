def predict(probe):
    # f(x) = ceil(x) on a band, else 0 [E2,E4,E6,E8]
    # Positive band: 0 < x <= 4.39 (4.39->5, 4.4->0) [E8]; 4.3->5, 4.4->0 [E6]
    # Negative band: -4.39 <= x <= -1 (-4.39->-4, -4.4->0) [E8]; -4.3->-4, -4.4->0 [E6]
    #   -1.0->-1, -0.8->0 so lower edge at -1 [E2,E4]
    #   0->0, 0.2->1 so positive lower edge at 0 [E2,E4]
    # Output = ceil(x) within band [E4: 0.2->1, 1.8->2, -1.2->-1, -3.8->-3]
    import math
    out = []
    for x in probe["x"]:
        if 0 < x <= 4.39:
            out.append(float(math.ceil(x)))
        elif -4.39 <= x <= -1:
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}
