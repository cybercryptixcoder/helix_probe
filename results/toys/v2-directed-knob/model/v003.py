def predict(probe):
    # x = a [E1, E2]
    # y = c [E1, E2]
    # size = 0.5*c - 1.5 [E1, E2]
    # b affects x: at b=5 x=5, at b=8 x=2 -> slope -1 per unit of b [E3]
    #   x = a - (b - 5) = a - b + 5 [E3]
    # switch has no observed effect yet [?]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    return {"x": a - b + 5, "y": c, "size": 0.5 * c - 1.5}
