import math

def predict(probe):
    # Beliefs about f:
    # - For x >= -79: outputs are independent random draws, roughly N(0, ~0.1),
    #   clipped to about ±0.32. Repeats at same x differ wildly [E10,E12,E18,E22].
    #   No dependence on x magnitude or nearby x [E16,E20].
    # - For x < -79: outputs are tiny constants ~0.006, essentially deterministic
    #   and independent of x [E9,E11,E14,E15,E21].
    # - Boundary at x = -79 (E15: -79.5 -> 0.0074, -80.2 -> 0.0073; E9: -79.1 -> 0.0059).
    # - Since the random part is unpredictable, best guess is the mean, ~0.
    xs = probe.get("x", [])
    out = []
    for x in xs:
        if x < -79:
            out.append(0.006)
        else:
            out.append(0.0)
    return {"y": out}
