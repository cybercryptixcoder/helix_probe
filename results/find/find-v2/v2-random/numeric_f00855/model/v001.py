def predict(probe):
    # f(x) is roughly constant at 25 across the whole tested domain [E1]
    # One value (x=2.9) returned 26, suggesting mild noise or a small local bump [E1]
    # Best guess: f(x) = 25 everywhere, with occasional +1 noise [E1]
    return {"y": [25 for _ in probe["x"]]}
