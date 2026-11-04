def predict(probe):
    # f(x) = 1 when -2 <= x <= 1, else 0 [E1]
    # Boundaries: -2 -> 0, -1 -> 1, 1 -> 1, 2 -> 0 [E1]
    return {"y": [1.0 if -2 <= x <= 1 else 0.0 for x in probe["x"]]}
