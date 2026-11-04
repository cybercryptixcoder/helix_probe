def predict(probe):
    # x>=0: y = -404.2*x - 154.8 [E1, E2]
    # x<0:  y = -35.72*x - 17.1  [E1, E2]
    # x=0 is a special point: y = -5401.17 [E2]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(-5401.17)
        elif x > 0:
            out.append(-404.2 * x - 154.8)
        else:
            out.append(-35.72 * x - 17.1)
    return {"y": out}
