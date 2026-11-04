def predict(probe):
    # f(x) = floor(x) + 1 for x > 0 [E1-E14]
    # f(x) = floor(x) - 1 for x <= 0 [E2, E12]
    # Exception: x = 33.333 gives -0.5235 instead of 34 [E14]
    #   This looks like a special value; possibly a small region around 33.333.
    #   Without more data, treat exactly 33.333 as special (?) [E14]
    import math
    out = []
    for x in probe["x"]:
        if x == 33.333:
            out.append(-0.5235)
        elif x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}
