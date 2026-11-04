def predict(probe):
    # All observed outputs are zero (signed zero) [E1]
    # Simplest hypothesis: f(x) = 0 for all x in domain
    return {"y": [0.0 for _ in probe["x"]]}
