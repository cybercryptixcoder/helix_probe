def predict(probe):
    # f(x) = 1 when -1.5 <= x <= 1.5, else 0 [E1, E2]
    # Lower boundary between -1.75 (0) and -1.5 (1); upper between 1.5 (1) and 1.75 (0) [E2]
    # Symmetric around 0, width 3 -> likely |x| <= 1.5 [E2]
    return {"y": [1.0 if -1.5 <= x <= 1.5 else 0.0 for x in probe["x"]]}
