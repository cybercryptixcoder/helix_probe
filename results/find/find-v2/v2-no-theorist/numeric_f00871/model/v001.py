def predict(probe):
    # All observed outputs are 0 (or -0.0) across a wide range of x [E1]
    # Hypothesis: f(x) = 0 everywhere on the tested domain [-128, 128].
    # No evidence of any other behavior yet.
    return {"y": [0.0 for _ in probe["x"]]}
