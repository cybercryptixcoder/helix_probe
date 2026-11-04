def predict(probe):
    # Output is ~25 for almost all inputs; 2.9 gave 26 [E1]
    # Hypothesis: f(x) = 25 + something small; maybe floor/round of a near-constant?
    # With only one experiment, best guess: constant 25, except near x≈3 -> 26?
    # Too little data to pin down. Predict 25 everywhere; mark uncertainty.
    return {"y": [25.0 for _ in probe["x"]]}
