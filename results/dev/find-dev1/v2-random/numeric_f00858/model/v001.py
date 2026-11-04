def predict(probe):
    # f(x) = 0 for all tested x in [-128,128] [E1]
    # No evidence of any nonzero output or undefined region yet [?]
    return {"y": [0.0 for _ in probe["x"]]}
