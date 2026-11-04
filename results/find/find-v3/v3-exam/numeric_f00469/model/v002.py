def predict(probe):
    # E2: f(x)=1 for x in [-1, 2] (inclusive), 0 elsewhere in tested range
    # E1: all inputs outside that region returned 0
    # Hypothesis: f(x) = 1 if -1 <= x <= 2 else 0
    return {"y": [1.0 if -1 <= x <= 2 else 0.0 for x in probe["x"]]}
