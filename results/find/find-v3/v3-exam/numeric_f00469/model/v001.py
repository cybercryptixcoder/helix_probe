def predict(probe):
    # E1: all 10 random inputs (spanning -62 to 88) returned 0.0
    # Best hypothesis: f(x) = 0 everywhere on the tested domain.
    # (No evidence of any nonzero region yet.)
    return {"y": [0.0 for _ in probe["x"]]}
