def predict(probe):
    # f(x) = 1 for x in [-1.5, 1.5], else 0 [E1, E2]
    # E2 shows 1 at -1.5 and 1.5, 0 at 3 and -3; boundaries within (-3,-1.5] and [1.5,3) ?
    # E1 shows 0 at -2 and 2, so interval is within (-2,2) and includes [-1.5,1.5] ?
    out = []
    for x in probe["x"]:
        if -1.5 <= x <= 1.5:
            out.append(1.0)
        else:
            out.append(0.0)
    return {"y": out}
