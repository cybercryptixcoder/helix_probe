def predict(probe):
    # f(x) = 1 when |x| is small, 0 otherwise [E2]
    # Boundary: 1 for x in [-1, 1] (inclusive), 0 outside [E2]
    #   -1 -> 1, -0.5 -> 1, 0 -> 1, 0.5 -> 1, 1 -> 1, 0.1 -> 1, -0.1 -> 1
    #   -10 -> 0, 2 -> 0, 3.7 -> 0, -3.7 -> 0, 5 -> 0, etc.
    # E3: 1.2 -> 1, so boundary extends beyond 1; 2 -> 0 [E2], so boundary in (1, 2]
    # ? Assume |x| <= 1.5 (between 1.2 and 2)
    return {"y": [1.0 if abs(x) <= 1.5 else 0.0 for x in probe["x"]]}
