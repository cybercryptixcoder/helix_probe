def predict(probe):
    # f(x) = x for |x| <= 2, and 0 elsewhere [E1]
    # Evidence: x=-2 -> -2, x=-1 -> -1, x=0 -> 0, x=1 -> 1, x=2 -> 2
    #           x=-5,-10,-20,...,120 -> 0
    # Boundary appears to be at |x| = 2 (inclusive inside, exclusive outside).
    # "?" Exact boundary between 2 and 5 unknown; assume |x| <= 2.
    out = []
    for x in probe.get("x", []):
        try:
            if -2 <= x <= 2:
                out.append(float(x))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
