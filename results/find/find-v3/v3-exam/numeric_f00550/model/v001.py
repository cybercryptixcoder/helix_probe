def predict(probe):
    # All observed outputs are -0.0 [E1]
    # Best guess: f(x) = 0 (or -0.0) for all x in domain
    return {"y": [-0.0 for _ in probe["x"]]}
