def predict(probe):
    # f(x) = x + 17.8 for x > 0 [E1, E2]
    # f(x) = x - 8.4 for x < 0 [E1, E2]
    # f(0) = 2058.0 (special value at exactly zero) [E2]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(2058.0)
        elif x > 0:
            out.append(x + 17.8)
        else:
            out.append(x - 8.4)
    return {"y": out}
