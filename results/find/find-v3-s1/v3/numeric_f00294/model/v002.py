def predict(probe):
    # y ≈ x + 17 for x > 0 [E1, E2]
    # y ≈ x - 8 for x < 0 [E1, E2]
    # y = 2058 at x = 0 (huge spike) [E2]
    # noise ~±0.5
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(2058.0)
        elif x > 0:
            out.append(x + 17)
        else:
            out.append(x - 8)
    return {"y": out}
