def predict(probe):
    # f(x) = floor(x) + 1 for x > 0 [E1-E14]
    # f(x) = floor(x) - 1 for x <= 0 [E2, E12]
    # Exception: x = 33.333 gives -0.5235 instead of 34 [E14]
    # Exception: x = 40.1 gives -0.6334 instead of 41 [E15]
    #   These look like special values; possibly a small region around them.
    #   Without more data, treat exactly these values as special (?) [E14, E15]
    import math
    special = {33.333: -0.5235, 40.1: -0.6334}
    out = []
    for x in probe["x"]:
        if x in special:
            out.append(special[x])
        elif x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}
