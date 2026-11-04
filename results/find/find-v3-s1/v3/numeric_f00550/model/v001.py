def predict(probe):
    # All observed outputs are -0.0 across the whole domain [-128,128] [E1]
    # No evidence of any region behaving differently; simplest hypothesis:
    # f(x) = 0 everywhere (possibly -0.0).
    return {"y": [-0.0 for _ in probe["x"]]}
