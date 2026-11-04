def predict(probe):
    # f(x) = 1 exactly when x is in {-1, 0, 1}; 0 elsewhere [E1]
    # (all other tested points, including -2 and 2, give 0)
    return {"y": [1.0 if x in (-1, 0, 1) else 0.0 for x in probe["x"]]}
