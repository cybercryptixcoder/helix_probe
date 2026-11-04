def predict(probe):
    # E1: all ten outputs are -0.0 across a wide range of x (positive, negative, near zero)
    # Best hypothesis: f(x) = 0 for all x in the domain.
    return {"y": [0.0 for _ in probe["x"]]}
