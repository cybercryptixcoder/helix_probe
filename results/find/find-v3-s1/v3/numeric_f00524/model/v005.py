def predict(probe):
    # f(x) = ceil(x) on a band, else 0 [E2, E4]
    # Positive side: ceil applies for x < 4.25, NOT for x >= 4.25 [E8]
    #   x=4.1 -> 5, x=4.25 -> 5, x=4.4 -> 0, x=4.5 -> 0 [E6, E8]
    # Negative side: ceil applies for x > -4.25, NOT for x <= -4.25 [E8]
    #   x=-4.1 -> -4, x=-4.25 -> -4, x=-4.4 -> 0, x=-4.5 -> 0 [E6, E8]
    # Band is (-4.25, 4.25) with ceil; boundary values 4.25/-4.25 still in band [E8]
    #   x=4.25 -> 5 (in), x=4.4 -> 0 (out); x=-4.25 -> -4 (in), x=-4.4 -> 0 (out)
    # So: ceil(x) if -4.25 <= x <= 4.25, else 0
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif -4.25 <= x <= 4.25:
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}
