def predict(probe):
    # y ≈ x + 17 for x > 0 [E1]
    # y ≈ x - 8 for x < 0 [E1]
    # noise ~±0.5; behavior at x = 0 unknown "?"
    return {"y": [x + 17 if x >= 0 else x - 8 for x in probe["x"]]}
