def predict(probe):
    xs = probe["x"]
    ys = []
    for x in xs:
        if x < 0:
            ys.append(-35.72 * x - 17.1)
        else:
            ys.append(-404.2 * x - 154.8)
    return {"y": ys}
