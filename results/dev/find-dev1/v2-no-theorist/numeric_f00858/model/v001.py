def predict(probe):
    # f(x) = 1 for x in {-1, 0, 1}, else 0 [E1]
    # Broad scan shows isolated spike at -1,0,1; all other tested points are 0 [E1]
    # ? Exact boundaries of the nonzero interval are unknown; tested only -1,0,1 nonzero,
    #   and -2, 2 are zero, so the interval is within [-1,1] and includes -1,0,1.
    out = []
    for x in probe["x"]:
        if x in (-1, 0, 1):
            out.append(1.0)
        else:
            out.append(0.0)
    return {"y": out}
