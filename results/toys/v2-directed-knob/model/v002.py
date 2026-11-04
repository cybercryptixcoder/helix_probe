def predict(probe):
    # x = a [E1, E2]
    # y = c [E1, E2]
    # size grows with c: size = 1.0 at c=5, 2.5 at c=8 -> slope 0.5 per unit [E1, E2]
    #   size = 0.5*c - 1.5 [E1, E2]
    # switch and b have no observed effect yet [?]
    a = probe.get("a", 5)
    c = probe.get("c", 5)
    return {"x": a, "y": c, "size": 0.5 * c - 1.5}
