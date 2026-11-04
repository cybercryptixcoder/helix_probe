def predict(probe):
    # Output takes only two values: -12.4 or 8.8 [E1, E2]
    # x > 0 -> -12.4, x < 0 -> 8.8 [E1, E2]
    # Exception: small positive x (0 < x < ~2.9) gives -11.4 [E1: x=2.9, E2: x=1.2]
    # ? Boundary of the small-positive region is unknown; 2.9 is included, so upper bound >= 2.9
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x > 0:
            if x <= 2.9:
                out.append(-11.4)
            else:
                out.append(-12.4)
        else:
            out.append(8.8)
    return {"y": out}
