def predict(probe):
    # f(x) = 11.2 - 22.5*x  for x > 0  [E1: exact on 88.2,66,72.7,21.3,2.9]
    # f(x) = 11.2 - 10.89*x for x < 0  [E1: exact on -6,-20.3,-24.3,-50.4,-61.7]
    # f(0) = 11.2 (both branches agree) [E1]
    ys = []
    for x in probe["x"]:
        if x > 0:
            ys.append(11.2 - 22.5 * x)
        elif x < 0:
            ys.append(11.2 - 10.89 * x)
        else:
            ys.append(11.2)
    return {"y": ys}
