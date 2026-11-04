def predict(probe):
    # y = 16.4*x - 2.5 for x > 0 [E1, E2, E3, E4]
    # y = -8.2*x + 2.5 for x < 0 [E1, E2, E3, E4]
    # at x = 0 exactly, y = 2.5 (the negative-side formula) [E2, E4]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(16.4 * x - 2.5)
        else:
            out.append(-8.2 * x + 2.5)
    return {"y": out}
