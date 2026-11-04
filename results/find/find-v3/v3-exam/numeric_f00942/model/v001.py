def predict(probe):
    # Piecewise linear with boundary at x=0 [E1]
    # x>=0: y = -404.2*x - 154.8  [E1: exact on 2.9, 21.3, 66, 72.7, 88.2]
    # x<0:  y = -35.72*x - 17.1   [E1: exact on -6, -20.3, -24.3, -50.4, -61.7]
    # x=0 branch is a guess (positive branch) [?]
    out = []
    for x in probe["x"]:
        if x >= 0:
            out.append(-404.2 * x - 154.8)
        else:
            out.append(-35.72 * x - 17.1)
    return {"y": out}
