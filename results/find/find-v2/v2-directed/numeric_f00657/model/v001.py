def predict(probe):
    # f(x) = 18 for x <= 0, and -18 for x > 0 [E1]
    # Boundary appears between 0 and 16; simplest guess is sign-based at 0 [E1]
    return {"y": [18.0 if x <= 0 else -18.0 for x in probe["x"]]}
