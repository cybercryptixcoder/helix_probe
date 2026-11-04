def predict(probe):
    # y = 16.4*x - 2.5 for x >= 0 [E1]
    # y = -8.2*x + 2.5 for x < 0 [E1]
    # boundary at 0 is a guess; data only constrains it to (-6, 2.9] [E1]
    out = []
    for x in probe["x"]:
        if x >= 0:
            out.append(16.4 * x - 2.5)
        else:
            out.append(-8.2 * x + 2.5)
    return {"y": out}
