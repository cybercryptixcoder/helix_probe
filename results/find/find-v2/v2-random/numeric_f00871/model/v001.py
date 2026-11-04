def predict(probe):
    # All observed outputs are ~0 (positive or negative zero) [E1]
    # Best hypothesis: f(x) = 0 for all x in domain [-128,128] (?)
    # Could be a function that rounds/truncates to zero, or sin-like near-zero,
    # but with only one experiment all-zero, simplest model is constant 0.
    return {"y": [0.0 for _ in probe["x"]]}
