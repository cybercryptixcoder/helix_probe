def predict(probe):
    # f(x) = 0 for all tested x in [-128,128] [E1]
    # No evidence of nonzero output anywhere yet; assume constant 0.
    return {"y": [0.0 for _ in probe["x"]]}
