def predict(probe):
    # Output is always ±18 [E1]
    # Sign depends on x: negative x -> +18, positive x -> -18 [E1]
    #   x=-20.3 -> 18, x=-61.7 -> 18, x=-24.3 -> 18, x=-50.4 -> 18, x=-6.0 -> 18
    #   x=88.2 -> -18, x=66.0 -> -18, x=2.9 -> -18, x=72.7 -> -18, x=21.3 -> -18
    # So y = -18 * sign(x)  (sign(0) unknown; guess 0 -> -18? mark ?)
    out = []
    for x in probe.get("x", []):
        if x is None:
            out.append(None)
        elif x < 0:
            out.append(18.0)
        else:
            out.append(-18.0)
    return {"y": out}
