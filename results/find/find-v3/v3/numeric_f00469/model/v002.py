def predict(probe):
    # f(x) = 1 when |x| is small, 0 otherwise [E2]
    # Boundary: 1 for x in [-1, 1] (inclusive), 0 outside [E2]
    #   -1 -> 1, -0.5 -> 1, 0 -> 1, 0.5 -> 1, 1 -> 1, 0.1 -> 1, -0.1 -> 1
    #   -10 -> 0, 2 -> 0, 3.7 -> 0, -3.7 -> 0, 5 -> 0, etc.
    # ? Exact boundary between 1 and 2 (and -1 and -2) is untested; assume |x| <= 1
    return {"y": [1.0 if abs(x) <= 1.0 else 0.0 for x in probe["x"]]}
