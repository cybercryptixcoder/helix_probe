def predict(probe):
    # Only evidence: f returns 0.0 for every tested x in [-128,128] [E1]
    # Best guess: f is the constant zero function.
    return {"y": [0.0 for _ in probe["x"]]}
