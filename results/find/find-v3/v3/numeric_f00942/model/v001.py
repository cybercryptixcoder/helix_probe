def predict(probe):
    # Piecewise linear [E1, E2]:
    # x < 0: f(x) = -35.72*x - 17.1  [E2: fits -1,-2,-5,-10,-40; E1 confirms]
    # x > 0: f(x) = -404.2*x - 154.8 [E2: fits 1,2,5,10,20,40; E1 confirms]
    # x == 0: f(0) = -5401.17 (special point) [E2]
    ys = []
    for x in probe["x"]:
        if x < 0:
            ys.append(-35.72 * x - 17.1)
        elif x > 0:
            ys.append(-404.2 * x - 154.8)
        else:
            ys.append(-5401.17)
    return {"y": ys}
