def predict(probe):
    # The box outputs ~81 for all ordinary inputs, with small variations.
    # E1: values cluster tightly around 81 (80.9856 to 81.0695).
    # The variation looks like a small oscillation/noise around 81.
    # Best guess: f(x) ≈ 81 + small perturbation. Without more data,
    # predict a constant 81 (the mean-ish). Marked "?".
    return {"y": [81.0 for _ in probe["x"]]}
