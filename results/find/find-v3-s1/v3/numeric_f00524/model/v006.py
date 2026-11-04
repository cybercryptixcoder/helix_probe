def predict(probe):
    # f(x) = ceil(x) on a band, else 0 [E2, E4]
    # Positive side: ceil applies for x <= 4.35, NOT for x >= 4.4 [E8, E10]
    #   x=4.25 -> 5, x=4.3 -> 5, x=4.35 -> 5, x=4.4 -> 0, x=4.5 -> 0 [E8, E10]
    # Negative side: ceil applies for x >= -4.35, NOT for x <= -4.4 [E8, E10]
    #   x=-4.25 -> -4, x=-4.3 -> -4, x=-4.35 -> -4, x=-4.4 -> 0, x=-4.5 -> 0 [E8, E10]
    # So: ceil(x) if -4.35 <= x <= 4.35, else 0
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif -4.35 <= x <= 4.35:
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}
